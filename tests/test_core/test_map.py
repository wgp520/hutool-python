from hutool import BiMap, DictUtil, MapUtil


class TestMapUtil:
    def test_is_empty(self):
        assert MapUtil.is_empty({}) is True
        assert MapUtil.is_empty(None) is True
        assert MapUtil.is_empty({"a": 1}) is False

    def test_is_not_empty(self):
        assert MapUtil.is_not_empty({"a": 1}) is True
        assert MapUtil.is_not_empty({}) is False

    def test_of(self):
        result = MapUtil.of("key", "value")
        assert result == {"key": "value"}

    def test_of_entries(self):
        result = MapUtil.of_entries(("a", 1), ("b", 2))
        assert result == {"a": 1, "b": 2}

    def test_of_array(self):
        result = MapUtil.of_array(["a", 1, "b", 2])
        assert result == {"a": 1, "b": 2}

    def test_filter(self):
        m = {"a": 1, "b": 2, "c": 3}
        result = MapUtil.filter(m, "a", "c")
        assert result == {"a": 1, "c": 3}

    def test_filter_by_func(self):
        m = {"a": 1, "b": 2, "c": 3}
        result = MapUtil.filter_by_func(m, lambda k, v: v > 1)
        assert result == {"b": 2, "c": 3}

    def test_map_values(self):
        m = {"a": 1, "b": 2}
        result = MapUtil.map_values(m, lambda v: v * 2)
        assert result == {"a": 2, "b": 4}

    def test_sort(self):
        m = {"c": 3, "a": 1, "b": 2}
        result = MapUtil.sort(m)
        keys = list(result.keys())
        assert keys == ["a", "b", "c"]

    def test_inverse(self):
        m = {"a": 1, "b": 2}
        result = MapUtil.inverse(m)
        assert result == {1: "a", 2: "b"}

    def test_empty_if_null(self):
        assert MapUtil.empty_if_null(None) == {}
        assert MapUtil.empty_if_null({"a": 1}) == {"a": 1}

    def test_get_str(self):
        m = {"key": "value"}
        assert MapUtil.get_str(m, "key") == "value"
        assert MapUtil.get_str(m, "missing") == ""

    def test_get_int(self):
        m = {"key": 42}
        assert MapUtil.get_int(m, "key") == 42
        assert MapUtil.get_int(m, "missing") == 0

    def test_join(self):
        m = {"a": 1, "b": 2}
        result = MapUtil.join(m, "&", "=")
        assert "a=1" in result
        assert "b=2" in result

    def test_sort_by_value(self):
        m = {"a": 3, "b": 1, "c": 2}
        result = MapUtil.sort_by_value(m)
        values = list(result.values())
        assert values == [1, 2, 3]

    def test_get_float(self):
        m = {"key": 3.14}
        assert MapUtil.get_float(m, "key") == 3.14
        assert MapUtil.get_float(m, "missing") == 0.0

    def test_get_bool(self):
        m = {"key": True}
        assert MapUtil.get_bool(m, "key") is True
        assert MapUtil.get_bool(m, "missing") is False


class TestBiMap:
    def test_put_and_get(self):
        bm = BiMap()
        bm["a"] = 1
        assert bm["a"] == 1

    def test_inverse(self):
        bm = BiMap()
        bm["a"] = 1
        bm["b"] = 2
        inv = bm.get_inverse()
        assert inv[1] == "a"
        assert inv[2] == "b"

    def test_overwrite(self):
        bm = BiMap()
        bm["a"] = 1
        bm["a"] = 2
        assert bm["a"] == 2


class TestDictUtil:
    def test_is_empty(self):
        assert DictUtil.is_empty({}) is True
        assert DictUtil.is_empty({"a": 1}) is False


class TestMapUtilTopN:
    def test_top_n_keys_basic(self):
        """测试取值最大的前 N 个键"""
        result = MapUtil.top_n_keys({"a": 3, "b": 1, "c": 5, "d": 2}, 2)
        assert result == ["c", "a"]

    def test_top_n_keys_zero(self):
        """测试 n=0"""
        result = MapUtil.top_n_keys({"a": 1}, 0)
        assert result == []

    def test_top_n_keys_n_larger_than_dict(self):
        """测试 n 大于字典长度"""
        result = MapUtil.top_n_keys({"a": 1, "b": 2}, 5)
        assert len(result) == 2
        assert result == ["b", "a"]

    def test_top_n_keys_empty_dict(self):
        """测试空字典"""
        result = MapUtil.top_n_keys({}, 3)
        assert result == []

    def test_top_n_keys_single(self):
        """测试取前 1 个"""
        result = MapUtil.top_n_keys({"x": 10, "y": 20, "z": 15}, 1)
        assert result == ["y"]
