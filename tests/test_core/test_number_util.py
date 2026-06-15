from decimal import Decimal

from hutool import NumberUtil


class TestNumberUtil:
    def test_add(self):
        assert NumberUtil.add(1, 2) == Decimal("3")
        assert NumberUtil.add(0.1, 0.2) == Decimal("0.3")

    def test_sub(self):
        assert NumberUtil.sub(3, 2) == Decimal("1")

    def test_mul(self):
        assert NumberUtil.mul(3, 2) == Decimal("6")

    def test_div(self):
        assert NumberUtil.div(6, 2) == Decimal("3")
        assert NumberUtil.div(10, 3) == Decimal("3.3333333333")

    def test_round(self):
        assert NumberUtil.round(3.456, 2) == Decimal("3.46")

    def test_round_str(self):
        result = NumberUtil.round_str(3.456, 2)
        assert result == "3.46"

    def test_is_number(self):
        assert NumberUtil.is_number("123") is True
        assert NumberUtil.is_number("12.3") is True
        assert NumberUtil.is_number("abc") is False
        assert NumberUtil.is_number(None) is False

    def test_is_int(self):
        assert NumberUtil.is_int("123") is True
        assert NumberUtil.is_int("12.3") is False

    def test_is_float(self):
        assert NumberUtil.is_float("12.3") is True
        assert NumberUtil.is_float("123") is False

    def test_parse_int(self):
        assert NumberUtil.parse_int("123") == 123
        assert NumberUtil.parse_int("abc", 0) == 0

    def test_parse_float(self):
        assert NumberUtil.parse_float("12.3") == 12.3
        assert NumberUtil.parse_float("abc", 0.0) == 0.0

    def test_to_decimal(self):
        assert NumberUtil.to_decimal(123) == Decimal("123")
        assert NumberUtil.to_decimal("12.3") == Decimal("12.3")

    def test_compare(self):
        assert NumberUtil.compare(3, 2) == 1
        assert NumberUtil.compare(2, 3) == -1
        assert NumberUtil.compare(3, 3) == 0

    def test_is_greater(self):
        assert NumberUtil.is_greater(3, 2) is True
        assert NumberUtil.is_greater(2, 3) is False

    def test_is_less(self):
        assert NumberUtil.is_less(2, 3) is True
        assert NumberUtil.is_less(3, 2) is False

    def test_min(self):
        assert NumberUtil.min(3, 1, 2) == 1

    def test_max(self):
        assert NumberUtil.max(3, 1, 2) == 3

    def test_is_odd(self):
        assert NumberUtil.is_odd(3) is True
        assert NumberUtil.is_odd(2) is False

    def test_is_even(self):
        assert NumberUtil.is_even(2) is True
        assert NumberUtil.is_even(3) is False

    def test_is_power_of_two(self):
        assert NumberUtil.is_power_of_two(8) is True
        assert NumberUtil.is_power_of_two(7) is False

    def test_factorial(self):
        assert NumberUtil.factorial(5) == 120
        assert NumberUtil.factorial(0) == 1

    def test_is_primes(self):
        assert NumberUtil.is_primes(7) is True
        assert NumberUtil.is_primes(4) is False
        assert NumberUtil.is_primes(2) is True

    def test_generate_random_number(self):
        result = NumberUtil.generate_random_number(1, 7, 6)
        assert len(result) == 6
        assert all(1 <= x < 7 for x in result)

    def test_pow(self):
        assert NumberUtil.pow(2, 3) == 8

    # ── int_or_default ──────────────────────────────────────

    def test_int_or_default_normal(self):
        """测试正常转换"""
        assert NumberUtil.int_or_default("123") == 123
        assert NumberUtil.int_or_default(456) == 456
        assert NumberUtil.int_or_default(3.7) == 3

    def test_int_or_default_none(self):
        """测试 None 返回默认值"""
        assert NumberUtil.int_or_default(None) == 0
        assert NumberUtil.int_or_default(None, 99) == 99

    def test_int_or_default_float_string(self):
        """测试浮点数字符串"""
        assert NumberUtil.int_or_default("3.14") == 3
        assert NumberUtil.int_or_default("0.99") == 0

    def test_int_or_default_invalid(self):
        """测试无效输入"""
        assert NumberUtil.int_or_default("abc") == 0
        assert NumberUtil.int_or_default("abc", -1) == -1

    def test_int_or_default_list(self):
        """测试列表取第一个元素"""
        assert NumberUtil.int_or_default([10, 20]) == 10

    # ── float_or_default ────────────────────────────────────

    def test_float_or_default_normal(self):
        """测试正常转换"""
        assert NumberUtil.float_or_default("3.14") == 3.14
        assert NumberUtil.float_or_default(42) == 42.0

    def test_float_or_default_none(self):
        """测试 None 返回默认值"""
        assert NumberUtil.float_or_default(None) == 0.0
        assert NumberUtil.float_or_default(None, 1.5) == 1.5

    def test_float_or_default_invalid(self):
        """测试无效输入"""
        assert NumberUtil.float_or_default("abc") == 0.0

    # ── avg ─────────────────────────────────────────────────

    def test_avg_basic(self):
        """测试基本平均值"""
        assert NumberUtil.avg([1, 2, 3, 4, 5]) == 3.0

    def test_avg_single(self):
        """测试单元素"""
        assert NumberUtil.avg([10]) == 10.0

    def test_avg_float(self):
        """测试浮点数平均值"""
        result = NumberUtil.avg([1.5, 2.5, 3.5])
        assert abs(result - 2.5) < 1e-9

    def test_avg_empty(self):
        """测试空列表返回 0"""
        assert NumberUtil.avg([]) == 0.0

    # ── median ──────────────────────────────────────────────

    def test_median_odd(self):
        """测试奇数个元素"""
        assert NumberUtil.median([3, 1, 2]) == 2

    def test_median_even(self):
        """测试偶数个元素"""
        assert NumberUtil.median([1, 2, 3, 4]) == 2.5

    def test_median_single(self):
        """测试单元素"""
        assert NumberUtil.median([5]) == 5

    def test_median_empty(self):
        """测试空列表返回 0"""
        assert NumberUtil.median([]) == 0.0

    # ── num_encode / num_decode ─────────────────────────────

    def test_num_encode_basic(self):
        """测试基本编码（Base62: 0-9, A-Z, a-z）"""
        assert NumberUtil.num_encode(0) == "0"
        assert NumberUtil.num_encode(1) == "1"
        assert NumberUtil.num_encode(35) == "Z"  # A=10, ..., Z=35
        assert NumberUtil.num_encode(61) == "z"  # a=36, ..., z=61

    def test_num_decode_basic(self):
        """测试基本解码"""
        assert NumberUtil.num_decode("0") == 0
        assert NumberUtil.num_decode("1") == 1
        assert NumberUtil.num_decode("Z") == 35
        assert NumberUtil.num_decode("z") == 61

    def test_num_encode_decode_roundtrip(self):
        """测试编码解码往返一致性"""
        for n in [0, 1, 10, 62, 100, 1000, 99999, 123456789]:
            encoded = NumberUtil.num_encode(n)
            decoded = NumberUtil.num_decode(encoded)
            assert decoded == n, f"Roundtrip failed for {n}: {encoded} -> {decoded}"

    def test_num_encode_negative(self):
        """测试负数编码"""
        result = NumberUtil.num_encode(-1)
        assert result.startswith("$")

    def test_num_decode_negative(self):
        """测试负数解码"""
        encoded = NumberUtil.num_encode(-42)
        assert NumberUtil.num_decode(encoded) == -42

    # ── bytes_to_int / int_to_bytes ─────────────────────────────────

    def test_bytes_to_int_basic(self):
        """测试 bytes 转 int"""
        assert NumberUtil.bytes_to_int(b"\x00\x00\x01\x00") == 256

    def test_bytes_to_int_single_byte(self):
        """测试单字节转 int"""
        assert NumberUtil.bytes_to_int(b"\xff") == 255

    def test_bytes_to_int_zero(self):
        """测试零值"""
        assert NumberUtil.bytes_to_int(b"\x00") == 0

    def test_int_to_bytes_basic(self):
        """测试 int 转 bytes"""
        assert NumberUtil.int_to_bytes(256, 2) == b"\x01\x00"

    def test_int_to_bytes_default_length(self):
        """测试默认长度 4 字节"""
        result = NumberUtil.int_to_bytes(1)
        assert len(result) == 4
        assert result == b"\x00\x00\x00\x01"

    def test_int_to_bytes_zero(self):
        """测试零值"""
        assert NumberUtil.int_to_bytes(0, 1) == b"\x00"

    def test_int_to_bytes_negative_raises(self):
        """测试负数抛异常"""
        import pytest

        with pytest.raises(ValueError):
            NumberUtil.int_to_bytes(-1)

    def test_bytes_int_roundtrip(self):
        """测试 bytes↔int 往返一致性"""
        for val in [0, 1, 255, 256, 65535, 12345678]:
            length = max(1, (val.bit_length() + 7) // 8)
            assert NumberUtil.bytes_to_int(NumberUtil.int_to_bytes(val, length)) == val
