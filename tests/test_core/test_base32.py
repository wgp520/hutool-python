from hutool import Base32Util


class TestBase32Util:
    """Base32Util 测试"""

    def test_encode(self):
        result = Base32Util.encode("Hello")
        assert result == "JBSWY3DP"

    def test_decode(self):
        result = Base32Util.decode("JBSWY3DP")
        assert result == b"Hello"

    def test_encode_hex(self):
        result = Base32Util.encode_hex("Hello")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_decode_hex(self):
        encoded = Base32Util.encode_hex("Hello")
        decoded = Base32Util.decode_hex(encoded)
        assert decoded == b"Hello"

    def test_decode_str_hex(self):
        encoded = Base32Util.encode_hex("Hello")
        decoded = Base32Util.decode_str_hex(encoded)
        assert decoded == "Hello"

    def test_roundtrip(self):
        original = "你好"
        encoded = Base32Util.encode(original)
        decoded = Base32Util.decode(encoded).decode("utf-8")
        assert decoded == original
