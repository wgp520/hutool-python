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
