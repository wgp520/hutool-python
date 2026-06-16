"""Bean工具类，提供对象与字典之间的转换、属性复制等功能"""

from typing import Any, List, Optional, Type, TypeVar

T = TypeVar("T")

__all__ = ("BeanUtil",)


class BeanUtil:
    """Bean工具类，提供对象属性的读写、对象与字典互转、属性复制等功能"""

    @staticmethod
    def get_field_value(bean: Any, field_name: str) -> Any:
        """
        获取对象字段值

        :param bean: 对象实例
        :param field_name: 字段名
        :return: 字段值，若字段不存在返回None
        """
        if bean is None:
            return None
        try:
            return getattr(bean, field_name, None)
        except Exception:
            return None

    @staticmethod
    def set_field_value(bean: Any, field_name: str, value: Any) -> None:
        """
        设置对象字段值

        :param bean: 对象实例
        :param field_name: 字段名
        :param value: 要设置的值
        """
        if bean is None:
            raise ValueError("Bean不能为None")
        setattr(bean, field_name, value)

    @staticmethod
    def map_to_bean(map_data: dict, bean_class: Type[T], ignore_error: bool = False) -> T:
        """
        字典转对象

        :param map_data: 字典数据
        :param bean_class: 目标Bean类型
        :param ignore_error: 是否忽略错误，若为True则跳过无法设置的字段
        :return: Bean对象
        """
        if map_data is None:
            raise ValueError("map_data不能为None")
        if bean_class is None:
            raise ValueError("bean_class不能为None")

        try:
            bean = bean_class()
        except Exception as e:
            raise TypeError(f"无法实例化{bean_class.__name__}: {e}") from e

        BeanUtil.fill_bean_with_map(map_data, bean, ignore_error)
        return bean

    @staticmethod
    def bean_to_map(bean: Any) -> dict:
        """
        对象转字典，将对象中所有非下划线开头的公共属性转为字典

        :param bean: Bean对象
        :return: 字典
        """
        if bean is None:
            raise ValueError("bean不能为None")

        result = {}
        # 使用__dict__获取实例属性
        if hasattr(bean, "__dict__"):
            for key, value in bean.__dict__.items():
                if not key.startswith("_"):
                    result[key] = value

        # 获取类级别的公共属性（非下划线开头、非方法、非内置类型）
        for key in dir(bean):
            if key.startswith("_"):
                continue
            if key in result:
                continue
            try:
                value = getattr(bean, key)
                if not callable(value):
                    result[key] = value
            except Exception:
                continue

        return result

    @staticmethod
    def copy_properties(source: Any, target: Any, *ignore_properties: str) -> None:
        """
        复制属性，将源对象的属性值复制到目标对象

        :param source: 源对象
        :param target: 目标对象
        :param ignore_properties: 忽略的属性名列表
        """
        if source is None:
            raise ValueError("source不能为None")
        if target is None:
            raise ValueError("target不能为None")

        ignore_set = set(ignore_properties)

        if hasattr(source, "__dict__"):
            for key, value in source.__dict__.items():
                if key.startswith("_") or key in ignore_set:
                    continue
                if hasattr(target, key) or not hasattr(target, "__dict__"):
                    try:
                        setattr(target, key, value)
                    except (AttributeError, TypeError):
                        pass

    @staticmethod
    def to_bean(source: Any, clazz: Type[T], copy_options: Optional[dict] = None) -> T:
        """
        转为指定类型对象

        :param source: 源对象或字典
        :param clazz: 目标类型
        :param copy_options: 复制选项字典，可包含ignore_properties列表
        :return: 转换后的对象
        """
        if source is None:
            return None
        if clazz is None:
            raise ValueError("clazz不能为None")

        if isinstance(source, dict):
            ignore_error = (copy_options or {}).get("ignore_error", False)
            return BeanUtil.map_to_bean(source, clazz, ignore_error=ignore_error)

        try:
            target = clazz()
        except Exception as e:
            raise TypeError(f"无法实例化{clazz.__name__}: {e}") from e

        ignore_properties = (copy_options or {}).get("ignore_properties", ())
        BeanUtil.copy_properties(source, target, *ignore_properties)
        return target

    @staticmethod
    def to_bean_list(source_list: list, clazz: Type[T]) -> List[T]:
        """
        转为对象列表

        :param source_list: 源列表（字典列表或对象列表）
        :param clazz: 目标类型
        :return: 转换后的对象列表
        """
        if source_list is None:
            return []
        return [BeanUtil.to_bean(item, clazz) for item in source_list]

    @staticmethod
    def is_readable_bean(obj: Any) -> bool:
        """
        是否为可读的Bean，即拥有至少一个非下划线开头的公共属性

        :param obj: 待检测对象
        :return: 是否为可读Bean
        """
        if obj is None:
            return False

        # 检查__dict__中是否有非下划线开头的属性
        if hasattr(obj, "__dict__"):
            for key in obj.__dict__:
                if not key.startswith("_"):
                    return True

        # 检查类级别的公共属性
        for key in dir(obj):
            if key.startswith("_"):
                continue
            try:
                value = getattr(obj, key)
                if not callable(value):
                    return True
            except Exception:
                continue

        return False

    @staticmethod
    def fill_bean_with_map(map_data: dict, bean: Any, ignore_error: bool = False) -> None:
        """
        用字典填充Bean，将字典中的键值对设置到Bean的对应属性上

        :param map_data: 字典数据
        :param bean: Bean对象
        :param ignore_error: 是否忽略设置错误
        """
        if map_data is None:
            raise ValueError("map_data不能为None")
        if bean is None:
            raise ValueError("bean不能为None")

        for key, value in map_data.items():
            try:
                setattr(bean, key, value)
            except Exception as e:
                if not ignore_error:
                    raise ValueError(f"设置字段{key}失败: {e}") from e

    @staticmethod
    def is_bean(obj: Any) -> bool:
        """判断对象是否为 Bean（有公共属性的对象）。

        :param obj: 待检查的对象
        :return: 是否为 Bean
        """
        if obj is None or isinstance(obj, (int, float, str, bool, bytes, list, tuple, dict)):
            return False
        return hasattr(obj, "__dict__") and any(not k.startswith("_") for k in obj.__dict__)

    @staticmethod
    def is_empty(bean: Any) -> bool:
        """判断 Bean 的所有公共字段是否都为 None。

        :param bean: Bean 对象
        :return: 是否所有字段为 None
        """
        if bean is None:
            return True
        if hasattr(bean, "__dict__"):
            for key, value in bean.__dict__.items():
                if not key.startswith("_") and value is not None:
                    return False
        return True

    @staticmethod
    def is_not_empty(bean: Any) -> bool:
        """判断 Bean 是否有非 None 字段。

        :param bean: Bean 对象
        :return: 是否有非 None 字段
        """
        return not BeanUtil.is_empty(bean)

    @staticmethod
    def has_null_field(bean: Any) -> bool:
        """判断 Bean 是否有 None 字段。

        :param bean: Bean 对象
        :return: 是否有 None 字段
        """
        if bean is None:
            return True
        if hasattr(bean, "__dict__"):
            for key, value in bean.__dict__.items():
                if not key.startswith("_") and value is None:
                    return True
        return False

    @staticmethod
    def desc_for_each(obj: Any, func: callable) -> None:
        """遍历对象的公共字段并应用函数。

        :param obj: 对象或字典
        :param func: 接受 (key, value) 参数的函数
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                func(key, value)
        elif hasattr(obj, "__dict__"):
            for key, value in obj.__dict__.items():
                if not key.startswith("_"):
                    func(key, value)

    @staticmethod
    def fill_bean(obj: Any, supplier: callable) -> None:
        """用默认值填充 Bean 中为 None 的字段。

        :param obj: Bean 对象
        :param supplier: 接受字段名返回默认值的函数
        """
        if obj is None:
            return
        if hasattr(obj, "__dict__"):
            for key in list(obj.__dict__.keys()):
                if not key.startswith("_") and getattr(obj, key) is None:
                    setattr(obj, key, supplier(key))

    @staticmethod
    def trim_str_fields(obj: Any) -> None:
        """对 Bean 中所有字符串字段执行 strip() 去除首尾空白。

        :param obj: Bean 对象
        """
        if obj is None:
            return
        if hasattr(obj, "__dict__"):
            for key, value in obj.__dict__.items():
                if not key.startswith("_") and isinstance(value, str):
                    setattr(obj, key, value.strip())

    @staticmethod
    def copy_to_list(source_list: list, clazz: Type[T]) -> List[T]:
        """将字典列表拷贝为指定类型的对象列表。

        等价于 :meth:`to_bean_list`。

        :param source_list: 字典列表
        :param clazz: 目标类型
        :return: 对象列表
        """
        return BeanUtil.to_bean_list(source_list, clazz)
