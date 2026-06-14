import inspect
from typing import Any, Dict, List, Type


class ReflectUtil:
    """反射工具类

    提供对Python对象的反射操作，包括获取/设置字段值、调用方法、
    获取字段和方法信息等。
    """

    @staticmethod
    def get_field_value(obj: Any, field_name: str) -> Any:
        """获取字段值

        :param obj: 对象
        :param field_name: 字段名
        :return: 字段值
        :raises AttributeError: 字段不存在
        """
        return getattr(obj, field_name)

    @staticmethod
    def set_field_value(obj: Any, field_name: str, value: Any) -> None:
        """设置字段值

        如果字段不存在则动态添加。

        :param obj: 对象
        :param field_name: 字段名
        :param value: 字段值
        """
        setattr(obj, field_name, value)

    @staticmethod
    def invoke(obj: Any, method_name: str, *args: Any, **kwargs: Any) -> Any:
        """调用方法

        :param obj: 对象
        :param method_name: 方法名
        :param args: 位置参数
        :param kwargs: 关键字参数
        :return: 方法返回值
        :raises AttributeError: 方法不存在
        :raises TypeError: 方法不可调用
        """
        method = getattr(obj, method_name)
        if not callable(method):
            raise TypeError(f"属性 '{method_name}' 不可调用")
        return method(*args, **kwargs)

    @staticmethod
    def get_fields(obj: Any) -> Dict[str, Any]:
        """获取所有字段

        返回对象的所有非方法属性及其值的字典。

        :param obj: 对象
        :return: 字段名到字段值的字典
        """
        result = {}
        for name, value in inspect.getmembers(obj):
            if not name.startswith("_") and not callable(value):
                result[name] = value
        return result

    @staticmethod
    def get_methods(obj: Any) -> List[str]:
        """获取所有方法名

        返回对象中不以单下划线开头的方法名称列表。

        :param obj: 对象或类
        :return: 方法名列表
        """
        return [name for name, value in inspect.getmembers(obj) if not name.startswith("_") and callable(value)]

    @staticmethod
    def has_field(obj: Any, field_name: str) -> bool:
        """是否有指定字段

        :param obj: 对象
        :param field_name: 字段名
        :return: 是否存在该字段
        """
        if not hasattr(obj, field_name):
            return False
        return not callable(getattr(obj, field_name))

    @staticmethod
    def has_method(obj: Any, method_name: str) -> bool:
        """是否有指定方法

        :param obj: 对象或类
        :param method_name: 方法名
        :return: 是否存在该方法
        """
        attr = getattr(obj, method_name, None)
        return attr is not None and callable(attr)

    @staticmethod
    def get_annotations(obj: Any) -> Dict[str, Any]:
        """获取类型注解

        获取对象（类或函数）的类型注解信息。

        :param obj: 类或函数
        :return: 类型注解字典
        """
        if isinstance(obj, type):
            return getattr(obj, "__annotations__", {})
        return getattr(obj, "__annotations__", {})

    @staticmethod
    def new_instance(cls: Type, *args: Any, **kwargs: Any) -> Any:
        """创建实例

        :param cls: 类
        :param args: 位置参数
        :param kwargs: 关键字参数
        :return: 创建的实例
        """
        return cls(*args, **kwargs)

    @staticmethod
    def get_super_class(cls: Type) -> Type:
        """获取父类

        :param cls: 类
        :return: 父类，如果没有父类则返回object
        """
        bases = cls.__bases__
        if bases:
            return bases[0]
        return object
