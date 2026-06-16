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

    def test_union_all(self):
        result = CollUtil.union_all([1, 2, 3], [2, 3, 4])
        assert result == [1, 2, 3, 2, 3, 4]

    def test_union_all_multiple(self):
        result = CollUtil.union_all([1], [2], [3])
        assert result == [1, 2, 3]

    def test_distinct_by(self):
        data = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}, {"id": 1, "name": "c"}]
        result = CollUtil.distinct_by(data, lambda x: x["id"])
        assert len(result) == 2
        assert result[0]["name"] == "a"
        assert result[1]["name"] == "b"

    def test_find_one_by_field(self):
        data = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
        result = CollUtil.find_one_by_field(data, "id", 2)
        assert result["name"] == "b"

    def test_find_one_by_field_not_found(self):
        data = [{"id": 1}, {"id": 2}]
        assert CollUtil.find_one_by_field(data, "id", 99) is None

    def test_sort_by_pinyin(self):
        result = CollUtil.sort_by_pinyin(["北京", "上海", "广州"])
        # without pypinyin, just returns sorted as-is
        assert isinstance(result, list)
        assert len(result) == 3

    def test_unmodifiable_coll(self):
        result = CollUtil.unmodifiable([1, 2, 3])
        assert isinstance(result, tuple)
        assert result == (1, 2, 3)

    def test_trans_coll(self):
        result = CollUtil.trans([1, 2, 3], lambda x: x * 2)
        assert result == [2, 4, 6]


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

    def test_to_linked_list(self):
        result = ListUtil.to_linked_list(1, 2, 3)
        assert result == [1, 2, 3]

    def test_sort_by_pinyin(self):
        result = ListUtil.sort_by_pinyin(["b", "a", "c"])
        assert result == ["a", "b", "c"]

    def test_swap_to(self):
        lst = [1, 2, 3, 4]
        ListUtil.swap_to(lst, 1, 3)
        assert lst == [1, 3, 4, 2]

    def test_swap_element(self):
        lst = [1, 2, 3, 2]
        ListUtil.swap_element(lst, 2, 99)
        assert lst == [1, 99, 3, 99]

    def test_unmodifiable(self):
        result = ListUtil.unmodifiable([1, 2, 3])
        assert isinstance(result, tuple)
        assert result == (1, 2, 3)


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

    def test_is_sub(self):
        assert CollUtil.is_sub([1, 2], [1, 2, 3]) is True
        assert CollUtil.is_sub([1, 4], [1, 2, 3]) is False
        assert CollUtil.is_sub([], [1, 2, 3]) is True
        assert CollUtil.is_sub(None, [1, 2]) is True
        assert CollUtil.is_sub([1], None) is False

    def test_intersection(self):
        result = CollUtil.intersection([1, 2, 3, 2], [2, 3, 4])
        assert result == [2, 3]
        assert CollUtil.intersection([], [1, 2]) == []
        assert CollUtil.intersection(None, [1, 2]) == []
        assert CollUtil.intersection([1, 2], None) == []

    def test_disjunction(self):
        result = sorted(CollUtil.disjunction([1, 2, 3], [2, 3, 4]))
        assert result == [1, 4]
        assert CollUtil.disjunction(None, None) == []

    def test_union(self):
        assert CollUtil.union([1, 2], [3, 4]) == [1, 2, 3, 4]
        assert CollUtil.union(None, [1]) == [1]
        assert CollUtil.union() == []

    def test_union_distinct(self):
        assert CollUtil.union_distinct([1, 2], [2, 3], [3, 4]) == [1, 2, 3, 4]
        assert CollUtil.union_distinct([1, 2], None, [3]) == [1, 2, 3]

    def test_intersection_distinct(self):
        assert CollUtil.intersection_distinct([1, 2, 2, 3], [2, 2, 3, 4]) == [2, 3]
        assert CollUtil.intersection_distinct(None, [1]) == []

    def test_subtract(self):
        assert CollUtil.subtract([1, 2, 3, 4], [2, 4]) == [1, 3]
        assert CollUtil.subtract(None, [1]) == []
        assert CollUtil.subtract([1, 2], None) == [1, 2]

    def test_safe_contains(self):
        assert CollUtil.safe_contains([1, 2, 3], 2) is True
        assert CollUtil.safe_contains(None, 1) is False
        assert CollUtil.safe_contains([1, 2], 5) is False

    def test_contains_by_pred(self):
        assert CollUtil.contains_by_pred([1, 2, 3], lambda x: x > 2) is True
        assert CollUtil.contains_by_pred([1, 2], lambda x: x > 5) is False
        assert CollUtil.contains_by_pred(None, lambda x: True) is False

    def test_count_map(self):
        result = CollUtil.count_map(["a", "b", "a", "c", "b", "a"])
        assert result == {"a": 3, "b": 2, "c": 1}

    def test_count_map_with_key_func(self):
        result = CollUtil.count_map([1, 2, 3, 4, 5], lambda x: "even" if x % 2 == 0 else "odd")
        assert result == {"odd": 3, "even": 2}

    def test_field_value_map(self):
        data = [{"name": "a", "id": 1}, {"name": "b", "id": 2}]
        result = CollUtil.field_value_map(data, "name", "id")
        assert result == {"a": 1, "b": 2}

    def test_to_map_list(self):
        data = [1, 2, 3, 4, 5]
        result = CollUtil.to_map_list(data, lambda x: "even" if x % 2 == 0 else "odd")
        assert result == {"odd": [1, 3, 5], "even": [2, 4]}

    def test_group(self):
        data = ["apple", "banana", "avocado", "blueberry"]
        result = CollUtil.group(data, lambda x: x[0])
        assert set(result.keys()) == {"a", "b"}
        assert len(result["a"]) == 2

    def test_group_by_field(self):
        data = [{"type": "a", "v": 1}, {"type": "b", "v": 2}, {"type": "a", "v": 3}]
        result = CollUtil.group_by_field(data, "type")
        assert len(result["a"]) == 2

    def test_sort_page_all(self):
        result = CollUtil.sort_page_all([3, 1, 2])
        assert result == [1, 2, 3]
        result2 = CollUtil.sort_page_all([3, 1, 2], reverse=True)
        assert result2 == [3, 2, 1]

    def test_pop_part(self):
        lst = [1, 2, 3, 4, 5]
        popped = CollUtil.pop_part(lst, 2)
        assert popped == [1, 2]
        assert lst == [3, 4, 5]

    def test_split_list(self):
        result = CollUtil.split_list([1, 2, 3, 4, 5], 2)
        assert result == [[1, 2], [3, 4], [5]]

    def test_edit(self):
        assert CollUtil.edit([1, 2, 3], lambda x: x * 2) == [2, 4, 6]
        assert CollUtil.edit(None, lambda x: x) == []

    def test_filter_new(self):
        assert CollUtil.filter_new([1, 2, 3, 4], lambda x: x % 2 == 0) == [2, 4]
        assert CollUtil.filter_new(None, lambda x: True) == []

    def test_extract(self):
        data = [{"name": "a"}, {"name": "b"}]
        assert CollUtil.extract(data, lambda x: x["name"]) == ["a", "b"]

    def test_get_field_values(self):
        data = [{"name": "a", "id": 1}, {"name": "b", "id": 2}]
        assert CollUtil.get_field_values(data, "name") == ["a", "b"]

    def test_index_of(self):
        assert CollUtil.index_of([1, 2, 3], 2) == 1
        assert CollUtil.index_of([1, 2, 3], 5) == -1
        assert CollUtil.index_of(None, 1) == -1

    def test_index_of_all(self):
        assert CollUtil.index_of_all([1, 2, 1, 3, 1], 1) == [0, 2, 4]
        assert CollUtil.index_of_all([1, 2, 3], 5) == []

    def test_add_if_absent(self):
        lst = [1, 2, 3]
        assert CollUtil.add_if_absent(lst, 2) is False
        assert CollUtil.add_if_absent(lst, 4) is True
        assert 4 in lst

    def test_get(self):
        assert CollUtil.get([1, 2, 3], 1) == 2
        assert CollUtil.get([1, 2, 3], 10) is None
        assert CollUtil.get(None, 0) is None
        assert CollUtil.get([1, 2], -1) is None

    def test_get_any(self):
        assert CollUtil.get_any([1, 2, 3]) == 1
        assert CollUtil.get_any(set()) is None
        assert CollUtil.get_any(None) is None

    def test_values_of_keys(self):
        data = [{"a": 1, "b": 2}, {"a": 3, "c": 4}]
        result = CollUtil.values_of_keys(data, ["a", "b"])
        assert result == [1, 2, 3]

    def test_size(self):
        assert CollUtil.size([1, 2, 3]) == 3
        assert CollUtil.size(None) == 0
        assert CollUtil.size({}) == 0

    def test_is_equal_list(self):
        assert CollUtil.is_equal_list([1, 2], [1, 2]) is True
        assert CollUtil.is_equal_list([1, 2], [1, 3]) is False
        assert CollUtil.is_equal_list(None, None) is True
        assert CollUtil.is_equal_list(None, [1]) is False

    # ListUtil tests

    def test_list_util_of(self):
        from hutool.core.coll import ListUtil

        assert ListUtil.of(1, 2, 3) == [1, 2, 3]

    def test_list_util_empty(self):
        from hutool.core.coll import ListUtil

        assert ListUtil.empty() == []

    def test_set_or_padding(self):
        from hutool.core.coll import ListUtil

        lst = [1, 2]
        result = ListUtil.set_or_padding(lst, 4, 99)
        assert result == [1, 2, None, None, 99]

    def test_last_index_of(self):
        from hutool.core.coll import ListUtil

        assert ListUtil.last_index_of([1, 2, 1, 3], 1) == 2
        assert ListUtil.last_index_of([1, 2, 3], 5) == -1

    def test_swap(self):
        from hutool.core.coll import ListUtil

        lst = [1, 2, 3]
        ListUtil.swap(lst, 0, 2)
        assert lst == [3, 2, 1]

    def test_move(self):
        from hutool.core.coll import ListUtil

        lst = [1, 2, 3, 4]
        ListUtil.move(lst, 0, 2)
        assert lst == [2, 3, 1, 4]

    def test_zip(self):
        from hutool.core.coll import ListUtil

        assert ListUtil.zip_([1, 2], ["a", "b"]) == [(1, "a"), (2, "b")]

    def test_split(self):
        from hutool.core.coll import ListUtil

        assert ListUtil.split([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test_split_avg(self):
        from hutool.core.coll import ListUtil

        result = ListUtil.split_avg([1, 2, 3, 4, 5], 2)
        assert len(result) == 2
