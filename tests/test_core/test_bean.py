from hutool import BeanUtil


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
