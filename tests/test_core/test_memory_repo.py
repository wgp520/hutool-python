import pytest

from hutool import MemoryRepo
from hutool.core.memory_repo import MultipleObjectsReturned, ObjectDoesNotExist


class User:
    def __init__(self, name, age, role="user"):
        self.name = name
        self.age = age
        self.role = role


class Dept:
    def __init__(self, name):
        self.name = name


class Employee:
    def __init__(self, name, dept):
        self.name = name
        self.dept = dept


USERS = [
    User("Alice", 30, "admin"),
    User("Bob", 25, "user"),
    User("Charlie", 35, "user"),
    User("Diana", 28, "admin"),
]


class TestMemoryRepoBasic:
    """基础操作测试"""

    def test_all(self):
        repo = MemoryRepo(USERS)
        assert len(repo.all()) == 4

    def test_count(self):
        repo = MemoryRepo(USERS)
        assert repo.count() == 4

    def test_exists(self):
        assert MemoryRepo(USERS).exists() is True
        assert MemoryRepo([]).exists() is False

    def test_iter(self):
        repo = MemoryRepo(USERS)
        names = [u.name for u in repo]
        assert names == ["Alice", "Bob", "Charlie", "Diana"]

    def test_getitem(self):
        repo = MemoryRepo(USERS)
        assert repo[0].name == "Alice"
        assert repo[-1].name == "Diana"

    def test_first(self):
        assert MemoryRepo(USERS).first().name == "Alice"
        assert MemoryRepo([]).first() is None

    def test_last(self):
        assert MemoryRepo(USERS).last().name == "Diana"
        assert MemoryRepo([]).last() is None


class TestMemoryRepoFilter:
    """过滤测试"""

    def test_filter_exact(self):
        result = MemoryRepo(USERS).filter(role="admin")
        assert result.count() == 2
        assert result[0].name == "Alice"

    def test_filter_gt(self):
        result = MemoryRepo(USERS).filter(age__gt=30)
        assert result.count() == 1
        assert result[0].name == "Charlie"

    def test_filter_gte(self):
        result = MemoryRepo(USERS).filter(age__gte=30)
        assert result.count() == 2

    def test_filter_lt(self):
        result = MemoryRepo(USERS).filter(age__lt=28)
        assert result.count() == 1

    def test_filter_lte(self):
        result = MemoryRepo(USERS).filter(age__lte=28)
        assert result.count() == 2

    def test_filter_contains(self):
        result = MemoryRepo(USERS).filter(name__contains="li")
        assert result.count() == 2  # Alice, Charlie

    def test_filter_callable(self):
        result = MemoryRepo(USERS).filter(age=lambda a: 25 <= a <= 30)
        assert result.count() == 3

    def test_filter_chained(self):
        result = MemoryRepo(USERS).filter(role="admin").filter(age__gte=30)
        assert result.count() == 1
        assert result[0].name == "Alice"

    def test_filter_in(self):
        result = MemoryRepo(USERS).filter(name__in=["Alice", "Bob"])
        assert result.count() == 2

    def test_filter_range(self):
        result = MemoryRepo(USERS).filter(age__range=(26, 32))
        assert result.count() == 2  # Alice(30), Diana(28)

    def test_filter_no_match(self):
        result = MemoryRepo(USERS).filter(role="superadmin")
        assert result.count() == 0


class TestMemoryRepoExclude:
    """排除测试"""

    def test_exclude(self):
        result = MemoryRepo(USERS).exclude(role="admin")
        assert result.count() == 2
        assert all(u.role == "user" for u in result)

    def test_exclude_gt(self):
        result = MemoryRepo(USERS).exclude(age__gte=30)
        assert result.count() == 2


class TestMemoryRepoOrderBy:
    """排序测试"""

    def test_order_by_asc(self):
        result = MemoryRepo(USERS).order_by("age")
        assert [u.name for u in result] == ["Bob", "Diana", "Alice", "Charlie"]

    def test_order_by_desc(self):
        result = MemoryRepo(USERS).order_by("-age")
        assert [u.name for u in result] == ["Charlie", "Alice", "Diana", "Bob"]


class TestMemoryRepoGet:
    """get/find_first 测试"""

    def test_get_success(self):
        user = MemoryRepo(USERS).get(name="Bob")
        assert user.age == 25

    def test_get_not_found(self):
        with pytest.raises(ObjectDoesNotExist):
            MemoryRepo(USERS).get(name="NotExist")

    def test_get_multiple(self):
        with pytest.raises(MultipleObjectsReturned):
            MemoryRepo(USERS).get(role="user")

    def test_find_first(self):
        user = MemoryRepo(USERS).find_first(role="admin")
        assert user.name == "Alice"

    def test_find_first_not_found(self):
        result = MemoryRepo(USERS).find_first(name="NotExist")
        assert result is None


class TestMemoryRepoNested:
    """嵌套属性测试"""

    def test_nested_filter(self):
        employees = [
            Employee("E1", Dept("Engineering")),
            Employee("E2", Dept("Sales")),
            Employee("E3", Dept("Engineering")),
        ]
        result = MemoryRepo(employees).filter(dept__name="Engineering")
        assert result.count() == 2

    def test_nested_order_by(self):
        employees = [
            Employee("E1", Dept("Sales")),
            Employee("E2", Dept("Engineering")),
        ]
        result = MemoryRepo(employees).order_by("dept__name")
        assert result[0].dept.name == "Engineering"


class TestMemoryRepoAsDict:
    """as_dict 测试"""

    def test_as_dict_single_key(self):
        repo = MemoryRepo(USERS)
        d = repo.as_dict("name")
        assert d["Alice"].age == 30

    def test_as_dict_multiple_keys(self):
        repo = MemoryRepo(USERS)
        d = repo.as_dict("name", "role")
        assert d[("Alice", "admin")].age == 30
