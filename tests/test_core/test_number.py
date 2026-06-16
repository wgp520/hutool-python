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

    def test_range_basic(self):
        assert NumberUtil.range_(0, 5) == [0, 1, 2, 3, 4]

    def test_range_step(self):
        assert NumberUtil.range_(0, 10, 3) == [0, 3, 6, 9]

    def test_append_range(self):
        lst = [10, 20]
        result = NumberUtil.append_range(lst, 0, 3)
        assert result == [10, 20, 0, 1, 2]

    def test_generate_by_set(self):
        result = NumberUtil.generate_by_set(3, 1, 10)
        assert len(result) == 3
        assert len(set(result)) == 3  # 不重复
        assert all(1 <= x <= 10 for x in result)

    def test_calculate_basic(self):
        assert NumberUtil.calculate("1 + 2 * 3") == 7.0

    def test_calculate_parentheses(self):
        assert NumberUtil.calculate("(1 + 2) * 3") == 9.0

    def test_calculate_unsafe_raises(self):
        import pytest

        with pytest.raises(ValueError):
            NumberUtil.calculate("import os")

    def test_sqrt(self):
        result = NumberUtil.sqrt(2, 5)
        assert abs(float(result) - 1.41421) < 0.0001

    def test_sqrt_perfect(self):
        assert NumberUtil.sqrt(9) == Decimal("3.0000000000")

    def test_sqrt_negative_raises(self):
        import pytest

        with pytest.raises(ValueError):
            NumberUtil.sqrt(-1)

    def test_is_integer(self):
        assert NumberUtil.is_integer("123") is True
        assert NumberUtil.is_integer("12.3") is False

    def test_is_double(self):
        assert NumberUtil.is_double("12.3") is True
        assert NumberUtil.is_double("123") is False

    def test_parse_number_int(self):
        assert NumberUtil.parse_number("123") == 123

    def test_parse_number_float(self):
        assert NumberUtil.parse_number("3.14") == 3.14

    def test_parse_long(self):
        assert NumberUtil.parse_long("123456789") == 123456789

    def test_parse_long_default(self):
        assert NumberUtil.parse_long("abc", -1) == -1

    def test_binary_to_long(self):
        """测试二进制字符串转 int"""
        assert NumberUtil.binary_to_long("1010") == 10
        assert NumberUtil.binary_to_long("0") == 0
        assert NumberUtil.binary_to_long("11111111") == 255

    def test_integer_sqrt(self):
        """测试整数平方根"""
        assert NumberUtil.integer_sqrt(0) == 0
        assert NumberUtil.integer_sqrt(1) == 1
        assert NumberUtil.integer_sqrt(4) == 2
        assert NumberUtil.integer_sqrt(9) == 3
        assert NumberUtil.integer_sqrt(10) == 3  # 向下取整
        assert NumberUtil.integer_sqrt(15) == 3
        assert NumberUtil.integer_sqrt(16) == 4

    def test_integer_sqrt_negative_raises(self):
        """测试负数抛异常"""
        import pytest

        with pytest.raises(ValueError):
            NumberUtil.integer_sqrt(-1)

    def test_process_multiple(self):
        """测试组合数 C(n, m)"""
        assert NumberUtil.process_multiple(5, 0) == 1
        assert NumberUtil.process_multiple(5, 1) == 5
        assert NumberUtil.process_multiple(5, 5) == 1
        assert NumberUtil.process_multiple(5, 2) == 10
        assert NumberUtil.process_multiple(6, 3) == 20
        assert NumberUtil.process_multiple(10, 3) == 120

    def test_parse_double(self):
        """测试带默认值的 float 解析"""
        assert NumberUtil.parse_double("3.14") == 3.14
        assert NumberUtil.parse_double("abc", 0.0) == 0.0
        assert NumberUtil.parse_double(None, -1.0) == -1.0
        assert NumberUtil.parse_double("100") == 100.0

    def test_to_big_integer(self):
        """测试转 int"""
        assert NumberUtil.to_big_integer(42) == 42
        assert NumberUtil.to_big_integer("12345") == 12345
        assert NumberUtil.to_big_integer(100) == 100

    def test_new_big_integer(self):
        """测试按进制解析"""
        assert NumberUtil.new_big_integer("ff", 16) == 255
        assert NumberUtil.new_big_integer("77", 8) == 63
        assert NumberUtil.new_big_integer("1010", 2) == 10

    def test_to_unsigned_byte_array(self):
        """测试转无符号字节数组"""
        result = NumberUtil.to_unsigned_byte_array(256)
        assert result == b"\x01\x00"  # 大端序

    def test_to_unsigned_byte_array_zero(self):
        assert NumberUtil.to_unsigned_byte_array(0) == b"\x00"

    def test_from_unsigned_byte_array(self):
        """测试从无符号字节数组恢复"""
        assert NumberUtil.from_unsigned_byte_array(b"\x00\x00\x01\x00") == 256
        assert NumberUtil.from_unsigned_byte_array(b"\xff") == 255

    def test_from_unsigned_byte_array_roundtrip(self):
        """测试无符号字节数组往返"""
        for val in [0, 1, 127, 128, 255, 256, 65535, 123456]:
            arr = NumberUtil.to_unsigned_byte_array(val)
            assert NumberUtil.from_unsigned_byte_array(arr) == val

    def test_range_method(self):
        """测试 range 方法"""
        assert NumberUtil.range_(0, 5) == [0, 1, 2, 3, 4]
        assert NumberUtil.range_(1, 10, 2) == [1, 3, 5, 7, 9]

    def test_generate(self):
        """测试生成随机整数列表"""
        result = NumberUtil.generate(5, 1, 100)
        assert len(result) == 5
        assert all(1 <= x < 100 for x in result)

    def test_null_to_zero(self):
        """测试 None 转 0"""
        assert NumberUtil.null_to_zero(None) == 0
        assert NumberUtil.null_to_zero(42) == 42
        assert NumberUtil.null_to_zero(0) == 0
