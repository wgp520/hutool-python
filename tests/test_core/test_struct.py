"""测试 Struct"""

import pytest

from hutool import Struct


class TestStruct:
    def test_attr_access(self):
        s = Struct({"name": "test", "age": 20})
        assert s.name == "test"
        assert s.age == 20

    def test_dict_access(self):
        s = Struct({"name": "test"})
        assert s["name"] == "test"

    def test_setattr(self):
        s = Struct()
        s.name = "hello"
        assert s["name"] == "hello"

    def test_delattr(self):
        s = Struct({"name": "test"})
        del s.name
        assert "name" not in s

    def test_missing_attr(self):
        s = Struct()
        with pytest.raises(AttributeError):
            _ = s.missing

    def test_repr(self):
        s = Struct({"a": 1})
        r = repr(s)
        assert "a=1" in r

    def test_dict_behavior(self):
        s = Struct({"a": 1, "b": 2})
        assert len(s) == 2
        assert "a" in s
        assert list(s.keys()) == ["a", "b"]

    def test_basic(self):
        data = {"name": "test", "age": 20}
        s = Struct.from_dict(data)
        assert isinstance(s, Struct)
        assert s.name == "test"

    def test_nested(self):
        data = {"user": {"name": "test", "address": {"city": "Beijing"}}}
        s = Struct.from_dict(data)
        assert s.user.name == "test"
        assert s.user.address.city == "Beijing"

    def test_list(self):
        data = {"data": [{"id": 1}, {"id": 2}]}
        s = Struct.from_dict(data)
        assert isinstance(s.data[0], Struct)
        assert s.data[0].id == 1

    def test_scalar(self):
        assert Struct.from_dict(42) == 42
        assert Struct.from_dict("hello") == "hello"
        assert Struct.from_dict(None) is None

    def test_non_recursive(self):
        data = {"user": {"name": "test"}}
        s = Struct.from_dict(data, recursive=False)
        assert isinstance(s, Struct)
        assert isinstance(s.user, dict)
        assert not isinstance(s.user, Struct)
