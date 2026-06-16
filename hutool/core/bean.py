"""Bean工具类，提供对象与字典之间的转换、属性复制等功能"""

import inspect
from types import SimpleNamespace
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

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

    @staticmethod
    def has_setter(bean: Any, field: str) -> bool:
        """判断 Bean 是否有指定字段的 setter。

        :param bean: Bean 对象或类
        :param field: 字段名
        :return: 是否有 setter
        """
        if bean is None:
            return False
        setter_name = "set_" + field
        if hasattr(bean, setter_name) and callable(getattr(bean, setter_name)):
            return True
        return hasattr(bean, field)

    @staticmethod
    def has_getter(bean: Any, field: str) -> bool:
        """判断 Bean 是否有指定字段的 getter。

        :param bean: Bean 对象或类
        :param field: 字段名
        :return: 是否有 getter
        """
        if bean is None:
            return False
        getter_name = "get_" + field
        if hasattr(bean, getter_name) and callable(getattr(bean, getter_name)):
            return True
        return hasattr(bean, field)

    @staticmethod
    def has_public_field(bean: Any, field: str) -> bool:
        """判断 Bean 是否有指定的公共字段。

        :param bean: Bean 对象
        :param field: 字段名
        :return: 是否有公共字段
        """
        if bean is None:
            return False
        if hasattr(bean, "__dict__"):
            return field in bean.__dict__ and not field.startswith("_")
        return hasattr(bean, field) and not field.startswith("_")

    @staticmethod
    def create_dyna_bean(clazz: Optional[type] = None) -> Any:
        """创建动态 Bean。

        若提供 clazz 则实例化该类，否则返回 SimpleNamespace。

        :param clazz: Bean 类型，为 None 时使用 SimpleNamespace
        :return: 动态 Bean 对象
        """
        if clazz is None:
            return SimpleNamespace()
        return clazz()

    @staticmethod
    def get_bean_desc(clazz: type) -> Dict[str, Any]:
        """获取 Bean 的描述信息。

        返回类名、模块、公共字段列表等。

        :param clazz: Bean 类
        :return: 描述字典
        """
        if clazz is None:
            return {}
        result = {
            "class_name": clazz.__name__,
            "module": getattr(clazz, "__module__", ""),
            "fields": [],
        }
        if hasattr(clazz, "__annotations__"):
            result["fields"] = list(clazz.__annotations__.keys())
        elif hasattr(clazz, "__init__"):
            try:
                sig = inspect.signature(clazz.__init__)
                result["fields"] = [p for p in sig.parameters if p != "self"]
            except (ValueError, TypeError):
                pass
        return result

    @staticmethod
    def get_property(bean: Any, name: str) -> Any:
        """获取 Bean 属性值。

        优先尝试 ``get_<name>`` 方法，再尝试直接 ``getattr``。

        :param bean: Bean 对象
        :param name: 属性名
        :return: 属性值
        """
        if bean is None:
            return None
        getter = "get_" + name
        if hasattr(bean, getter) and callable(getattr(bean, getter)):
            return getattr(bean, getter)()
        return getattr(bean, name, None)

    @staticmethod
    def set_property(bean: Any, name: str, value: Any) -> None:
        """设置 Bean 属性值。

        优先尝试 ``set_<name>`` 方法，再尝试直接 ``setattr``。

        :param bean: Bean 对象
        :param name: 属性名
        :param value: 属性值
        """
        if bean is None:
            raise ValueError("bean 不能为 None")
        setter = "set_" + name
        if hasattr(bean, setter) and callable(getattr(bean, setter)):
            getattr(bean, setter)(value)
        else:
            setattr(bean, name, value)

    @staticmethod
    def map_to_bean_ignore_case(map_data: dict, clazz: Type[T]) -> T:
        """字典转对象（忽略键名大小写）。

        将字典键转为小写后与 Bean 属性的小写名匹配。

        :param map_data: 字典数据
        :param clazz: 目标 Bean 类型
        :return: Bean 对象
        """
        if map_data is None:
            raise ValueError("map_data 不能为 None")
        bean = clazz()
        BeanUtil.fill_bean_with_map_ignore_case(map_data, bean)
        return bean

    @staticmethod
    def fill_bean_with_map_ignore_case(map_data: dict, bean: Any) -> None:
        """用字典填充 Bean（忽略键名大小写）。

        :param map_data: 字典数据
        :param bean: Bean 对象
        """
        if map_data is None or bean is None:
            return
        bean_fields = {}
        if hasattr(bean, "__dict__"):
            for k in bean.__dict__:
                if not k.startswith("_"):
                    bean_fields[k.lower()] = k
        for key in dir(bean):
            if not key.startswith("_"):
                bean_fields[key.lower()] = key

        for key, value in map_data.items():
            real_key = bean_fields.get(key.lower())
            if real_key is not None:
                try:
                    setattr(bean, real_key, value)
                except (AttributeError, TypeError):
                    pass

    @staticmethod
    def to_bean_ignore_error(source: Any, clazz: Type[T]) -> T:
        """转为 Bean 对象，忽略转换错误。

        :param source: 源对象或字典
        :param clazz: 目标类型
        :return: Bean 对象
        """
        if source is None:
            return None
        if isinstance(source, dict):
            return BeanUtil.map_to_bean(source, clazz, ignore_error=True)
        try:
            target = clazz()
            BeanUtil.copy_properties(source, target)
            return target
        except Exception:
            return clazz()

    @staticmethod
    def to_bean_ignore_case(source: Any, clazz: Type[T]) -> T:
        """转为 Bean 对象，忽略大小写。

        :param source: 源对象或字典
        :param clazz: 目标类型
        :return: Bean 对象
        """
        if source is None:
            return None
        if isinstance(source, dict):
            return BeanUtil.map_to_bean_ignore_case(source, clazz)
        try:
            target = clazz()
            BeanUtil.copy_properties(source, target)
            return target
        except Exception:
            return clazz()

    @staticmethod
    def bean_to_map_enhanced(
        bean: Any,
        is_underline: bool = True,
        ignore_null: bool = False,
    ) -> dict:
        """对象转字典（增强版）。

        :param bean: Bean 对象
        :param is_underline: 是否将驼峰转为下划线
        :param ignore_null: 是否忽略 None 值
        :return: 字典
        """
        if bean is None:
            return {}
        result = BeanUtil.bean_to_map(bean)
        if ignore_null:
            result = {k: v for k, v in result.items() if v is not None}
        if is_underline:
            import re

            new_result = {}
            for k, v in result.items():
                snake = re.sub(r"([A-Z])", r"_\1", k).lower().lstrip("_")
                new_result[snake] = v
            result = new_result
        return result

    @staticmethod
    def copy_properties_with_options(
        source: Any,
        target: Any,
        copy_options: Optional[dict] = None,
    ) -> None:
        """带选项的属性复制。

        copy_options 支持的键：
        - ``ignore_properties``: 忽略的属性名列表
        - ``ignore_null``: 是否跳过 None 值
        - ``ignore_case``: 是否忽略属性名大小写

        :param source: 源对象
        :param target: 目标对象
        :param copy_options: 复制选项
        """
        if source is None or target is None:
            return
        opts = copy_options or {}
        ignore_props = set(opts.get("ignore_properties", ()))
        ignore_null = opts.get("ignore_null", False)
        ignore_case = opts.get("ignore_case", False)

        if ignore_case:
            ignore_props_lower = {p.lower() for p in ignore_props}
            target_fields = {}
            if hasattr(target, "__dict__"):
                for k in target.__dict__:
                    if not k.startswith("_"):
                        target_fields[k.lower()] = k

        source_dict = BeanUtil.bean_to_map(source) if not isinstance(source, dict) else source

        for key, value in source_dict.items():
            if ignore_null and value is None:
                continue
            if ignore_case:
                if key.lower() in ignore_props_lower:
                    continue
                real_key = target_fields.get(key.lower(), key)
            else:
                if key in ignore_props:
                    continue
                real_key = key
            try:
                setattr(target, real_key, value)
            except (AttributeError, TypeError):
                pass

    @staticmethod
    def is_match_name(name1: str, name2: str, ignore_case: bool = True) -> bool:
        """判断两个名称是否匹配。

        :param name1: 名称 1
        :param name2: 名称 2
        :param ignore_case: 是否忽略大小写
        :return: 是否匹配
        """
        if name1 is None or name2 is None:
            return name1 is name2
        if ignore_case:
            return name1.lower() == name2.lower()
        return name1 == name2

    @staticmethod
    def edit(lst: list, func: Callable[[Any], Any]) -> list:
        """对 Bean 列表中的每个元素应用转换函数。

        :param lst: Bean 列表
        :param func: 转换函数
        :return: 转换后的列表
        """
        if lst is None:
            return []
        return [func(item) for item in lst]

    @staticmethod
    def has_null_field_with_ignore(bean: Any, ignore_fields: Optional[List[str]] = None) -> bool:
        """判断 Bean 是否有 None 字段（可指定忽略字段）。

        :param bean: Bean 对象
        :param ignore_fields: 要忽略的字段名列表
        :return: 是否有 None 字段
        """
        if bean is None:
            return True
        ignore = set(ignore_fields or [])
        if hasattr(bean, "__dict__"):
            for key, value in bean.__dict__.items():
                if not key.startswith("_") and key not in ignore and value is None:
                    return True
        return False

    @staticmethod
    def get_field_names(obj: Any) -> List[str]:
        """获取对象的所有公共字段名。

        :param obj: 对象
        :return: 字段名列表
        """
        if obj is None:
            return []
        names = []
        if hasattr(obj, "__dict__"):
            for key in obj.__dict__:
                if not key.startswith("_"):
                    names.append(key)
        if not names:
            for key in dir(obj):
                if key.startswith("_"):
                    continue
                try:
                    value = getattr(obj, key)
                    if not callable(value):
                        names.append(key)
                except Exception:
                    continue
        return names

    @staticmethod
    def is_common_fields_equal(obj1: Any, obj2: Any) -> bool:
        """判断两个对象的公共字段值是否相等。

        取两个对象字段名的交集，比较对应值。

        :param obj1: 对象 1
        :param obj2: 对象 2
        :return: 公共字段是否全部相等
        """
        if obj1 is None and obj2 is None:
            return True
        if obj1 is None or obj2 is None:
            return False
        fields1 = set(BeanUtil.get_field_names(obj1))
        fields2 = set(BeanUtil.get_field_names(obj2))
        common = fields1 & fields2
        if not common:
            return True
        for name in common:
            v1 = BeanUtil.get_property(obj1, name)
            v2 = BeanUtil.get_property(obj2, name)
            if v1 != v2:
                return False
        return True
