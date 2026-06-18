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

    def test_new_tree_map(self):
        m = MapUtil.new_tree_map()
        assert isinstance(m, dict)

    def test_new_identity_map(self):
        m = MapUtil.new_identity_map()
        assert isinstance(m, dict)

    def test_new_concurrent_hash_map(self):
        m = MapUtil.new_concurrent_hash_map()
        assert isinstance(m, dict)

    def test_wrap(self):
        m = {"a": 1, "b": 2}
        wrapped = MapUtil.wrap(m)
        assert wrapped["a"] == 1
        assert wrapped["b"] == 2

    def test_unmodifiable(self):
        m = {"a": 1}
        result = MapUtil.unmodifiable(m)
        assert result["a"] == 1

    def test_get_short(self):
        m = {"x": 100}
        assert MapUtil.get_short(m, "x") == 100
        assert MapUtil.get_short(m, "y", 0) == 0

    def test_get_char(self):
        m = {"c": "A"}
        assert MapUtil.get_char(m, "c") == "A"
        assert MapUtil.get_char(m, "d", "?") == "?"

    def test_empty(self):
        m = MapUtil.empty()
        assert isinstance(m, dict)
        assert len(m) == 0

    # ── get_ignore_case ─────────────────────────────────────────

    def test_get_ignore_case_exact(self):
        """精确匹配也能正常返回。"""
        m = {"name": "Alice"}
        assert MapUtil.get_ignore_case(m, "name") == "Alice"

    def test_get_ignore_case_upper(self):
        """键全大写，查询全小写。"""
        m = {"NAME": "Alice"}
        assert MapUtil.get_ignore_case(m, "name") == "Alice"

    def test_get_ignore_case_mixed(self):
        """混合大小写。"""
        m = {"Content-Type": "application/json"}
        assert MapUtil.get_ignore_case(m, "content-type") == "application/json"
        assert MapUtil.get_ignore_case(m, "CONTENT-TYPE") == "application/json"
        assert MapUtil.get_ignore_case(m, "Content-Type") == "application/json"

    def test_get_ignore_case_not_found(self):
        """未找到返回默认值。"""
        m = {"name": "Alice"}
        assert MapUtil.get_ignore_case(m, "age") is None
        assert MapUtil.get_ignore_case(m, "age", 0) == 0

    def test_get_ignore_case_empty_dict(self):
        """空字典返回默认值。"""
        assert MapUtil.get_ignore_case({}, "key", "default") == "default"

    def test_get_ignore_case_none_dict(self):
        """None 字典返回默认值。"""
        assert MapUtil.get_ignore_case(None, "key") is None

    def test_get_ignore_case_non_str_key_ignored(self):
        """非字符串键不会匹配。"""
        m = {1: "int_key", "Name": "Alice"}
        assert MapUtil.get_ignore_case(m, "name") == "Alice"
        assert MapUtil.get_ignore_case(m, "1") is None

    def test_get_ignore_case_first_match(self):
        """存在多个大小写匹配时返回第一个。"""
        m = {"Name": "first", "name": "second"}
        values = {"first", "second"}
        result = MapUtil.get_ignore_case(m, "NAME")
        assert result in values

    def test_put_and_get(self):
        bm = BiMap()
        bm["a"] = 1
        assert bm["a"] == 1

    def test_inverse_v2(self):
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

    def test_to_camel_case_map(self):
        result = MapUtil.to_camel_case_map({"first_name": "John", "last_name": "Doe"})
        assert result == {"firstName": "John", "lastName": "Doe"}

    def test_to_object_array(self):
        result = MapUtil.to_object_array({"a": 1, "b": 2})
        assert result == [["a", 1], ["b", 2]]

    def test_join_ignore_null(self):
        result = MapUtil.join_ignore_null({"a": 1, "b": None, "c": 3})
        assert "a=1" in result
        assert "c=3" in result
        assert "b" not in result

    def test_edit_map(self):
        result = MapUtil.edit({"a": 1, "b": 2}, lambda k, v: v * 10)
        assert result == {"a": 10, "b": 20}

    def test_map_function(self):
        result = MapUtil.map_({"a": 1, "b": 2}, key_func=str.upper, value_func=lambda v: v * 2)
        assert result == {"A": 2, "B": 4}

    def test_reverse_map(self):
        result = MapUtil.reverse({"a": 1, "b": 2})
        assert result == {1: "a", 2: "b"}

    def test_rename_key(self):
        m = {"old": 1, "b": 2}
        MapUtil.rename_key(m, "old", "new")
        assert m == {"new": 1, "b": 2}

    def test_remove_null_value(self):
        m = {"a": 1, "b": None, "c": 3}
        MapUtil.remove_null_value(m)
        assert m == {"a": 1, "c": 3}

    def test_remove_by_value(self):
        m = {"a": 1, "b": 2, "c": 1}
        MapUtil.remove_by_value(m, 1)
        assert m == {"b": 2}

    def test_remove_if(self):
        m = {"a": 1, "b": 2, "c": 3}
        MapUtil.remove_if(m, lambda k, v: v > 1)
        assert m == {"a": 1}

    def test_get_any(self):
        m = {"a": 1, "b": 2}
        assert MapUtil.get_any(m, "x", "b", "a") == 2
        assert MapUtil.get_any(m, "x", "y") is None
        assert MapUtil.get_any(None, "a") is None

    def test_get_double(self):
        m = {"a": 1, "b": "2.5"}
        assert MapUtil.get_double(m, "a") == 1.0
        assert MapUtil.get_double(m, "b") == 2.5
        assert MapUtil.get_double(m, "c", 99.0) == 99.0

    def test_get_long(self):
        m = {"a": 1.5, "b": "2"}
        assert MapUtil.get_long(m, "a") == 1
        assert MapUtil.get_long(m, "b") == 2
        assert MapUtil.get_long(m, "c", 99) == 99

    def test_entry(self):
        assert MapUtil.entry("key", "value") == {"key": "value"}

    def test_compute_if_absent(self):
        m = {"a": 1}
        result = MapUtil.compute_if_absent(m, "b", lambda k: 42)
        assert result == 42
        assert m["b"] == 42
        # Should not overwrite
        result2 = MapUtil.compute_if_absent(m, "b", lambda k: 99)
        assert result2 == 42

    def test_partition_map(self):
        m = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        result = MapUtil.partition(m, 2)
        assert len(result) == 3
        total = {}
        for part in result:
            total.update(part)
        assert total == m

    def test_flatten(self):
        m = {"a": {"b": 1, "c": {"d": 2}}, "e": 3}
        result = MapUtil.flatten(m)
        assert result == {"a.b": 1, "a.c.d": 2, "e": 3}

    def test_values_of_keys(self):
        m = {"a": 1, "b": 2, "c": 3}
        result = MapUtil.values_of_keys(m, ["a", "c"])
        assert result == [1, 3]

    def test_split_by_size_basic(self):
        m = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        result = MapUtil.split_by_size(m, 2)
        assert len(result) == 3
        assert len(result[0]) == 2
        assert len(result[1]) == 2
        assert len(result[2]) == 1

    def test_split_by_size_empty(self):
        assert MapUtil.split_by_size({}, 2) == []

    def test_split_by_size_invalid(self):
        import pytest

        with pytest.raises(ValueError):
            MapUtil.split_by_size({"a": 1}, 0)

    def test_sort_by_key_basic(self):
        m = {"b": 2, "a": 1, "c": 3}
        result = MapUtil.sort_by_key(m)
        assert list(result.keys()) == ["a", "b", "c"]

    def test_sort_by_key_reverse(self):
        m = {"b": 2, "a": 1, "c": 3}
        result = MapUtil.sort_by_key(m, reverse=True)
        assert list(result.keys()) == ["c", "b", "a"]

    def test_sort_by_key_empty(self):
        result = MapUtil.sort_by_key({})
        assert len(result) == 0
