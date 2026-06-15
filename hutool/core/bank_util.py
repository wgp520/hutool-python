"""
银行工具类

提供 IBAN（国际银行账号）的计算和验证功能。
基于 ISO 7064 mod 97-10 标准。
"""

from string import ascii_uppercase


class BankUtil:
    """银行工具类，提供 IBAN 计算和验证。

    IBAN（International Bank Account Number）是国际银行账号标准，
    校验算法基于 ISO 7064 mod 97-10。
    """

    @staticmethod
    def calculate_iban(account: str, bank_code: str, country: str = "DE") -> str:
        """
        根据账号和银行代码计算 IBAN。

        算法步骤：

        1. 将银行代码和账号拼接为 BBAN（Basic Bank Account Number）
        2. 将国家代码 + 两个校验位（00）追加到 BBAN 末尾
        3. 将字母转换为数字（A=10, B=11, ..., Z=35）
        4. 对 97 取模，用 98 减去余数得到校验位

        :param account: 银行账号
        :param bank_code: 银行代码（如德国的 BLZ）
        :param country: 国家代码，默认 ``"DE"``
        :return: 完整的 IBAN 字符串

        ::

            >>> BankUtil.calculate_iban('1234567890', '37040044')
            'DE89370400441234567890'
        """
        bban = f"{int(bank_code):08d}{int(account):010d}"
        tmp = BankUtil._convert_chars(f"{bban}{country.upper()}00")
        check = 98 - (int(tmp) % 97)
        return f"{country.upper()}{check:02d}{bban}"

    @staticmethod
    def check_iban(iban: str) -> bool:
        """
        验证 IBAN 是否合法。

        将 IBAN 的前 4 位（国家代码 + 校验位）移到末尾，
        将字母转换为数字后对 97 取模，结果应为 1。

        :param iban: IBAN 字符串
        :return: 是否合法

        ::

            >>> BankUtil.check_iban('DE89370400441234567890')
            True
            >>> BankUtil.check_iban('DE00370400441234567890')
            False
        """
        if not iban or len(iban) < 5:
            return False
        # 前 4 位移到末尾
        rearranged = iban[4:] + iban[:4]
        # 将字母转换为数字
        numeric_str = BankUtil._convert_chars(rearranged)
        try:
            return int(numeric_str) % 97 == 1
        except (ValueError, OverflowError):
            return False

    @staticmethod
    def _convert_chars(text: str) -> str:
        """
        将字符串中的字母转换为对应的数字（A=10, B=11, ..., Z=35），
        数字保持不变。

        :param text: 输入字符串
        :return: 纯数字字符串
        """
        result = []
        for ch in text:
            if ch.isdigit():
                result.append(ch)
            elif ch.isalpha():
                result.append(str(ascii_uppercase.index(ch.upper()) + 10))
            else:
                raise ValueError(f"IBAN 包含无效字符: '{ch}'")
        return "".join(result)
