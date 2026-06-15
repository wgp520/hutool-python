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
