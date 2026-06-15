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
