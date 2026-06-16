from types import SimpleNamespace

import pytest

from hutool import BeanUtil


class _SampleBean:
    def __init__(self):
        self.name = "test"
        self.age = 25
        self.email = None


class TestBeanUtil:
    def test_get_field_value(self):
        class User:
            name = "test"
            age = 20

        result = BeanUtil.get_field_value(User(), "name")
        assert result == "test"

    def test_set_field_value(self):
        class User:
            name = "test"

        obj = User()
        BeanUtil.set_field_value(obj, "name", "new")
        assert obj.name == "new"

    def test_bean_to_map(self):
        class User:
            name = "test"
            age = 20

        result = BeanUtil.bean_to_map(User())
        assert isinstance(result, dict)

    def test_map_to_bean(self):
        class User:
            name = None
            age = None

        m = {"name": "test", "age": 20}
        result = BeanUtil.map_to_bean(m, User)
        assert result.name == "test"
        assert result.age == 20

    def test_copy_properties(self):
        class Source:
            def __init__(self):
                self.name = "test"
                self.age = 20

        class Target:
            def __init__(self):
                self.name = None
                self.age = None

        src = Source()
        tgt = Target()
        BeanUtil.copy_properties(src, tgt)
        assert tgt.name == "test"
        assert tgt.age == 20

    def test_is_bean(self):
        class User:
            name = "test"

        assert BeanUtil.is_readable_bean(User()) is True
        assert BeanUtil.is_readable_bean("string") is False

    def test_bean_to_map_with_properties(self):
        class User:
            def __init__(self):
                self.name = "test"
                self.age = 20
                self._secret = "hidden"

        result = BeanUtil.bean_to_map(User())
        assert isinstance(result, dict)

    def test_is_bean_method(self):
        class User:
            def __init__(self):
                self.name = "test"

        assert BeanUtil.is_bean(User()) is True
        assert BeanUtil.is_bean("string") is False
        assert BeanUtil.is_bean(None) is False
        assert BeanUtil.is_bean({}) is False

    def test_is_empty(self):
        class User:
            def __init__(self):
                self.name = None
                self.age = None

        u = User()
        assert BeanUtil.is_empty(u) is True
        u.name = "test"
        assert BeanUtil.is_empty(u) is False

    def test_is_not_empty(self):
        class User:
            def __init__(self):
                self.name = "test"

        assert BeanUtil.is_not_empty(User()) is True

    def test_has_null_field(self):
        class User:
            def __init__(self):
                self.name = "test"
                self.age = None

        assert BeanUtil.has_null_field(User()) is True
        u = User()
        u.age = 20
        assert BeanUtil.has_null_field(u) is False

    def test_desc_for_each_dict(self):
        result = {}
        BeanUtil.desc_for_each({"a": 1, "b": 2}, lambda k, v: result.update({k: v * 2}))
        assert result == {"a": 2, "b": 4}

    def test_fill_bean(self):
        class User:
            def __init__(self):
                self.name = None
                self.age = None

        u = User()
        BeanUtil.fill_bean(u, lambda key: f"default_{key}")
        assert u.name == "default_name"
        assert u.age == "default_age"

    def test_trim_str_fields(self):
        class User:
            def __init__(self):
                self.name = "  hello  "
                self.age = 25

        u = User()
        BeanUtil.trim_str_fields(u)
        assert u.name == "hello"
        assert u.age == 25  # 非字符串字段不变

    def test_trim_str_fields_none(self):
        BeanUtil.trim_str_fields(None)  # 不抛异常

    def test_copy_to_list(self):
        data = [{"name": "a"}, {"name": "b"}]

        class User:
            def __init__(self):
                self.name = None

        result = BeanUtil.copy_to_list(data, User)
        assert len(result) == 2
        assert result[0].name == "a"

    def test_has_setter(self):
        bean = _SampleBean()
        assert BeanUtil.has_setter(bean, "name") is True

    def test_has_getter(self):
        bean = _SampleBean()
        assert BeanUtil.has_getter(bean, "name") is True

    def test_has_public_field(self):
        bean = _SampleBean()
        assert BeanUtil.has_public_field(bean, "name") is True
        assert BeanUtil.has_public_field(bean, "_private") is False
        assert BeanUtil.has_public_field(None, "x") is False

    def test_create_dyna_bean(self):
        bean = BeanUtil.create_dyna_bean()
        assert isinstance(bean, SimpleNamespace)
        bean.x = 10
        assert bean.x == 10

    def test_create_dyna_bean_with_class(self):
        bean = BeanUtil.create_dyna_bean(_SampleBean)
        assert isinstance(bean, _SampleBean)

    def test_get_bean_desc(self):
        desc = BeanUtil.get_bean_desc(_SampleBean)
        assert desc["class_name"] == "_SampleBean"
        assert isinstance(desc["fields"], list)

    def test_get_property(self):
        bean = _SampleBean()
        assert BeanUtil.get_property(bean, "name") == "test"
        assert BeanUtil.get_property(bean, "age") == 25
        assert BeanUtil.get_property(None, "x") is None

    def test_set_property(self):
        bean = _SampleBean()
        BeanUtil.set_property(bean, "name", "new")
        assert bean.name == "new"
        with pytest.raises(ValueError):
            BeanUtil.set_property(None, "x", 1)

    def test_map_to_bean_ignore_case(self):
        data = {"Name": "hello", "AGE": 30}
        bean = BeanUtil.map_to_bean_ignore_case(data, _SampleBean)
        assert bean.name == "hello"
        assert bean.age == 30

    def test_to_bean_ignore_error(self):
        data = {"name": "test", "nonexistent": "val"}
        bean = BeanUtil.to_bean_ignore_error(data, _SampleBean)
        assert bean.name == "test"

    def test_to_bean_ignore_case(self):
        data = {"Name": "abc", "Age": 20}
        bean = BeanUtil.to_bean_ignore_case(data, _SampleBean)
        assert bean.name == "abc"
        assert bean.age == 20

    def test_to_bean_ignore_case_none(self):
        assert BeanUtil.to_bean_ignore_case(None, _SampleBean) is None

    def test_bean_to_map_enhanced(self):
        bean = _SampleBean()
        result = BeanUtil.bean_to_map_enhanced(bean, is_underline=False, ignore_null=True)
        assert "name" in result
        assert "email" not in result  # email is None

    def test_bean_to_map_enhanced_underline(self):
        class CamelBean:
            def __init__(self):
                self.firstName = "John"
                self.lastName = "Doe"

        bean = CamelBean()
        result = BeanUtil.bean_to_map_enhanced(bean, is_underline=True, ignore_null=False)
        assert "first_name" in result
        assert "last_name" in result

    def test_copy_properties_with_options(self):
        src = _SampleBean()
        src.name = "src_name"
        dst = SimpleNamespace(name=None, age=None, email=None)
        BeanUtil.copy_properties_with_options(src, dst, copy_options={"ignore_properties": ["age"]})
        assert dst.name == "src_name"
        assert dst.age is None

    def test_copy_properties_with_options_ignore_null(self):
        src = _SampleBean()
        dst = SimpleNamespace(name=None, age=None, email=None)
        BeanUtil.copy_properties_with_options(src, dst, copy_options={"ignore_null": True})
        assert dst.name == "test"
        assert dst.age == 25
        assert dst.email is None  # skipped because src.email is None

    def test_is_match_name(self):
        assert BeanUtil.is_match_name("Hello", "hello") is True
        assert BeanUtil.is_match_name("Hello", "hello", ignore_case=False) is False
        assert BeanUtil.is_match_name(None, None) is True
        assert BeanUtil.is_match_name(None, "x") is False

    def test_edit(self):
        beans = [_SampleBean(), _SampleBean()]
        names = BeanUtil.edit(beans, lambda b: b.name)
        assert names == ["test", "test"]

    def test_edit_none(self):
        assert BeanUtil.edit(None, lambda x: x) == []

    def test_has_null_field_with_ignore(self):
        bean = _SampleBean()
        assert BeanUtil.has_null_field_with_ignore(bean) is True
        assert BeanUtil.has_null_field_with_ignore(bean, ignore_fields=["email"]) is False

    def test_get_field_names(self):
        bean = _SampleBean()
        names = BeanUtil.get_field_names(bean)
        assert "name" in names
        assert "age" in names
        assert "email" in names

    def test_get_field_names_none(self):
        assert BeanUtil.get_field_names(None) == []

    def test_is_common_fields_equal(self):
        a = _SampleBean()
        b = _SampleBean()
        assert BeanUtil.is_common_fields_equal(a, b) is True

    def test_is_common_fields_not_equal(self):
        a = _SampleBean()
        b = _SampleBean()
        b.name = "different"
        assert BeanUtil.is_common_fields_equal(a, b) is False

    def test_is_common_fields_both_none(self):
        assert BeanUtil.is_common_fields_equal(None, None) is True

    def test_is_common_fields_one_none(self):
        assert BeanUtil.is_common_fields_equal(_SampleBean(), None) is False
