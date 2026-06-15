"""
内存数据仓库，提供类 Django ORM 的内存数据查询接口。

支持 ``filter/exclude/order_by/get/first/last`` 等链式查询操作。
"""

from functools import reduce
from itertools import filterfalse
from operator import attrgetter
from typing import List, TypeVar

T = TypeVar("T")


class ObjectDoesNotExist(Exception):
    """查询结果为空时抛出。"""

    pass


class MultipleObjectsReturned(Exception):
    """查询结果多于一条时抛出。"""

    pass


def _lookups(filter_name):
    # type: (str) -> Optional[Callable]
    """
    获取内置查询谓词函数。

    :param filter_name: 查询谓词名称
    :return: 谓词函数，或 None
    """
    return {
        "gt": lambda obj_value, value: obj_value > value,
        "gte": lambda obj_value, value: obj_value >= value,
        "lt": lambda obj_value, value: obj_value < value,
        "lte": lambda obj_value, value: obj_value <= value,
        "startswith": lambda obj_value, value: obj_value.startswith(value),
        "istartswith": lambda obj_value, value: obj_value.lower().startswith(value.lower()),
        "endswith": lambda obj_value, value: obj_value.endswith(value),
        "iendswith": lambda obj_value, value: obj_value.lower().endswith(value.lower()),
        "contains": lambda obj_value, value: value in obj_value,
        "icontains": lambda obj_value, value: value.lower() in obj_value.lower(),
        "not_equal_to": lambda obj_value, value: obj_value != value,
        "in": lambda obj_value, value: obj_value in value,
        "not_in": lambda obj_value, value: obj_value not in value,
        "range": lambda obj_value, range_values: range_values[0] <= obj_value <= range_values[1],
    }.get(filter_name)


class MemoryRepo:
    """内存数据仓库，提供类 Django ORM 的内存数据查询接口。

    支持 ``filter/exclude/order_by/get/first/last`` 等链式查询操作。

    Examples::

        class User:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        repo = MemoryRepo([
            User("Alice", 30),
            User("Bob", 25),
            User("Charlie", 35),
        ])

        # 过滤
        result = repo.filter(age__gte=30).order_by("name")
        for user in result:
            print(user.name)  # Alice, Charlie

        # 获取单条
        bob = repo.get(name="Bob")

    :param queryset: 初始数据列表
    """

    def __init__(self, queryset: List[T]):
        self._data = list(queryset)

    @property
    def _queryset(self):
        # type: () -> List[T]
        return self._data

    def __iter__(self):
        return iter(self._queryset)

    def __getitem__(self, index):
        return self._queryset[index]

    def __len__(self):
        return len(self._queryset)

    def __bool__(self):
        return len(self._queryset) > 0

    def _copy(self, queryset):
        # type: (List[T]) -> MemoryRepo
        return self.__class__(queryset)

    def _filter_or_exclude(self, **kwargs):
        # type: (**Any) -> Callable
        """构建过滤函数。"""

        def _filter(obj):
            for key, value in kwargs.items():
                field_lookup = _lookups(key.split("__")[-1])
                lookup_key = key.replace("__", ".").split(".")

                # 如果 value 是可调用对象，用作自定义谓词
                if callable(value):
                    if not value(reduce(getattr, lookup_key, obj)):
                        return False
                    continue

                if field_lookup:
                    # 有查询谓词时，移除最后一段（谓词名）
                    lookup_key.pop()
                    lookup_match = field_lookup(reduce(getattr, lookup_key, obj), value)
                    if not lookup_match:
                        return False
                    continue

                field_match = reduce(getattr, lookup_key, obj) == value
                if not field_match:
                    return False
            return True

        return _filter

    # ── 查询方法 ──────────────────────────────────────────

    def filter(self, **kwargs):
        # type: (**Any) -> MemoryRepo
        """
        过滤数据，返回新仓库。

        支持 Django 风格的查询谓词，如 ``age__gt=18``、``name__contains="a"``。

        :param kwargs: 过滤条件
        :return: 过滤后的新 MemoryRepo
        """
        return self._copy(list(filter(self._filter_or_exclude(**kwargs), self._queryset)))

    def exclude(self, **kwargs):
        # type: (**Any) -> MemoryRepo
        """
        排除数据（与 filter 相反），返回新仓库。

        :param kwargs: 排除条件
        :return: 排除后的新 MemoryRepo
        """
        return self._copy(list(filterfalse(self._filter_or_exclude(**kwargs), self._queryset)))

    def order_by(self, key):
        # type: (str) -> MemoryRepo
        """
        排序，返回新仓库。

        以 ``"-"`` 前缀表示降序（如 ``"-age"``）。
        支持 ``"__"`` 嵌套属性（如 ``"dept__name"``）。

        :param key: 排序键，如 ``"name"`` 或 ``"-age"``
        :return: 排序后的新 MemoryRepo
        """
        reverse = False
        if key.startswith("-"):
            reverse = True
            key = key[1:]
        attr_key = key.replace("__", ".")
        return self._copy(sorted(self._queryset, key=attrgetter(attr_key), reverse=reverse))

    def get(self, **kwargs):
        # type: (**Any) -> T
        """
        获取满足条件的唯一一条记录。

        :param kwargs: 过滤条件
        :return: 匹配的记录
        :raises ObjectDoesNotExist: 无匹配记录
        :raises MultipleObjectsReturned: 匹配多于一条
        """
        clone = self.filter(**kwargs)
        num = len(clone)
        if num == 1:
            return clone[0]
        if not num:
            raise ObjectDoesNotExist("查询结果为空")
        raise MultipleObjectsReturned(f"查询返回了 {num} 条结果，期望 1 条")

    def find_first(self, **kwargs):
        # type: (**Any) -> Optional[T]
        """
        获取满足条件的第一条记录，无匹配时返回 ``None``。

        :param kwargs: 过滤条件
        :return: 匹配的记录或 None
        """
        clone = self.filter(**kwargs)
        if clone:
            return clone[0]
        return None

    def first(self):
        # type: () -> Optional[T]
        """
        获取第一条记录。

        :return: 第一条记录，仓库为空时返回 None
        """
        if self._queryset:
            return self._queryset[0]
        return None

    def last(self):
        # type: () -> Optional[T]
        """
        获取最后一条记录。

        :return: 最后一条记录，仓库为空时返回 None
        """
        if self._queryset:
            return self._queryset[-1]
        return None

    def all(self):
        # type: () -> MemoryRepo
        """
        返回所有数据的副本。

        :return: 包含所有数据的新 MemoryRepo
        """
        return self._copy(list(self._queryset))

    def exists(self):
        # type: () -> bool
        """
        判断是否有数据。

        :return: 是否非空
        """
        return bool(self)

    def count(self):
        # type: () -> int
        """
        返回数据条数。

        :return: 数据条数
        """
        return len(self)

    def as_dict(self, *keys):
        # type: (*str) -> Dict[tuple, T]
        """
        将数据转为字典，以指定字段的组合作为键。

        Examples::

            repo.as_dict("name")
            # {"Alice": <User>, "Bob": <User>, ...}

            repo.as_dict("name", "age")
            # {("Alice", 30): <User>, ...}

        :param keys: 一个或多个字段名
        :return: 以字段值元组为键的字典
        """
        d = {}  # type: Dict[tuple, T]
        for item in self._queryset:
            if len(keys) == 1:
                d[getattr(item, keys[0])] = item
            else:
                d[tuple(getattr(item, key) for key in keys)] = item
        return d
