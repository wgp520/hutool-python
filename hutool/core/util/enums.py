from enum import Enum
from typing import Any, Callable, List, Optional, Type


class EnumUtil:
    """枚举工具类

    提供对Python枚举类型的常用操作方法，包括获取名称、值、查找等。
    """

    @staticmethod
    def get_names(enum_class: Type[Enum]) -> List[str]:
        """获取所有枚举名称

        :param enum_class: 枚举类
        :return: 枚举名称列表
        """
        return [member.name for member in enum_class]

    @staticmethod
    def get_values(enum_class: Type[Enum]) -> list:
        """获取所有枚举值

        :param enum_class: 枚举类
        :return: 枚举值列表
        """
        return [member.value for member in enum_class]

    @staticmethod
    def get_items(enum_class: Type[Enum]) -> dict:
        """获取所有枚举项为字典

        :param enum_class: 枚举类
        :return: 以枚举名称为键、枚举值为值的字典
        """
        return {member.name: member.value for member in enum_class}

    @staticmethod
    def contains(enum_class: Type[Enum], value: Any) -> bool:
        """是否包含指定值

        :param enum_class: 枚举类
        :param value: 待检查的值
        :return: 是否包含该值
        """
        try:
            enum_class(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def of(enum_class: Type[Enum], name: str) -> Optional[Enum]:
        """根据名称获取枚举

        :param enum_class: 枚举类
        :param name: 枚举成员名称
        :return: 对应的枚举成员，未找到返回None
        """
        try:
            return enum_class[name]
        except KeyError:
            return None

    @staticmethod
    def of_value(enum_class: Type[Enum], value: Any) -> Optional[Enum]:
        """根据值获取枚举

        :param enum_class: 枚举类
        :param value: 枚举成员的值
        :return: 对应的枚举成员，未找到返回None
        """
        try:
            return enum_class(value)
        except ValueError:
            return None

    @staticmethod
    def get_by_func(
        enum_class: Type[Enum], func: Callable[[Enum], bool], default: Optional[Enum] = None
    ) -> Optional[Enum]:
        """通过自定义函数查找枚举

        遍历所有枚举成员，返回第一个使函数返回True的成员。

        :param enum_class: 枚举类
        :param func: 接收枚举成员并返回布尔值的函数
        :param default: 未找到时的默认值，默认为None
        :return: 匹配的枚举成员，未找到返回default
        """
        for member in enum_class:
            if func(member):
                return member
        return default

    @staticmethod
    def is_enum_class(obj: Any) -> bool:
        """判断对象是否为枚举类。

        :param obj: 对象
        :return: 是否为枚举类
        """
        return isinstance(obj, type) and issubclass(obj, Enum)

    @staticmethod
    def is_enum(obj: Any) -> bool:
        """判断对象是否为枚举成员。

        :param obj: 对象
        :return: 是否为枚举成员
        """
        return isinstance(obj, Enum)

    @staticmethod
    def from_string(enum_class: Type[Enum], name: str) -> Enum:
        """根据名称获取枚举成员，未找到时抛出异常。

        :param enum_class: 枚举类
        :param name: 枚举成员名称
        :return: 枚举成员
        :raises ValueError: 未找到时
        """
        return enum_class[name]

    @staticmethod
    def from_string_quietly(enum_class: Type[Enum], name: str) -> Optional[Enum]:
        """根据名称静默获取枚举成员。

        :param enum_class: 枚举类
        :param name: 枚举成员名称
        :return: 枚举成员，未找到返回 None
        """
        try:
            return enum_class[name]
        except (KeyError, ValueError):
            return None

    @staticmethod
    def get_field_values(enum_class: Type[Enum], field: str) -> list:
        """获取所有枚举成员的指定属性值列表。

        :param enum_class: 枚举类
        :param field: 属性名称
        :return: 属性值列表
        """
        result = []
        for member in enum_class:
            result.append(getattr(member, field, None))
        return result

    @staticmethod
    def get_field_names(enum_class: Type[Enum]) -> List[str]:
        """获取所有枚举成员名称（同 get_names）。

        :param enum_class: 枚举类
        :return: 名称列表
        """
        return EnumUtil.get_names(enum_class)

    @staticmethod
    def get_enum_map(enum_class: Type[Enum]) -> dict:
        """获取枚举映射（name -> member）。

        :param enum_class: 枚举类
        :return: 名称到成员的字典
        """
        return {member.name: member for member in enum_class}

    @staticmethod
    def get_name_field_map(enum_class: Type[Enum], field: str) -> dict:
        """获取名称到指定属性值的映射。

        :param enum_class: 枚举类
        :param field: 属性名称
        :return: 名称到属性值的字典
        """
        return {member.name: getattr(member, field, None) for member in enum_class}
