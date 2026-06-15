from hutool import HexUtil


class TestHexUtil:
    def test_encode_hex_str(self):
        result = HexUtil.encode_hex_str(b"hello")
        assert result == "68656C6C6F"

    def test_encode_hex_str_lower(self):
        result = HexUtil.encode_hex_str(b"\xab\xcd", lower_case=True)
        assert result == "abcd"

    def test_encode_hex_str_upper(self):
        result = HexUtil.encode_hex_str(b"\xab\xcd", lower_case=False)
        assert result == "ABCD"

    def test_decode_hex(self):
        result = HexUtil.decode_hex("68656c6c6f")
        assert result == b"hello"

    def test_to_hex(self):
        assert HexUtil.to_hex(255) == "FF"
        assert HexUtil.to_hex(0) == "0"

    def test_hex_to_int(self):
        assert HexUtil.hex_to_int("ff") == 255
        assert HexUtil.hex_to_int("0") == 0

    def test_encode_color_str(self):
        result = HexUtil.encode_color_str((255, 0, 0))
        assert result == "#FF0000"

    def test_decode_color(self):
        result = HexUtil.decode_color("#ff0000")
        assert result == (255, 0, 0)

    def test_roundtrip(self):
        original = b"Hello, World!"
        hex_str = HexUtil.encode_hex_str(original)
        decoded = HexUtil.decode_hex(hex_str)
        assert decoded == original

    def test_is_hex_number_true(self):
        assert HexUtil.is_hex_number("1A2B3C") is True
        assert HexUtil.is_hex_number("0xFF") is True

    def test_is_hex_number_false(self):
        assert HexUtil.is_hex_number("xyz") is False
        assert HexUtil.is_hex_number("") is False

    def test_to_unicode_hex(self):
        assert HexUtil.to_unicode_hex("中") == "\\u4e2d"
        assert HexUtil.to_unicode_hex("A") == "\\u0041"
