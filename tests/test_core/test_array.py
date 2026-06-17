from hutool import ArrayUtil


class TestArrayUtil:
    def test_is_empty(self):
        assert ArrayUtil.is_empty([]) is True
        assert ArrayUtil.is_empty(None) is True
        assert ArrayUtil.is_empty([1]) is False

    def test_is_not_empty(self):
        assert ArrayUtil.is_not_empty([1]) is True
        assert ArrayUtil.is_not_empty([]) is False

    def test_length(self):
        assert ArrayUtil.length([1, 2, 3]) == 3
        assert ArrayUtil.length([]) == 0

    def test_append(self):
        result = ArrayUtil.append([1, 2], 3, 4)
        assert result == [1, 2, 3, 4]

    def test_insert(self):
        result = ArrayUtil.insert([1, 3], 1, 2)
        assert result == [1, 2, 3]

    def test_remove(self):
        result = ArrayUtil.remove([1, 2, 3], 1)
        assert result == [1, 3]

    def test_remove_ele(self):
        result = ArrayUtil.remove_ele([1, 2, 3, 2], 2)
        assert result == [1, 3, 2]  # removes first occurrence only

    def test_index_of(self):
        assert ArrayUtil.index_of([1, 2, 3], 2) == 1
        assert ArrayUtil.index_of([1, 2, 3], 4) == -1

    def test_contains(self):
        assert ArrayUtil.contains([1, 2, 3], 2) is True
        assert ArrayUtil.contains([1, 2, 3], 4) is False

    def test_contains_any(self):
        assert ArrayUtil.contains_any([1, 2, 3], 2, 5) is True
        assert ArrayUtil.contains_any([1, 2, 3], 4, 5) is False

    def test_sub(self):
        result = ArrayUtil.sub([1, 2, 3, 4], 1, 3)
        assert result == [2, 3]

    def test_join(self):
        assert ArrayUtil.join(["a", "b", "c"], ",") == "a,b,c"

    def test_reverse(self):
        result = ArrayUtil.reverse([1, 2, 3])
        assert result == [3, 2, 1]

    def test_shuffle(self):
        arr = [1, 2, 3, 4, 5]
        result = ArrayUtil.shuffle(arr)
        assert sorted(result) == sorted(arr)

    def test_distinct(self):
        result = ArrayUtil.distinct([1, 2, 2, 3, 3])
        assert result == [1, 2, 3]

    def test_filter(self):
        result = ArrayUtil.filter([1, 2, 3, 4], lambda x: x % 2 == 0)
        assert result == [2, 4]

    def test_map(self):
        result = ArrayUtil.map([1, 2, 3], lambda x: x * 2)
        assert result == [2, 4, 6]

    def test_flatten(self):
        result = ArrayUtil.flatten([[1, 2], [3, 4], [5]])
        assert result == [1, 2, 3, 4, 5]

    def test_fill(self):
        result = ArrayUtil.fill(0, 3)
        assert result == [0, 0, 0]

    def test_has_null(self):
        assert ArrayUtil.has_null(1, None, 3) is True
        assert ArrayUtil.has_null(1, 2, 3) is False

    def test_first_non_null(self):
        assert ArrayUtil.first_non_null(None, None, 3) == 3

    def test_zip(self):
        # ArrayUtil doesn't have zip, but dict(zip()) works
        result = dict(zip(["a", "b"], [1, 2]))
        assert result == {"a": 1, "b": 2}

    def test_to_list(self):
        result = ArrayUtil.to_list(range(3))
        assert result == [0, 1, 2]

    def test_swap(self):
        result = ArrayUtil.swap([1, 2, 3], 0, 2)
        assert result == [3, 2, 1]

    def test_default_if_empty(self):
        assert ArrayUtil.default_if_empty([], [1]) == [1]
        assert ArrayUtil.default_if_empty([2], [1]) == [2]
        assert ArrayUtil.default_if_empty(None, [1]) == [1]

    def test_first_match(self):
        assert ArrayUtil.first_match([1, 2, 3], lambda x: x > 1) == 2
        assert ArrayUtil.first_match([1, 2, 3], lambda x: x > 10) is None

    def test_match_index(self):
        assert ArrayUtil.match_index([1, 2, 3], lambda x: x == 2) == 1
        assert ArrayUtil.match_index([1, 2, 3], lambda x: x > 10) == -1

    def test_set_or_append(self):
        arr = [1, 2]
        ArrayUtil.set_or_append(arr, 1, 99)
        assert arr[1] == 99
        # 越界时追加
        ArrayUtil.set_or_append(arr, 10, 100)
        assert arr[-1] == 100

    def test_replace(self):
        arr = [1, 2, 3]
        old = ArrayUtil.replace(arr, 1, 99)
        assert old == 2
        assert arr[1] == 99

    def test_resize(self):
        result = ArrayUtil.resize([1, 2, 3], 5, 0)
        assert result == [1, 2, 3, 0, 0]
        result = ArrayUtil.resize([1, 2, 3], 2, 0)
        assert result == [1, 2]

    def test_add_all(self):
        assert ArrayUtil.add_all([1, 2], 3, 4) == [1, 2, 3, 4]

    def test_copy(self):
        result = ArrayUtil.copy([1, 2, 3], 2)
        assert result == [1, 2]

    def test_clone(self):
        original = [1, 2, 3]
        cloned = ArrayUtil.clone(original)
        assert cloned == original
        assert cloned is not original

    def test_edit(self):
        result = ArrayUtil.edit([1, 2, 3], lambda x: x * 2)
        assert result == [2, 4, 6]

    def test_remove_null(self):
        result = ArrayUtil.remove_null([1, None, 2, None, 3])
        assert result == [1, 2, 3]

    def test_remove_empty(self):
        result = ArrayUtil.remove_empty(["a", "", "b", None, "c"])
        assert result == ["a", "b", "c"]

    def test_remove_blank(self):
        result = ArrayUtil.remove_blank(["a", "  ", "b", "", "c"])
        assert result == ["a", "b", "c"]

    def test_null_to_empty(self):
        assert ArrayUtil.null_to_empty(None) == []
        assert ArrayUtil.null_to_empty([1, 2]) == [1, 2]

    def test_index_of_ignore_case(self):
        assert ArrayUtil.index_of_ignore_case(["A", "b", "C"], "c") == 2
        assert ArrayUtil.index_of_ignore_case(["A", "b"], "d") == -1

    def test_contains_ignore_case(self):
        assert ArrayUtil.contains_ignore_case(["A", "b", "C"], "c") is True
        assert ArrayUtil.contains_ignore_case(["A", "b"], "d") is False

    def test_is_array(self):
        assert ArrayUtil.is_array([1, 2]) is True
        assert ArrayUtil.is_array((1, 2)) is True
        assert ArrayUtil.is_array("str") is False

    def test_get(self):
        assert ArrayUtil.get([1, 2, 3], 1) == 2
        assert ArrayUtil.get([1, 2, 3], 5) is None

    def test_get_any(self):
        result = ArrayUtil.get_any([1, 2, 3])
        assert result == 1
        assert ArrayUtil.get_any([]) is None

    def test_index_of_sub(self):
        assert ArrayUtil.index_of_sub([1, 2, 3, 4, 5], [3, 4]) == 2
        assert ArrayUtil.index_of_sub([1, 2, 3], [4, 5]) == -1

    def test_last_index_of_sub(self):
        assert ArrayUtil.last_index_of_sub([1, 2, 3, 2, 3, 4], [2, 3]) == 3

    def test_is_all_empty(self):
        assert ArrayUtil.is_all_empty([], [], []) is True
        assert ArrayUtil.is_all_empty([], [1]) is False

    def test_is_all_not_empty(self):
        assert ArrayUtil.is_all_not_empty([1], [2]) is True
        assert ArrayUtil.is_all_not_empty([1], []) is False

    def test_is_all_not_null(self):
        assert ArrayUtil.is_all_not_null([1], [2]) is True
        assert ArrayUtil.is_all_not_null(None, [1]) is False

    def test_is_sorted_asc(self):
        assert ArrayUtil.is_sorted_asc([1, 2, 3]) is True
        assert ArrayUtil.is_sorted_asc([3, 2, 1]) is False

    def test_is_sorted_desc(self):
        assert ArrayUtil.is_sorted_desc([3, 2, 1]) is True
        assert ArrayUtil.is_sorted_desc([1, 2, 3]) is False

    def test_is_sorted_custom(self):
        # is_sorted checks: comparator(a, b) > 0 means not sorted
        # 降序比较器：a > b 时返回 -1（sorted），a < b 时返回 1（not sorted）
        data = ["c", "b", "a"]
        assert ArrayUtil.is_sorted(data, lambda a, b: (b > a) - (b < a)) is True

    def test_is_sub(self):
        assert ArrayUtil.is_sub([1, 2, 3, 4, 5], [2, 3, 4]) is True
        assert ArrayUtil.is_sub([1, 2, 3], [4, 5]) is False

    def test_map_to_set(self):
        result = ArrayUtil.map_to_set([1, 2, 3], lambda x: x * 2)
        assert result == {2, 4, 6}

    def test_to_array(self):
        assert ArrayUtil.to_array((1, 2, 3)) == [1, 2, 3]
        assert ArrayUtil.to_array(range(3)) == [0, 1, 2]

    def test_zip_arrays(self):
        result = ArrayUtil.zip_arrays([1, 2], ["a", "b", "c"])
        assert len(result) == 3
        assert result[0] == (1, "a")
        assert result[2] is not None  # fillvalue
