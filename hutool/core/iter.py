"""
迭代工具类，提供常用的 itertools recipes。

对应 Python 官方 itertools recipes 文档中的常用工具函数，
兼容 Python 3.8（不依赖 3.10+ 的 ``itertools.pairwise``）。
"""

import collections
import itertools
from typing import Any, Callable, Iterable, Optional, Tuple, TypeVar

T = TypeVar("T")


class IterUtil:
    """迭代工具类，提供常用的 itertools recipes。

    所有方法均为静态方法，输入为任意可迭代对象，
    返回列表或生成器（按需）。
    """

    @staticmethod
    def take(n: int, iterable: Iterable) -> list:
        """
        取可迭代对象的前 *n* 项，返回列表。

        Examples::

            IterUtil.take(3, range(10))  -> [0, 1, 2]
            IterUtil.take(5, "Hello")    -> ['H', 'e', 'l', 'l', 'o']

        :param n: 取前 N 项
        :param iterable: 可迭代对象
        :return: 前 N 项组成的列表
        """
        return list(itertools.islice(iterable, n))

    @staticmethod
    def tail(n: int, iterable: Iterable) -> list:
        """
        取可迭代对象的后 *n* 项。

        Examples::

            IterUtil.tail(3, range(10))  -> [7, 8, 9]

        :param n: 取后 N 项
        :param iterable: 可迭代对象
        :return: 后 N 项组成的列表
        """
        return list(collections.deque(iterable, maxlen=n))

    @staticmethod
    def nth(iterable: Iterable, n: int, default: Any = None) -> Any:
        """
        返回可迭代对象的第 *n* 项（从 0 开始）。

        越界时返回 *default*。

        Examples::

            IterUtil.nth(range(10), 3)   -> 3
            IterUtil.nth(range(3), 10)   -> None
            IterUtil.nth(range(3), 10, -1) -> -1

        :param iterable: 可迭代对象
        :param n: 索引（从 0 开始）
        :param default: 越界时的默认值
        :return: 第 N 项或默认值
        """
        return next(itertools.islice(iterable, n, None), default)

    @staticmethod
    def all_equal(iterable: Iterable) -> bool:
        """
        判断可迭代对象中的所有元素是否相等。

        空可迭代对象返回 ``True``。

        Examples::

            IterUtil.all_equal([1, 1, 1])  -> True
            IterUtil.all_equal([1, 2, 1])  -> False

        :param iterable: 可迭代对象
        :return: 是否所有元素相等
        """
        g = itertools.groupby(iterable)
        return next(g, True) and not next(g, False)

    @staticmethod
    def quantify(iterable: Iterable, pred: Callable = bool) -> int:
        """
        统计可迭代对象中满足谓词条件的元素数量。

        Examples::

            IterUtil.quantify([1, 2, 3, 4], lambda x: x % 2 == 0)  -> 2

        :param iterable: 可迭代对象
        :param pred: 谓词函数，默认为 ``bool``（统计真值个数）
        :return: 满足条件的元素数量
        """
        return sum(1 for item in iterable if pred(item))

    @staticmethod
    def flatten(list_of_lists: Iterable) -> itertools.chain:
        """
        将一层嵌套的可迭代对象展平。

        返回生成器，惰性求值。

        Examples::

            list(IterUtil.flatten([[1, 2], [3, 4], [5]]))  -> [1, 2, 3, 4, 5]

        :param list_of_lists: 嵌套可迭代对象
        :return: 展平后的生成器
        """
        return itertools.chain.from_iterable(list_of_lists)

    @staticmethod
    def pairwise(iterable: Iterable) -> Iterable[Tuple]:
        """
        将可迭代对象中的相邻元素配对。

        返回 ``(s0, s1), (s1, s2), (s2, s3), ...`` 形式的生成器。

        兼容 Python 3.8（3.10+ 有 ``itertools.pairwise``）。

        Examples::

            list(IterUtil.pairwise("ABC"))  -> [('A','B'), ('B','C')]

        :param iterable: 可迭代对象
        :return: 相邻配对的生成器
        """
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    @staticmethod
    def grouper(iterable: Iterable, n: int, fillvalue: Any = None) -> Iterable[tuple]:
        """
        将可迭代对象按固定长度 *n* 分组，不足的用 *fillvalue* 填充。

        Examples::

            list(IterUtil.grouper("ABCDEFG", 3, 'x'))
            -> [('A','B','C'), ('D','E','F'), ('G','x','x')]

        :param iterable: 可迭代对象
        :param n: 每组长度
        :param fillvalue: 填充值
        :return: 分组元组的生成器
        """
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args, fillvalue=fillvalue)

    @staticmethod
    def roundrobin(*iterables: Iterable) -> Iterable:
        """
        交替轮询多个可迭代对象。

        Examples::

            list(IterUtil.roundrobin("ABC", "D", "EF"))
            -> ['A', 'D', 'E', 'B', 'F', 'C']

        :param iterables: 多个可迭代对象
        :return: 交替轮询的生成器
        """
        num_active = len(iterables)
        if num_active == 0:
            return
        nexts = itertools.cycle(iter(it).__next__ for it in iterables)
        while num_active:
            try:
                for next_func in nexts:
                    yield next_func()
            except StopIteration:
                num_active -= 1
                nexts = itertools.cycle(itertools.islice(nexts, num_active))

    @staticmethod
    def partition(pred: Callable, iterable: Iterable) -> Tuple[Iterable, Iterable]:
        """
        按谓词将可迭代对象分为两组：不满足条件的和满足条件的。

        返回 ``(false_iter, true_iter)`` 两个生成器。

        Examples::

            f, t = IterUtil.partition(lambda x: x % 2, range(5))
            list(f)  -> [0, 2, 4]
            list(t)  -> [1, 3]

        :param pred: 谓词函数
        :param iterable: 可迭代对象
        :return: ``(false_iter, true_iter)`` 元组
        """
        t1, t2 = itertools.tee(iterable)
        return itertools.filterfalse(pred, t1), filter(pred, t2)

    @staticmethod
    def powerset(iterable: Iterable) -> itertools.chain:
        """
        计算可迭代对象的幂集（所有子集）。

        Examples::

            list(IterUtil.powerset([1, 2, 3]))
            -> [(), (1,), (2,), (3,), (1,2), (1,3), (2,3), (1,2,3)]

        :param iterable: 可迭代对象
        :return: 幂集的生成器
        """
        s = list(iterable)
        return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))

    @staticmethod
    def unique_everseen(iterable: Iterable, key: Optional[Callable] = None) -> Iterable:
        """
        保序去重（记住所有已见元素）。

        与 :meth:`CollUtil.distinct` 功能类似，但返回生成器。

        Examples::

            list(IterUtil.unique_everseen("AAAABBBCCDAABBB"))  -> ['A','B','C','D']
            list(IterUtil.unique_everseen("ABBCcAD", str.lower))  -> ['A','B','C','D']

        :param iterable: 可迭代对象
        :param key: 可选的键函数，用于比较前转换元素
        :return: 去重后的生成器
        """
        seen = set()
        seen_add = seen.add
        if key is None:
            for element in itertools.filterfalse(seen.__contains__, iterable):
                seen_add(element)
                yield element
        else:
            for element in iterable:
                k = key(element)
                if k not in seen:
                    seen_add(k)
                    yield element

    @staticmethod
    def is_empty(iterable: Iterable) -> bool:
        """判断可迭代对象是否为空。

        :param iterable: 可迭代对象
        :return: 是否为空
        """
        if iterable is None:
            return True
        try:
            next(iter(iterable))
            return False
        except StopIteration:
            return True

    @staticmethod
    def is_not_empty(iterable: Iterable) -> bool:
        """判断可迭代对象是否不为空。

        :param iterable: 可迭代对象
        :return: 是否不为空
        """
        return not IterUtil.is_empty(iterable)

    @staticmethod
    def has_null(iterable: Iterable) -> bool:
        """判断可迭代对象中是否有 None 元素。

        :param iterable: 可迭代对象
        :return: 是否包含 None
        """
        if iterable is None:
            return False
        return any(item is None for item in iterable)

    @staticmethod
    def is_all_null(iterable: Iterable) -> bool:
        """判断可迭代对象中是否所有元素都为 None。

        :param iterable: 可迭代对象
        :return: 是否全部为 None
        """
        if iterable is None:
            return True
        return all(item is None for item in iterable)

    @staticmethod
    def count_map(iterable: Iterable, key_func: Optional[Callable] = None) -> dict:
        """统计各元素出现次数。

        :param iterable: 可迭代对象
        :param key_func: 可选的键函数
        :return: {元素: 出现次数}
        """
        result = {}
        for item in iterable:
            key = key_func(item) if key_func else item
            result[key] = result.get(key, 0) + 1
        return result

    @staticmethod
    def field_value_map(iterable: Iterable, key_field: str, value_field: str) -> dict:
        """将可迭代对象转为 {key_field值: value_field值} 映射。

        :param iterable: 可迭代对象（元素为 dict 或对象）
        :param key_field: 作为键的字段名
        :param value_field: 作为值的字段名
        :return: 字典映射
        """
        result = {}
        for item in iterable:
            if isinstance(item, dict):
                k = item.get(key_field)
                v = item.get(value_field)
            else:
                k = getattr(item, key_field, None)
                v = getattr(item, value_field, None)
            result[k] = v
        return result

    @staticmethod
    def join(iterable: Iterable, separator: str = ",") -> str:
        """将可迭代对象的元素拼接为字符串。

        :param iterable: 可迭代对象
        :param separator: 分隔符
        :return: 拼接后的字符串
        """
        return separator.join(str(item) for item in iterable)

    @staticmethod
    def to_map(iterable: Iterable, key_func: Callable, value_func: Optional[Callable] = None) -> dict:
        """将可迭代对象转为字典。

        :param iterable: 可迭代对象
        :param key_func: 键函数
        :param value_func: 值函数（默认元素本身）
        :return: 字典
        """
        result = {}
        for item in iterable:
            key = key_func(item)
            value = value_func(item) if value_func else item
            result[key] = value
        return result

    @staticmethod
    def to_list(iterable: Iterable) -> list:
        """将可迭代对象转为列表。

        :param iterable: 可迭代对象
        :return: 列表
        """
        if iterable is None:
            return []
        return list(iterable)

    @staticmethod
    def get(iterable: Iterable, index: int) -> Any:
        """获取可迭代对象中指定索引的元素。

        :param iterable: 可迭代对象
        :param index: 索引
        :return: 元素，越界返回 None
        """
        if iterable is None:
            return None
        try:
            for i, item in enumerate(iterable):
                if i == index:
                    return item
        except TypeError:
            return None
        return None

    @staticmethod
    def get_first(iterable: Iterable) -> Any:
        """获取第一个元素。

        :param iterable: 可迭代对象
        :return: 第一个元素，为空返回 None
        """
        if iterable is None:
            return None
        try:
            return next(iter(iterable))
        except StopIteration:
            return None

    @staticmethod
    def get_first_none_null(iterable: Iterable) -> Any:
        """获取第一个非 None 的元素。

        :param iterable: 可迭代对象
        :return: 第一个非 None 元素，全为 None 则返回 None
        """
        if iterable is None:
            return None
        for item in iterable:
            if item is not None:
                return item
        return None

    @staticmethod
    def first_match(iterable: Iterable, predicate: Callable[[Any], bool]) -> Any:
        """获取第一个满足条件的元素。

        :param iterable: 可迭代对象
        :param predicate: 条件函数
        :return: 满足条件的第一个元素，无匹配返回 None
        """
        if iterable is None:
            return None
        for item in iterable:
            if predicate(item):
                return item
        return None

    @staticmethod
    def get_element_type(iterable: Iterable) -> Optional[type]:
        """获取可迭代对象中第一个元素的类型。

        :param iterable: 可迭代对象
        :return: 元素类型，为空返回 None
        """
        if iterable is None:
            return None
        try:
            first = next(iter(iterable))
            return type(first)
        except StopIteration:
            return None

    @staticmethod
    def edit(iterable: Iterable, func: Callable[[Any], Any]) -> list:
        """对每个元素应用函数。

        :param iterable: 可迭代对象
        :param func: 转换函数
        :return: 转换后的列表
        """
        if iterable is None:
            return []
        return [func(item) for item in iterable]

    @staticmethod
    def filter_(iterable: Iterable, predicate: Callable[[Any], bool]) -> list:
        """过滤并返回新列表。

        :param iterable: 可迭代对象
        :param predicate: 过滤条件
        :return: 过滤后的列表
        """
        if iterable is None:
            return []
        return [item for item in iterable if predicate(item)]

    @staticmethod
    def filter_to_list(iterable: Iterable, predicate: Callable[[Any], bool]) -> list:
        """过滤并返回新列表（等同于 filter_）。

        :param iterable: 可迭代对象
        :param predicate: 过滤条件
        :return: 过滤后的列表
        """
        return IterUtil.filter_(iterable, predicate)

    @staticmethod
    def for_each(iterable: Iterable, func: Callable[[Any], None]) -> None:
        """对每个元素执行操作。

        :param iterable: 可迭代对象
        :param func: 操作函数
        """
        if iterable is not None:
            for item in iterable:
                func(item)

    @staticmethod
    def to_str(iterable: Iterable, separator: str = ",") -> str:
        """将可迭代对象转为字符串表示。

        :param iterable: 可迭代对象
        :param separator: 分隔符
        :return: 字符串
        """
        return IterUtil.join(iterable, separator)

    @staticmethod
    def size(iterable: Iterable) -> int:
        """获取可迭代对象的大小。

        :param iterable: 可迭代对象
        :return: 元素个数
        """
        if iterable is None:
            return 0
        if hasattr(iterable, "__len__"):
            return len(iterable)
        count = 0
        for _ in iterable:
            count += 1
        return count

    @staticmethod
    def is_equal_list(list1: list, list2: list) -> bool:
        """判断两个列表是否相等。

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
    def to_list_map(iterable: Iterable, key_func: Callable, value_func: Optional[Callable] = None) -> dict:
        """将可迭代对象转为 {key: [values]} 字典。

        :param iterable: 可迭代对象
        :param key_func: 提取键的函数
        :param value_func: 提取值的函数，为 None 时使用元素本身
        :return: 分组字典
        """
        result = {}
        for item in iterable:
            key = key_func(item)
            value = value_func(item) if value_func else item
            result.setdefault(key, []).append(value)
        return result

    @staticmethod
    def filtered(iterable: Iterable, predicate: Callable[[Any], bool]) -> Iterable:
        """返回惰性过滤后的迭代器。

        :param iterable: 可迭代对象
        :param predicate: 过滤条件函数
        :return: 过滤后的迭代器
        """
        return filter(predicate, iterable)

    @staticmethod
    def empty():
        """返回空迭代器。

        :return: 空迭代器
        """
        return iter([])

    @staticmethod
    def trans(iterable: Iterable, func: Callable) -> list:
        """迭代器类型转换。

        :param iterable: 可迭代对象
        :param func: 转换函数
        :return: 转换后的列表
        """
        return [func(item) for item in iterable]

    @staticmethod
    def clear(lst: list) -> None:
        """清空列表。

        :param lst: 列表
        """
        if lst is not None:
            lst.clear()

    @staticmethod
    def prepend(value: Any, iterable: Iterable) -> Iterable:
        """在迭代器前插入一个元素。

        :param value: 要插入的值
        :param iterable: 可迭代对象
        :return: 迭代器
        """
        return itertools.chain([value], iterable)

    @staticmethod
    def tabulate(func: Callable[[int], Any], start: int = 0) -> Iterable:
        """从函数生成迭代器 ``func(start), func(start+1), ...``。

        :param func: 接受 int 参数的函数
        :param start: 起始索引，默认 ``0``
        :return: 无限迭代器
        """
        return (func(i) for i in itertools.count(start))

    @staticmethod
    def consume(iterator: Iterable, n: int) -> None:
        """消耗迭代器的前 N 个元素（无返回值）。

        :param iterator: 迭代器
        :param n: 要消耗的元素数量
        """
        collections.deque(itertools.islice(iterator, n), maxlen=0)

    @staticmethod
    def pad_none(iterable: Iterable) -> Iterable:
        """迭代器结束后无限返回 ``None``。

        :param iterable: 可迭代对象
        :return: 无限迭代器
        """
        return itertools.chain(iterable, itertools.repeat(None))

    @staticmethod
    def n_cycles(iterable: Iterable, n: int) -> Iterable:
        """将迭代器重复 N 次。

        :param iterable: 可迭代对象
        :param n: 重复次数
        :return: 重复后的迭代器
        """
        return itertools.chain.from_iterable(itertools.repeat(tuple(iterable), n))

    @staticmethod
    def iter_except(
        func: Callable,
        exception: type = Exception,
        first: Any = None,
    ) -> Iterable:
        """迭代直到抛出异常。

        常用于集合迭代，当迭代结束时会抛出 ``exception``。

        :param func: 无参数的调用函数（每次调用返回下一个元素）
        :param exception: 终止异常类型，默认 ``Exception``
        :param first: 首次调用的默认值（不使用）
        :return: 迭代器
        """
        try:
            yield func()
        except exception:
            return
        while True:
            try:
                yield func()
            except exception:
                break

    @staticmethod
    def first_true(
        iterable: Iterable,
        predicate: Optional[Callable[[Any], bool]] = None,
        default: Any = None,
    ) -> Any:
        """返回第一个使谓词为 True 的元素。

        :param iterable: 可迭代对象
        :param predicate: 判断函数，默认 ``bool``
        :param default: 无匹配时的默认值
        :return: 第一个满足条件的元素，或默认值
        """
        if predicate is None:
            predicate = bool
        return next(filter(predicate, iterable), default)

    @staticmethod
    def random_product(*iterables: Iterable, repeat: int = 1) -> tuple:
        """从多个迭代器中随机选取组合。

        :param iterables: 多个可迭代对象
        :param repeat: 重复次数，默认 ``1``
        :return: 随机选取的元组
        """
        import random as _random

        pools = [tuple(pool) for pool in iterables] * repeat
        return tuple(_random.choice(pool) for pool in pools)

    @staticmethod
    def random_permutation(iterable: Iterable, r: Optional[int] = None) -> list:
        """随机排列。

        :param iterable: 可迭代对象
        :param r: 选取元素数量，默认为全部
        :return: 随机排列的列表
        """
        import random as _random

        pool = list(iterable)
        r = r if r is not None else len(pool)
        return _random.sample(pool, r)

    @staticmethod
    def random_combination(iterable: Iterable, r: int) -> tuple:
        """随机组合（无放回，无序）。

        :param iterable: 可迭代对象
        :param r: 选取元素数量
        :return: 随机组合的元组
        """
        import random as _random

        pool = tuple(iterable)
        indices = sorted(_random.sample(range(len(pool)), r))
        return tuple(pool[i] for i in indices)

    @staticmethod
    def nth_combination(iterable: Iterable, r: int, index: int) -> tuple:
        """返回第 N 个组合（等价于 ``itertools.combinations`` 的第 ``index`` 个结果）。

        :param iterable: 可迭代对象
        :param r: 组合长度
        :param index: 组合索引
        :return: 第 N 个组合的元组
        """
        pool = tuple(iterable)
        n = len(pool)
        if r < 0 or r > n:
            raise ValueError("r must be in range [0, n)")
        c = 1
        k = min(r, n - r)
        for i in range(1, k + 1):
            c = c * (n - k + i) // i
        if index < 0:
            index += c
        if index < 0 or index >= c:
            raise IndexError("combination index out of range")
        result = []
        while r:
            c, n, r = c * r // n, n - 1, r - 1
            while index >= c:
                index -= c
                c, n = c * (n - r) // n, n - 1
            result.append(pool[len(pool) - 1 - n])
        return tuple(result)
