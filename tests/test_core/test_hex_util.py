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
