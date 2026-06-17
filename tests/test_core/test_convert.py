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

    def test_number_to_chinese(self):
        assert ConvertUtil.number_to_chinese(123) == "一百二十三"
        assert ConvertUtil.number_to_chinese(0) == "零"

    def test_digit_to_chinese(self):
        assert ConvertUtil.digit_to_chinese(123) == "壹佰贰拾叁"
        assert ConvertUtil.digit_to_chinese(0) == "零"

    def test_chinese_to_number(self):
        assert ConvertUtil.chinese_to_number("一百二十三") == 123
        assert ConvertUtil.chinese_to_number("零") == 0

    def test_number_to_word(self):
        assert ConvertUtil.number_to_word(1) == "one"
        assert ConvertUtil.number_to_word(0) == "zero"
        assert ConvertUtil.number_to_word(12) == "twelve"

    def test_number_to_simple(self):
        assert ConvertUtil.number_to_simple(1500) == "1.5K"
        assert ConvertUtil.number_to_simple(2000000) == "2.0M"
        assert ConvertUtil.number_to_simple(500) == "500"

    def test_to_sbc(self):
        result = ConvertUtil.to_sbc("ABC")
        assert result == "ＡＢＣ"

    def test_to_dbc(self):
        result = ConvertUtil.to_dbc("ＡＢＣ")
        assert result == "ABC"

    def test_chinese_money_to_number(self):
        result = ConvertUtil.chinese_money_to_number("壹佰贰拾叁")
        assert result == 123

    def test_dict_to_tabular(self):
        data = {"r1": {"a": 1, "b": 2}, "r2": {"a": 3, "b": 4}}
        table = ConvertUtil.dict_to_tabular(data)
        assert table[0] == ["a", "b"]
        assert len(table) == 3  # header + 2 rows

    def test_dict_to_tabular_empty(self):
        assert ConvertUtil.dict_to_tabular({}) == []

    def test_list_to_tabular(self):
        data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        table = ConvertUtil.list_to_tabular(data)
        assert table[0] == ["name", "age"]
        assert table[1] == ["Alice", 30]

    def test_list_to_tabular_empty(self):
        assert ConvertUtil.list_to_tabular([]) == []

    def test_list_to_tabular_custom_headers(self):
        data = [{"a": 1, "b": 2}]
        table = ConvertUtil.list_to_tabular(data, headers=["b"])
        assert table[0] == ["b"]
        assert table[1] == [2]
