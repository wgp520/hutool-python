from hutool import URLUtil


class TestURLUtil:
    def test_encode(self):
        result = URLUtil.encode("hello world")
        assert "hello" in result
        assert "world" in result

    def test_decode(self):
        result = URLUtil.decode("hello%20world")
        assert result == "hello world"

    def test_encode_params(self):
        result = URLUtil.encode_params("a=1&b=2")
        assert "a" in result
        assert "1" in result

    def test_build_url(self):
        result = URLUtil.build_url("http://example.com", {"key": "value"})
        assert "http://example.com" in result
        assert "key=value" in result

    def test_get_path(self):
        result = URLUtil.get_path("http://example.com/path/to/resource")
        assert result == "/path/to/resource"

    def test_get_host(self):
        result = URLUtil.get_host("http://example.com:8080/path")
        assert result == "example.com"

    def test_get_port(self):
        result = URLUtil.get_port("http://example.com:8080/path")
        assert result == 8080

    def test_normalize(self):
        result = URLUtil.normalize("http://example.com/a/../b")
        assert "/b" in result

    def test_encode_decode_roundtrip(self):
        original = "hello 世界!"
        encoded = URLUtil.encode(original)
        decoded = URLUtil.decode(encoded)
        assert decoded == original

    def test_build_query_encoded(self):
        result = URLUtil.build_query({"key": "hello world", "num": "1"})
        assert "key=hello+world" in result or "key=hello%20world" in result
        assert "num=1" in result

    def test_build_query_not_encoded(self):
        result = URLUtil.build_query({"key": "val"}, is_encode=False)
        assert result == "key=val"

    def test_build_query_empty(self):
        assert URLUtil.build_query({}) == ""

    def test_encode_blank(self):
        assert URLUtil.encode_blank("hello world") == "hello%20world"

    def test_encode_blank_none(self):
        assert URLUtil.encode_blank("") == ""

    def test_complete_url(self):
        result = URLUtil.complete_url("http://example.com/a/b", "../c")
        assert result == "http://example.com/c"

    def test_get_params(self):
        result = URLUtil.get_params("http://example.com?a=1&b=2")
        assert result == {"a": "1", "b": "2"}

    def test_normalize_backslash(self):
        """测试反斜杠替换"""
        result = URLUtil.normalize("http://example.com\\path\\to")
        assert "\\" not in result
        assert result == "http://example.com/path/to"

    def test_normalize_double_slash_merge(self):
        """测试路径中连续斜杠合并"""
        result = URLUtil.normalize("http://example.com//path//to")
        assert result == "http://example.com/path/to"

    def test_get_data_uri_base64(self):
        """测试构建 base64 Data URI"""
        result = URLUtil.get_data_uri_base64("image/png", "iVBORw0KGgo=")
        assert result == "data:image/png;base64,iVBORw0KGgo="

    def test_get_data_uri(self):
        """测试构建 Data URI"""
        result = URLUtil.get_data_uri("text/plain", "base64", "SGVsbG8=")
        assert result == "data:text/plain;base64,SGVsbG8="

    def test_get_data_uri_with_charset(self):
        """测试带字符集的 Data URI"""
        result = URLUtil.get_data_uri("text/html", None, "<p>hi</p>", charset="utf-8")
        assert result == "data:text/html;charset=utf-8,<p>hi</p>"

    def test_get_data_uri_minimal(self):
        """测试最小 Data URI"""
        result = URLUtil.get_data_uri(data="hello")
        assert result == "data:,hello"
