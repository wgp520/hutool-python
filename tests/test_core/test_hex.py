from hutool import HexUtil


class TestHexUtil:
    def test_encode_hex_str(self):
        result = HexUtil.encode_hex_str(b"hello")
        assert result == "68656c6c6f"  # 默认小写

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

    def test_encode_hex_str_default_lowercase(self):
        """测试默认小写（与 Java Hutool 一致）"""
        assert HexUtil.encode_hex_str(b"\xab\xcd") == "abcd"

    def test_encode_hex_str_uppercase(self):
        """测试大写输出"""
        assert HexUtil.encode_hex_str(b"\xab\xcd", lower_case=False) == "ABCD"

    def test_encode_hex_string(self):
        """测试字符串转十六进制"""
        result = HexUtil.encode_hex("Hello", charset="utf-8")
        assert result == "48656c6c6f"

    def test_encode_hex_bytes(self):
        """测试字节数组转十六进制"""
        result = HexUtil.encode_hex(b"\x00\xff")
        assert result == "00ff"

    def test_decode_hex_str(self):
        """测试十六进制字符串解码"""
        assert HexUtil.decode_hex_str("48656c6c6f") == "Hello"

    def test_hex_to_long(self):
        """测试十六进制转 long"""
        assert HexUtil.hex_to_long("ff") == 255
        assert HexUtil.hex_to_long("0xFF") == 255
        assert HexUtil.hex_to_long("100000000") == 4294967296

    def test_hex_to_float(self):
        """测试十六进制转 float（IEEE 754）"""
        # 0x3F800000 = 1.0f
        result = HexUtil.hex_to_float("3f800000")
        assert abs(result - 1.0) < 1e-6

    def test_hex_to_double(self):
        """测试十六进制转 double（IEEE 754）"""
        # 0x3FF0000000000000 = 1.0
        result = HexUtil.hex_to_double("3ff0000000000000")
        assert abs(result - 1.0) < 1e-10

    def test_to_hex_long(self):
        """测试 long 转十六进制"""
        assert HexUtil.to_hex_long(255) == "ff"
        assert HexUtil.to_hex_long(0) == "0"

    def test_to_hex_float(self):
        """测试 float 转十六进制"""
        result = HexUtil.to_hex_float(1.0)
        assert result == "3f800000"

    def test_to_hex_double(self):
        """测试 double 转十六进制"""
        result = HexUtil.to_hex_double(1.0)
        assert result == "3ff0000000000000"

    def test_float_hex_roundtrip(self):
        """测试 float 十六进制往返"""

        for val in [1.0, 3.14, -1.0, 0.0, 1e10]:
            hex_str = HexUtil.to_hex_float(val)
            result = HexUtil.hex_to_float(hex_str)
            assert abs(result - val) < 1e-5, f"Roundtrip failed for {val}"

    def test_double_hex_roundtrip(self):
        """测试 double 十六进制往返"""
        for val in [1.0, 3.141592653589793, -1.0, 0.0, 1e100]:
            hex_str = HexUtil.to_hex_double(val)
            result = HexUtil.hex_to_double(hex_str)
            assert abs(result - val) < 1e-10, f"Roundtrip failed for {val}"

    def test_append_hex(self):
        """测试追加十六进制"""
        builder = []
        HexUtil.append_hex(builder, 0xAB)
        assert builder == ["a", "b"]

    def test_append_hex_upper(self):
        """测试追加大写十六进制"""
        builder = []
        HexUtil.append_hex(builder, 0xFF, lower_case=False)
        assert builder == ["F", "F"]

    def test_to_big_integer(self):
        """测试十六进制转大整数"""
        assert HexUtil.to_big_integer("ff") == 255
        assert HexUtil.to_big_integer("0xFF") == 255
        assert HexUtil.to_big_integer("100000000") == 4294967296
