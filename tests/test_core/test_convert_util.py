"""Tests for ConvertUtil."""

from hutool import ConvertUtil


class TestConvertUtil:
    def test_bytes_to_int_basic(self):
        assert ConvertUtil.bytes_to_int(b"\x00\x00\x01\x00") == 256

    def test_bytes_to_int_single(self):
        assert ConvertUtil.bytes_to_int(b"\xff") == 255

    def test_bytes_to_int_zero(self):
        assert ConvertUtil.bytes_to_int(b"\x00") == 0

    def test_int_to_bytes_basic(self):
        assert ConvertUtil.int_to_bytes(256, 2) == b"\x01\x00"

    def test_int_to_bytes_default_length(self):
        result = ConvertUtil.int_to_bytes(1)
        assert len(result) == 4
        assert result == b"\x00\x00\x00\x01"

    def test_int_to_bytes_zero(self):
        assert ConvertUtil.int_to_bytes(0, 1) == b"\x00"

    def test_int_to_bytes_negative_raises(self):
        import pytest

        with pytest.raises(ValueError):
            ConvertUtil.int_to_bytes(-1)

    def test_bytes_int_roundtrip(self):
        for val in [0, 1, 255, 256, 65535, 12345678]:
            length = max(1, (val.bit_length() + 7) // 8)
            assert ConvertUtil.bytes_to_int(ConvertUtil.int_to_bytes(val, length)) == val

    def test_to_str_bytes(self):
        assert ConvertUtil.to_str(b"hello") == "hello"

    def test_to_str_str(self):
        assert ConvertUtil.to_str("world") == "world"

    def test_to_str_int(self):
        assert ConvertUtil.to_str(123) == "123"

    def test_to_str_none(self):
        assert ConvertUtil.to_str(None) == ""

    def test_to_str_encoding(self):
        data = "你好".encode("gbk")
        assert ConvertUtil.to_str(data, encoding="gbk") == "你好"

    def test_convert_str_to_int(self):
        assert ConvertUtil.convert("123", int) == 123

    def test_convert_int_to_str(self):
        assert ConvertUtil.convert(3.14, str) == "3.14"

    def test_convert_none_to_int(self):
        assert ConvertUtil.convert(None, int) == 0

    def test_convert_none_to_str(self):
        assert ConvertUtil.convert(None, str) == ""

    def test_convert_none_to_float(self):
        assert ConvertUtil.convert(None, float) == 0.0

    def test_convert_same_type(self):
        assert ConvertUtil.convert(42, int) == 42
