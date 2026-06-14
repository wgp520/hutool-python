from hutool import JSONUtil


class TestJSONUtil:
    def test_parse_obj(self):
        result = JSONUtil.parse_obj('{"key": "value"}')
        assert result == {"key": "value"}

    def test_parse_array(self):
        result = JSONUtil.parse_array("[1, 2, 3]")
        assert result == [1, 2, 3]

    def test_parse(self):
        assert JSONUtil.parse('{"a": 1}') == {"a": 1}
        assert JSONUtil.parse("[1, 2]") == [1, 2]

    def test_to_json_str(self):
        result = JSONUtil.to_json_str({"key": "value"})
        assert "key" in result
        assert "value" in result

    def test_to_json_pretty_str(self):
        result = JSONUtil.to_json_pretty_str({"key": "value"})
        assert "\n" in result

    def test_create_obj(self):
        result = JSONUtil.create_obj()
        assert isinstance(result, dict)

    def test_create_array(self):
        result = JSONUtil.create_array()
        assert isinstance(result, list)

    def test_is_json(self):
        assert JSONUtil.is_json('{"key": "value"}') is True
        assert JSONUtil.is_json("[1, 2]") is True
        assert JSONUtil.is_json("not json") is False

    def test_is_json_obj(self):
        assert JSONUtil.is_json_obj('{"key": "value"}') is True
        assert JSONUtil.is_json_obj("[1, 2]") is False

    def test_is_json_array(self):
        assert JSONUtil.is_json_array("[1, 2]") is True
        assert JSONUtil.is_json_array('{"key": "value"}') is False

    def test_format_json(self):
        result = JSONUtil.format_json('{"key":"value","num":1}')
        assert "\n" in result

    def test_compress(self):
        formatted = '{\n  "key": "value"\n}'
        result = JSONUtil.compress(formatted)
        assert "\n" not in result

    def test_get_by_path(self):
        data = {"a": {"b": {"c": 42}}}
        result = JSONUtil.get_by_path(data, "a.b.c")
        assert result == 42

    def test_get_by_path_array(self):
        data = {"items": [{"name": "first"}, {"name": "second"}]}
        result = JSONUtil.get_by_path(data, "items[0].name")
        assert result == "first"

    def test_put_by_path(self):
        data = {}
        JSONUtil.put_by_path(data, "a.b.c", 42)
        assert data["a"]["b"]["c"] == 42

    def test_to_bean(self):
        class User:
            def __init__(self, **kwargs):
                self.name = kwargs.get("name")
                self.age = kwargs.get("age")

        result = JSONUtil.to_bean('{"name": "test", "age": 20}', User)
        assert result.name == "test"
        assert result.age == 20

    def test_to_bean_list(self):
        class User:
            def __init__(self, **kwargs):
                self.name = kwargs.get("name")

        result = JSONUtil.to_bean_list('[{"name": "a"}, {"name": "b"}]', User)
        assert len(result) == 2
        assert result[0].name == "a"

    def test_from_bean(self):
        class User:
            def __init__(self):
                self.name = "test"
                self.age = 20

        result = JSONUtil.from_bean(User())
        assert "test" in result
