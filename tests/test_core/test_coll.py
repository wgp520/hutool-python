from hutool import CollUtil, ListUtil


class TestCollUtil:
    def test_is_empty(self):
        assert CollUtil.is_empty([]) is True
        assert CollUtil.is_empty(None) is True
        assert CollUtil.is_empty([1]) is False

    def test_is_not_empty(self):
        assert CollUtil.is_not_empty([1]) is True
        assert CollUtil.is_not_empty([]) is False

    def test_has_null(self):
        assert CollUtil.has_null([1, None, 3]) is True
        assert CollUtil.has_null([1, 2, 3]) is False

    def test_contains(self):
        assert CollUtil.contains([1, 2, 3], 2) is True
        assert CollUtil.contains([1, 2, 3], 4) is False

    def test_contains_any(self):
        assert CollUtil.contains_any([1, 2, 3], 2, 5) is True
        assert CollUtil.contains_any([1, 2, 3], 4, 5) is False

    def test_to_list(self):
        result = CollUtil.to_list(range(3))
        assert result == [0, 1, 2]

    def test_to_set(self):
        result = CollUtil.to_set([1, 2, 2, 3])
        assert result == {1, 2, 3}

    def test_group_by(self):
        data = [{"type": "a", "val": 1}, {"type": "b", "val": 2}, {"type": "a", "val": 3}]
        result = CollUtil.group_by(data, lambda x: x["type"])
        assert len(result["a"]) == 2
        assert len(result["b"]) == 1

    def test_partition(self):
        result = CollUtil.partition([1, 2, 3, 4, 5], 2)
        assert result == [[1, 2], [3, 4], [5]]

    def test_filter(self):
        result = CollUtil.filter([1, 2, 3, 4], lambda x: x % 2 == 0)
        assert result == [2, 4]

    def test_map(self):
        result = CollUtil.map_list([1, 2, 3], lambda x: x * 2)
        assert result == [2, 4, 6]

    def test_distinct(self):
        result = CollUtil.distinct([1, 2, 2, 3, 3])
        assert result == [1, 2, 3]

    def test_sort(self):
        result = CollUtil.sort([3, 1, 2])
        assert result == [1, 2, 3]

    def test_sort_reverse(self):
        result = CollUtil.sort([3, 1, 2], reverse=True)
        assert result == [3, 2, 1]

    def test_reverse(self):
        result = CollUtil.reverse([1, 2, 3])
        assert result == [3, 2, 1]

    def test_min(self):
        assert CollUtil.min_val([3, 1, 2]) == 1

    def test_max(self):
        assert CollUtil.max_val([3, 1, 2]) == 3

    def test_count(self):
        assert CollUtil.count([1, 2, 3, 4], lambda x: x % 2 == 0) == 2

    def test_find_first(self):
        result = CollUtil.find_first([1, 2, 3, 4], lambda x: x > 2)
        assert result == 3

    def test_find_last(self):
        result = CollUtil.find_last([1, 2, 3, 4], lambda x: x > 2)
        assert result == 4

    def test_any_match(self):
        assert CollUtil.any_match([1, 2, 3], lambda x: x > 2) is True
        assert CollUtil.any_match([1, 2, 3], lambda x: x > 5) is False

    def test_all_match(self):
        assert CollUtil.all_match([1, 2, 3], lambda x: x > 0) is True
        assert CollUtil.all_match([1, 2, 3], lambda x: x > 2) is False

    def test_none_match(self):
        assert CollUtil.none_match([1, 2, 3], lambda x: x > 5) is True
        assert CollUtil.none_match([1, 2, 3], lambda x: x > 2) is False

    def test_join(self):
        assert CollUtil.join(["a", "b", "c"], ",") == "a,b,c"

    def test_get_first(self):
        assert CollUtil.get_first([1, 2, 3]) == 1
        assert CollUtil.get_first([]) is None

    def test_get_last(self):
        assert CollUtil.get_last([1, 2, 3]) == 3
        assert CollUtil.get_last([]) is None

    def test_page(self):
        result = CollUtil.page([1, 2, 3, 4, 5], 1, 2)
        assert result == [1, 2]
        result = CollUtil.page([1, 2, 3, 4, 5], 2, 2)
        assert result == [3, 4]

    def test_new_array_list(self):
        result = CollUtil.new_array_list(1, 2, 3)
        assert result == [1, 2, 3]

    def test_new_hash_set(self):
        result = CollUtil.new_hash_set(1, 2, 2, 3)
        assert result == {1, 2, 3}

    def test_zip(self):
        result = CollUtil.zip_list(["a", "b"], [1, 2])
        assert result == {"a": 1, "b": 2}

    def test_remove_null(self):
        result = CollUtil.remove_null([1, None, 2, None, 3])
        assert result == [1, 2, 3]

    def test_flat_map(self):
        result = CollUtil.flat_map([[1, 2], [3, 4]], lambda x: x)
        assert result == [1, 2, 3, 4]

    def test_reduce(self):
        from functools import reduce

        result = reduce(lambda a, b: a + b, [1, 2, 3, 4], 0)
        assert result == 10


class TestListUtil:
    def test_sub(self):
        result = ListUtil.sub([1, 2, 3, 4], 1, 3)
        assert result == [2, 3]

    def test_page(self):
        result = ListUtil.page([1, 2, 3, 4, 5], 1, 2)
        assert result == [1, 2]

    def test_empty_if_null(self):
        assert ListUtil.empty_if_none(None) == []
        assert ListUtil.empty_if_none([1, 2]) == [1, 2]

    def test_default_if_empty(self):
        assert ListUtil.default_if_empty([], [1, 2]) == [1, 2]
        assert ListUtil.default_if_empty([3], [1, 2]) == [3]


class TestCollUtilSafeMinMax:
    """测试 safe_min 和 safe_max 方法"""

    # ── safe_min ────────────────────────────────────────────

    def test_safe_min_basic(self):
        """测试基本最小值"""
        assert CollUtil.safe_min([3, 1, 2]) == 1

    def test_safe_min_none(self):
        """测试 None 返回 None"""
        assert CollUtil.safe_min(None) is None

    def test_safe_min_empty(self):
        """测试空列表返回 None"""
        assert CollUtil.safe_min([]) is None

    def test_safe_min_single(self):
        """测试单元素"""
        assert CollUtil.safe_min([42]) == 42

    def test_safe_min_negative(self):
        """测试负数"""
        assert CollUtil.safe_min([-5, -1, -10]) == -10

    def test_safe_min_strings(self):
        """测试字符串"""
        assert CollUtil.safe_min(["banana", "apple", "cherry"]) == "apple"

    # ── safe_max ────────────────────────────────────────────

    def test_safe_max_basic(self):
        """测试基本最大值"""
        assert CollUtil.safe_max([3, 1, 2]) == 3

    def test_safe_max_none(self):
        """测试 None 返回 None"""
        assert CollUtil.safe_max(None) is None

    def test_safe_max_empty(self):
        """测试空列表返回 None"""
        assert CollUtil.safe_max([]) is None

    def test_safe_max_single(self):
        """测试单元素"""
        assert CollUtil.safe_max([42]) == 42

    def test_safe_max_negative(self):
        """测试负数"""
        assert CollUtil.safe_max([-5, -1, -10]) == -1

    def test_safe_max_strings(self):
        """测试字符串"""
        assert CollUtil.safe_max(["banana", "apple", "cherry"]) == "cherry"

    # ── find_duplicates ────────────────────────────────────

    def test_find_duplicates_basic(self):
        """测试基本查重"""
        assert CollUtil.find_duplicates([1, 2, 3, 2, 4, 3]) == [2, 3]

    def test_find_duplicates_no_duplicates(self):
        """测试无重复"""
        assert CollUtil.find_duplicates([1, 2, 3]) == []

    def test_find_duplicates_none_input(self):
        """测试 None 输入"""
        assert CollUtil.find_duplicates(None) == []

    def test_find_duplicates_empty(self):
        """测试空列表"""
        assert CollUtil.find_duplicates([]) == []

    def test_find_duplicates_strings(self):
        """测试字符串查重"""
        assert CollUtil.find_duplicates(["a", "b", "a", "c", "b"]) == ["a", "b"]
