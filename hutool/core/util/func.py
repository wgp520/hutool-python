"""函数字符串解析工具类。"""

import ast
import builtins
import importlib
import logging
from functools import partial
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class FuncUtil:
    """函数调用字符串解析与执行工具类。

    基于 Python AST 模块，将函数调用字符串（如 ``"math.sqrt(2)"``）解析为
    可调用对象或直接执行。

    支持的功能：

    - 解析函数字符串为 ``(模块名, 函数名, 位置参数, 关键字参数)``
    - 解析嵌套调用（如 ``"datetime.datetime(2024, 1, 1)"``）
    - 将字符串转为 ``functools.partial`` 可调用对象
    - 直接执行函数字符串并返回结果
    - 通过点分路径解析任意 Python 对象
    """

    # ── 解析 ─────────────────────────────────────────────────

    @staticmethod
    def parse_func(
        func_str: str,
    ) -> Optional[Tuple[Optional[str], str, List[Any], Dict[str, Any]]]:
        """解析函数调用字符串。

        :param func_str: 函数调用字符串，如 ``"math.sqrt(2)"``
        :return: ``(模块名, 函数名, 位置参数列表, 关键字参数字典)``，无法解析时返回 ``None``

        示例::

            >>> FuncUtil.parse_func("math.sqrt(2)")
            ('math', 'sqrt', [2], {})
            >>> FuncUtil.parse_func("len([1, 2, 3])")
            (None, 'len', [[1, 2, 3]], {})
        """
        try:
            tree = ast.parse(func_str)
        except SyntaxError:
            return None
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                return FuncUtil.parse_call(node)
        return None

    @staticmethod
    def parse_arg(arg: Any) -> Any:
        """解析单个参数。

        支持嵌套函数调用（递归执行）、Python 字面量（int/str/list/dict 等）、
        以及 AST 节点回退为源码字符串。

        :param arg: 参数（AST 节点或原始值）
        :return: 解析后的参数值
        """
        if isinstance(arg, ast.Call):
            module_name, func_name, args, kwargs = FuncUtil.parse_call(arg)
            if module_name is None:
                func = getattr(builtins, func_name, None)
            else:
                func = getattr(importlib.import_module(module_name), func_name)
            return func(*args, **kwargs)

        try:
            return ast.literal_eval(arg)
        except (ValueError, SyntaxError):
            pass

        if isinstance(arg, ast.AST):
            return ast.unparse(arg)
        return arg

    @staticmethod
    def parse_call(node: ast.Call) -> Tuple[Optional[str], str, List[Any], Dict[str, Any]]:
        """解析 AST Call 节点。

        :param node: AST 函数调用节点
        :return: ``(模块名, 函数名, 位置参数列表, 关键字参数字典)``

        示例 AST 结构 (``math.sqrt(2)``)::

            Call(func=Attribute(value=Name(id='math'), attr='sqrt'),
                 args=[Constant(value=2)], keywords=[])
        """
        module: Optional[str] = None
        func_name: Any = node.func

        if isinstance(node.func, ast.Attribute):
            parts: List[str] = []
            value = node.func.value
            while isinstance(value, ast.Attribute):
                parts.append(value.attr)
                value = value.value
            parts.append(value.id if isinstance(value, ast.Name) else "")
            module = ".".join(parts[::-1])
            func_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            func_name = node.func.id

        args = [FuncUtil.parse_arg(a) for a in node.args]
        kwargs = {kw.arg: FuncUtil.parse_arg(kw.value) for kw in node.keywords}
        return module, func_name, args, kwargs

    # ── 转换为可调用对象 ──────────────────────────────────────

    @staticmethod
    def callable_func(func_str: str, model: Any = None) -> Optional[Callable[..., Any]]:
        """解析函数字符串并返回可调用对象。

        返回值为 ``functools.partial``，已绑定预设参数，调用时可追加参数。

        :param func_str: 函数调用字符串
        :param model: 指定模块对象；为 ``None`` 时自动从字符串中导入
        :return: 可调用对象，解析失败返回 ``None``

        示例::

            >>> sqrt = FuncUtil.callable_func("math.sqrt(2)")
            >>> sqrt()
            1.4142135623730951
        """
        if parse_result := FuncUtil.parse_func(func_str):
            module_name, func_name, args, kwargs = parse_result
            if model is not None:
                func = getattr(model, func_name)
            elif module_name is None:
                func = getattr(builtins, func_name, None)
            else:
                func = getattr(importlib.import_module(module_name), func_name)
            if func is None:
                return None
            return partial(func, *args, **kwargs)
        return None

    # ── 新增：执行 ───────────────────────────────────────────

    @staticmethod
    def call_func(func_str: str, *extra_args: Any, model: Any = None, **extra_kwargs: Any) -> Any:
        """解析并执行函数字符串，返回结果。

        :param func_str: 函数调用字符串
        :param extra_args: 追加的位置参数（在原有参数之后）
        :param model: 指定模块对象
        :param extra_kwargs: 追加的关键字参数
        :return: 函数执行结果
        :raises ValueError: 无法解析函数字符串
        :raises ImportError: 无法导入模块
        :raises AttributeError: 无法找到函数

        示例::

            >>> FuncUtil.call_func("math.sqrt", 4)
            2.0
            >>> FuncUtil.call_func("len", [1, 2, 3])
            3
        """
        if parse_result := FuncUtil.parse_func(func_str):
            module_name, func_name, args, kwargs = parse_result
            if model is not None:
                func = getattr(model, func_name)
            elif module_name is None:
                func = getattr(builtins, func_name, None)
            else:
                func = getattr(importlib.import_module(module_name), func_name)
        else:
            # 尝试作为点分路径直接解析（也支持内置函数名）
            fn = FuncUtil.resolve_func(func_str)
            if fn is None:
                raise ValueError(f"无法解析函数字符串: {func_str}")
            return fn(*extra_args, **extra_kwargs)

        return func(*args, *extra_args, **kwargs, **extra_kwargs)

    @staticmethod
    def safe_call(
        func_str: str,
        *extra_args: Any,
        default: Any = None,
        model: Any = None,
        **extra_kwargs: Any,
    ) -> Any:
        """解析并执行函数字符串，失败时返回默认值（不抛异常）。

        :param func_str: 函数调用字符串
        :param extra_args: 追加的位置参数
        :param default: 出错时返回的默认值
        :param model: 指定模块对象
        :param extra_kwargs: 追加的关键字参数
        :return: 函数执行结果，失败返回 ``default``

        示例::

            >>> FuncUtil.safe_call("math.sqrt", 4)
            2.0
            >>> FuncUtil.safe_call("invalid.func", default=-1)
            -1
        """
        try:
            return FuncUtil.call_func(func_str, *extra_args, model=model, **extra_kwargs)
        except Exception:
            logger.debug("safe_call 执行失败: %s", func_str, exc_info=True)
            return default

    # ── 新增：查询 ───────────────────────────────────────────

    @staticmethod
    def is_callable(func_str: str) -> bool:
        """判断字符串是否为合法的函数调用表达式。

        仅检查语法层面是否可解析，不验证模块/函数是否存在。

        :param func_str: 待检查的字符串
        :return: 是否为合法的函数调用

        示例::

            >>> FuncUtil.is_callable("math.sqrt(2)")
            True
            >>> FuncUtil.is_callable("not a function")
            False
        """
        try:
            tree = ast.parse(func_str)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    return True
            return False
        except SyntaxError:
            return False

    @staticmethod
    def get_func_name(func_str: str) -> Optional[str]:
        """提取函数调用字符串中的函数名。

        :param func_str: 函数调用字符串
        :return: 函数名，无法解析时返回 ``None``

        示例::

            >>> FuncUtil.get_func_name("math.sqrt(2)")
            'sqrt'
            >>> FuncUtil.get_func_name("datetime.datetime.now()")
            'now'
        """
        try:
            tree = ast.parse(func_str)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute):
                        return node.func.attr
                    if isinstance(node.func, ast.Name):
                        return node.func.id
        except SyntaxError:
            pass
        return None

    # ── 新增：点分路径解析 ───────────────────────────────────

    @staticmethod
    def resolve_func(dotted_path: str) -> Any:
        """将点分路径解析为 Python 对象。

        支持模块属性、类方法、嵌套属性等任意 Python 对象的获取。

        :param dotted_path: 点分路径，如 ``"math.sqrt"`` 或 ``"datetime.datetime.now"``
        :return: 解析到的对象，失败返回 ``None``

        示例::

            >>> FuncUtil.resolve_func("math.sqrt")
            <built-in function sqrt>
            >>> FuncUtil.resolve_func("os.path.join")
            <function join at 0x...>
        """
        parts = dotted_path.split(".")

        # 先尝试内置函数（单段路径且在 builtins 中）
        if len(parts) == 1:
            obj = getattr(builtins, parts[0], None)
            if obj is not None:
                return obj

        # 从最长的模块路径开始尝试导入
        for i in range(len(parts), 0, -1):
            module_path = ".".join(parts[:i])
            try:
                obj = importlib.import_module(module_path)
                for attr in parts[i:]:
                    obj = getattr(obj, attr)
                return obj
            except (ImportError, AttributeError):
                continue
        return None
