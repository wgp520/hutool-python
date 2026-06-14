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
