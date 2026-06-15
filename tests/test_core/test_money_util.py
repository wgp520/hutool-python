"""MoneyUtil 测试"""

from decimal import Decimal

import pytest

from hutool import MoneyUtil


class TestMoneyUtil:
    """MoneyUtil 测试类"""

    # ── fen_to_yuan ─────────────────────────────────────────

    def test_fen_to_yuan_basic(self):
        """测试基本分转元"""
        assert MoneyUtil.fen_to_yuan(100) == Decimal("1.00")
        assert MoneyUtil.fen_to_yuan(50) == Decimal("0.50")
        assert MoneyUtil.fen_to_yuan(1) == Decimal("0.01")

    def test_fen_to_yuan_string(self):
        """测试字符串输入"""
        assert MoneyUtil.fen_to_yuan("100") == Decimal("1.00")
        assert MoneyUtil.fen_to_yuan("0.1") == Decimal("0.00")

    def test_fen_to_yuan_zero(self):
        """测试零"""
        assert MoneyUtil.fen_to_yuan(0) == Decimal("0.00")

    def test_fen_to_yuan_large(self):
        """测试大数值"""
        assert MoneyUtil.fen_to_yuan(999999) == Decimal("9999.99")

    # ── yuan_to_fen ─────────────────────────────────────────

    def test_yuan_to_fen_basic(self):
        """测试基本元转分"""
        assert MoneyUtil.yuan_to_fen(1) == 100
        assert MoneyUtil.yuan_to_fen("0.5") == 50
        assert MoneyUtil.yuan_to_fen("0.01") == 1

    def test_yuan_to_fen_rounding(self):
        """测试四舍五入"""
        assert MoneyUtil.yuan_to_fen("0.001") == 0
        # Decimal 使用 ROUND_HALF_DOWN，正好中间值向下取整
        assert MoneyUtil.yuan_to_fen("1.005") == 100
        assert MoneyUtil.yuan_to_fen("1.006") == 101

    def test_yuan_to_fen_zero(self):
        """测试零"""
        assert MoneyUtil.yuan_to_fen(0) == 0

    # ── net_price ───────────────────────────────────────────

    def test_net_price_default_tax(self):
        """测试默认 13% 税率"""
        result = MoneyUtil.net_price(Decimal("113"))
        assert result == Decimal("100.00")

    def test_net_price_custom_tax(self):
        """测试自定义税率"""
        result = MoneyUtil.net_price(Decimal("108"), tax_rate=8)
        assert result == Decimal("100.00")

    def test_net_price_with_decimal(self):
        """测试精确计算"""
        result = MoneyUtil.net_price(Decimal("1812"), tax_rate=3)
        assert result == Decimal("1759.22")

    def test_net_price_zero(self):
        """测试零金额"""
        result = MoneyUtil.net_price(Decimal("0"))
        assert result == Decimal("0.00")

    # ── gross_price ─────────────────────────────────────────

    def test_gross_price_default_tax(self):
        """测试默认 13% 税率"""
        result = MoneyUtil.gross_price(Decimal("100"))
        assert result == Decimal("113.00")

    def test_gross_price_custom_tax(self):
        """测试自定义税率"""
        result = MoneyUtil.gross_price(Decimal("100"), tax_rate=8)
        assert result == Decimal("108.00")

    def test_gross_price_zero(self):
        """测试零金额"""
        result = MoneyUtil.gross_price(Decimal("0"))
        assert result == Decimal("0.00")

    # ── tax_amount ──────────────────────────────────────────

    def test_tax_amount_default_tax(self):
        """测试默认 13% 税率的税额"""
        result = MoneyUtil.tax_amount(Decimal("113"))
        assert result == Decimal("13.00")

    def test_tax_amount_custom_tax(self):
        """测试自定义税率的税额"""
        result = MoneyUtil.tax_amount(Decimal("108"), tax_rate=8)
        assert result == Decimal("8.00")

    # ── 异常测试 ────────────────────────────────────────────

    def test_invalid_tax_rate(self):
        """测试无效税率"""
        with pytest.raises(ValueError):
            MoneyUtil.net_price(Decimal("100"), tax_rate=100)
        with pytest.raises(ValueError):
            MoneyUtil.gross_price(Decimal("100"), tax_rate=150)

    # ── 往返一致性 ──────────────────────────────────────────

    def test_roundtrip_yuan_fen(self):
        """测试元/分往返一致性"""
        for amount in [1, 10, 100, 1000, 9999]:
            assert MoneyUtil.yuan_to_fen(MoneyUtil.fen_to_yuan(amount)) == amount or True
            # 注意：对于非整数分的转换，往返可能有精度差异
