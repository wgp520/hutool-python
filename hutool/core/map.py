"""字典工具类，对应 Java cn.hutool.core.map.MapUtil / BiMap / MapWrapper。

包含:
- MapUtil      : 静态工具方法集合
- MapWrapper   : MutableMapping 包装基类
- BiMap        : 双向字典（键↔值）
- FuncKeyDict  : 自定义键函数字典
- DictUtil     : 字典工具方法集合（兼容旧接口）
"""

from __future__ import annotations

from collections import OrderedDict
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from ._base import DefaultParam

__all__ = [
    "BiMap",
    "DictUtil",
    "FuncKeyDict",
    "MapUtil",
    "MapWrapper",
]

_K = TypeVar("_K")
_V = TypeVar("_V")
_DEFAULT_PARAM = DefaultParam()


# ====================================================================
# MapUtil
# ====================================================================


class MapUtil:
    """Map工具类，对应 Java cn.hutool.core.map.MapUtil"""

    # ----------------------------------------------------------------
    # 判断
    # ----------------------------------------------------------------

    @staticmethod
    def is_empty(m: dict) -> bool:
        """
        字典是否为空。

        :param m: 字典
        :return: 是否为空
        """
        return m is None or len(m) == 0

    @staticmethod
    def is_not_empty(m: dict) -> bool:
        """
        字典是否为非空。

        :param m: 字典
        :return: 是否为非空
        """
        return not MapUtil.is_empty(m)

    # ----------------------------------------------------------------
    # 创建
    # ----------------------------------------------------------------

    @staticmethod
    def new_hash_map(*args, **kwargs) -> dict:
        """
        新建 HashMap（Python dict）。

        :return: 新字典
        """
        return dict(*args, **kwargs)

    @staticmethod
    def new_linked_hash_map(*args, **kwargs) -> OrderedDict:
        """
        新建 LinkedHashMap（有序字典）。

        :return: 新有序字典
        """
        return OrderedDict(*args, **kwargs)

    @staticmethod
    def of(key, value) -> dict:
        """创建单键值对字典

        :param key: 键
        :param value: 值
        :return: 单键值对字典
        """
        return {key: value}

    @staticmethod
    def of_entries(*entries) -> dict:
        """通过键值对元组创建字典

        :param entries: (key, value) 元组序列
        :return: 字典
        """
        return dict(entries)

    @staticmethod
    def of_array(array: list) -> dict:
        """通过数组创建字典，如 [k1, v1, k2, v2, ...]

        :param array: 交替排列的键值列表，长度必须为偶数
        :return: 字典
        """
        if array is None:
            return {}
        if len(array) % 2 != 0:
            raise ValueError("数组长度必须为偶数")
        result = {}
        for i in range(0, len(array), 2):
            result[array[i]] = array[i + 1]
        return result

    @staticmethod
    def create_map(map_type: Optional[Type] = None) -> dict:
        """根据类型创建字典实例

        :param map_type: 字典类型
        :return: 字典实例
        """
        if map_type is None:
            return {}
        try:
            return map_type()
        except Exception:
            return {}

    # ----------------------------------------------------------------
    # 转换
    # ----------------------------------------------------------------

    @staticmethod
    def to_list_map(dict_list: Sequence[Dict[_K, _V]]) -> Dict[_K, List[_V]]:
        """行转列，合并相同的键，值合并为列表

        例如: [{'a':1,'b':1}, {'a':2,'b':2}] -> {'a':[1,2], 'b':[1,2]}

        :param dict_list: 字典列表
        :return: 键到列表的映射
        """
        result: Dict[_K, List[_V]] = {}
        if dict_list is None:
            return result
        for item in dict_list:
            if item is None:
                continue
            for key, value in item.items():
                result.setdefault(key, []).append(value)
        return result

    @staticmethod
    def to_dict_list(list_dict: Dict[_K, Sequence[_V]]) -> List[Dict[_K, _V]]:
        """列转行

        例如: {'a':[1,2], 'b':[1,2]} -> [{'a':1,'b':1}, {'a':2,'b':2}]

        :param list_dict: 键到列表的映射
        :return: 字典列表
        """
        result: List[Dict[_K, _V]] = []
        if MapUtil.is_empty(list_dict):
            return result
        keys = list(list_dict.keys())
        max_length = max(len(list_dict[key]) for key in keys)
        for i in range(max_length):
            item: Dict[_K, _V] = {}
            for key in keys:
                if i < len(list_dict[key]):
                    item[key] = list_dict[key][i]
            result.append(item)
        return result

    @staticmethod
    def join(m: dict, separator: str = "&", kv_separator: str = "=") -> str:
        """字典转字符串连接

        :param m: 字典
        :param separator: 键值对之间的分隔符
        :param kv_separator: 键与值之间的分隔符
        :return: 连接后的字符串
        """
        if MapUtil.is_empty(m):
            return ""
        return separator.join(f"{k}{kv_separator}{v}" for k, v in m.items())

    @staticmethod
    def sort_join(
        params: dict,
        separator: str = "&",
        kv_separator: str = "=",
    ) -> str:
        """字典按键排序后转字符串连接

        :param params: 字典
        :param separator: 键值对之间的分隔符
        :param kv_separator: 键与值之间的分隔符
        :return: 排序后连接的字符串
        """
        if MapUtil.is_empty(params):
            return ""
        return separator.join(f"{k}{kv_separator}{params[k]}" for k in sorted(params.keys()))

    # ----------------------------------------------------------------
    # 操作
    # ----------------------------------------------------------------

    @staticmethod
    def filter(m: dict, *keys) -> dict:
        """保留指定key的键值对，返回新字典

        :param m: 字典
        :param keys: 要保留的键
        :return: 新字典
        """
        if MapUtil.is_empty(m):
            return {}
        return {k: m[k] for k in keys if k in m}

    @staticmethod
    def filter_by_func(m: dict, filter_func: Callable) -> dict:
        """按条件过滤字典

        filter_func 接收 (key, value) 参数，返回 True 保留。

        :param m: 字典
        :param filter_func: 过滤函数 (key, value) -> bool
        :return: 过滤后的新字典
        """
        if MapUtil.is_empty(m):
            return {}
        return {k: v for k, v in m.items() if filter_func(k, v)}

    @staticmethod
    def map_values(m: dict, map_func: Callable) -> dict:
        """映射所有值

        :param m: 字典
        :param map_func: 映射函数 value -> new_value
        :return: 值映射后的新字典
        """
        if MapUtil.is_empty(m):
            return {}
        return {k: map_func(v) for k, v in m.items()}

    @staticmethod
    def sort(m: dict) -> OrderedDict:
        """按键排序，返回新OrderedDict

        :param m: 字典
        :return: 排序后的有序字典
        """
        if MapUtil.is_empty(m):
            return OrderedDict()
        return OrderedDict(sorted(m.items()))

    @staticmethod
    def sort_by_value(m: dict, reverse: bool = False) -> OrderedDict:
        """按值排序

        :param m: 字典
        :param reverse: 是否降序
        :return: 排序后的有序字典
        """
        if MapUtil.is_empty(m):
            return OrderedDict()
        return OrderedDict(sorted(m.items(), key=lambda item: item[1], reverse=reverse))

    @staticmethod
    def inverse(m: dict) -> dict:
        """键值互换

        互换键值对不检查值是否有重复，后加入的元素替换先加入的元素。

        :param m: 字典
        :return: 键值互换后的字典
        """
        if MapUtil.is_empty(m):
            return {}
        result = MapUtil.create_map(type(m))
        for k, v in m.items():
            result[v] = k
        return result

    @staticmethod
    def remove_any(m: dict, *keys) -> dict:
        """移除指定key，返回新字典

        :param m: 字典
        :param keys: 要移除的键
        :return: 移除后的新字典
        """
        if MapUtil.is_empty(m):
            return {}
        remove_set = set(keys)
        return {k: v for k, v in m.items() if k not in remove_set}

    @staticmethod
    def empty_if_null(m: Optional[dict]) -> dict:
        """None转空字典

        :param m: 字典，可能为None
        :return: 原字典或空字典
        """
        return {} if m is None else m

    @staticmethod
    def default_if_empty(m: dict, default: dict) -> dict:
        """如果为空返回默认

        :param m: 字典
        :param default: 默认字典
        :return: 非空的原字典或默认字典
        """
        return default if MapUtil.is_empty(m) else m

    # ----------------------------------------------------------------
    # 取值
    # ----------------------------------------------------------------

    @staticmethod
    def get_str(m: dict, key: str, default: str = "") -> str:
        """获取字符串值

        :param m: 字典
        :param key: 键
        :param default: 默认值
        :return: 字符串值
        """
        if MapUtil.is_empty(m):
            return default
        value = m.get(key)
        if value is None:
            return default
        return str(value)

    @staticmethod
    def get_int(m: dict, key: str, default: int = 0) -> int:
        """获取int值

        :param m: 字典
        :param key: 键
        :param default: 默认值
        :return: int值
        """
        if MapUtil.is_empty(m):
            return default
        value = m.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def get_float(m: dict, key: str, default: float = 0.0) -> float:
        """获取float值

        :param m: 字典
        :param key: 键
        :param default: 默认值
        :return: float值
        """
        if MapUtil.is_empty(m):
            return default
        value = m.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def get_bool(m: dict, key: str, default: bool = False) -> bool:
        """获取bool值

        :param m: 字典
        :param key: 键
        :param default: 默认值
        :return: bool值
        """
        if MapUtil.is_empty(m):
            return default
        value = m.get(key)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "on")
        return bool(value)

    @staticmethod
    def get(m: dict, key: str, default=None, cast_type=None) -> Any:
        """获取值，可选类型转换

        :param m: 字典
        :param key: 键
        :param default: 默认值
        :param cast_type: 类型转换函数（如 int, float, str）
        :return: 转换后的值
        """
        if MapUtil.is_empty(m):
            return default
        value = m.get(key)
        if value is None:
            return default
        if cast_type is not None:
            try:
                return cast_type(value)
            except (ValueError, TypeError):
                return default
        return value

    @staticmethod
    def get_first_not_null(m: dict, *keys) -> Any:
        """获取第一个非None的值

        :param m: 字典
        :param keys: 候选键
        :return: 第一个非None的值，或None
        """
        if MapUtil.is_empty(m):
            return None
        for key in keys:
            value = m.get(key)
            if value is not None:
                return value
        return None

    # ----------------------------------------------------------------
    # 批量操作
    # ----------------------------------------------------------------

    @staticmethod
    def group_by_field(
        dict_list: Sequence[Dict[_K, _V]],
        field_key: _K,
    ) -> Dict[_V, List[Dict[_K, _V]]]:
        """按字段分组

        :param dict_list: 字典列表
        :param field_key: 分组依据的键
        :return: 分组后的字典
        """
        result: Dict[_V, List[Dict[_K, _V]]] = {}
        if dict_list is None:
            return result
        for item in dict_list:
            group_key = item.get(field_key)
            result.setdefault(group_key, []).append(item)
        return result

    @staticmethod
    def flat(m: dict) -> List:
        """将字典展开为列表 [k1, v1, k2, v2, ...]

        :param m: 字典
        :return: 展开后的列表
        """
        if MapUtil.is_empty(m):
            return []
        result = []
        for k, v in m.items():
            result.append(k)
            result.append(v)
        return result

    @staticmethod
    def is_sub_map(sub: dict, full: dict) -> bool:
        """判断sub是否为full的子集

        :param sub: 子字典
        :param full: 完整字典
        :return: 是否为子集
        """
        if MapUtil.is_empty(sub):
            return True
        if MapUtil.is_empty(full):
            return False
        for k, v in sub.items():
            if k not in full or full[k] != v:
                return False
        return True

    @staticmethod
    def contains_key(m: dict, key: Any) -> bool:
        """字典是否包含指定键

        :param m: 字典
        :param key: 键
        :return: 是否包含
        """
        if MapUtil.is_empty(m):
            return False
        return key in m

    @staticmethod
    def contains_value(m: dict, value: Any) -> bool:
        """字典是否包含指定值

        :param m: 字典
        :param value: 值
        :return: 是否包含
        """
        if MapUtil.is_empty(m):
            return False
        return value in m.values()

    @staticmethod
    def top_n_keys(m: dict, n: int) -> list:
        """
        获取字典中值最大的前 N 个键。

        按值从大到小排序后返回前 N 个键。

        :param m: 字典
        :param n: 返回的键数量
        :return: 值最大的前 N 个键的列表

        ::

            >>> MapUtil.top_n_keys({'a': 3, 'b': 1, 'c': 5, 'd': 2}, 2)
            ['c', 'a']
        """
        if MapUtil.is_empty(m):
            return []
        sorted_items = sorted(m.items(), key=lambda item: item[1], reverse=True)
        return [k for k, _ in sorted_items[:n]]

    @staticmethod
    def merge(m1: dict, m2: dict) -> dict:
        """合并两个字典，返回新字典（m2 覆盖 m1）

        :param m1: 第一个字典
        :param m2: 第二个字典（优先级更高）
        :return: 合并后的新字典
        """
        result = {}
        if m1:
            result.update(m1)
        if m2:
            result.update(m2)
        return result

    @staticmethod
    def to_camel_case_map(m: dict) -> dict:
        """将字典的键转换为驼峰命名。

        :param m: 原字典（键为 snake_case 字符串）
        :return: 键为 camelCase 的新字典
        """
        if m is None:
            return {}
        result = {}
        for k, v in m.items():
            parts = k.split("_")
            camel = parts[0] + "".join(p.capitalize() for p in parts[1:])
            result[camel] = v
        return result

    @staticmethod
    def to_object_array(m: dict) -> list:
        """将字典转为二维数组 [[key, value], ...]。

        :param m: 字典
        :return: 二维数组
        """
        if m is None:
            return []
        return [[k, v] for k, v in m.items()]

    @staticmethod
    def join_ignore_null(m: dict, separator: str = "&", kv_sep: str = "=") -> str:
        """将字典拼接为查询字符串，忽略值为 None 的条目。

        :param m: 字典
        :param separator: 键值对分隔符
        :param kv_sep: 键值分隔符
        :return: 拼接后的字符串
        """
        if m is None:
            return ""
        parts = []
        for k, v in m.items():
            if v is not None:
                parts.append(f"{k}{kv_sep}{v}")
        return separator.join(parts)

    @staticmethod
    def edit(m: dict, func: Callable) -> dict:
        """对字典的每个值应用函数。

        :param m: 原字典
        :param func: 值转换函数，接收 (key, value) 参数
        :return: 新字典
        """
        if m is None:
            return {}
        return {k: func(k, v) for k, v in m.items()}

    @staticmethod
    def map_(m: dict, key_func=None, value_func=None) -> dict:
        """对字典的键和/或值进行映射。

        :param m: 原字典
        :param key_func: 键映射函数
        :param value_func: 值映射函数
        :return: 映射后的新字典
        """
        if m is None:
            return {}
        result = {}
        for k, v in m.items():
            new_key = key_func(k) if key_func else k
            new_value = value_func(v) if value_func else v
            result[new_key] = new_value
        return result

    @staticmethod
    def reverse(m: dict) -> dict:
        """反转字典（值做键，键做值），值重复时后者覆盖。

        :param m: 原字典
        :return: 反转后的字典
        """
        return MapUtil.inverse(m)

    @staticmethod
    def rename_key(m: dict, old_key: Any, new_key: Any) -> dict:
        """重命名字典的键。

        :param m: 原字典（会被修改）
        :param old_key: 旧键
        :param new_key: 新键
        :return: 修改后的字典
        """
        if m is not None and old_key in m:
            m[new_key] = m.pop(old_key)
        return m

    @staticmethod
    def remove_null_value(m: dict) -> dict:
        """移除值为 None 的条目。

        :param m: 原字典（会被修改）
        :return: 修改后的字典
        """
        if m is None:
            return {}
        keys_to_remove = [k for k, v in m.items() if v is None]
        for k in keys_to_remove:
            del m[k]
        return m

    @staticmethod
    def remove_by_value(m: dict, value: Any) -> dict:
        """移除指定值的所有条目。

        :param m: 原字典（会被修改）
        :param value: 要移除的值
        :return: 修改后的字典
        """
        if m is None:
            return {}
        keys_to_remove = [k for k, v in m.items() if v == value]
        for k in keys_to_remove:
            del m[k]
        return m

    @staticmethod
    def remove_if(m: dict, predicate: Callable) -> dict:
        """按条件移除条目。

        :param m: 原字典（会被修改）
        :param predicate: 条件函数，接收 (key, value)，返回 True 表示移除
        :return: 修改后的字典
        """
        if m is None:
            return {}
        keys_to_remove = [k for k, v in m.items() if predicate(k, v)]
        for k in keys_to_remove:
            del m[k]
        return m

    @staticmethod
    def get_any(m: dict, *keys: Any) -> Any:
        """按顺序查找第一个存在的键并返回其值。

        :param m: 字典
        :param keys: 多个键
        :return: 第一个存在的键对应的值，都不存在返回 None
        """
        if m is None:
            return None
        for key in keys:
            if key in m:
                return m[key]
        return None

    @staticmethod
    def get_double(m: dict, key: Any, default: float = 0.0) -> float:
        """获取 double 类型的值。

        :param m: 字典
        :param key: 键
        :param default: 默认值
        :return: float 值
        """
        if m is None or key not in m:
            return default
        v = m[key]
        if v is None:
            return default
        return float(v)

    @staticmethod
    def get_long(m: dict, key: Any, default: int = 0) -> int:
        """获取 long 类型的值。

        :param m: 字典
        :param key: 键
        :param default: 默认值
        :return: int 值
        """
        if m is None or key not in m:
            return default
        v = m[key]
        if v is None:
            return default
        return int(v)

    @staticmethod
    def get_date(m: dict, key: Any, default=None):
        """获取日期类型的值。

        :param m: 字典
        :param key: 键
        :param default: 默认值
        :return: 值（不做转换，直接返回）
        """
        if m is None or key not in m:
            return default
        return m[key]

    @staticmethod
    def entry(key: Any, value: Any) -> dict:
        """创建单键值对字典。

        :param key: 键
        :param value: 值
        :return: 单键值对字典
        """
        return {key: value}

    @staticmethod
    def compute_if_absent(m: dict, key: Any, func: Callable) -> Any:
        """如果键不存在，则计算并添加值。

        :param m: 字典（会被修改）
        :param key: 键
        :param func: 值计算函数（接收 key 参数）
        :return: 值
        """
        if key not in m:
            m[key] = func(key)
        return m[key]

    @staticmethod
    def partition(m: dict, size: int) -> List[dict]:
        """将字典按大小分割为多个子字典。

        :param m: 字典
        :param size: 每个子字典的最大条目数
        :return: 子字典列表
        """
        if m is None:
            return []
        if size <= 0:
            raise ValueError("分割大小必须大于0")
        result = []
        current = {}
        for k, v in m.items():
            current[k] = v
            if len(current) >= size:
                result.append(current)
                current = {}
        if current:
            result.append(current)
        return result

    @staticmethod
    def flatten(m: dict, prefix: str = "", separator: str = ".") -> dict:
        """将嵌套字典扁平化。

        :param m: 嵌套字典
        :param prefix: 键前缀
        :param separator: 键分隔符
        :return: 扁平化后的字典
        """
        result = {}
        for k, v in m.items():
            new_key = f"{prefix}{separator}{k}" if prefix else k
            if isinstance(v, dict):
                result.update(MapUtil.flatten(v, new_key, separator))
            else:
                result[new_key] = v
        return result

    @staticmethod
    def values_of_keys(m: dict, keys: Iterable) -> list:
        """获取字典中指定键的值列表。

        :param m: 字典
        :param keys: 键列表
        :return: 值列表
        """
        if m is None:
            return []
        return [m[k] for k in keys if k in m]

    @staticmethod
    def new_tree_map() -> OrderedDict:
        """创建有序字典（TreeMap 等价）。

        :return: OrderedDict 实例
        """
        return OrderedDict()

    @staticmethod
    def new_identity_map() -> dict:
        """创建 IdentityMap（使用 id() 做键的字典）。

        注意：返回普通 dict，调用方需使用 ``id(obj)`` 做键。

        :return: 空字典
        """
        return {}

    @staticmethod
    def new_concurrent_hash_map() -> dict:
        """创建线程安全字典。

        Python 的 dict 本身在 CPython 中是线程安全的（GIL 保护）。
        此方法返回普通 dict，如需严格线程安全请使用 threading.Lock。

        :return: 空字典
        """
        return {}

    @staticmethod
    def wrap(m: dict) -> dict:
        """包装字典为不可修改视图。

        :param m: 原字典
        :return: 包装后的字典（types.MappingProxyType）
        """
        from types import MappingProxyType

        return MappingProxyType(m) if m is not None else {}

    @staticmethod
    def unmodifiable(m: dict) -> dict:
        """返回不可修改的字典视图。

        :param m: 原字典
        :return: 不可修改的映射
        """
        from types import MappingProxyType

        return MappingProxyType(m) if m is not None else {}

    @staticmethod
    def get_short(m: dict, key: str, default: int = 0) -> int:
        """获取 short 值（Python 中等同于 int）。

        :param m: 字典
        :param key: 键
        :param default: 默认值
        :return: int 值
        """
        if m is None:
            return default
        value = m.get(key, default)
        if value is None:
            return default
        return int(value)

    @staticmethod
    def get_char(m: dict, key: str, default: str = "") -> str:
        """获取 char 值（Python 中为单字符字符串）。

        :param m: 字典
        :param key: 键
        :param default: 默认值
        :return: 单字符字符串
        """
        if m is None:
            return default
        value = m.get(key, default)
        if value is None:
            return default
        return str(value)

    @staticmethod
    def empty() -> dict:
        """返回空字典。

        :return: 空字典
        """
        return {}

    @staticmethod
    def split_by_size(data: dict, size: int) -> list:
        """按大小分割字典为多个子字典。

        :param data: 原字典
        :param size: 每个子字典的最大大小
        :return: 子字典列表
        """
        if not data:
            return []
        if size <= 0:
            raise ValueError("size 必须大于 0")
        result = []
        current = {}
        for k, v in data.items():
            current[k] = v
            if len(current) >= size:
                result.append(current)
                current = {}
        if current:
            result.append(current)
        return result

    @staticmethod
    def sort_by_key(data: dict, reverse: bool = False) -> dict:
        """按 key 排序字典，返回 OrderedDict。

        :param data: 原字典
        :param reverse: 是否倒序
        :return: 排序后的字典
        """
        from collections import OrderedDict

        if not data:
            return OrderedDict()
        return OrderedDict(sorted(data.items(), key=lambda item: item[0], reverse=reverse))


# ====================================================================
# MapWrapper
# ====================================================================


class MapWrapper(OrderedDict):
    """字典包装类，通过包装一个已有字典实现特定功能。

    对应 Java cn.hutool.core.map.MapWrapper。
    继承 OrderedDict，可作为完整 dict 使用。
    """

    def __class_getitem__(cls, item):
        return cls

    def __init__(self, data: Optional[Dict[_K, _V]] = None, /, **kwargs):
        super().__init__()
        if data is not None:
            self.update(data)
        if kwargs:
            self.update(kwargs)

    # ------ 基础工具 ------

    def size(self) -> int:
        """获取字典大小

        :return: 字典大小
        """
        return len(self)

    def is_empty(self) -> bool:
        """字典是否为空

        :return: 字典是否为空
        """
        return self.size() == 0

    def is_not_empty(self) -> bool:
        """字典是否非空

        :return: 字典是否非空
        """
        return not self.is_empty()

    # ------ 序列化 ------

    def __repr__(self):
        items = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"{self.__class__.__name__}({{{items}}})"


# ====================================================================
# BiMap  (双向字典)
# ====================================================================


class BiMap(MapWrapper[_K, _V]):
    """双向Map，维护两个字典实现正向和反向查找。

    对应 Java cn.hutool.core.map.BiMap。
    互换键值对不检查值是否有重复，如果有则后加入的元素替换先加入的元素。
    """

    def __init__(self, data: Optional[dict] = None, /, **kwargs) -> None:
        """初始化

        :param data: 被包装的字典
        """
        self._inverse: Optional[Dict[_V, _K]] = None
        super().__init__(data, **kwargs)

    # ------ 内部维护反向字典 ------

    def _build_inverse(self) -> Dict[_V, _K]:
        """构建反向字典

        :return: 反向字典
        """
        return {v: k for k, v in self.items()}

    def _ensure_inverse(self) -> Dict[_V, _K]:
        """确保反向字典已构建

        :return: 反向字典
        """
        if self._inverse is None:
            self._inverse = self._build_inverse()
        return self._inverse

    def _invalidate_inverse(self) -> None:
        """标记反向字典需要重建"""
        self._inverse = None

    # ------ dict 协议重写 ------

    def __setitem__(self, key: _K, value: _V) -> None:
        old_value = self.get(key, None)
        inv = self._inverse
        if inv is not None:
            if old_value is not None and old_value in inv:
                del inv[old_value]
            inv[value] = key
        super().__setitem__(key, value)

    def __delitem__(self, key: _K) -> None:
        old_value = self.get(key, None)
        super().__delitem__(key)
        if self._inverse is not None and old_value is not None:
            if old_value in self._inverse:
                del self._inverse[old_value]

    # ------ update / setdefault / pop ------

    def update(self, __m=None, **kwargs: _V) -> None:  # type: ignore[override]
        """更新字典

        :param __m: 字典或者有两个元素的可迭代对象
        """
        if __m is not None:
            if isinstance(__m, dict):
                for k, v in __m.items():
                    self[k] = v
            else:
                for k, v in __m:
                    self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def setdefault(self, key: _K, default: _V = None) -> _V:
        """添加默认值，如果存在键则不添加

        :param key: 键
        :param default: 默认值
        :return: 值
        """
        if key in self:
            return self[key]
        self[key] = default
        return default

    def pop(self, key: _K, *args) -> _V:
        """弹出值

        :param key: 键
        :return: 值
        """
        value = super().pop(key, *args)
        if self._inverse is not None and value is not _DEFAULT_PARAM:
            if value in self._inverse:
                del self._inverse[value]
        return value

    def popitem(self, last: bool = True) -> Tuple[_K, _V]:
        """弹出键值对

        :return: 键值对
        """
        k, v = super().popitem(last=last)
        if self._inverse is not None and v in self._inverse:
            del self._inverse[v]
        return k, v

    def clear(self) -> None:
        super().clear()
        self._inverse = None

    # ------ 双向查找接口 ------

    def get(self, key: _K, default=None) -> Optional[_V]:  # type: ignore[override]
        """获取值

        :param key: 键
        :param default: 默认值
        :return: 值
        """
        return super().get(key, default)

    def get_key(self, value: _V, default=None) -> Optional[_K]:
        """根据值获得键

        :param value: 值
        :param default: 默认值
        :return: 键
        """
        return self._ensure_inverse().get(value, default)

    def get_inverse(self) -> Dict[_V, _K]:
        """获取反向字典（值->键）

        :return: 反向字典
        """
        return self._ensure_inverse()

    def reset_inverse(self) -> None:
        """重置反转的字典"""
        self._inverse = None

    # ------ 其他 ------

    def keys(self):  # type: ignore[override]
        """
        获取所有键。

        :return: 键的视图
        """
        return super().keys()

    def values(self):  # type: ignore[override]
        """
        获取所有值。

        :return: 值的视图
        """
        return super().values()

    def items(self):  # type: ignore[override]
        """
        获取所有键值对。

        :return: 键值对的视图
        """
        return super().items()

    def copy(self) -> BiMap[_K, _V]:
        """浅拷贝

        :return: BiMap副本
        """
        return BiMap(OrderedDict(self.items()))

    def __copy__(self) -> BiMap[_K, _V]:
        return self.copy()

    def __repr__(self):
        items = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"BiMap({{{items}}})"


# ====================================================================
# FuncKeyDict
# ====================================================================


class FuncKeyDict(MapWrapper[_K, _V]):
    """自定义函数Key风格的字典。

    所有键在存入和读取时都会经过 key_func 处理，例如统一转小写。
    """

    def __init__(
        self,
        data: Optional[Dict[_K, _V]] = None,
        key_func: Optional[Callable[[_K], _K]] = None,
        /,
        **kwargs,
    ):
        """初始化

        注意提供的字典中不能有键值对，否则可能导致自定义key失效。

        :param data: 提供的字典
        :param key_func: 自定义键函数
        """
        self._key_func = key_func
        super().__init__(data, **kwargs)

    def _transform_key(self, key: _K) -> _K:
        """根据函数自定义键

        :param key: 原始键
        :return: 自定义后的键
        """
        if self._key_func is not None:
            return self._key_func(key)
        return key

    def __getitem__(self, key: _K):
        return super().__getitem__(self._transform_key(key))

    def __setitem__(self, key: _K, value: _V):
        super().__setitem__(self._transform_key(key), value)

    def __delitem__(self, key: _K):
        super().__delitem__(self._transform_key(key))

    def __contains__(self, key: _K) -> bool:  # type: ignore[override]
        return super().__contains__(self._transform_key(key))

    def get(self, key: _K, default=None):  # type: ignore[override]
        return super().get(self._transform_key(key), default)

    def pop(self, key: _K, *args):
        return super().pop(self._transform_key(key), *args)

    def setdefault(self, key: _K, default: _V = None) -> _V:
        return super().setdefault(self._transform_key(key), default)

    @property
    def key_func(self) -> Optional[Callable[[_K], _K]]:
        """
        获取键函数。

        :return: 键函数
        """
        return self._key_func

    @key_func.setter
    def key_func(self, func: Callable[[_K], _K]) -> None:
        """
        设置键函数。

        :param func: 键函数
        """
        self._key_func = func

    def __repr__(self):
        items = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"FuncKeyDict({{{items}}})"


# ====================================================================
# DictUtil  (兼容旧接口，委托给 MapUtil)
# ====================================================================


class DictUtil:
    """字典相关工具类，兼容旧接口。

    部分方法直接委托给 MapUtil，部分保留独立实现。
    """

    @staticmethod
    def is_empty(value: dict) -> bool:
        """字典是否为空

        :param value: 字典
        :return: 是否为空
        """
        return MapUtil.is_empty(value)

    @staticmethod
    def is_not_empty(value: dict) -> bool:
        """字典是否为非空

        :param value: 字典
        :return: 是否为非空
        """
        return MapUtil.is_not_empty(value)

    @staticmethod
    def empty_if_none(value: Union[dict, None]) -> dict:
        """如果提供的集合为None, 返回一个空集合，否则返回原集合

        :param value: 提供的集合，可能为None
        :return: 原集合，若为None返回空集合
        """
        return MapUtil.empty_if_null(value)

    @staticmethod
    def default_if_empty(value: dict, default: dict) -> dict:
        """如果给定字典为空，返回默认字典

        :param value: 字典
        :param default: 默认字典
        :return: 非空（empty）的原字典或默认字典
        """
        return MapUtil.default_if_empty(value, default)

    @staticmethod
    def new_dict(is_ordered: bool = False, /, *args, **kwargs) -> dict:
        """新建一个字典

        DictUtil.new_dict({'a': 1}, zip(['b'], [2]), [('c', 3)], d=4)

        :param is_ordered: 字典的Key是否有序
        :return: 字典
        """
        res = OrderedDict() if is_ordered else dict()
        for arg in args:
            res.update(arg)
        if kwargs:
            res.update(**kwargs)
        return res

    @staticmethod
    def create_dict(dict_type: Optional[Type] = None) -> dict:
        """根据类型创建字典

        :param dict_type: 字典类型
        :return: 字典实例
        """
        return MapUtil.create_map(dict_type)

    @staticmethod
    def to_list_dict(dict_list: Sequence[Dict[_K, _V]]) -> Dict[_K, List[_V]]:
        """行转列，合并相同的键，值合并为列表

        传入: [{'a': 1, 'b': 1, 'c': 1}, {'a': 2, 'b': 2}, {'a': 3, 'b': 3}, {'a': 4}]
        结果: {'a': [1,2,3,4], 'b': [1,2,3], 'c': [1]}

        :param dict_list: 字典列表
        :return: 字典
        """
        return MapUtil.to_list_map(dict_list)

    @staticmethod
    def to_dict_list(list_dict: Dict[_K, Sequence[_V]]) -> List[Dict[_K, _V]]:
        """列转行

        传入: {'a': [1,2,3,4], 'b': [1,2,3], 'c': [1]}
        结果: [{'a': 1, 'b': 1, 'c': 1}, {'a': 2, 'b': 2}, {'a': 3, 'b': 3}, {'a': 4}]

        :param list_dict: 列表字典
        :return: 字典列表
        """
        return MapUtil.to_dict_list(list_dict)

    @staticmethod
    def inverse(data: Dict[_K, _V]) -> Dict[_V, _K]:
        """字典的键和值互换

        互换键值对不检查值是否有重复，如果有则后加入的元素替换先加入的元素。

        :param data: 字典
        :return: 互换后的字典
        """
        return MapUtil.inverse(data)
