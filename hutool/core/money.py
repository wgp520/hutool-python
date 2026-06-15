"""
货币计算工具类

提供元/分转换和含税/不含税价格计算功能。
所有计算使用 ``Decimal`` 精确运算，避免浮点精度问题。
"""

from decimal import ROUND_HALF_DOWN, Decimal


class MoneyUtil:
    """货币计算工具类。

    提供元（Yuan）/ 分（Fen）转换和含税 / 不含税价格计算，
    默认增值税率为 13%（中国标准增值税率）。
    所有计算使用 ``Decimal`` 精确运算。
    """

    # 默认增值税率（百分比）
    DEFAULT_TAX_RATE: Decimal = Decimal("13")

    @staticmethod
    def fen_to_yuan(amount):
        # type: (Union[int, str, Decimal]) -> Decimal
        """
        分转元。

        :param amount: 分金额（整数、字符串或 Decimal）
        :return: 元金额（Decimal，保留两位小数）

        ::

            >>> MoneyUtil.fen_to_yuan(100)
            Decimal('1.00')
            >>> MoneyUtil.fen_to_yuan(1)
            Decimal('0.01')
            >>> MoneyUtil.fen_to_yuan('50')
            Decimal('0.50')
        """
        value = Decimal(str(amount)) / 100
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_DOWN)

    @staticmethod
    def yuan_to_fen(amount):
        # type: (Union[float, str, Decimal]) -> int
        """
        元转分（四舍五入到分）。

        :param amount: 元金额
        :return: 分金额（整数）

        ::

            >>> MoneyUtil.yuan_to_fen(1)
            100
            >>> MoneyUtil.yuan_to_fen('0.5')
            50
            >>> MoneyUtil.yuan_to_fen('0.01')
            1
            >>> MoneyUtil.yuan_to_fen('0.001')
            0
        """
        value = Decimal(str(amount)) * 100
        return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_DOWN))

    @staticmethod
    def net_price(amount, tax_rate=None):
        # type: (Union[float, str, Decimal], Optional[float]) -> Decimal
        """
        根据含税价计算不含税价（去税价）。

        公式：不含税价 = 含税价 / (1 + 税率/100)

        :param amount: 含税价金额
        :param tax_rate: 税率百分比，默认为 13%
        :return: 不含税价（Decimal，保留两位小数）
        :raises ValueError: 税率大于等于 100%

        ::

            >>> MoneyUtil.net_price(Decimal('113'))
            Decimal('100.00')
            >>> MoneyUtil.net_price(Decimal('108'), tax_rate=8)
            Decimal('100.00')
        """
        rate = MoneyUtil._resolve_tax_rate(tax_rate)
        amount = Decimal(str(amount))
        divisor = (Decimal(100) + rate) / Decimal(100)
        result = amount / divisor
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_DOWN)

    @staticmethod
    def gross_price(amount, tax_rate=None):
        # type: (Union[float, str, Decimal], Optional[float]) -> Decimal
        """
        根据不含税价计算含税价。

        公式：含税价 = 不含税价 × (1 + 税率/100)

        :param amount: 不含税价金额
        :param tax_rate: 税率百分比，默认为 13%
        :return: 含税价（Decimal，保留两位小数）
        :raises ValueError: 税率大于等于 100%

        ::

            >>> MoneyUtil.gross_price(Decimal('100'))
            Decimal('113.00')
            >>> MoneyUtil.gross_price(Decimal('100'), tax_rate=8)
            Decimal('108.00')
        """
        rate = MoneyUtil._resolve_tax_rate(tax_rate)
        amount = Decimal(str(amount))
        multiplier = (Decimal(100) + rate) / Decimal(100)
        result = amount * multiplier
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_DOWN)

    @staticmethod
    def tax_amount(amount, tax_rate=None):
        # type: (Union[float, str, Decimal], Optional[float]) -> Decimal
        """
        计算税额（含税价中的税额部分）。

        公式：税额 = 含税价 - 不含税价

        :param amount: 含税价金额
        :param tax_rate: 税率百分比，默认为 13%
        :return: 税额（Decimal，保留两位小数）
        :raises ValueError: 税率大于等于 100%

        ::

            >>> MoneyUtil.tax_amount(Decimal('113'))
            Decimal('13.00')
        """
        net = MoneyUtil.net_price(amount, tax_rate)
        return Decimal(str(amount)) - net

    @staticmethod
    def _resolve_tax_rate(tax_rate):
        # type: (Optional[float]) -> Decimal
        """解析税率参数，返回 Decimal。"""
        if tax_rate is None:
            return MoneyUtil.DEFAULT_TAX_RATE
        rate = Decimal(str(tax_rate))
        if rate >= 100:
            raise ValueError(f"税率必须小于 100%，当前值: {tax_rate}")
        return rate
