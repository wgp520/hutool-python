from enum import Enum

import pytest

from hutool import ClassUtil, EnumUtil, ReflectUtil


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class TestEnumUtil:
    def test_get_names(self):
        names = EnumUtil.get_names(Color)
        assert "RED" in names
        assert "GREEN" in names

    def test_get_values(self):
        values = EnumUtil.get_values(Color)
        assert 1 in values
        assert 2 in values

    def test_contains(self):
        assert EnumUtil.contains(Color, 1) is True
        assert EnumUtil.contains(Color, 99) is False

    def test_get_by_name(self):
        result = EnumUtil.of(Color, "RED")
        assert result == Color.RED


class TestClassUtil:
    def test_get_class_name(self):
        result = ClassUtil.get_class_name(Color)
        assert "Color" in result

    def test_is_basic_type(self):
        assert ClassUtil.is_basic_type(42) is True
        assert ClassUtil.is_basic_type("hello") is True
        assert ClassUtil.is_basic_type([1, 2]) is False


class TestReflectUtil:
    def test_get_field_value(self):
        class Obj:
            name = "test"

        result = ReflectUtil.get_field_value(Obj(), "name")
        assert result == "test"

    def test_set_field_value(self):
        class Obj:
            name = "test"

        obj = Obj()
        ReflectUtil.set_field_value(obj, "name", "new")
        assert obj.name == "new"

    def test_get_method(self):
        obj = "hello"
        result = ReflectUtil.invoke(obj, "upper")
        assert result == "HELLO"

    def test_is_enum_class(self):
        assert EnumUtil.is_enum_class(Color) is True
        assert EnumUtil.is_enum_class(Color.RED) is False
        assert EnumUtil.is_enum_class("str") is False

    def test_is_enum(self):
        assert EnumUtil.is_enum(Color.RED) is True
        assert EnumUtil.is_enum(Color) is False

    def test_from_string(self):
        assert EnumUtil.from_string(Color, "RED") == Color.RED
        with pytest.raises(KeyError):
            EnumUtil.from_string(Color, "NONEXISTENT")

    def test_from_string_quietly(self):
        assert EnumUtil.from_string_quietly(Color, "RED") == Color.RED
        assert EnumUtil.from_string_quietly(Color, "NONEXISTENT") is None

    def test_get_field_values(self):
        values = EnumUtil.get_field_values(Color, "value")
        assert set(values) == {1, 2, 3}

    def test_get_field_names(self):
        names = EnumUtil.get_field_names(Color)
        assert set(names) == {"RED", "GREEN", "BLUE"}

    def test_get_enum_map(self):
        m = EnumUtil.get_enum_map(Color)
        assert m["RED"] == Color.RED

    def test_get_name_field_map(self):
        m = EnumUtil.get_name_field_map(Color, "value")
        assert m == {"RED": 1, "GREEN": 2, "BLUE": 3}
