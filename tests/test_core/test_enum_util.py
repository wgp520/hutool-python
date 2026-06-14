from enum import Enum

from hutool import ClassUtil
from hutool import EnumUtil
from hutool import ReflectUtil


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
