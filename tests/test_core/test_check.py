"""CheckUtil 测试"""

import pytest

from hutool import CheckUtil, ValidateException


class TestCheckUtil:
    """CheckUtil 测试类"""

    # ── EAN 校验位 ─────────────────────────────────────────

    def test_ean_digit_basic(self):
        """测试基本 EAN 校验位计算"""
        assert CheckUtil.ean_digit("400599871650") == "2"
        assert CheckUtil.ean_digit("1234567890123") == "1"
        assert CheckUtil.ean_digit("062235652032") == "4"
        assert CheckUtil.ean_digit("978014200057") == "1"

    def test_ean_digit_empty(self):
        """测试空字符串"""
        assert CheckUtil.ean_digit("") == "0"

    def test_ean_digit_single(self):
        """测试单个数字"""
        assert CheckUtil.ean_digit("2") == "4"

    def test_ean_digit_long(self):
        """测试长数字串"""
        assert CheckUtil.ean_digit("999999999999999999999999999999999999999999999999999999999999") == "0"

    def test_ean_digit_nve(self):
        """测试 NVE 校验位"""
        assert CheckUtil.ean_digit("34005998000000027") == "5"

    # ── EAN 验证 ────────────────────────────────────────────

    def test_verify_ean_valid(self):
        """测试有效 EAN"""
        assert CheckUtil.verify_ean("4005998000007") is True
        assert CheckUtil.verify_ean("12345678901231") is True

    def test_verify_ean_invalid(self):
        """测试无效 EAN"""
        assert CheckUtil.verify_ean("4005998000000") is False

    def test_verify_ean_non_digit(self):
        """测试非数字字符串"""
        assert CheckUtil.verify_ean("foobar") is False

    def test_verify_ean_empty(self):
        """测试空字符串"""
        assert CheckUtil.verify_ean("") is False

    # ── Verhoeff 校验位 ────────────────────────────────────

    def test_verhoeff_digit_known_values(self):
        """测试已知 Verhoeff 校验位值"""
        assert CheckUtil.verhoeff_digit("123456654321") == "9"
        assert CheckUtil.verhoeff_digit("1") == "5"
        assert CheckUtil.verhoeff_digit("11") == "3"
        assert CheckUtil.verhoeff_digit("5743839105748193475681981039847561718657489228374") == "3"
        assert CheckUtil.verhoeff_digit("10003729") == "1"
        assert CheckUtil.verhoeff_digit("505") == "3"
        assert CheckUtil.verhoeff_digit("050") == "3"

    def test_verhoeff_digit_edge_cases(self):
        """测试 Verhoeff 边界情况"""
        assert CheckUtil.verhoeff_digit("161") == "8"
        assert CheckUtil.verhoeff_digit("616") == "8"
        assert CheckUtil.verhoeff_digit("272") == "5"
        assert CheckUtil.verhoeff_digit("727") == "5"

    # ── Verhoeff 验证 ──────────────────────────────────────

    def test_verify_verhoeff_valid(self):
        """测试有效 Verhoeff 验证"""
        assert CheckUtil.verify_verhoeff("1234566543219") is True

    def test_verify_verhoeff_invalid(self):
        """测试无效 Verhoeff 验证"""
        assert CheckUtil.verify_verhoeff("1234566543210") is False

    def test_verify_verhoeff_empty(self):
        """测试空字符串"""
        assert CheckUtil.verify_verhoeff("") is False

    def test_verify_verhoeff_non_digit(self):
        """测试非数字"""
        assert CheckUtil.verify_verhoeff("abc") is False

    # ── build_verhoeff_id ──────────────────────────────────

    def test_build_verhoeff_id_default_length(self):
        """测试默认长度的 ID 生成"""
        assert CheckUtil.build_verhoeff_id("Foo", 1) == "Foo00011"
        assert CheckUtil.build_verhoeff_id("Foo", 1, length=8) == "Foo000000017"

    def test_build_verhoeff_id_custom_length(self):
        """测试自定义长度"""
        result = CheckUtil.build_verhoeff_id("ORD", 123, length=6)
        assert result.startswith("ORD000123")
        assert len(result) == 10

    # ── is_mac ─────────────────────────────────────────────

    def test_is_mac_colon(self):
        """测试冒号分隔的 MAC 地址"""
        assert CheckUtil.is_mac("00:1A:2B:3C:4D:5E") is True

    def test_is_mac_dash(self):
        """测试横杠分隔的 MAC 地址"""
        assert CheckUtil.is_mac("00-1A-2B-3C-4D-5E") is True

    def test_is_mac_lowercase(self):
        """测试小写 MAC 地址"""
        assert CheckUtil.is_mac("aa:bb:cc:dd:ee:ff") is True

    def test_is_mac_invalid(self):
        """测试无效 MAC"""
        assert CheckUtil.is_mac("invalid") is False
        assert CheckUtil.is_mac("") is False
        assert CheckUtil.is_mac("00:1A:2B:3C:4D") is False

    # ── is_chinese ─────────────────────────────────────────

    def test_is_chinese_true(self):
        """测试全中文"""
        assert CheckUtil.is_chinese("你好世界") is True

    def test_is_chinese_false(self):
        """测试混合字符"""
        assert CheckUtil.is_chinese("你好world") is False

    def test_is_chinese_empty(self):
        """测试空字符串"""
        assert CheckUtil.is_chinese("") is False

    # ── is_english ─────────────────────────────────────────

    def test_is_english_true(self):
        """测试全英文"""
        assert CheckUtil.is_english("Hello") is True

    def test_is_english_false(self):
        """测试含数字"""
        assert CheckUtil.is_english("Hello123") is False

    def test_is_english_chinese(self):
        """测试含中文"""
        assert CheckUtil.is_english("Hello你好") is False

    # ── is_symbol ──────────────────────────────────────────

    def test_is_symbol_true(self):
        """测试全符号"""
        assert CheckUtil.is_symbol("!@#$%") is True

    def test_is_symbol_false(self):
        """测试含字母"""
        assert CheckUtil.is_symbol("!@#abc") is False

    # ── contains_url ───────────────────────────────────────

    def test_contains_url_http(self):
        """测试包含 http URL"""
        assert CheckUtil.contains_url("visit https://example.com now") is True

    def test_contains_url_no_url(self):
        """测试无 URL"""
        assert CheckUtil.contains_url("no url here") is False

    def test_contains_url_empty(self):
        """测试空字符串"""
        assert CheckUtil.contains_url("") is False

    # ── is_blank_line ──────────────────────────────────────

    def test_is_blank_line_spaces(self):
        """测试空白行"""
        assert CheckUtil.is_blank_line("   ") is True

    def test_is_blank_line_not_blank(self):
        """测试非空白行"""
        assert CheckUtil.is_blank_line("hello") is False

    def test_is_blank_line_empty(self):
        """测试空字符串"""
        assert CheckUtil.is_blank_line("") is True

    # ── is_qq ──────────────────────────────────────────────

    def test_is_qq_valid(self):
        """测试有效 QQ 号"""
        assert CheckUtil.is_qq("123456789") is True

    def test_is_qq_start_zero(self):
        """测试以 0 开头"""
        assert CheckUtil.is_qq("01234") is False

    def test_is_qq_too_short(self):
        """测试过短"""
        assert CheckUtil.is_qq("123") is False

    def test_is_qq_too_long(self):
        """测试过长"""
        assert CheckUtil.is_qq("123456789012") is False

    # ── is_date_time ───────────────────────────────────────

    def test_is_date_time_valid(self):
        """测试有效日期时间"""
        assert CheckUtil.is_date_time("2024-01-15 08:30:00") is True

    def test_is_date_time_invalid_month(self):
        """测试无效月份"""
        assert CheckUtil.is_date_time("2024-13-01 00:00:00") is False

    def test_is_date_time_invalid_day(self):
        """测试无效日期"""
        assert CheckUtil.is_date_time("2024-02-30 00:00:00") is False

    def test_is_date_time_empty(self):
        """测试空字符串"""
        assert CheckUtil.is_date_time("") is False

    # ── is_post_code ───────────────────────────────────────

    def test_is_post_code_valid(self):
        """测试有效邮编"""
        assert CheckUtil.is_post_code("100000") is True

    def test_is_post_code_invalid(self):
        """测试无效邮编"""
        assert CheckUtil.is_post_code("1234") is False

    def test_is_post_code_letters(self):
        """测试含字母"""
        assert CheckUtil.is_post_code("12345a") is False

    def test_basic(self):
        result = CheckUtil.build_verhoeff_id("INV", 42, length=6)
        assert result.startswith("INV")
        assert result == "INV000042" + result[-1]
        assert len(result) == 10  # "INV" + 6 digits + 1 check

    def test_no_padding(self):
        result = CheckUtil.build_verhoeff_id("ORD", 7, length=1)
        assert result.startswith("ORD7")
        assert len(result) == 5  # "ORD" + "7" + 1 check

    def test_check_digit_is_digit(self):
        result = CheckUtil.build_verhoeff_id("T", 123, length=3)
        assert result[-1].isdigit()

    def test_zero(self):
        result = CheckUtil.build_verhoeff_id("X", 0, length=1)
        assert result == "X0" + result[-1]

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            CheckUtil.build_verhoeff_id("X", -1)

    def test_large_number(self):
        result = CheckUtil.build_verhoeff_id("ID", 999999, length=6)
        assert result == "ID999999" + result[-1]

    def test_consistency(self):
        """同一输入应产生相同的校验位"""
        r1 = CheckUtil.build_verhoeff_id("INV", 42, length=6)
        r2 = CheckUtil.build_verhoeff_id("INV", 42, length=6)
        assert r1 == r2

    def test_different_numbers_different_check(self):
        """不同数字应产生不同的校验位"""
        r1 = CheckUtil.build_verhoeff_id("INV", 1, length=1)
        r2 = CheckUtil.build_verhoeff_id("INV", 2, length=1)
        assert r1 != r2

    def test_is_phone_number(self):
        assert CheckUtil.is_phone_number("13812345678") is True
        assert CheckUtil.is_phone_number("12345678") is False

    def test_is_bank_card_valid(self):
        # Luhn-valid 16-digit card number
        assert CheckUtil.is_bank_card("4539578763621486") is True

    def test_is_bank_card_invalid(self):
        assert CheckUtil.is_bank_card("1234567890123456789") is False
        assert CheckUtil.is_bank_card("abc") is False
        assert CheckUtil.is_bank_card("") is False

    def test_is_date_formats(self):
        assert CheckUtil.is_date("2024-01-15") is True
        assert CheckUtil.is_date("2024/01/15") is True
        assert CheckUtil.is_date("20240115") is True
        assert CheckUtil.is_date("2024.01.15") is True
        assert CheckUtil.is_date("not-a-date") is False

    def test_is_date_invalid_date(self):
        assert CheckUtil.is_date("2024-13-01") is False
        assert CheckUtil.is_date("2024-02-30") is False

    def test_is_ip(self):
        assert CheckUtil.is_ip("192.168.1.1") is True
        assert CheckUtil.is_ip("::1") is True
        assert CheckUtil.is_ip("not-an-ip") is False

    def test_is_unicode(self):
        assert CheckUtil.is_unicode("hello") is True
        assert CheckUtil.is_unicode("你好") is True
        assert CheckUtil.is_unicode("") is True
        assert CheckUtil.is_unicode(None) is False

    def test_dpd_check_digit(self):
        digit = CheckUtil.dpd_check_digit("01234567890123")
        assert isinstance(digit, str)
        assert len(digit) == 1
        assert digit.isdigit()

    def test_dpd_check_digit_invalid(self):
        with pytest.raises(ValueError):
            CheckUtil.dpd_check_digit("abc")


# ================================================================== #
#  is_* 校验方法测试
# ================================================================== #


class TestCheckUtilIsMethods:
    """is_* 校验方法测试"""

    # ── is_email ───────────────────────────────────────────

    def test_is_email_valid(self):
        assert CheckUtil.is_email("test@example.com") is True
        assert CheckUtil.is_email("user.name@domain.org") is True
        assert CheckUtil.is_email("user+tag@example.com") is True

    def test_is_email_invalid(self):
        assert CheckUtil.is_email("invalid") is False
        assert CheckUtil.is_email("@example.com") is False
        assert CheckUtil.is_email("test@") is False
        assert CheckUtil.is_email("") is False

    # ── is_ipv4 ────────────────────────────────────────────

    def test_is_ipv4_valid(self):
        assert CheckUtil.is_ipv4("192.168.1.1") is True
        assert CheckUtil.is_ipv4("0.0.0.0") is True
        assert CheckUtil.is_ipv4("255.255.255.255") is True

    def test_is_ipv4_invalid(self):
        assert CheckUtil.is_ipv4("256.0.0.1") is False
        assert CheckUtil.is_ipv4("192.168.1") is False
        assert CheckUtil.is_ipv4("abc") is False
        assert CheckUtil.is_ipv4("") is False

    # ── is_ipv6 ────────────────────────────────────────────

    def test_is_ipv6_valid(self):
        assert CheckUtil.is_ipv6("::1") is True
        assert CheckUtil.is_ipv6("fe80::1") is True
        assert CheckUtil.is_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334") is True

    def test_is_ipv6_invalid(self):
        assert CheckUtil.is_ipv6("invalid") is False
        assert CheckUtil.is_ipv6("") is False
        assert CheckUtil.is_ipv6("192.168.1.1") is False

    # ── is_url ─────────────────────────────────────────────

    def test_is_url_valid(self):
        assert CheckUtil.is_url("https://example.com") is True
        assert CheckUtil.is_url("http://example.com/path?q=1") is True
        assert CheckUtil.is_url("ftp://files.example.com") is True

    def test_is_url_invalid(self):
        assert CheckUtil.is_url("not_a_url") is False
        assert CheckUtil.is_url("") is False

    # ── is_uuid ────────────────────────────────────────────

    def test_is_uuid_valid(self):
        assert CheckUtil.is_uuid("550e8400-e29b-41d4-a716-446655440000") is True
        assert CheckUtil.is_uuid("a]b-c-d-e-f") is False  # invalid chars

    def test_is_uuid_invalid(self):
        assert CheckUtil.is_uuid("invalid") is False
        assert CheckUtil.is_uuid("") is False

    # ── is_mobile ──────────────────────────────────────────

    def test_is_mobile_valid(self):
        assert CheckUtil.is_mobile("13800138000") is True
        assert CheckUtil.is_mobile("+8613800138000") is True
        assert CheckUtil.is_mobile("8613800138000") is True
        assert CheckUtil.is_mobile("19912345678") is True

    def test_is_mobile_invalid(self):
        assert CheckUtil.is_mobile("12345678901") is False
        assert CheckUtil.is_mobile("10000138000") is False
        assert CheckUtil.is_mobile("") is False

    # ── is_plate_number ────────────────────────────────────

    def test_is_plate_number_valid(self):
        # 京A12345J 是合法的旧式车牌（末位是校验字母）
        assert CheckUtil.is_plate_number("京A12345J") is True
        # 沪AF12345 是合法的新能源车牌
        assert CheckUtil.is_plate_number("沪AF12345") is True

    def test_is_plate_number_invalid(self):
        assert CheckUtil.is_plate_number("invalid") is False
        assert CheckUtil.is_plate_number("") is False

    # ── is_car_vin ─────────────────────────────────────────

    def test_is_car_vin_valid(self):
        assert CheckUtil.is_car_vin("LSVCA2A49GN202573") is True

    def test_is_car_vin_invalid(self):
        assert CheckUtil.is_car_vin("invalid") is False
        assert CheckUtil.is_car_vin("") is False

    # ── is_car_driving_licence ─────────────────────────────

    def test_is_car_driving_licence_valid(self):
        assert CheckUtil.is_car_driving_licence("123456789012") is True

    def test_is_car_driving_licence_invalid(self):
        assert CheckUtil.is_car_driving_licence("123") is False
        assert CheckUtil.is_car_driving_licence("") is False

    # ── is_birthday ────────────────────────────────────────

    def test_is_birthday_valid(self):
        assert CheckUtil.is_birthday("2000-01-15") is True
        assert CheckUtil.is_birthday("2000/01/15") is True
        assert CheckUtil.is_birthday("2000年01月15日") is True
        assert CheckUtil.is_birthday("00-01-15") is True

    def test_is_birthday_invalid(self):
        assert CheckUtil.is_birthday("2000-13-01") is False
        assert CheckUtil.is_birthday("2000-02-30") is False
        assert CheckUtil.is_birthday("invalid") is False
        assert CheckUtil.is_birthday("") is False

    # ── is_chinese_name ────────────────────────────────────

    def test_is_chinese_name_valid(self):
        assert CheckUtil.is_chinese_name("张三") is True
        assert CheckUtil.is_chinese_name("迪丽热巴") is True

    def test_is_chinese_name_invalid(self):
        assert CheckUtil.is_chinese_name("张") is False  # too short
        assert CheckUtil.is_chinese_name("Zhang") is False
        assert CheckUtil.is_chinese_name("") is False

    # ── is_credit_code ─────────────────────────────────────

    def test_is_credit_code_valid(self):
        assert CheckUtil.is_credit_code("91350100M000100Y43") is True

    def test_is_credit_code_invalid(self):
        assert CheckUtil.is_credit_code("invalid") is False
        assert CheckUtil.is_credit_code("") is False

    # ── is_citizen_id ──────────────────────────────────────

    def test_is_citizen_id_valid(self):
        # 计算一个已知校验码的身份证号
        # 11010519491231002 → 校验码 X
        assert CheckUtil.is_citizen_id("11010519491231002X") is True
        # 11010519491231002X 的校验码计算：
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        body = "11010519491231002"
        total = sum(int(body[i]) * weights[i] for i in range(17))
        check_codes = "10X98765432"
        expected = check_codes[total % 11]
        assert expected == "X"

    def test_is_citizen_id_invalid(self):
        assert CheckUtil.is_citizen_id("123456789012345678") is False
        assert CheckUtil.is_citizen_id("invalid") is False
        assert CheckUtil.is_citizen_id("") is False

    # ── is_money ───────────────────────────────────────────

    def test_is_money_valid(self):
        assert CheckUtil.is_money("100") is True
        assert CheckUtil.is_money("99.99") is True
        assert CheckUtil.is_money("0.01") is True

    def test_is_money_invalid(self):
        assert CheckUtil.is_money("-10") is False
        assert CheckUtil.is_money("abc") is False
        assert CheckUtil.is_money("") is False

    # ── is_general ─────────────────────────────────────────

    def test_is_general_valid(self):
        assert CheckUtil.is_general("hello_123") is True
        assert CheckUtil.is_general("ABC") is True

    def test_is_general_invalid(self):
        assert CheckUtil.is_general("hello 123") is False
        assert CheckUtil.is_general("") is False

    # ── is_general_with_chinese ────────────────────────────

    def test_is_general_with_chinese_valid(self):
        assert CheckUtil.is_general_with_chinese("你好abc_123") is True
        assert CheckUtil.is_general_with_chinese("你好") is True

    def test_is_general_with_chinese_invalid(self):
        assert CheckUtil.is_general_with_chinese("hello 你好") is False
        assert CheckUtil.is_general_with_chinese("") is False

    # ── is_word ────────────────────────────────────────────

    def test_is_word_valid(self):
        assert CheckUtil.is_word("Hello") is True
        assert CheckUtil.is_word("abc") is True

    def test_is_word_invalid(self):
        assert CheckUtil.is_word("Hello123") is False
        assert CheckUtil.is_word("") is False

    # ── is_hex ─────────────────────────────────────────────

    def test_is_hex_valid(self):
        assert CheckUtil.is_hex("0A1B2C") is True
        assert CheckUtil.is_hex("abcdef") is True

    def test_is_hex_invalid(self):
        assert CheckUtil.is_hex("GHI") is False
        assert CheckUtil.is_hex("") is False

    # ── is_letter ──────────────────────────────────────────

    def test_is_letter_valid(self):
        assert CheckUtil.is_letter("abc") is True
        assert CheckUtil.is_letter("ABC") is True

    def test_is_letter_invalid(self):
        assert CheckUtil.is_letter("abc123") is False
        assert CheckUtil.is_letter("") is False

    # ── is_number ──────────────────────────────────────────

    def test_is_number_valid(self):
        assert CheckUtil.is_number("12345") is True

    def test_is_number_invalid(self):
        assert CheckUtil.is_number("123a") is False
        assert CheckUtil.is_number("") is False

    # ── is_zip_code ────────────────────────────────────────

    def test_is_zip_code_valid(self):
        assert CheckUtil.is_zip_code("100000") is True

    def test_is_zip_code_invalid(self):
        assert CheckUtil.is_zip_code("1234") is False
        assert CheckUtil.is_zip_code("12345a") is False
        assert CheckUtil.is_zip_code("") is False

    # ── is_between ─────────────────────────────────────────

    def test_is_between_int(self):
        assert CheckUtil.is_between(5, 1, 10) is True
        assert CheckUtil.is_between(1, 1, 10) is True
        assert CheckUtil.is_between(10, 1, 10) is True
        assert CheckUtil.is_between(0, 1, 10) is False

    def test_is_between_str(self):
        assert CheckUtil.is_between("c", "a", "z") is True
        assert CheckUtil.is_between("a", "a", "z") is True

    def test_is_between_none(self):
        assert CheckUtil.is_between(None, 1, 10) is False

    def test_is_between_incompatible(self):
        assert CheckUtil.is_between("hello", 1, 10) is False

    # ── has_chinese ────────────────────────────────────────

    def test_has_chinese_true(self):
        assert CheckUtil.has_chinese("hello你好") is True
        assert CheckUtil.has_chinese("你好world") is True

    def test_has_chinese_false(self):
        assert CheckUtil.has_chinese("hello") is False
        assert CheckUtil.has_chinese("") is False

    # ── has_number ─────────────────────────────────────────

    def test_has_number_true(self):
        assert CheckUtil.has_number("hello123") is True
        assert CheckUtil.has_number("1abc") is True

    def test_has_number_false(self):
        assert CheckUtil.has_number("hello") is False
        assert CheckUtil.has_number("") is False

    # ── is_null / is_not_null ──────────────────────────────

    def test_is_null(self):
        assert CheckUtil.is_null(None) is True
        assert CheckUtil.is_null("") is False
        assert CheckUtil.is_null(0) is False

    def test_is_not_null(self):
        assert CheckUtil.is_not_null("hello") is True
        assert CheckUtil.is_not_null(None) is False

    # ── is_empty / is_not_empty ────────────────────────────

    def test_is_empty(self):
        assert CheckUtil.is_empty(None) is True
        assert CheckUtil.is_empty("") is True
        assert CheckUtil.is_empty([]) is True
        assert CheckUtil.is_empty({}) is True
        assert CheckUtil.is_empty(()) is True
        assert CheckUtil.is_empty(set()) is True

    def test_is_not_empty(self):
        assert CheckUtil.is_not_empty("hello") is True
        assert CheckUtil.is_not_empty([1]) is True
        assert CheckUtil.is_not_empty("") is False

    # ── is_true_bool / is_false_bool ───────────────────────

    def test_is_true_bool(self):
        assert CheckUtil.is_true_bool(True) is True
        assert CheckUtil.is_true_bool(1) is False
        assert CheckUtil.is_true_bool("true") is False

    def test_is_false_bool(self):
        assert CheckUtil.is_false_bool(False) is True
        assert CheckUtil.is_false_bool(0) is False
        assert CheckUtil.is_false_bool("false") is False


# ================================================================== #
#  validate_* 校验方法测试
# ================================================================== #


class TestCheckUtilValidateMethods:
    """validate_* 校验方法测试"""

    # ── validate_email ─────────────────────────────────────

    def test_validate_email_pass(self):
        CheckUtil.validate_email("test@example.com")

    def test_validate_email_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_email("invalid")

    # ── validate_ipv4 ──────────────────────────────────────

    def test_validate_ipv4_pass(self):
        CheckUtil.validate_ipv4("192.168.1.1")

    def test_validate_ipv4_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_ipv4("256.0.0.1")

    # ── validate_ipv6 ──────────────────────────────────────

    def test_validate_ipv6_pass(self):
        CheckUtil.validate_ipv6("::1")

    def test_validate_ipv6_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_ipv6("invalid")

    # ── validate_url ───────────────────────────────────────

    def test_validate_url_pass(self):
        CheckUtil.validate_url("https://example.com")

    def test_validate_url_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_url("not_a_url")

    # ── validate_uuid ──────────────────────────────────────

    def test_validate_uuid_pass(self):
        CheckUtil.validate_uuid("550e8400-e29b-41d4-a716-446655440000")

    def test_validate_uuid_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_uuid("invalid")

    # ── validate_mobile ────────────────────────────────────

    def test_validate_mobile_pass(self):
        CheckUtil.validate_mobile("13800138000")

    def test_validate_mobile_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_mobile("12345678901")

    # ── validate_plate_number ──────────────────────────────

    def test_validate_plate_number_pass(self):
        CheckUtil.validate_plate_number("京A12345J")
        CheckUtil.validate_plate_number("沪AF12345")

    def test_validate_plate_number_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_plate_number("invalid")

    # ── validate_car_vin ───────────────────────────────────

    def test_validate_car_vin_pass(self):
        CheckUtil.validate_car_vin("LSVCA2A49GN202573")

    def test_validate_car_vin_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_car_vin("invalid")

    # ── validate_car_driving_licence ───────────────────────

    def test_validate_car_driving_licence_pass(self):
        CheckUtil.validate_car_driving_licence("123456789012")

    def test_validate_car_driving_licence_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_car_driving_licence("123")

    # ── validate_birthday ──────────────────────────────────

    def test_validate_birthday_pass(self):
        CheckUtil.validate_birthday("2000-01-15")

    def test_validate_birthday_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_birthday("2000-13-01")

    # ── validate_chinese ───────────────────────────────────

    def test_validate_chinese_pass(self):
        CheckUtil.validate_chinese("你好世界")

    def test_validate_chinese_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_chinese("你好world")

    # ── validate_chinese_name ──────────────────────────────

    def test_validate_chinese_name_pass(self):
        CheckUtil.validate_chinese_name("张三")

    def test_validate_chinese_name_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_chinese_name("张")

    # ── validate_credit_code ───────────────────────────────

    def test_validate_credit_code_pass(self):
        CheckUtil.validate_credit_code("91350100M000100Y43")

    def test_validate_credit_code_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_credit_code("invalid")

    # ── validate_citizen_id_number ─────────────────────────

    def test_validate_citizen_id_number_pass(self):
        CheckUtil.validate_citizen_id_number("11010519491231002X")

    def test_validate_citizen_id_number_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_citizen_id_number("123456789012345678")

    # ── validate_money ─────────────────────────────────────

    def test_validate_money_pass(self):
        CheckUtil.validate_money("100")

    def test_validate_money_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_money("-10")

    # ── validate_general ───────────────────────────────────

    def test_validate_general_pass(self):
        CheckUtil.validate_general("hello_123")

    def test_validate_general_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_general("hello 123")

    # ── validate_general_with_chinese ──────────────────────

    def test_validate_general_with_chinese_pass(self):
        CheckUtil.validate_general_with_chinese("你好abc_123")

    def test_validate_general_with_chinese_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_general_with_chinese("hello 你好")

    # ── validate_word ──────────────────────────────────────

    def test_validate_word_pass(self):
        CheckUtil.validate_word("Hello")

    def test_validate_word_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_word("Hello123")

    # ── validate_hex ───────────────────────────────────────

    def test_validate_hex_pass(self):
        CheckUtil.validate_hex("0A1B2C")

    def test_validate_hex_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_hex("GHI")

    # ── validate_letter ────────────────────────────────────

    def test_validate_letter_pass(self):
        CheckUtil.validate_letter("abc")

    def test_validate_letter_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_letter("abc123")

    # ── validate_number ────────────────────────────────────

    def test_validate_number_pass(self):
        CheckUtil.validate_number("12345")

    def test_validate_number_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_number("123a")

    # ── validate_zip_code ──────────────────────────────────

    def test_validate_zip_code_pass(self):
        CheckUtil.validate_zip_code("100000")

    def test_validate_zip_code_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_zip_code("1234")

    # ── validate_between ───────────────────────────────────

    def test_validate_between_pass(self):
        CheckUtil.validate_between(5, 1, 10)

    def test_validate_between_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_between(0, 1, 10)

    # ── validate_not_empty ─────────────────────────────────

    def test_validate_not_empty_pass(self):
        CheckUtil.validate_not_empty("hello")

    def test_validate_not_empty_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_not_empty("")

    def test_validate_not_empty_none_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_not_empty(None)

    # ── validate_not_null ──────────────────────────────────

    def test_validate_not_null_pass(self):
        CheckUtil.validate_not_null("hello")

    def test_validate_not_null_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_not_null(None)

    # ── validate_null ──────────────────────────────────────

    def test_validate_null_pass(self):
        CheckUtil.validate_null(None)

    def test_validate_null_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_null("hello")

    # ── validate_empty ─────────────────────────────────────

    def test_validate_empty_pass(self):
        CheckUtil.validate_empty(None)
        CheckUtil.validate_empty("")
        CheckUtil.validate_empty([])

    def test_validate_empty_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_empty("hello")

    # ── validate_true ──────────────────────────────────────

    def test_validate_true_pass(self):
        CheckUtil.validate_true(True)

    def test_validate_true_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_true(False)

    def test_validate_true_non_bool_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_true(1)

    # ── validate_false ─────────────────────────────────────

    def test_validate_false_pass(self):
        CheckUtil.validate_false(False)

    def test_validate_false_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_false(True)

    # ── validate_equal ─────────────────────────────────────

    def test_validate_equal_pass(self):
        CheckUtil.validate_equal("hello", "hello")
        CheckUtil.validate_equal(None, None)

    def test_validate_equal_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_equal("hello", "world")

    # ── validate_not_equal ─────────────────────────────────

    def test_validate_not_equal_pass(self):
        CheckUtil.validate_not_equal("hello", "world")

    def test_validate_not_equal_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_not_equal("hello", "hello")

    # ── validate_not_empty_and_equal ───────────────────────

    def test_validate_not_empty_and_equal_pass(self):
        CheckUtil.validate_not_empty_and_equal("hello", "hello")

    def test_validate_not_empty_and_equal_empty_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_not_empty_and_equal("", "hello")

    def test_validate_not_empty_and_equal_not_equal_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_not_empty_and_equal("hello", "world")

    # ── validate_not_empty_and_not_equal ───────────────────

    def test_validate_not_empty_and_not_equal_pass(self):
        CheckUtil.validate_not_empty_and_not_equal("hello", "world")

    def test_validate_not_empty_and_not_equal_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_not_empty_and_not_equal("hello", "hello")

    # ── validate_upper_case ────────────────────────────────

    def test_validate_upper_case_pass(self):
        CheckUtil.validate_upper_case("HELLO")

    def test_validate_upper_case_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_upper_case("hello")

    def test_validate_upper_case_empty_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_upper_case("")

    # ── validate_lower_case ────────────────────────────────

    def test_validate_lower_case_pass(self):
        CheckUtil.validate_lower_case("hello")

    def test_validate_lower_case_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_lower_case("HELLO")

    # ── validate_match_regex ───────────────────────────────

    def test_validate_match_regex_pass(self):
        CheckUtil.validate_match_regex("hello", r"^h\w+$")

    def test_validate_match_regex_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_match_regex("world", r"^h\w+$")

    # ── validate_mac ───────────────────────────────────────

    def test_validate_mac_pass(self):
        CheckUtil.validate_mac("00:1A:2B:3C:4D:5E")

    def test_validate_mac_fail(self):
        with pytest.raises(ValidateException):
            CheckUtil.validate_mac("invalid")

    # ── check_index_limit ──────────────────────────────────

    def test_check_index_limit_pass(self):
        assert CheckUtil.check_index_limit(2, 5) == 2
        assert CheckUtil.check_index_limit(0, 5) == 0
        assert CheckUtil.check_index_limit(4, 5) == 4

    def test_check_index_limit_fail_negative(self):
        with pytest.raises(ValidateException):
            CheckUtil.check_index_limit(-1, 5)

    def test_check_index_limit_fail_overflow(self):
        with pytest.raises(ValidateException):
            CheckUtil.check_index_limit(5, 5)

    # ── custom error messages ──────────────────────────────

    def test_validate_custom_error_msg(self):
        with pytest.raises(ValidateException, match="自定义错误"):
            CheckUtil.validate_email("invalid", error_msg="自定义错误")

    def test_validate_not_empty_custom_msg(self):
        with pytest.raises(ValidateException, match="不能为空"):
            CheckUtil.validate_not_empty("", error_msg="不能为空")
