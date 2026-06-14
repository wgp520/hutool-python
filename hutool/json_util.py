import json
import re
from typing import Any, List, Optional, Type, Union


class JSONUtil:
    """JSON工具类"""

    @staticmethod
    def create_obj() -> dict:
        """创建空JSON对象"""
        return {}

    @staticmethod
    def create_array() -> list:
        """创建空JSON数组"""
        return []

    # ------------------------------------------------------------------ #
    #  解析
    # ------------------------------------------------------------------ #

    @staticmethod
    def parse_obj(json_str: str) -> dict:
        """解析JSON字符串为字典"""
        result = json.loads(json_str)
        if not isinstance(result, dict):
            raise ValueError("JSON字符串不是对象类型")
        return result

    @staticmethod
    def parse_array(json_str: str) -> list:
        """解析JSON字符串为列表"""
        result = json.loads(json_str)
        if not isinstance(result, list):
            raise ValueError("JSON字符串不是数组类型")
        return result

    @staticmethod
    def parse(json_str: str):
        """解析JSON字符串，自动返回对应Python类型"""
        return json.loads(json_str)

    # ------------------------------------------------------------------ #
    #  序列化
    # ------------------------------------------------------------------ #

    @staticmethod
    def to_json_str(obj: Any, indent: Optional[int] = None) -> str:
        """对象转JSON字符串

        :param obj: 待序列化的对象
        :param indent: 缩进空格数，None表示不缩进
        """
        return json.dumps(obj, ensure_ascii=False, indent=indent)

    @staticmethod
    def to_json_pretty_str(obj: Any) -> str:
        """对象转格式化JSON字符串（缩进2空格）"""
        return json.dumps(obj, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------ #
    #  Bean 转换（简易实现，基于类构造器）
    # ------------------------------------------------------------------ #

    @staticmethod
    def to_bean(json_str: str, bean_class: Type):
        """JSON字符串转对象

        将JSON解析为字典后，通过 bean_class(\\*\\*dict) 构造实例。
        如果 bean_class 提供了 from_dict 类方法，则优先调用。
        """
        data = json.loads(json_str)
        if hasattr(bean_class, "from_dict") and callable(bean_class.from_dict):
            return bean_class.from_dict(data)
        if isinstance(data, dict):
            return bean_class(**data)
        return bean_class(data)

    @staticmethod
    def to_bean_list(json_str: str, element_class: Type) -> list:
        """JSON字符串转对象列表"""
        data = json.loads(json_str)
        if not isinstance(data, list):
            raise ValueError("JSON字符串不是数组类型")
        if hasattr(element_class, "from_dict") and callable(element_class.from_dict):
            return [element_class.from_dict(item) for item in data]
        return [element_class(**item) if isinstance(item, dict) else element_class(item) for item in data]

    @staticmethod
    def from_bean(obj: Any) -> str:
        """对象转JSON字符串

        如果对象具有 to_dict 方法则先调用，否则直接序列化。
        """
        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            return json.dumps(obj.to_dict(), ensure_ascii=False)
        return json.dumps(obj, ensure_ascii=False, default=str)

    # ------------------------------------------------------------------ #
    #  文件读写
    # ------------------------------------------------------------------ #

    @staticmethod
    def read_json(path: str, charset: str = "utf-8"):
        """读取JSON文件并解析"""
        with open(path, encoding=charset) as f:
            return json.load(f)

    @staticmethod
    def read_json_object(path: str, charset: str = "utf-8") -> dict:
        """读取JSON文件为字典"""
        result = JSONUtil.read_json(path, charset)
        if not isinstance(result, dict):
            raise ValueError("JSON文件内容不是对象类型")
        return result

    @staticmethod
    def read_json_array(path: str, charset: str = "utf-8") -> list:
        """读取JSON文件为列表"""
        result = JSONUtil.read_json(path, charset)
        if not isinstance(result, list):
            raise ValueError("JSON文件内容不是数组类型")
        return result

    @staticmethod
    def write_json(path: str, obj: Any, charset: str = "utf-8", indent: Optional[int] = None) -> None:
        """写入JSON文件

        :param path: 文件路径
        :param obj: 待写入对象
        :param charset: 文件编码
        :param indent: 缩进空格数，None表示不缩进
        """
        with open(path, "w", encoding=charset) as f:
            json.dump(obj, f, ensure_ascii=False, indent=indent)

    # ------------------------------------------------------------------ #
    #  校验
    # ------------------------------------------------------------------ #

    @staticmethod
    def is_json(str_val: str) -> bool:
        """是否为有效JSON"""
        try:
            json.loads(str_val)
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def is_json_obj(str_val: str) -> bool:
        """是否为JSON对象"""
        try:
            return isinstance(json.loads(str_val), dict)
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def is_json_array(str_val: str) -> bool:
        """是否为JSON数组"""
        try:
            return isinstance(json.loads(str_val), list)
        except (json.JSONDecodeError, TypeError):
            return False

    # ------------------------------------------------------------------ #
    #  格式化 / 压缩
    # ------------------------------------------------------------------ #

    @staticmethod
    def format_json(json_str: str, indent: int = 2) -> str:
        """格式化JSON字符串"""
        obj = json.loads(json_str)
        return json.dumps(obj, ensure_ascii=False, indent=indent)

    @staticmethod
    def compress(json_str: str) -> str:
        """压缩JSON（去除所有空白）"""
        obj = json.loads(json_str)
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

    # ------------------------------------------------------------------ #
    #  路径操作（支持 'a.b.c' 和 'a[0].b'）
    # ------------------------------------------------------------------ #

    @staticmethod
    def _parse_path_keys(path: str) -> List[Union[str, int]]:
        """将路径字符串解析为键列表

        例如 'a.b[0].c' -> ['a', 'b', 0, 'c']
        """
        keys: List[Union[str, int]] = []
        for part in re.split(r"\.(?![^\[]*\])", path):
            # 处理 key[index] 形式
            match = re.match(r"^(\w+)((?:\[\d+\])*)$", part)
            if match:
                keys.append(match.group(1))
                for idx in re.findall(r"\[(\d+)\]", match.group(2)):
                    keys.append(int(idx))
            elif part:
                keys.append(part)
        return keys

    @staticmethod
    def get_by_path(json_data: Any, path: str) -> Any:
        """按路径获取值

        :param json_data: JSON数据（字典或列表）
        :param path: 路径，如 'a.b.c' 或 'a[0].b'
        :return: 对应路径的值，路径不存在时返回 None
        """
        keys = JSONUtil._parse_path_keys(path)
        current = json_data
        for key in keys:
            if current is None:
                return None
            try:
                current = current[key]
            except (KeyError, IndexError, TypeError):
                return None
        return current

    @staticmethod
    def put_by_path(json_data: Any, path: str, value: Any) -> None:
        """按路径设置值

        :param json_data: JSON数据（字典或列表）
        :param path: 路径，如 'a.b.c' 或 'a[0].b'
        :param value: 要设置的值
        """
        keys = JSONUtil._parse_path_keys(path)
        if not keys:
            raise ValueError("路径不能为空")
        current = json_data
        for key in keys[:-1]:
            next_key = keys[keys.index(key) + 1] if keys.index(key) + 1 < len(keys) else None
            if isinstance(current, dict):
                if key not in current:
                    current[key] = {} if isinstance(next_key, str) else []
                current = current[key]
            elif isinstance(current, list):
                while len(current) <= key:
                    current.append(None)
                if current[key] is None:
                    current[key] = {} if isinstance(next_key, str) else []
                current = current[key]
            else:
                raise TypeError(f"无法在路径 '{path}' 上设置值：中间节点类型不支持")
        last_key = keys[-1]
        current[last_key] = value
