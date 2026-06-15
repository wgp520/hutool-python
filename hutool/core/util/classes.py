import importlib
from typing import Any, List, Type


class ClassUtil:
    """类工具类

    提供对Python类和对象的常用操作方法，包括获取类名、模块名、类型判断等。
    """

    @staticmethod
    def get_class_name(obj: Any, is_simple: bool = True) -> str:
        """获取类名

        :param obj: 对象或类
        :param is_simple: 是否返回简单类名（不含模块路径），默认True
        :return: 类名字符串
        """
        if isinstance(obj, type):
            cls = obj
        else:
            cls = type(obj)

        if is_simple:
            return cls.__name__
        else:
            module = cls.__module__
            if module == "builtins":
                return cls.__name__
            return f"{module}.{cls.__name__}"

    @staticmethod
    def get_package_name(obj: Any) -> str:
        """获取模块名

        :param obj: 对象或类
        :return: 模块名字符串
        """
        if isinstance(obj, type):
            cls = obj
        else:
            cls = type(obj)

        return cls.__module__

    @staticmethod
    def is_basic_type(obj: Any) -> bool:
        """是否为基本类型

        基本类型包括：int, float, str, bool, bytes, complex, type(None)

        :param obj: 待检查的对象
        :return: 是否为基本类型
        """
        basic_types = (int, float, str, bool, bytes, complex, type(None))
        return isinstance(obj, basic_types)

    @staticmethod
    def is_instance(obj: Any, class_or_tuple: Any) -> bool:
        """是否为指定类型的实例

        :param obj: 待检查的对象
        :param class_or_tuple: 类或类的元组
        :return: 是否为指定类型的实例
        """
        return isinstance(obj, class_or_tuple)

    @staticmethod
    def get_public_fields(obj: Any) -> List[str]:
        """获取公开字段

        返回对象中不以单下划线开头的属性名称列表。

        :param obj: 对象
        :return: 公开字段名列表
        """
        return [attr for attr in dir(obj) if not attr.startswith("_") and not callable(getattr(obj, attr, None))]

    @staticmethod
    def get_methods(obj: Any) -> List[str]:
        """获取方法列表

        返回对象中不以单下划线开头的方法名称列表。

        :param obj: 对象或类
        :return: 方法名列表
        """
        return [attr for attr in dir(obj) if not attr.startswith("_") and callable(getattr(obj, attr, None))]

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
    def create_instance(class_path: str) -> Any:
        """通过完整类路径创建实例

        支持模块级函数和类实例化两种方式。
        例如: 'json.loads', 'datetime.datetime', 'collections.OrderedDict'

        :param class_path: 完整类路径或函数路径，如 'datetime.datetime'
        :return: 创建的实例或返回的函数结果
        :raises ImportError: 模块导入失败
        :raises AttributeError: 属性不存在
        """
        parts = class_path.rsplit(".", 1)
        if len(parts) != 2:
            raise ValueError(f"无效的类路径: {class_path}，需要包含模块和类名/函数名")

        module_path, attr_name = parts
        module = importlib.import_module(module_path)
        obj = getattr(module, attr_name)

        if isinstance(obj, type):
            return obj()
        return obj

    @staticmethod
    def is_subclass(cls: Type, parent_cls: Type) -> bool:
        """是否为子类

        :param cls: 待检查的类
        :param parent_cls: 父类
        :return: 是否为父类的子类
        """
        try:
            return issubclass(cls, parent_cls)
        except TypeError:
            return False
