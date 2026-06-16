from hutool import Base64Util


class TestBase64Util:
    """Base64Util 测试"""

    def test_encode_str(self):
        result = Base64Util.encode_str("Hello")
        assert result == "SGVsbG8="

    def test_encode_bytes(self):
        result = Base64Util.encode(b"Hello")
        assert result == b"SGVsbG8="

    def test_decode(self):
        result = Base64Util.decode("SGVsbG8=")
        assert result == b"Hello"

    def test_decode_str(self):
        result = Base64Util.decode_str("SGVsbG8=")
        assert result == "Hello"

    def test_encode_url_safe(self):
        result = Base64Util.encode_url_safe(b"test?data&more")
        assert isinstance(result, bytes)
        assert b"+" not in result
        assert b"/" not in result

    def test_encode_without_padding(self):
        result = Base64Util.encode_without_padding(b"a")
        assert isinstance(result, bytes)
        assert b"=" not in result
        assert result == b"YQ"

    def test_is_base64_valid(self):
        assert Base64Util.is_base64("SGVsbG8=") is True

    def test_is_base64_invalid(self):
        assert Base64Util.is_base64("not!!!base64===valid") is False

    def test_roundtrip(self):
        original = "你好世界 Hello 🌍"
        encoded = Base64Util.encode_str(original)
        decoded = Base64Util.decode_str(encoded)
        assert decoded == original
