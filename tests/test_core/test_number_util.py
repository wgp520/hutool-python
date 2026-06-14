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
