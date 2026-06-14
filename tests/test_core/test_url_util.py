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
