"""
校验码计算工具类

对应 Java cn.hutool.core.util 的校验码相关功能。
提供 EAN/UPC 条形码校验位和 Verhoeff 校验位算法。
"""

import re


class CheckUtil:
    """校验码计算工具类，提供各种校验码算法。

    包含以下算法：

    - **EAN/UPC/NVE** 校验位：广泛用于商品条形码
    - **Verhoeff** 校验位：基于二面体群 D₅，可检测所有单字符错误和相邻换位错误
    """

    # ------------------------------------------------------------------ #
    #  EAN / UPC / NVE
    # ------------------------------------------------------------------ #

    @staticmethod
    def ean_digit(digits: str) -> str:
        """
        计算 EAN/UPC/NVE 条形码的校验位。

        算法：从右向左，奇数位乘 3、偶数位乘 1，求和后取模 10 的补数。

        :param digits: 条形码数字字符串（不含校验位）
        :return: 校验位字符串（单个数字字符）

        ::

            >>> CheckUtil.ean_digit('400599871650')
            '2'
            >>> CheckUtil.ean_digit('1234567890123')
            '1'
        """
        factor = 3
        total = 0
        for index in range(len(digits) - 1, -1, -1):
            total += int(digits[index]) * factor
            factor = 4 - factor
        return str((10 - (total % 10)) % 10)

    @staticmethod
    def verify_ean(code: str) -> bool:
        """
        验证 EAN/UPC 条形码的校验码是否正确。

        :param code: 完整的条形码字符串（含校验位）
        :return: 校验码是否正确

        ::

            >>> CheckUtil.verify_ean('4005998000007')
            True
            >>> CheckUtil.verify_ean('4005998000000')
            False
            >>> CheckUtil.verify_ean('foobar')
            False
        """
        code = str(code)
        if not code.isdigit():
            return False
        return CheckUtil.ean_digit(code[:-1]) == code[-1]

    # ------------------------------------------------------------------ #
    #  Verhoeff（二面体群 D₅）
    # ------------------------------------------------------------------ #

    # 乘法表
    _VERHOEFF_D = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
        (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
        (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
        (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
        (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
        (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
        (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
        (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
        (9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
    )

    # 逆元表
    _VERHOEFF_INV = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)

    # 排列权重表
    _VERHOEFF_P = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
        (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
        (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
        (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
        (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
        (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
        (7, 0, 4, 6, 9, 1, 3, 2, 5, 8),
    )

    @staticmethod
    def verhoeff_digit(digits: str) -> str:
        """
        计算 Verhoeff 校验位（基于二面体群 D₅）。

        Verhoeff 算法可以检测所有单字符错误和相邻字符换位错误，
        优于传统的模 10 校验。

        :param digits: 数字字符串（不含校验位）
        :return: 校验位字符串（单个数字字符）

        ::

            >>> CheckUtil.verhoeff_digit('123456654321')
            '9'
            >>> CheckUtil.verhoeff_digit('1')
            '5'
        """
        d = CheckUtil._VERHOEFF_D
        inv = CheckUtil._VERHOEFF_INV
        p = CheckUtil._VERHOEFF_P

        check = 0
        for i, ch in enumerate(reversed(digits)):
            digit = ord(ch) - 48
            check = d[check][p[(i + 1) % 8][digit]]
        return str(inv[check])

    @staticmethod
    def verify_verhoeff(digits_with_check: str) -> bool:
        """
        验证带 Verhoeff 校验位的数字字符串是否合法。

        :param digits_with_check: 含校验位的数字字符串
        :return: 校验位是否正确

        ::

            >>> CheckUtil.verify_verhoeff('1234566543219')
            True
            >>> CheckUtil.verify_verhoeff('1234566543210')
            False
        """
        if not digits_with_check or not digits_with_check.isdigit():
            return False
        body = digits_with_check[:-1]
        check = digits_with_check[-1]
        return CheckUtil.verhoeff_digit(body) == check

    @staticmethod
    def build_verhoeff_id(prefix: str, number: int, length: int = 4) -> str:
        """
        生成带 Verhoeff 校验位的 ID 字符串。

        将数字左补零到指定长度后，追加 Verhoeff 校验位，再拼接前缀。

        :param prefix: ID 前缀
        :param number: 数字编号
        :param length: 数字部分的最小长度，默认为 4
        :return: 带校验位的完整 ID 字符串

        ::

            >>> CheckUtil.build_verhoeff_id('Foo', 1)
            'Foo00011'
            >>> CheckUtil.build_verhoeff_id('Foo', 1, length=8)
            'Foo000000017'
        """
        number_str = str(number).rjust(length, "0")
        checksum = CheckUtil.verhoeff_digit(number_str)
        return prefix + number_str + checksum

    # ------------------------------------------------------------------ #
    #  文本校验方法
    # ------------------------------------------------------------------ #

    @staticmethod
    def is_mac(text: str) -> bool:
        """
        校验 MAC 地址格式。

        支持 ``XX:XX:XX:XX:XX:XX`` 和 ``XX-XX-XX-XX-XX-XX`` 格式（不区分大小写）。

        :param text: 待校验的字符串
        :return: 是否为合法的 MAC 地址

        ::

            >>> CheckUtil.is_mac('00:1A:2B:3C:4D:5E')
            True
            >>> CheckUtil.is_mac('00-1A-2B-3C-4D-5E')
            True
            >>> CheckUtil.is_mac('invalid')
            False
        """
        if not text:
            return False
        return bool(re.match(r"^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$", text))

    @staticmethod
    def is_chinese(text: str) -> bool:
        """
        判断字符串是否全部由中文字符组成。

        :param text: 待校验的字符串
        :return: 是否全部为中文字符

        ::

            >>> CheckUtil.is_chinese('你好世界')
            True
            >>> CheckUtil.is_chinese('你好world')
            False
        """
        if not text:
            return False
        return bool(re.match(r"^[一-龥]+$", text))

    @staticmethod
    def is_english(text: str) -> bool:
        """
        判断字符串是否全部由英文字母组成。

        :param text: 待校验的字符串
        :return: 是否全部为英文字母

        ::

            >>> CheckUtil.is_english('Hello')
            True
            >>> CheckUtil.is_english('Hello123')
            False
        """
        if not text:
            return False
        return text.isalpha() and text.isascii()

    @staticmethod
    def is_symbol(text: str) -> bool:
        """
        判断字符串是否全部由符号（非字母数字和空白）组成。

        :param text: 待校验的字符串
        :return: 是否全部为符号

        ::

            >>> CheckUtil.is_symbol('!@#$%')
            True
            >>> CheckUtil.is_symbol('!@#abc')
            False
        """
        if not text:
            return False
        return bool(re.match(r"^[^\w\s]+$", text))

    @staticmethod
    def contains_url(text: str) -> bool:
        """
        判断字符串中是否包含 URL。

        :param text: 待检查的字符串
        :return: 是否包含 URL

        ::

            >>> CheckUtil.contains_url('visit https://example.com now')
            True
            >>> CheckUtil.contains_url('no url here')
            False
        """
        if not text:
            return False
        return bool(re.search(r'https?://[^\s<>"\']+|www\.[^\s<>"\']+', text))

    @staticmethod
    def is_blank_line(text: str) -> bool:
        """
        判断字符串是否为空白行（仅含空白字符或为空）。

        :param text: 待校验的字符串
        :return: 是否为空白行

        ::

            >>> CheckUtil.is_blank_line('   ')
            True
            >>> CheckUtil.is_blank_line('hello')
            False
        """
        if text is None:
            return True
        return text.strip() == ""

    @staticmethod
    def is_qq(text: str) -> bool:
        """
        校验 QQ 号码格式。

        QQ 号为 5~11 位数字，且不以 0 开头。

        :param text: 待校验的字符串
        :return: 是否为合法的 QQ 号码

        ::

            >>> CheckUtil.is_qq('123456789')
            True
            >>> CheckUtil.is_qq('01234')
            False
            >>> CheckUtil.is_qq('123')
            False
        """
        if not text:
            return False
        return bool(re.match(r"^[1-9]\d{4,10}$", text))

    @staticmethod
    def is_date_time(text: str) -> bool:
        """
        校验日期时间格式（``YYYY-MM-DD HH:mm:ss``）。

        会检查日期和时间的值范围合法性。

        :param text: 待校验的字符串
        :return: 是否为合法的日期时间格式

        ::

            >>> CheckUtil.is_date_time('2024-01-15 08:30:00')
            True
            >>> CheckUtil.is_date_time('2024-13-01 00:00:00')
            False
        """
        if not text:
            return False
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})$", text)
        if not m:
            return False
        year, month, day, hour, minute, second = (int(x) for x in m.groups())
        if not (1 <= month <= 12):
            return False
        if not (1 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
            return False
        import calendar as _cal

        _, max_day = _cal.monthrange(year, month)
        return 1 <= day <= max_day

    @staticmethod
    def is_post_code(text: str) -> bool:
        """
        校验邮政编码格式（中国 6 位邮编）。

        :param text: 待校验的字符串
        :return: 是否为合法的邮政编码

        ::

            >>> CheckUtil.is_post_code('100000')
            True
            >>> CheckUtil.is_post_code('1234')
            False
        """
        if not text:
            return False
        return bool(re.match(r"^\d{6}$", text))
