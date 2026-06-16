from hutool import IterUtil


class TestIterUtilTake:
    """测试 take 方法"""

    def test_take_basic(self):
        """测试基本取前 N 项"""
        assert IterUtil.take(3, range(10)) == [0, 1, 2]

    def test_take_zero(self):
        """测试取 0 项"""
        assert IterUtil.take(0, range(5)) == []

    def test_take_more_than_available(self):
        """测试取超过可用数量"""
        assert IterUtil.take(10, [1, 2, 3]) == [1, 2, 3]

    def test_take_string(self):
        """测试字符串迭代"""
        assert IterUtil.take(3, "Hello") == ["H", "e", "l"]


class TestIterUtilTail:
    """测试 tail 方法"""

    def test_tail_basic(self):
        """测试基本取后 N 项"""
        assert IterUtil.tail(3, range(10)) == [7, 8, 9]

    def test_tail_zero(self):
        """测试取 0 项"""
        assert IterUtil.tail(0, range(5)) == []

    def test_tail_more_than_available(self):
        """测试取超过可用数量"""
        assert IterUtil.tail(5, [1, 2, 3]) == [1, 2, 3]


class TestIterUtilNth:
    """测试 nth 方法"""

    def test_nth_basic(self):
        """测试基本取第 N 项"""
        assert IterUtil.nth(range(10), 3) == 3

    def test_nth_first(self):
        """测试取第 0 项"""
        assert IterUtil.nth([10, 20, 30], 0) == 10

    def test_nth_out_of_range(self):
        """测试越界返回默认值"""
        assert IterUtil.nth(range(3), 10) is None
        assert IterUtil.nth(range(3), 10, -1) == -1


class TestIterUtilAllEqual:
    """测试 all_equal 方法"""

    def test_all_equal_true(self):
        """测试所有元素相等"""
        assert IterUtil.all_equal([1, 1, 1]) is True

    def test_all_equal_false(self):
        """测试元素不全相等"""
        assert IterUtil.all_equal([1, 2, 1]) is False

    def test_all_equal_empty(self):
        """测试空列表"""
        assert IterUtil.all_equal([]) is True

    def test_all_equal_single(self):
        """测试单元素"""
        assert IterUtil.all_equal([42]) is True


class TestIterUtilQuantify:
    """测试 quantify 方法"""

    def test_quantify_basic(self):
        """测试基本统计"""
        assert IterUtil.quantify([1, 2, 3, 4], lambda x: x % 2 == 0) == 2

    def test_quantify_bool(self):
        """测试默认 bool 谓词"""
        assert IterUtil.quantify([True, False, 1, 0, "", "x"]) == 3


class TestIterUtilFlatten:
    """测试 flatten 方法"""

    def test_flatten_basic(self):
        """测试基本展平"""
        result = list(IterUtil.flatten([[1, 2], [3, 4], [5]]))
        assert result == [1, 2, 3, 4, 5]

    def test_flatten_empty(self):
        """测试空列表"""
        result = list(IterUtil.flatten([]))
        assert result == []


class TestIterUtilPairwise:
    """测试 pairwise 方法"""

    def test_pairwise_basic(self):
        """测试基本配对"""
        result = list(IterUtil.pairwise("ABC"))
        assert result == [("A", "B"), ("B", "C")]

    def test_pairwise_numbers(self):
        """测试数字配对"""
        result = list(IterUtil.pairwise([1, 2, 3, 4]))
        assert result == [(1, 2), (2, 3), (3, 4)]

    def test_pairwise_empty(self):
        """测试空列表"""
        result = list(IterUtil.pairwise([]))
        assert result == []

    def test_pairwise_single(self):
        """测试单元素"""
        result = list(IterUtil.pairwise([1]))
        assert result == []


class TestIterUtilGrouper:
    """测试 grouper 方法"""

    def test_grouper_basic(self):
        """测试基本分组"""
        result = list(IterUtil.grouper("ABCDEFG", 3, "x"))
        assert result == [("A", "B", "C"), ("D", "E", "F"), ("G", "x", "x")]

    def test_grouper_exact(self):
        """测试正好分完"""
        result = list(IterUtil.grouper("ABCDEF", 3))
        assert result == [("A", "B", "C"), ("D", "E", "F")]


class TestIterUtilRoundrobin:
    """测试 roundrobin 方法"""

    def test_roundrobin_basic(self):
        """测试交替轮询"""
        result = list(IterUtil.roundrobin("ABC", "D", "EF"))
        assert result == ["A", "D", "E", "B", "F", "C"]

    def test_roundrobin_two(self):
        """测试两个迭代器"""
        result = list(IterUtil.roundrobin([1, 3, 5], [2, 4]))
        assert result == [1, 2, 3, 4, 5]


class TestIterUtilPartition:
    """测试 partition 方法"""

    def test_partition_basic(self):
        """测试基本分区"""
        f, t = IterUtil.partition(lambda x: x % 2, range(5))
        assert list(f) == [0, 2, 4]
        assert list(t) == [1, 3]

    def test_partition_empty(self):
        """测试空列表"""
        f, t = IterUtil.partition(lambda x: x > 0, [])
        assert list(f) == []
        assert list(t) == []


class TestIterUtilPowerset:
    """测试 powerset 方法"""

    def test_powerset_basic(self):
        """测试基本幂集"""
        result = list(IterUtil.powerset([1, 2, 3]))
        assert result == [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]

    def test_powerset_empty(self):
        """测试空列表"""
        result = list(IterUtil.powerset([]))
        assert result == [()]


class TestIterUtilUniqueEverseen:
    """测试 unique_everseen 方法"""

    def test_unique_everseen_basic(self):
        """测试基本保序去重"""
        result = list(IterUtil.unique_everseen("AAAABBBCCDAABBB"))
        assert result == ["A", "B", "C", "D"]

    def test_unique_everseen_with_key(self):
        """测试带键函数的去重"""
        result = list(IterUtil.unique_everseen("ABBCcAD", str.lower))
        assert result == ["A", "B", "C", "D"]

    def test_unique_everseen_numbers(self):
        """测试数字去重"""
        result = list(IterUtil.unique_everseen([3, 1, 2, 1, 3, 2]))
        assert result == [3, 1, 2]

    def test_is_empty(self):
        assert IterUtil.is_empty([]) is True
        assert IterUtil.is_empty(None) is True
        assert IterUtil.is_empty([1]) is False
        assert IterUtil.is_empty(iter([])) is True

    def test_is_not_empty(self):
        assert IterUtil.is_not_empty([1]) is True
        assert IterUtil.is_not_empty([]) is False

    def test_has_null(self):
        assert IterUtil.has_null([1, None, 3]) is True
        assert IterUtil.has_null([1, 2, 3]) is False
        assert IterUtil.has_null(None) is False

    def test_is_all_null(self):
        assert IterUtil.is_all_null([None, None]) is True
        assert IterUtil.is_all_null([None, 1]) is False
        assert IterUtil.is_all_null(None) is True

    def test_count_map(self):
        result = IterUtil.count_map(["a", "b", "a"])
        assert result == {"a": 2, "b": 1}

    def test_count_map_with_key_func(self):
        result = IterUtil.count_map([1, 2, 3, 4], lambda x: "e" if x % 2 == 0 else "o")
        assert result == {"o": 2, "e": 2}

    def test_field_value_map(self):
        data = [{"n": "a", "v": 1}, {"n": "b", "v": 2}]
        result = IterUtil.field_value_map(data, "n", "v")
        assert result == {"a": 1, "b": 2}

    def test_join(self):
        assert IterUtil.join([1, 2, 3], "-") == "1-2-3"
        assert IterUtil.join(["a", "b"]) == "a,b"

    def test_to_map(self):
        data = [("a", 1), ("b", 2)]
        result = IterUtil.to_map(data, lambda x: x[0], lambda x: x[1])
        assert result == {"a": 1, "b": 2}

    def test_to_list(self):
        assert IterUtil.to_list([1, 2, 3]) == [1, 2, 3]
        assert IterUtil.to_list(None) == []
        assert IterUtil.to_list(range(3)) == [0, 1, 2]

    def test_get(self):
        assert IterUtil.get([10, 20, 30], 1) == 20
        assert IterUtil.get([10, 20], 10) is None
        assert IterUtil.get(None, 0) is None

    def test_get_first(self):
        assert IterUtil.get_first([10, 20]) == 10
        assert IterUtil.get_first([]) is None
        assert IterUtil.get_first(None) is None

    def test_get_first_none_null(self):
        assert IterUtil.get_first_none_null([None, 1, 2]) == 1
        assert IterUtil.get_first_none_null([None, None]) is None

    def test_first_match(self):
        assert IterUtil.first_match([1, 2, 3, 4], lambda x: x > 2) == 3
        assert IterUtil.first_match([1, 2], lambda x: x > 10) is None

    def test_get_element_type(self):
        assert IterUtil.get_element_type([1, 2, 3]) is int
        assert IterUtil.get_element_type(["a", "b"]) is str
        assert IterUtil.get_element_type([]) is None

    def test_edit(self):
        assert IterUtil.edit([1, 2, 3], lambda x: x * 2) == [2, 4, 6]
        assert IterUtil.edit(None, lambda x: x) == []

    def test_filter(self):
        assert IterUtil.filter_([1, 2, 3, 4], lambda x: x % 2 == 0) == [2, 4]

    def test_for_each(self):
        result = []
        IterUtil.for_each([1, 2, 3], lambda x: result.append(x))
        assert result == [1, 2, 3]

    def test_to_str(self):
        assert IterUtil.to_str([1, 2, 3], "-") == "1-2-3"

    def test_size(self):
        assert IterUtil.size([1, 2, 3]) == 3
        assert IterUtil.size(None) == 0
        assert IterUtil.size(range(5)) == 5

    def test_is_equal_list(self):
        assert IterUtil.is_equal_list([1, 2], [1, 2]) is True
        assert IterUtil.is_equal_list([1, 2], [1, 3]) is False
        assert IterUtil.is_equal_list(None, None) is True
