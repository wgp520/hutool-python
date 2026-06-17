from hutool import ObjectUtil


class TestObjectUtil:
    def test_equals(self):
        assert ObjectUtil.equals("abc", "abc") is True
        assert ObjectUtil.equals("abc", "def") is False
        assert ObjectUtil.equals(None, None) is True

    def test_not_equal(self):
        assert ObjectUtil.not_equal("abc", "def") is True

    def test_is_null(self):
        assert ObjectUtil.is_null(None) is True
        assert ObjectUtil.is_null("") is False

    def test_is_not_null(self):
        assert ObjectUtil.is_not_null("") is True
        assert ObjectUtil.is_not_null(None) is False

    def test_is_empty(self):
        assert ObjectUtil.is_empty(None) is True
        assert ObjectUtil.is_empty("") is True
        assert ObjectUtil.is_empty([]) is True
        assert ObjectUtil.is_empty({}) is True
        assert ObjectUtil.is_empty("abc") is False

    def test_is_not_empty(self):
        assert ObjectUtil.is_not_empty("abc") is True

    def test_default_if_null(self):
        assert ObjectUtil.default_if_null(None, "default") == "default"
        assert ObjectUtil.default_if_null("value", "default") == "value"

    def test_default_if_empty(self):
        assert ObjectUtil.default_if_empty("", "default") == "default"
        assert ObjectUtil.default_if_empty("value", "default") == "value"

    def test_length(self):
        assert ObjectUtil.length("abc") == 3
        assert ObjectUtil.length([1, 2]) == 2
        assert ObjectUtil.length(None) == 0

    def test_contains(self):
        assert ObjectUtil.contains("abc", "b") is True
        assert ObjectUtil.contains([1, 2, 3], 2) is True

    def test_is_basic_type(self):
        assert ObjectUtil.is_basic_type(1) is True
        assert ObjectUtil.is_basic_type("str") is True
        assert ObjectUtil.is_basic_type([1]) is False

    def test_has_null(self):
        assert ObjectUtil.has_null(1, None, 3) is True
        assert ObjectUtil.has_null(1, 2, 3) is False

    def test_has_empty(self):
        assert ObjectUtil.has_empty("", "abc") is True
        assert ObjectUtil.has_empty("abc", "def") is False

    def test_to_string(self):
        assert ObjectUtil.to_string(None) == ""
        assert ObjectUtil.to_string(123) == "123"

    def test_clone_if_possible(self):
        original = [1, 2, 3]
        cloned = ObjectUtil.clone_if_possible(original)
        assert cloned == original
        assert cloned is not original
        assert ObjectUtil.clone_if_possible("str") == "str"

    def test_is_valid_if_number(self):
        assert ObjectUtil.is_valid_if_number(1.5) is True
        assert ObjectUtil.is_valid_if_number(float("nan")) is False
        assert ObjectUtil.is_valid_if_number(float("inf")) is False
        assert ObjectUtil.is_valid_if_number(42) is True

    def test_default_if_null_supplier(self):
        assert ObjectUtil.default_if_null_supplier(None, lambda: "default") == "default"
        assert ObjectUtil.default_if_null_supplier("val", lambda: "default") == "val"

    def test_default_if_empty_supplier(self):
        assert ObjectUtil.default_if_empty_supplier(None, lambda: "default") == "default"
        assert ObjectUtil.default_if_empty_supplier("", lambda: "default") == "default"
        assert ObjectUtil.default_if_empty_supplier([], lambda: []) == []
        assert ObjectUtil.default_if_empty_supplier("val", lambda: "default") == "val"

    def test_default_if_blank_supplier(self):
        assert ObjectUtil.default_if_blank_supplier("   ", lambda: "default") == "default"
        assert ObjectUtil.default_if_blank_supplier(None, lambda: "default") == "default"
        assert ObjectUtil.default_if_blank_supplier("hello", lambda: "default") == "hello"

    def test_get_attr_safe_normal(self):
        class Obj:
            x = 42

        assert ObjectUtil.get_attr_safe(Obj(), "x") == 42

    def test_get_attr_safe_missing(self):
        class Obj:
            pass

        assert ObjectUtil.get_attr_safe(Obj(), "missing", "default") == "default"

    def test_get_attr_safe_none(self):
        assert ObjectUtil.get_attr_safe(None, "x", "default") == "default"

    def test_unpack_to_dict_from_dict(self):
        d = {"a": 1, "b": 2}
        result = ObjectUtil.unpack_to_dict(d)
        assert result == d

    def test_unpack_to_dict_with_fields(self):
        d = {"a": 1, "b": 2, "c": 3}
        result = ObjectUtil.unpack_to_dict(d, fields=["a", "c"])
        assert result == {"a": 1, "c": 3}

    def test_unpack_to_dict_none(self):
        assert ObjectUtil.unpack_to_dict(None) == {}

    def test_none_on_exception_normal(self):
        @ObjectUtil.none_on_exception
        def ok():
            return 42

        assert ok() == 42

    def test_none_on_exception_error(self):
        @ObjectUtil.none_on_exception
        def fail():
            raise ValueError("oops")

        assert fail() is None

    def test_empty_count(self):
        assert ObjectUtil.empty_count(None, "", [], "hello") == 3

    def test_empty_count_no_empty(self):
        assert ObjectUtil.empty_count("a", [1], 42) == 0

    def test_empty_count_all_empty(self):
        assert ObjectUtil.empty_count(None, "", {}, set()) == 4

    def test_get_key_fmt_dict_camel(self):
        data = {"user_name": "test"}
        result = ObjectUtil.get_key_fmt(data, "userName", fmt="camel")
        assert result == "test"

    def test_get_key_fmt_dict_snake(self):
        data = {"userName": "test"}
        result = ObjectUtil.get_key_fmt(data, "user_name", fmt="snake")
        assert result == "test"

    def test_get_key_fmt_dict_direct(self):
        data = {"name": "test"}
        result = ObjectUtil.get_key_fmt(data, "name")
        assert result == "test"

    def test_get_key_fmt_dict_default(self):
        data = {"name": "test"}
        result = ObjectUtil.get_key_fmt(data, "missing", default="N/A")
        assert result == "N/A"

    def test_get_key_fmt_none(self):
        assert ObjectUtil.get_key_fmt(None, "x", default="N/A") == "N/A"

    def test_get_key_fmt_object(self):
        class User:
            def __init__(self):
                self.user_name = "test"

        result = ObjectUtil.get_key_fmt(User(), "user_name")
        assert result == "test"
