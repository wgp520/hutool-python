"""
Python port of Java Hutool's ObjectUtil.

对象工具类，提供对象比较、空值判断、默认值处理、类型判断等常用对象工具方法。
"""

import copy
from typing import Any, Optional, Sized

__all__ = [
    "ObjectUtil",
]


class ObjectUtil:
    """对象工具类，对应 Java cn.hutool.core.util.ObjectUtil"""

    @staticmethod
    def equals(obj1: Any, obj2: Any) -> bool:
        """
        比较两个对象是否相等，null安全。
        当两对象均为None时返回True，当其中之一为None时返回False。

        :param obj1: 对象1
        :param obj2: 对象2
        :return: 是否相等
        """
        if obj1 is obj2:
            return True
        if obj1 is None or obj2 is None:
            return False
        return obj1 == obj2

    @staticmethod
    def not_equal(obj1: Any, obj2: Any) -> bool:
        """
        比较两个对象是否不等，null安全。

        :param obj1: 对象1
        :param obj2: 对象2
        :return: 是否不等
        """
        return not ObjectUtil.equals(obj1, obj2)

    @staticmethod
    def length(obj: Any) -> int:
        """
        获取对象长度，支持 str、list、tuple、dict、bytes 等可计算长度的对象。
        当对象为None时返回0。

        :param obj: 对象
        :return: 长度
        """
        if obj is None:
            return 0
        if isinstance(obj, Sized):
            return len(obj)
        # 对于不支持len的对象，尝试迭代计数
        raise TypeError(f"Object of type '{type(obj).__name__}' has no len()")

    @staticmethod
    def contains(obj: Any, element: Any) -> bool:
        """
        对象中是否包含元素。
        支持的类型：
        - str: 检查是否包含子串
        - dict: 检查是否包含key
        - set: 检查是否包含元素
        - list/tuple/其他可迭代对象: 检查是否包含元素

        当对象为None时返回False。

        :param obj: 对象
        :param element: 元素
        :return: 是否包含
        """
        if obj is None:
            return False
        if isinstance(obj, str):
            if element is None:
                return False
            return str(element) in obj
        if isinstance(obj, dict):
            return element in obj
        if isinstance(obj, (set, frozenset)):
            return element in obj
        if isinstance(obj, (list, tuple)):
            return element in obj
        # 兜底：尝试使用 in 运算符
        try:
            return element in obj
        except TypeError:
            return False

    @staticmethod
    def is_null(obj: Any) -> bool:
        """
        检查对象是否为None。

        :param obj: 对象
        :return: 是否为None
        """
        return obj is None

    @staticmethod
    def is_not_null(obj: Any) -> bool:
        """
        检查对象是否不为None。

        :param obj: 对象
        :return: 是否不为None
        """
        return obj is not None

    @staticmethod
    def is_empty(obj: Any) -> bool:
        """
        检查对象是否为空（None或空容器）。
        支持 str、list、tuple、dict、set、frozenset、bytes、bytearray。
        对于非上述类型，如果为None则返回True，否则返回False。

        :param obj: 对象
        :return: 是否为空
        """
        if obj is None:
            return True
        if isinstance(obj, (str, bytes, bytearray, list, tuple, dict, set, frozenset)):
            return len(obj) == 0
        return False

    @staticmethod
    def is_not_empty(obj: Any) -> bool:
        """
        检查对象是否为非空。

        :param obj: 对象
        :return: 是否为非空
        """
        return not ObjectUtil.is_empty(obj)

    @staticmethod
    def default_if_null(obj: Any, default_value: Any) -> Any:
        """
        如果obj为None，返回默认值，否则返回obj本身。

        :param obj: 对象
        :param default_value: 默认值
        :return: 对象或默认值
        """
        return default_value if obj is None else obj

    @staticmethod
    def default_if_empty(obj: Any, default_value: Any) -> Any:
        """
        如果obj为空（None或空容器），返回默认值，否则返回obj本身。

        :param obj: 对象
        :param default_value: 默认值
        :return: 对象或默认值
        """
        return default_value if ObjectUtil.is_empty(obj) else obj

    @staticmethod
    def default_if_blank(obj: Optional[str], default_value: str) -> str:
        """
        如果字符串为空白（None、空串或纯空白），返回默认值。

        :param obj: 字符串对象
        :param default_value: 默认值
        :return: 字符串或默认值
        """
        if obj is None:
            return default_value
        if isinstance(obj, str) and obj.strip() == "":
            return default_value
        return obj

    @staticmethod
    def clone(obj: Any) -> Any:
        """
        深拷贝对象。当对象为None时返回None。

        :param obj: 对象
        :return: 深拷贝后的对象
        """
        if obj is None:
            return None
        return copy.deepcopy(obj)

    @staticmethod
    def is_basic_type(obj: Any) -> bool:
        """
        是否为基本类型，包括 int、float、complex、bool、str、bytes、None。

        :param obj: 对象
        :return: 是否为基本类型
        """
        if obj is None:
            return True
        return isinstance(obj, (int, float, complex, bool, str, bytes))

    @staticmethod
    def compare(c1: Any, c2: Any) -> int:
        """
        比较两个对象的大小。
        当c1为None时，c2为None返回0，否则返回-1。
        当c2为None时，返回1。
        两者均非None时使用比较运算符。

        与Java Comparable接口行为一致：
        - c1 == c2 -> 0
        - c1 < c2  -> -1
        - c1 > c2  -> 1

        :param c1: 对象1
        :param c2: 对象2
        :return: 比较结果，0表示相等，-1表示c1小于c2，1表示c1大于c2
        """
        if c1 is None:
            return 0 if c2 is None else -1
        if c2 is None:
            return 1
        if c1 == c2:
            return 0
        return -1 if c1 < c2 else 1

    @staticmethod
    def to_string(obj: Any, default: str = "") -> str:
        """
        将对象转为字符串，当对象为None时返回默认值。

        :param obj: 对象
        :param default: 默认值
        :return: 字符串
        """
        if obj is None:
            return default
        return str(obj)

    @staticmethod
    def has_null(*args: Any) -> bool:
        """
        检查参数中是否有None。
        当没有参数传入时返回False。

        :param args: 参数列表
        :return: 是否包含None
        """
        for arg in args:
            if arg is None:
                return True
        return False

    @staticmethod
    def has_empty(*args: Any) -> bool:
        """
        检查参数中是否有空值（None或空容器）。
        当没有参数传入时返回False。

        :param args: 参数列表
        :return: 是否包含空值
        """
        for arg in args:
            if ObjectUtil.is_empty(arg):
                return True
        return False

    @staticmethod
    def is_all_empty(*args: Any) -> bool:
        """
        检查是否全部为空。
        当没有参数传入时返回True。

        :param args: 参数列表
        :return: 是否全部为空
        """
        for arg in args:
            if ObjectUtil.is_not_empty(arg):
                return False
        return True

    @staticmethod
    def is_all_not_empty(*args: Any) -> bool:
        """
        检查是否全部为非空。
        当没有参数传入时返回True。

        :param args: 参数列表
        :return: 是否全部为非空
        """
        for arg in args:
            if ObjectUtil.is_empty(arg):
                return False
        return True
