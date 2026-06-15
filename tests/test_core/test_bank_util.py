"""BankUtil 测试"""

import pytest

from hutool import BankUtil


class TestBankUtil:
    """BankUtil 测试类"""

    # ── calculate_iban ──────────────────────────────────────

    def test_calculate_iban_german(self):
        """测试德国 IBAN 计算和验证的往返一致性"""
        iban = BankUtil.calculate_iban("1234567890", "37040044")
        assert iban.startswith("DE")
        assert len(iban) == 22
        # 计算出的 IBAN 必须通过验证
        assert BankUtil.check_iban(iban) is True

    def test_calculate_iban_country_code(self):
        """测试国家代码大写转换"""
        iban = BankUtil.calculate_iban("1234567890", "37040044", country="de")
        assert iban.startswith("DE")

    def test_calculate_iban_format(self):
        """测试 IBAN 格式"""
        iban = BankUtil.calculate_iban("1234567890", "37040044")
        assert len(iban) == 22  # DE + 2 check + 8 BLZ + 10 account
        assert iban[:2].isalpha()
        assert iban[2:4].isdigit()
        assert iban[4:].isdigit()

    # ── check_iban ──────────────────────────────────────────

    def test_check_iban_valid(self):
        """测试有效 IBAN（往返验证）"""
        iban = BankUtil.calculate_iban("1234567890", "37040044")
        assert BankUtil.check_iban(iban) is True

    def test_check_iban_invalid_check(self):
        """测试无效校验位"""
        assert BankUtil.check_iban("DE00370400441234567890") is False

    def test_check_iban_too_short(self):
        """测试过短的 IBAN"""
        assert BankUtil.check_iban("DE") is False

    def test_check_iban_empty(self):
        """测试空字符串"""
        assert BankUtil.check_iban("") is False

    def test_check_iban_roundtrip(self):
        """测试计算后再验证的一致性"""
        iban = BankUtil.calculate_iban("9876543210", "20050550")
        assert BankUtil.check_iban(iban) is True

    # ── _convert_chars ──────────────────────────────────────

    def test_convert_chars(self):
        """测试字符转换"""
        assert BankUtil._convert_chars("DE89") == "131489"
        assert BankUtil._convert_chars("1234") == "1234"

    def test_convert_chars_invalid(self):
        """测试无效字符"""
        with pytest.raises(ValueError):
            BankUtil._convert_chars("DE@89")
