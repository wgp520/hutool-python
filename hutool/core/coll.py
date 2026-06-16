"""
集合与列表工具类

对应 Java cn.hutool.core.collection.CollUtil 和 ListUtil
"""

import copy
import random
from typing import (
    Any,
    Callable,
    Iterable,
    List,
    Optional,
    Sequence,
    TypeVar,
)

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class CollUtil:
    """集合工具类，对应 Java cn.hutool.core.collection.CollUtil"""

    # ── 判断 ──────────────────────────────────────────────

    @staticmethod
    def is_empty(coll) -> bool:
        """
        集合是否为空，None 也视为空。

        支持 list/tuple/set/dict/frozenset。

        :param coll: 集合对象
        :return: 是否为空
        """
        if coll is None:
            return True
        return len(coll) == 0

    @staticmethod
    def is_not_empty(coll) -> bool:
        """
        集合是否为非空。

        :param coll: 集合对象
        :return: 是否为非空
        """
        return not CollUtil.is_empty(coll)

    @staticmethod
    def has_null(coll: Sequence) -> bool:
        """
        集合中是否有 None 元素。

        :param coll: 序列对象
        :return: 是否包含 None 元素
        """
        if coll is None:
            return True
        return any(element is None for element in coll)

    @staticmethod
    def contains(coll: Iterable, element: Any) -> bool:
        """
        是否包含指定元素。

        :param coll: 可迭代集合
        :param element: 待查找的元素
        :return: 是否包含
        """
        if coll is None:
            return False
        return element in coll

    @staticmethod
    def contains_any(coll: Iterable, *elements) -> bool:
        """
        是否包含任意一个指定元素。

        :param coll: 可迭代集合
        :param elements: 待查找的元素
        :return: 是否包含任意一个
        """
        if coll is None or not elements:
            return False
        if isinstance(coll, (set, frozenset)):
            return any(e in coll for e in elements)
        coll_set = set(coll) if not isinstance(coll, set) else coll
        return any(e in coll_set for e in elements)

    @staticmethod
    def contains_all(coll: Iterable, *elements) -> bool:
        """
        是否包含全部指定元素。

        :param coll: 可迭代集合
        :param elements: 待查找的元素
        :return: 是否包含全部
        """
        if coll is None:
            return False
        if not elements:
            return True
        coll_set = set(coll) if not isinstance(coll, set) else coll
        return all(e in coll_set for e in elements)

    # ── 创建 ──────────────────────────────────────────────

    @staticmethod
    def new_array_list(*args) -> list:
        """
        新建 ArrayList（Python list），可传入初始元素。

        :param args: 初始元素
        :return: 新列表
        """
        return list(args) if args else []

    @staticmethod
    def new_hash_set(*args) -> set:
        """
        新建 HashSet（Python set），可传入初始元素。

        :param args: 初始元素
        :return: 新集合
        """
        return set(args) if args else set()

    # ── 转换 ──────────────────────────────────────────────

    @staticmethod
    def to_list(iterable: Iterable) -> list:
        """
        转为列表。

        :param iterable: 可迭代对象
        :return: 列表
        """
        if iterable is None:
            return []
        if isinstance(iterable, list):
            return list(iterable)
        return list(iterable)

    @staticmethod
    def to_set(iterable: Iterable) -> set:
        """
        转为集合。

        :param iterable: 可迭代对象
        :return: 集合
        """
        if iterable is None:
            return set()
        return set(iterable)

    @staticmethod
    def to_map(
        items: Sequence,
        key_func: Callable,
        value_func: Optional[Callable] = None,
    ) -> dict:
        """列表转 Map，通过 key_func 提取键，value_func 提取值（默认值为元素本身）

        :param items: 待转换的列表
        :param key_func: 键提取函数
        :param value_func: 值提取函数，默认为元素本身
        :return: 字典
        """
        if items is None:
            return {}
        if value_func is None:

            def value_func(x):
                return x

        return {key_func(item): value_func(item) for item in items}

    @staticmethod
    def group_by(coll: Iterable, key_func: Callable) -> dict:
        """按条件分组，返回 {key: [items]}

        :param coll: 待分组集合
        :param key_func: 分组键提取函数
        :return: 分组字典
        """
        result: dict = {}
        if coll is None:
            return result
        for item in coll:
            key = key_func(item)
            result.setdefault(key, []).append(item)
        return result

    @staticmethod
    def partition(coll: List[T], size: int) -> List[List[T]]:
        """将列表按指定大小分割为子列表

        :param coll: 待分割列表
        :param size: 每个子列表的最大大小
        :return: 分割后的二维列表
        :raises ValueError: size 小于等于 0
        """
        if coll is None:
            return []
        if size <= 0:
            raise ValueError(f"size 必须大于 0，当前值: {size}")
        return [coll[i : i + size] for i in range(0, len(coll), size)]

    @staticmethod
    def zip_list(keys: list, values: list) -> dict:
        """两个列表合并为字典

        :param keys: 键列表
        :param values: 值列表
        :return: 合并后的字典
        """
        if keys is None or values is None:
            return {}
        return dict(zip(keys, values))

    # ── 操作 ──────────────────────────────────────────────

    @staticmethod
    def add_all(coll: list, *elements) -> list:
        """添加所有元素到列表，返回新列表

        :param coll: 原列表
        :param elements: 要添加的元素
        :return: 新列表
        """
        result = list(coll) if coll else []
        result.extend(elements)
        return result

    @staticmethod
    def remove_null(coll: list) -> list:
        """移除所有 None 元素，返回新列表

        :param coll: 原列表
        :return: 不含 None 的新列表
        """
        if coll is None:
            return []
        return [item for item in coll if item is not None]

    @staticmethod
    def filter(coll: List[T], filter_func: Callable[[T], bool]) -> List[T]:
        """过滤集合

        :param coll: 待过滤列表
        :param filter_func: 过滤函数，返回 True 保留
        :return: 过滤后的新列表
        """
        if coll is None:
            return []
        return [item for item in coll if filter_func(item)]

    @staticmethod
    def map_list(coll: List[T], map_func: Callable[[T], V]) -> List[V]:
        """映射集合

        :param coll: 待映射列表
        :param map_func: 映射函数
        :return: 映射后的新列表
        """
        if coll is None:
            return []
        return [map_func(item) for item in coll]

    @staticmethod
    def flat_map(coll: Iterable, map_func: Callable) -> list:
        """flatMap — 先映射再展平

        :param coll: 待处理集合
        :param map_func: 映射函数，返回可迭代对象
        :return: 展平后的新列表
        """
        if coll is None:
            return []
        result: list = []
        for item in coll:
            mapped = map_func(item)
            if mapped is not None:
                result.extend(mapped)
        return result

    @staticmethod
    def distinct(coll: List[T]) -> List[T]:
        """去重，保持顺序

        :param coll: 原列表
        :return: 去重后的新列表
        """
        if coll is None:
            return []
        seen: set = set()
        result: List[T] = []
        for item in coll:
            try:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            except TypeError:
                # 不可哈希元素退化为 O(n) 线性查找
                if item not in result:
                    result.append(item)
        return result

    @staticmethod
    def sort(
        coll: List[T],
        key_func: Optional[Callable] = None,
        reverse: bool = False,
    ) -> List[T]:
        """排序，返回新列表

        :param coll: 待排序列表
        :param key_func: 排序键函数
        :param reverse: 是否降序
        :return: 排序后的新列表
        """
        if coll is None:
            return []
        return sorted(coll, key=key_func, reverse=reverse)

    @staticmethod
    def reverse(coll: List[T]) -> List[T]:
        """反转，返回新列表

        :param coll: 原列表
        :return: 反转后的新列表
        """
        if coll is None:
            return []
        return list(reversed(coll))

    @staticmethod
    def shuffle(coll: List[T]) -> List[T]:
        """随机打乱，返回新列表

        :param coll: 原列表
        :return: 打乱后的新列表
        """
        if coll is None:
            return []
        result = list(coll)
        random.shuffle(result)
        return result

    @staticmethod
    def min_val(coll: Iterable) -> Any:
        """取最小值

        :param coll: 可迭代集合
        :return: 最小值
        :raises ValueError: 集合为空
        """
        if coll is None:
            raise ValueError("集合为 None")
        items = list(coll)
        if not items:
            raise ValueError("集合为空")
        return min(items)

    @staticmethod
    def max_val(coll: Iterable) -> Any:
        """取最大值

        :param coll: 可迭代集合
        :return: 最大值
        :raises ValueError: 集合为空
        """
        if coll is None:
            raise ValueError("集合为 None")
        items = list(coll)
        if not items:
            raise ValueError("集合为空")
        return max(items)

    @staticmethod
    def safe_min(coll: Iterable):
        # type: (Iterable) -> Optional[Any]
        """
        安全地获取集合最小值，空集合返回 ``None`` 而非抛出异常。

        :param coll: 可迭代集合
        :return: 最小值，集合为空或为 ``None`` 时返回 ``None``
        """
        if coll is None:
            return None
        items = list(coll)
        if not items:
            return None
        return min(items)

    @staticmethod
    def safe_max(coll: Iterable):
        # type: (Iterable) -> Optional[Any]
        """
        安全地获取集合最大值，空集合返回 ``None`` 而非抛出异常。

        :param coll: 可迭代集合
        :return: 最大值，集合为空或为 ``None`` 时返回 ``None``
        """
        if coll is None:
            return None
        items = list(coll)
        if not items:
            return None
        return max(items)

    @staticmethod
    def count(coll: Iterable, predicate: Callable) -> int:
        """统计满足条件的元素个数

        :param coll: 可迭代集合
        :param predicate: 判断条件
        :return: 满足条件的元素数量
        """
        if coll is None:
            return 0
        return sum(1 for item in coll if predicate(item))

    @staticmethod
    def find_first(
        coll: Iterable,
        predicate: Callable,
    ) -> Optional[T]:
        """查找第一个满足条件的元素

        :param coll: 可迭代集合
        :param predicate: 判断条件
        :return: 第一个满足条件的元素，未找到返回 None
        """
        if coll is None:
            return None
        for item in coll:
            if predicate(item):
                return item
        return None

    @staticmethod
    def find_last(
        coll: List[T],
        predicate: Callable[[T], bool],
    ) -> Optional[T]:
        """查找最后一个满足条件的元素

        :param coll: 列表
        :param predicate: 判断条件
        :return: 最后一个满足条件的元素，未找到返回 None
        """
        if coll is None:
            return None
        for item in reversed(coll):
            if predicate(item):
                return item
        return None

    @staticmethod
    def any_match(coll: Iterable, predicate: Callable) -> bool:
        """是否任意一个匹配

        :param coll: 可迭代集合
        :param predicate: 判断条件
        :return: 是否有任一元素满足条件
        """
        if coll is None:
            return False
        return any(predicate(item) for item in coll)

    @staticmethod
    def all_match(coll: Iterable, predicate: Callable) -> bool:
        """是否全部匹配

        :param coll: 可迭代集合
        :param predicate: 判断条件
        :return: 是否所有元素都满足条件
        """
        if coll is None:
            return True
        return all(predicate(item) for item in coll)

    @staticmethod
    def none_match(coll: Iterable, predicate: Callable) -> bool:
        """是否无匹配

        :param coll: 可迭代集合
        :param predicate: 判断条件
        :return: 是否没有元素满足条件
        """
        return not CollUtil.any_match(coll, predicate)

    # ── 工具 ──────────────────────────────────────────────

    @staticmethod
    def join(coll: Iterable, separator: str = ",") -> str:
        """用连接符连接集合元素

        :param coll: 可迭代集合
        :param separator: 分隔符
        :return: 连接后的字符串
        """
        if coll is None:
            return ""
        return separator.join(str(item) for item in coll)

    @staticmethod
    def find_duplicates(lst: List[T]) -> List[T]:
        """
        查找列表中的重复元素，保留首次出现顺序。

        Examples::

            find_duplicates([1, 2, 3, 2, 4, 3]) -> [2, 3]

        :param lst: 待查找列表
        :return: 重复元素列表（保序）
        """
        if lst is None:
            return []
        seen = set()
        duplicates = []
        for item in lst:
            if item in seen:
                if item not in duplicates:
                    duplicates.append(item)
            else:
                seen.add(item)
        return duplicates

    @staticmethod
    def get_first(coll: Iterable) -> Optional[T]:
        """获取第一个元素

        :param coll: 可迭代集合
        :return: 第一个元素，为空时返回 None
        """
        if coll is None:
            return None
        for item in coll:
            return item
        return None

    @staticmethod
    def get_last(coll: List[T]) -> Optional[T]:
        """获取最后一个元素

        :param coll: 列表
        :return: 最后一个元素，为空时返回 None
        """
        if coll is None or len(coll) == 0:
            return None
        return coll[-1]

    @staticmethod
    def sub_list(coll: List[T], start: int, end: int) -> List[T]:
        """获取子列表

        :param coll: 原列表
        :param start: 起始索引（包含）
        :param end: 结束索引（不包含）
        :return: 子列表
        """
        if coll is None:
            return []
        return coll[start:end]

    @staticmethod
    def page(coll: List[T], page_num: int, page_size: int) -> List[T]:
        """分页，page_num 从 1 开始

        :param coll: 原列表
        :param page_num: 页码（从 1 开始）
        :param page_size: 每页大小
        :return: 当前页数据
        :raises ValueError: 参数非法
        """
        if coll is None:
            return []
        if page_num < 1:
            raise ValueError(f"page_num 必须 >= 1，当前值: {page_num}")
        if page_size < 1:
            raise ValueError(f"page_size 必须 >= 1，当前值: {page_size}")
        start = (page_num - 1) * page_size
        end = start + page_size
        return coll[start:end]

    @staticmethod
    def for_each(coll: Iterable, consumer: Callable) -> None:
        """遍历集合并对每个元素执行操作

        :param coll: 可迭代集合
        :param consumer: 消费函数
        """
        if coll is None:
            return
        for item in coll:
            consumer(item)

    @staticmethod
    def empty_if_none(coll) -> list:
        """None 转空列表

        :param coll: 可能为 None 的集合
        :return: 原集合或空列表
        """
        if coll is None:
            return []
        return list(coll)

    @staticmethod
    def default_if_empty(coll: list, default: list) -> list:
        """如果为空则返回默认值

        :param coll: 可能为空的列表
        :param default: 默认列表
        :return: 原列表或默认列表
        """
        if CollUtil.is_empty(coll):
            return default if default is not None else []
        return coll

    # ── 集合运算 ──────────────────────────────────────────────

    @staticmethod
    def is_sub(list1: list, list2: list) -> bool:
        """判断 list1 是否为 list2 的子集

        :param list1: 候选子集
        :param list2: 候选超集
        :return: 是否为子集
        """
        if list1 is None:
            return True
        if list2 is None:
            return False
        set2 = set(list2)
        return all(item in set2 for item in list1)

    @staticmethod
    def intersection(coll1: Iterable, coll2: Iterable) -> list:
        """求两个集合的交集，保持元素首次出现顺序

        :param coll1: 第一个集合
        :param coll2: 第二个集合
        :return: 交集列表
        """
        if coll1 is None or coll2 is None:
            return []
        set2 = set(coll2)
        seen: set = set()
        result: list = []
        for item in coll1:
            if item in set2 and item not in seen:
                seen.add(item)
                result.append(item)
        return result

    @staticmethod
    def disjunction(coll1: Iterable, coll2: Iterable) -> list:
        """求两个集合的对称差集（在 coll1 或 coll2 中但不同时在两者中的元素）

        :param coll1: 第一个集合
        :param coll2: 第二个集合
        :return: 对称差集列表
        """
        if coll1 is None and coll2 is None:
            return []
        if coll1 is None:
            return list(coll2)
        if coll2 is None:
            return list(coll1)
        set1 = set(coll1)
        set2 = set(coll2)
        return list(set1.symmetric_difference(set2))

    # ---- 集合运算（增强） ----

    @staticmethod
    def union(*colls: Iterable) -> list:
        """合并多个集合（不去重）。

        :param colls: 多个可迭代对象
        :return: 合并后的列表
        """
        result = []
        for c in colls:
            if c is not None:
                result.extend(c)
        return result

    @staticmethod
    def union_distinct(*colls: Iterable) -> list:
        """合并多个集合并去重。

        :param colls: 多个可迭代对象
        :return: 去重后的列表（保持首次出现顺序）
        """
        seen = set()
        result = []
        for c in colls:
            if c is not None:
                for item in c:
                    if item not in seen:
                        seen.add(item)
                        result.append(item)
        return result

    @staticmethod
    def intersection_distinct(coll1: Iterable, coll2: Iterable) -> list:
        """求交集（去重）。

        :param coll1: 集合1
        :param coll2: 集合2
        :return: 交集列表
        """
        if coll1 is None or coll2 is None:
            return []
        set2 = set(coll2)
        seen = set()
        result = []
        for item in coll1:
            if item in set2 and item not in seen:
                seen.add(item)
                result.append(item)
        return result

    @staticmethod
    def subtract(coll1: Iterable, coll2: Iterable) -> list:
        """求差集（coll1 有但 coll2 没有，不去重）。

        :param coll1: 集合1
        :param coll2: 集合2
        :return: 差集列表
        """
        if coll1 is None:
            return []
        if coll2 is None:
            return list(coll1)
        set2 = set(coll2)
        return [item for item in coll1 if item not in set2]

    # ---- 安全操作 ----

    @staticmethod
    def safe_contains(coll, element: Any) -> bool:
        """安全地判断集合是否包含元素（None 安全）。

        :param coll: 集合（可为 None）
        :param element: 要查找的元素
        :return: 是否包含
        """
        if coll is None:
            return False
        return element in coll

    @staticmethod
    def contains_by_pred(coll: Iterable, predicate: Callable[[Any], bool]) -> bool:
        """判断集合中是否有满足条件的元素。

        :param coll: 可迭代对象
        :param predicate: 条件函数
        :return: 是否有满足条件的元素
        """
        if coll is None:
            return False
        return any(predicate(item) for item in coll)

    # ---- 统计/映射 ----

    @staticmethod
    def count_map(coll: Iterable, key_func: Optional[Callable[[Any], Any]] = None) -> dict:
        """统计集合中各元素出现次数。

        :param coll: 可迭代对象
        :param key_func: 可选的键函数，用于分组统计
        :return: {元素: 出现次数}
        """
        result = {}
        for item in coll:
            key = key_func(item) if key_func else item
            result[key] = result.get(key, 0) + 1
        return result

    @staticmethod
    def field_value_map(coll: Iterable, key_field: str, value_field: str) -> dict:
        """将集合转为 {key_field值: value_field值} 的映射。

        :param coll: 可迭代对象（元素为 dict 或对象）
        :param key_field: 作为键的字段名
        :param value_field: 作为值的字段名
        :return: 字典映射
        """
        result = {}
        for item in coll:
            if isinstance(item, dict):
                k = item.get(key_field)
                v = item.get(value_field)
            else:
                k = getattr(item, key_field, None)
                v = getattr(item, value_field, None)
            result[k] = v
        return result

    @staticmethod
    def to_map_list(coll: Iterable, key_func: Callable) -> dict:
        """按 key_func 分组，值为列表。

        :param coll: 可迭代对象
        :param key_func: 键函数
        :return: {key: [values]}
        """
        result = {}
        for item in coll:
            key = key_func(item)
            result.setdefault(key, []).append(item)
        return result

    # ---- 分组/排序 ----

    @staticmethod
    def group(coll: Iterable, key_func: Callable) -> dict:
        """按条件分组。

        :param coll: 可迭代对象
        :param key_func: 分组键函数
        :return: {key: [items]}
        """
        return CollUtil.to_map_list(coll, key_func)

    @staticmethod
    def group_by_field(coll: Iterable, field: str) -> dict:
        """按字段分组。

        :param coll: 可迭代对象（元素为 dict 或对象）
        :param field: 分组字段名
        :return: {field_value: [items]}
        """

        def _key(item):
            if isinstance(item, dict):
                return item.get(field)
            return getattr(item, field, None)

        return CollUtil.group(coll, _key)

    @staticmethod
    def sort_page_all(coll: Iterable, key_func: Optional[Callable] = None, reverse: bool = False) -> list:
        """排序后返回全部。

        :param coll: 可迭代对象
        :param key_func: 排序键函数
        :param reverse: 是否降序
        :return: 排序后的列表
        """
        lst = list(coll) if coll is not None else []
        return sorted(lst, key=key_func, reverse=reverse) if key_func else sorted(lst, reverse=reverse)

    # ---- 工具方法 ----

    @staticmethod
    def pop_part(lst: list, count: int) -> list:
        """从列表头部弹出指定数量的元素。

        :param lst: 列表（会被修改）
        :param count: 弹出数量
        :return: 弹出的元素列表
        """
        if lst is None or count <= 0:
            return []
        result = []
        for _ in range(min(count, len(lst))):
            result.append(lst.pop(0))
        return result

    @staticmethod
    def split_list(lst: list, size: int) -> List[list]:
        """将列表按指定大小分割为多个子列表。

        :param lst: 列表
        :param size: 每个子列表的最大大小
        :return: 分割后的子列表
        """
        if lst is None:
            return []
        if size <= 0:
            raise ValueError("分割大小必须大于0")
        return [lst[i : i + size] for i in range(0, len(lst), size)]

    @staticmethod
    def edit(coll: Iterable, func: Callable[[Any], Any]) -> list:
        """对集合中每个元素应用函数并返回新列表。

        :param coll: 可迭代对象
        :param func: 转换函数
        :return: 转换后的新列表
        """
        if coll is None:
            return []
        return [func(item) for item in coll]

    @staticmethod
    def filter_new(coll: Iterable, predicate: Callable[[Any], bool]) -> list:
        """过滤并返回新列表（filter 的列表版本）。

        :param coll: 可迭代对象
        :param predicate: 过滤条件
        :return: 过滤后的新列表
        """
        if coll is None:
            return []
        return [item for item in coll if predicate(item)]

    @staticmethod
    def extract(coll: Iterable, func: Callable[[Any], Any]) -> list:
        """提取集合中每个元素的某个属性或转换结果。

        :param coll: 可迭代对象
        :param func: 提取函数
        :return: 提取结果列表
        """
        return CollUtil.edit(coll, func)

    @staticmethod
    def get_field_values(coll: Iterable, field: str) -> list:
        """获取集合中每个元素的某个字段值。

        :param coll: 可迭代对象（元素为 dict 或对象）
        :param field: 字段名
        :return: 字段值列表
        """

        def _get(item):
            if isinstance(item, dict):
                return item.get(field)
            return getattr(item, field, None)

        return CollUtil.edit(coll, _get)

    @staticmethod
    def index_of(coll: Sequence, element: Any) -> int:
        """查找元素在集合中的索引。

        :param coll: 序列
        :param element: 要查找的元素
        :return: 索引，不存在返回 -1
        """
        if coll is None:
            return -1
        try:
            return coll.index(element)
        except ValueError:
            return -1

    @staticmethod
    def index_of_all(coll: Sequence, element: Any) -> List[int]:
        """查找元素在集合中的所有索引。

        :param coll: 序列
        :param element: 要查找的元素
        :return: 索引列表
        """
        if coll is None:
            return []
        return [i for i, x in enumerate(coll) if x == element]

    @staticmethod
    def add_if_absent(lst: list, element: Any) -> bool:
        """如果元素不在列表中则添加。

        :param lst: 列表（会被修改）
        :param element: 要添加的元素
        :return: 是否添加了新元素
        """
        if element not in lst:
            lst.append(element)
            return True
        return False

    @staticmethod
    def get(coll: Sequence, index: int) -> Any:
        """安全地获取集合中指定索引的元素。

        :param coll: 序列
        :param index: 索引
        :return: 元素，越界返回 None
        """
        if coll is None or index < 0 or index >= len(coll):
            return None
        return coll[index]

    @staticmethod
    def get_any(coll: Iterable) -> Any:
        """获取集合中任意一个元素。

        :param coll: 可迭代对象
        :return: 任意元素，空集合返回 None
        """
        if coll is None:
            return None
        try:
            return next(iter(coll))
        except StopIteration:
            return None

    @staticmethod
    def values_of_keys(coll: Iterable, keys: Iterable) -> list:
        """获取字典集合中指定键的值。

        :param coll: 字典列表
        :param keys: 键列表
        :return: 值列表
        """
        result = []
        for item in coll:
            if isinstance(item, dict):
                for key in keys:
                    if key in item:
                        result.append(item[key])
        return result

    @staticmethod
    def size(coll) -> int:
        """获取集合大小（None 安全）。

        :param coll: 集合（可为 None）
        :return: 大小，None 返回 0
        """
        if coll is None:
            return 0
        return len(coll)

    @staticmethod
    def is_equal_list(list1: list, list2: list) -> bool:
        """判断两个列表是否相等（逐元素比较）。

        :param list1: 列表1
        :param list2: 列表2
        :return: 是否相等
        """
        if list1 is None and list2 is None:
            return True
        if list1 is None or list2 is None:
            return False
        if len(list1) != len(list2):
            return False
        return all(a == b for a, b in zip(list1, list2))

    @staticmethod
    def union_all(*colls: Iterable) -> list:
        """不去重并集。

        :param colls: 多个集合
        :return: 合并后的列表（不去重）
        """
        result = []
        for coll in colls:
            if coll is not None:
                result.extend(coll)
        return result

    @staticmethod
    def subtract_to_list(coll1: Iterable, coll2: Iterable) -> list:
        """差集，返回列表。

        :param coll1: 集合1
        :param coll2: 集合2
        :return: 属于 coll1 但不属于 coll2 的元素列表
        """
        return CollUtil.subtract(coll1, coll2)

    @staticmethod
    def new_linked_hash_set(*args) -> dict:
        """创建有序集合（Python 中用 dict 实现保序去重）。

        :param args: 初始元素
        :return: 有序集合（字典键）
        """
        return dict.fromkeys(args)

    @staticmethod
    def list(*args) -> list:
        """创建列表。

        :param args: 初始元素
        :return: 列表
        """
        return list(args)

    @staticmethod
    def new_linked_list(*args) -> list:
        """创建列表（LinkedList 等价）。

        :param args: 初始元素
        :return: 列表
        """
        return list(args)

    @staticmethod
    def create(coll_type, *args):
        """按类型创建集合并填充元素。

        :param coll_type: 集合类型（list, set, tuple 等）
        :param args: 初始元素
        :return: 指定类型的集合
        """
        return coll_type(args)

    @staticmethod
    def distinct_by(coll: Iterable, key_func: Callable) -> list:
        """按 key 函数去重。

        :param coll: 可迭代对象
        :param key_func: 提取去重键的函数
        :return: 去重后的列表
        """
        seen = set()
        result = []
        for item in coll:
            key = key_func(item)
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result

    @staticmethod
    def remove_any(coll: list, *elements) -> list:
        """移除列表中的指定元素。

        :param coll: 列表
        :param elements: 待移除的元素
        :return: 移除后的列表
        """
        result = list(coll)
        for ele in elements:
            while ele in result:
                result.remove(ele)
        return result

    @staticmethod
    def remove_empty(coll: list) -> list:
        """移除列表中的空字符串和 None。

        :param coll: 列表
        :return: 移除后的列表
        """
        return [x for x in coll if x is not None and x != ""]

    @staticmethod
    def remove_blank(coll: list) -> list:
        """移除列表中的空白字符串和 None。

        :param coll: 列表
        :return: 移除后的列表
        """
        return [x for x in coll if x is not None and (not isinstance(x, str) or x.strip())]

    @staticmethod
    def field_value_as_map(coll: Iterable, key_field: str, value_field: str) -> dict:
        """提取字段值构建 Map（同 field_value_map 别名）。

        :param coll: 可迭代对象
        :param key_field: 键字段名
        :param value_field: 值字段名
        :return: 字段值映射
        """
        return CollUtil.field_value_map(coll, key_field, value_field)

    @staticmethod
    def find_one_by_field(coll: Iterable, field: str, value: Any):
        """按字段查找单个元素。

        :param coll: 可迭代对象
        :param field: 字段名
        :param value: 期望的字段值
        :return: 匹配的元素，未找到返回 None
        """
        for item in coll:
            if (hasattr(item, field) and getattr(item, field) == value) or (
                isinstance(item, dict) and item.get(field) == value
            ):
                return item
        return None

    @staticmethod
    def last_index_of(coll: Sequence, element: Any) -> int:
        """查找元素最后出现的索引。

        :param coll: 序列
        :param element: 待查找元素
        :return: 最后出现的索引，未找到返回 -1
        """
        for i in range(len(coll) - 1, -1, -1):
            if coll[i] == element:
                return i
        return -1

    @staticmethod
    def to_tree_set(coll: Iterable, key_func: Optional[Callable] = None) -> list:
        """排序后去重。

        :param coll: 可迭代对象
        :param key_func: 排序键函数，可选
        :return: 排序去重后的列表
        """
        if key_func:
            unique = list({key_func(x): x for x in coll}.values())
            return sorted(unique, key=key_func)
        return sorted(set(coll))

    @staticmethod
    def add_all_if_not_contains(lst: list, *elements) -> list:
        """仅当元素不在列表中时才添加。

        :param lst: 列表
        :param elements: 待添加的元素
        :return: 添加后的列表
        """
        for ele in elements:
            if ele not in lst:
                lst.append(ele)
        return lst

    @staticmethod
    def get_element_type(coll: Iterable) -> Optional[type]:
        """获取集合中第一个非 None 元素的类型。

        :param coll: 可迭代对象
        :return: 元素类型，空集合返回 None
        """
        for item in coll:
            if item is not None:
                return type(item)
        return None

    @staticmethod
    def sort_by_pinyin(coll: list) -> list:
        """按拼音排序（适用于中文字符串列表）。

        :param coll: 字符串列表
        :return: 排序后的新列表
        """
        try:
            from pypinyin import lazy_pinyin

            return sorted(coll, key=lambda x: lazy_pinyin(str(x)))
        except ImportError:
            return sorted(coll, key=str)

    @staticmethod
    def reverse_new(coll: list) -> list:
        """反转列表，返回新列表（不修改原列表）。

        :param coll: 列表
        :return: 反转后的新列表
        """
        return list(reversed(coll))

    @staticmethod
    def key_set(coll_of_pairs: Iterable) -> list:
        """获取键值对集合的键列表。

        :param coll_of_pairs: 键值对可迭代对象（字典列表或 tuple 列表）
        :return: 键列表
        """
        result = []
        for item in coll_of_pairs:
            if isinstance(item, dict):
                result.extend(item.keys())
            elif isinstance(item, (list, tuple)) and len(item) >= 1:
                result.append(item[0])
        return result

    @staticmethod
    def unmodifiable(coll):
        """返回不可修改的列表视图（使用 tuple 包装）。

        :param coll: 集合
        :return: 不可修改的 tuple
        """
        return tuple(coll) if coll is not None else ()

    @staticmethod
    def clear(lst: list) -> None:
        """清空列表。

        :param lst: 列表
        """
        if lst is not None:
            lst.clear()

    @staticmethod
    def trans(coll: Iterable, func: Callable) -> list:
        """集合类型转换。

        :param coll: 可迭代对象
        :param func: 转换函数
        :return: 转换后的列表
        """
        return [func(item) for item in coll]


class ListUtil:
    """列表工具类"""

    @staticmethod
    def sub(lst: List[T], start: int, end: int) -> List[T]:
        """获取子列表，支持负索引

        :param lst: 原列表
        :param start: 起始索引（包含），支持负数
        :param end: 结束索引（不包含），支持负数
        :return: 子列表
        """
        if lst is None:
            return []
        return lst[start:end]

    @staticmethod
    def page(lst: List[T], page_num: int, page_size: int) -> List[T]:
        """分页

        :param lst: 原列表
        :param page_num: 页码（从 1 开始）
        :param page_size: 每页大小
        :return: 当前页数据
        """
        return CollUtil.page(lst, page_num, page_size)

    @staticmethod
    def empty_if_none(lst: Optional[List[T]]) -> List[T]:
        """None 转空列表

        :param lst: 可能为 None 的列表
        :return: 原列表或空列表
        """
        if lst is None:
            return []
        return lst

    @staticmethod
    def default_if_empty(
        lst: Optional[List[T]],
        default: List[T],
    ) -> List[T]:
        """如果为空则返回默认值

        :param lst: 可能为空的列表
        :param default: 默认列表
        :return: 原列表或默认列表
        """
        return CollUtil.default_if_empty(lst, default)

    @staticmethod
    def to_tree(
        lst: List[dict],
        id_field: str = "id",
        parent_field: str = "parentId",
        children_field: str = "children",
    ) -> List[dict]:
        """列表转树结构

        将扁平的、通过 parentId 互相引用的字典列表转换为嵌套树形结构。
        根节点的 parent_field 值为 None / 0 / 空字符串 / 不存在。

        :param lst: 扁平字典列表
        :param id_field: 主键字段名
        :param parent_field: 父级引用字段名
        :param children_field: 子节点列表字段名
        :return: 树形结构的根节点列表（深拷贝，不修改原数据）
        """
        if not lst:
            return []

        # 深拷贝避免修改原始数据
        items = copy.deepcopy(lst)

        # 建立 id -> node 映射，同时初始化 children
        node_map: dict = {}
        for item in items:
            item.setdefault(children_field, [])
            node_map[item[id_field]] = item

        # 根节点判定：parent 为 None、0、"" 或字段不存在
        root_values = {None, 0, ""}

        roots: List[dict] = []
        for item in items:
            parent_val = item.get(parent_field)
            if parent_val in root_values or parent_val not in node_map:
                # 是根节点（parent 为空、或 parent 引用不存在的节点也视为根）
                roots.append(item)
            else:
                # 挂到父节点的 children
                node_map[parent_val][children_field].append(item)

        return roots

    @staticmethod
    def sort_by_property(
        lst: List,
        prop_name: str,
        reverse: bool = False,
    ) -> List:
        """按属性排序

        适用于元素为字典或对象的列表。字典按键取值，对象按 getattr 取值。

        :param lst: 待排序列表
        :param prop_name: 属性名
        :param reverse: 是否降序
        :return: 排序后的新列表
        """
        if lst is None:
            return []

        def _key(item):
            if isinstance(item, dict):
                return item.get(prop_name)
            return getattr(item, prop_name, None)

        return sorted(lst, key=_key, reverse=reverse)

    @staticmethod
    def of(*elements: T) -> List[T]:
        """从可变参数创建列表。

        :param elements: 元素
        :return: 新列表
        """
        return list(elements)

    @staticmethod
    def empty() -> list:
        """返回空列表。

        :return: 空列表
        """
        return []

    @staticmethod
    def set_or_padding(lst: list, index: int, element: Any) -> list:
        """设置元素到指定索引，越界时自动填充 None。

        :param lst: 列表（会被修改）
        :param index: 索引
        :param element: 元素
        :return: 修改后的列表
        """
        if lst is None:
            lst = []
        while len(lst) <= index:
            lst.append(None)
        lst[index] = element
        return lst

    @staticmethod
    def last_index_of(lst: Sequence, element: Any) -> int:
        """查找元素最后一次出现的索引。

        :param lst: 序列
        :param element: 要查找的元素
        :return: 索引，不存在返回 -1
        """
        if lst is None:
            return -1
        for i in range(len(lst) - 1, -1, -1):
            if lst[i] == element:
                return i
        return -1

    @staticmethod
    def index_of_all(lst: Sequence, element: Any) -> List[int]:
        """查找元素的所有索引。

        :param lst: 序列
        :param element: 要查找的元素
        :return: 索引列表
        """
        return CollUtil.index_of_all(lst, element)

    @staticmethod
    def swap(lst: list, index1: int, index2: int) -> list:
        """交换列表中两个位置的元素。

        :param lst: 列表（会被修改）
        :param index1: 索引1
        :param index2: 索引2
        :return: 修改后的列表
        """
        if lst is None or len(lst) == 0:
            return lst
        lst[index1], lst[index2] = lst[index2], lst[index1]
        return lst

    @staticmethod
    def move(lst: list, src_index: int, dest_index: int) -> list:
        """移动列表中的元素到新位置。

        :param lst: 列表（会被修改）
        :param src_index: 源索引
        :param dest_index: 目标索引
        :return: 修改后的列表
        """
        if lst is None or src_index == dest_index:
            return lst
        element = lst.pop(src_index)
        lst.insert(dest_index, element)
        return lst

    @staticmethod
    def zip_(lst1: list, lst2: list) -> List[tuple]:
        """将两个列表压缩为元组列表。

        :param lst1: 列表1
        :param lst2: 列表2
        :return: [(a1, b1), (a2, b2), ...]
        """
        return list(zip(lst1, lst2))

    @staticmethod
    def split(lst: list, size: int) -> List[list]:
        """将列表按指定大小分割。

        :param lst: 列表
        :param size: 每份大小
        :return: 分割后的子列表
        """
        return CollUtil.split_list(lst, size)

    @staticmethod
    def split_avg(lst: list, limit: int) -> List[list]:
        """将列表平均分割为指定份数。

        :param lst: 列表
        :param limit: 份数
        :return: 平均分割后的子列表
        """
        if lst is None:
            return []
        if limit <= 0:
            raise ValueError("份数必须大于0")
        n = len(lst)
        if n == 0:
            return [[] for _ in range(limit)]
        size = (n + limit - 1) // limit  # 向上取整
        return [lst[i : i + size] for i in range(0, n, size)][:limit]

    @staticmethod
    def to_linked_list(*elements) -> list:
        """创建列表。

        :param elements: 初始元素
        :return: 列表
        """
        return list(elements)

    @staticmethod
    def sort_by_pinyin(lst: list) -> list:
        """按拼音排序。

        :param lst: 字符串列表
        :return: 排序后的新列表
        """
        try:
            from pypinyin import lazy_pinyin

            return sorted(lst, key=lambda x: lazy_pinyin(str(x)))
        except ImportError:
            return sorted(lst, key=str)

    @staticmethod
    def swap_to(lst: list, src_index: int, dest_index: int) -> list:
        """将元素从源位置移动到目标位置。

        :param lst: 列表
        :param src_index: 源索引
        :param dest_index: 目标索引
        :return: 修改后的列表
        """
        if not lst or src_index == dest_index:
            return lst
        element = lst.pop(src_index)
        lst.insert(dest_index, element)
        return lst

    @staticmethod
    def swap_element(lst: list, old_element, new_element) -> list:
        """替换列表中的所有指定元素。

        :param lst: 列表
        :param old_element: 旧元素
        :param new_element: 新元素
        :return: 修改后的列表
        """
        for i, item in enumerate(lst):
            if item == old_element:
                lst[i] = new_element
        return lst

    @staticmethod
    def unmodifiable(lst) -> list:
        """返回不可修改的列表（使用 tuple 包装）。

        :param lst: 列表
        :return: 不可修改的 tuple
        """
        return tuple(lst) if lst is not None else ()
