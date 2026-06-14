from hutool import Base32, Base64


class TestBase64:
    def test_encode_bytes(self):
        result = Base64.encode(b"hello")
        assert result == "aGVsbG8="

    def test_encode_str(self):
        result = Base64.encode_str("hello")
        assert result == "aGVsbG8="

    def test_decode(self):
        result = Base64.decode("aGVsbG8=")
        assert result == b"hello"

    def test_decode_str(self):
        result = Base64.decode_str("aGVsbG8=")
        assert result == "hello"

    def test_encode_url_safe(self):
        result = Base64.encode_url_safe(b"hello world?")
        assert "+" not in result
        assert "/" not in result

    def test_decode_url_safe(self):
        encoded = Base64.encode_url_safe(b"test data")
        result = Base64.decode_url_safe(encoded)
        assert result == b"test data"

    def test_roundtrip(self):
        original = "Hello, 世界!"
        encoded = Base64.encode_str(original)
        decoded = Base64.decode_str(encoded)
        assert decoded == original

    def test_encode_chinese(self):
        result = Base64.encode_str("中文")
        decoded = Base64.decode_str(result)
        assert decoded == "中文"


class TestBase32:
    def test_encode(self):
        result = Base32.encode(b"hello")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_decode(self):
        encoded = Base32.encode(b"hello")
        result = Base32.decode(encoded)
        assert result == b"hello"

    def test_roundtrip(self):
        original = b"Hello, World!"
        encoded = Base32.encode(original)
        decoded = Base32.decode(encoded)
        assert decoded == original
