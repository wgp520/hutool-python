"""CheckUtil 测试"""

from hutool import CheckUtil


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
        # 123456654321 的校验位是 9，拼接后为 1234566543219
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
        # 3(prefix) + 6(number) + 1(check digit) = 10
        assert len(result) == 10

    # ── is_mac ──────────────────────────────────────────────────────

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

    # ── is_chinese ──────────────────────────────────────────────────

    def test_is_chinese_true(self):
        """测试全中文"""
        assert CheckUtil.is_chinese("你好世界") is True

    def test_is_chinese_false(self):
        """测试混合字符"""
        assert CheckUtil.is_chinese("你好world") is False

    def test_is_chinese_empty(self):
        """测试空字符串"""
        assert CheckUtil.is_chinese("") is False

    # ── is_english ──────────────────────────────────────────────────

    def test_is_english_true(self):
        """测试全英文"""
        assert CheckUtil.is_english("Hello") is True

    def test_is_english_false(self):
        """测试含数字"""
        assert CheckUtil.is_english("Hello123") is False

    def test_is_english_chinese(self):
        """测试含中文"""
        assert CheckUtil.is_english("Hello你好") is False

    # ── is_symbol ───────────────────────────────────────────────────

    def test_is_symbol_true(self):
        """测试全符号"""
        assert CheckUtil.is_symbol("!@#$%") is True

    def test_is_symbol_false(self):
        """测试含字母"""
        assert CheckUtil.is_symbol("!@#abc") is False

    # ── contains_url ────────────────────────────────────────────────

    def test_contains_url_http(self):
        """测试包含 http URL"""
        assert CheckUtil.contains_url("visit https://example.com now") is True

    def test_contains_url_no_url(self):
        """测试无 URL"""
        assert CheckUtil.contains_url("no url here") is False

    def test_contains_url_empty(self):
        """测试空字符串"""
        assert CheckUtil.contains_url("") is False

    # ── is_blank_line ───────────────────────────────────────────────

    def test_is_blank_line_spaces(self):
        """测试空白行"""
        assert CheckUtil.is_blank_line("   ") is True

    def test_is_blank_line_not_blank(self):
        """测试非空白行"""
        assert CheckUtil.is_blank_line("hello") is False

    def test_is_blank_line_empty(self):
        """测试空字符串"""
        assert CheckUtil.is_blank_line("") is True

    # ── is_qq ───────────────────────────────────────────────────────

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

    # ── is_date_time ────────────────────────────────────────────────

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

    # ── is_post_code ────────────────────────────────────────────────

    def test_is_post_code_valid(self):
        """测试有效邮编"""
        assert CheckUtil.is_post_code("100000") is True

    def test_is_post_code_invalid(self):
        """测试无效邮编"""
        assert CheckUtil.is_post_code("1234") is False

    def test_is_post_code_letters(self):
        """测试含字母"""
        assert CheckUtil.is_post_code("12345a") is False
