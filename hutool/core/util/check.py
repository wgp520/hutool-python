"""
校验码计算工具类

对应 Java cn.hutool.core.util 的校验码相关功能。
提供 EAN/UPC 条形码校验位和 Verhoeff 校验位算法，以及通用数据校验方法。
"""

import re
from typing import Any, Optional

from ..exceptions import ValidateException
from .object import ObjectUtil


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
        if number < 0:
            raise ValueError(f"number 必须为非负整数，实际为 {number}")
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

    # ================================================================== #
    #  通用校验正则常量
    # ================================================================== #

    _RE_GENERAL = re.compile(r"^\w+$")
    _RE_GENERAL_WITH_CHINESE = re.compile(r"^[一-鿿\w]+$")
    _RE_IPV4 = re.compile(
        r"^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)\."
        r"(25[0-5]|2[0-4]\d|[0-1]?\d?\d)\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)$"
    )
    _RE_IPV6 = re.compile(
        r"(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|"
        r"([0-9a-fA-F]{1,4}:){1,7}:|"
        r"([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|"
        r"([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|"
        r"([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|"
        r"([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|"
        r"([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|"
        r"[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|"
        r":((:[0-9a-fA-F]{1,4}){1,7}|:)|"
        r"fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]+|"
        r"::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?[0-9])?[0-9])\.){3}(25[0-5]|(2[0-4]|1?[0-9])?[0-9])|"
        r"([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?[0-9])?[0-9])\.){3}(25[0-5]|(2[0-4]|1?[0-9])?[0-9]))"
    )
    _RE_URL = re.compile(r"[a-zA-Z]+://[\w\-+&@#/%?=~_|!:,.;]*[\w\-+&@#/%=~_|]")
    _RE_UUID = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        re.IGNORECASE,
    )
    _RE_MOBILE = re.compile(r"^(?:0|86|\+86)?1[3-9]\d{9}$")
    _RE_MONEY = re.compile(r"^(\d+(?:\.\d+)?)$")
    _RE_HEX = re.compile(r"^[a-fA-F0-9]+$")
    _RE_WORD = re.compile(r"^[a-zA-Z]+$")
    _RE_LETTER = _RE_WORD
    _RE_NUMBER = re.compile(r"^\d+$")
    _RE_ZIP_CODE = re.compile(r"^\d{6}$")
    _RE_CITIZEN_ID = re.compile(r"^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$")
    _RE_CREDIT_CODE = re.compile(r"^[0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}$")
    _RE_CHINESE_NAME = re.compile(r"^[㐀-鿿豈-﫿·]{2,60}$")
    _RE_PLATE_NUMBER = re.compile(
        r"^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤川青藏琼宁]"
        r"[A-Z]"
        r"([0-9]{5}[ABCDEFGHJK]|[ABCDEFGHJKP][A-HJ-NP-Z0-9][0-9]{4})$"
    )
    _RE_CAR_VIN = re.compile(
        r"^[A-HJ-NPR-Z0-9]{8}[X0-9]"
        r"([A-HJ-NPR-Z0-9]{3}\d{5}|[A-HJ-NPR-Z0-9]{5}\d{3})$"
    )
    _RE_CAR_DRIVING_LICENCE = re.compile(r"^[0-9]{12}$")
    _RE_BIRTHDAY = re.compile(r"^(\d{2,4})([/\-.年]?)(\d{1,2})([/\-.月]?)(\d{1,2})日?$")
    _RE_HAS_CHINESE = re.compile(r"[一-鿿]")
    _RE_HAS_NUMBER = re.compile(r"\d")

    # ================================================================== #
    #  is_* 校验方法
    # ================================================================== #

    @staticmethod
    def is_email(value: str) -> bool:
        """
        校验是否为合法的邮箱地址（RFC 5322 规范）。

        :param value: 待校验的字符串
        :return: 是否为合法邮箱

        ::

            >>> CheckUtil.is_email('test@example.com')
            True
            >>> CheckUtil.is_email('invalid')
            False
        """
        if not value:
            return False
        pattern = (
            r"^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
            r'|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")'
            r"@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)$"
        )
        return bool(re.match(pattern, value, re.IGNORECASE))

    @staticmethod
    def is_ipv4(value: str) -> bool:
        """
        校验是否为合法的 IPv4 地址。

        :param value: 待校验的字符串
        :return: 是否为合法 IPv4 地址

        ::

            >>> CheckUtil.is_ipv4('192.168.1.1')
            True
            >>> CheckUtil.is_ipv4('256.0.0.1')
            False
        """
        if not value:
            return False
        return bool(CheckUtil._RE_IPV4.match(value))

    @staticmethod
    def is_ipv6(value: str) -> bool:
        """
        校验是否为合法的 IPv6 地址。

        :param value: 待校验的字符串
        :return: 是否为合法 IPv6 地址

        ::

            >>> CheckUtil.is_ipv6('::1')
            True
            >>> CheckUtil.is_ipv6('fe80::1')
            True
            >>> CheckUtil.is_ipv6('invalid')
            False
        """
        if not value:
            return False
        return bool(CheckUtil._RE_IPV6.match(value))

    @staticmethod
    def is_url(value: str) -> bool:
        """
        校验是否为合法的 URL。

        :param value: 待校验的字符串
        :return: 是否为合法 URL

        ::

            >>> CheckUtil.is_url('https://example.com')
            True
            >>> CheckUtil.is_url('not_a_url')
            False
        """
        if not value:
            return False
        return bool(CheckUtil._RE_URL.match(value))

    @staticmethod
    def is_uuid(value: str) -> bool:
        """
        校验是否为合法的 UUID。

        :param value: 待校验的字符串
        :return: 是否为合法 UUID

        ::

            >>> CheckUtil.is_uuid('550e8400-e29b-41d4-a716-446655440000')
            True
            >>> CheckUtil.is_uuid('invalid')
            False
        """
        if not value:
            return False
        return bool(CheckUtil._RE_UUID.match(value))

    @staticmethod
    def is_mobile(mobile: str) -> bool:
        """
        校验是否为中国大陆手机号（严格模式）。

        支持 ``+86``、``86``、``0`` 前缀，第二位为 3-9。

        :param mobile: 待校验的字符串
        :return: 是否为合法手机号

        ::

            >>> CheckUtil.is_mobile('13800138000')
            True
            >>> CheckUtil.is_mobile('+8613800138000')
            True
            >>> CheckUtil.is_mobile('12345678901')
            False
        """
        if not mobile:
            return False
        return bool(CheckUtil._RE_MOBILE.match(mobile))

    @staticmethod
    def is_plate_number(plate_number: str) -> bool:
        """
        校验是否为中国车牌号（含新能源车牌）。

        :param plate_number: 待校验的字符串
        :return: 是否为合法车牌号

        ::

            >>> CheckUtil.is_plate_number('京A12345')
            True
            >>> CheckUtil.is_plate_number('沪AF12345')
            True
            >>> CheckUtil.is_plate_number('invalid')
            False
        """
        if not plate_number:
            return False
        return bool(CheckUtil._RE_PLATE_NUMBER.match(plate_number))

    @staticmethod
    def is_car_vin(vin: str) -> bool:
        """
        校验是否为合法的车辆识别码（VIN）。

        :param vin: 待校验的字符串
        :return: 是否为合法 VIN

        ::

            >>> CheckUtil.is_car_vin('LSVCA2A49GN202573')
            True
            >>> CheckUtil.is_car_vin('invalid')
            False
        """
        if not vin:
            return False
        return bool(CheckUtil._RE_CAR_VIN.match(vin))

    @staticmethod
    def is_car_driving_licence(licence: str) -> bool:
        """
        校验是否为合法的驾驶证号（12 位数字）。

        :param licence: 待校验的字符串
        :return: 是否为合法驾驶证号

        ::

            >>> CheckUtil.is_car_driving_licence('123456789012')
            True
            >>> CheckUtil.is_car_driving_licence('123')
            False
        """
        if not licence:
            return False
        return bool(CheckUtil._RE_CAR_DRIVING_LICENCE.match(licence))

    @staticmethod
    def is_birthday(birthday: str) -> bool:
        """
        校验是否为合法的生日日期。

        支持多种分隔符：``-``、``/``、``.``、``年月日``。

        :param birthday: 待校验的字符串
        :return: 是否为合法生日

        ::

            >>> CheckUtil.is_birthday('2000-01-15')
            True
            >>> CheckUtil.is_birthday('2000年01月15日')
            True
            >>> CheckUtil.is_birthday('2000-13-01')
            False
        """
        if not birthday:
            return False
        m = CheckUtil._RE_BIRTHDAY.match(birthday)
        if not m:
            return False
        year = int(m.group(1))
        month = int(m.group(3))
        day = int(m.group(5))
        if not (1 <= month <= 12):
            return False
        import calendar as _cal

        _, max_day = _cal.monthrange(year, month)
        return 1 <= day <= max_day

    @staticmethod
    def is_chinese_name(name: str) -> bool:
        """
        校验是否为合法的中文姓名（2-60 个汉字，含 ``·``）。

        :param name: 待校验的字符串
        :return: 是否为合法中文姓名

        ::

            >>> CheckUtil.is_chinese_name('张三')
            True
            >>> CheckUtil.is_chinese_name('迪丽热巴·迪力木拉提')
            True
            >>> CheckUtil.is_chinese_name('张')
            False
        """
        if not name:
            return False
        return bool(CheckUtil._RE_CHINESE_NAME.match(name))

    @staticmethod
    def is_credit_code(credit_code: str) -> bool:
        """
        校验是否为合法的统一社会信用代码。

        :param credit_code: 待校验的字符串
        :return: 是否为合法信用代码

        ::

            >>> CheckUtil.is_credit_code('91350100M000100Y43')
            True
            >>> CheckUtil.is_credit_code('invalid')
            False
        """
        if not credit_code:
            return False
        return bool(CheckUtil._RE_CREDIT_CODE.match(credit_code))

    @staticmethod
    def is_citizen_id(id_card: str) -> bool:
        """
        校验是否为合法的 18 位居民身份证号（含校验码验证）。

        :param id_card: 待校验的字符串
        :return: 是否为合法身份证号

        ::

            >>> CheckUtil.is_citizen_id('11010519491231002X')
            True
            >>> CheckUtil.is_citizen_id('123456789012345678')
            False
        """
        if not id_card:
            return False
        if not CheckUtil._RE_CITIZEN_ID.match(id_card):
            return False
        # 校验码验证
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = "10X98765432"
        body = id_card[:17]
        try:
            total = sum(int(body[i]) * weights[i] for i in range(17))
        except (ValueError, IndexError):
            return False
        expected = check_codes[total % 11]
        return id_card[17].upper() == expected

    @staticmethod
    def is_money(money: str) -> bool:
        """
        校验是否为合法的金额格式（正整数或正小数）。

        :param money: 待校验的字符串
        :return: 是否为合法金额

        ::

            >>> CheckUtil.is_money('100')
            True
            >>> CheckUtil.is_money('99.99')
            True
            >>> CheckUtil.is_money('-10')
            False
        """
        if not money:
            return False
        return bool(CheckUtil._RE_MONEY.match(money))

    @staticmethod
    def is_general(value: str) -> bool:
        """
        校验是否为通用字符串（字母、数字、下划线，即 ``\\w+``）。

        :param value: 待校验的字符串
        :return: 是否为通用字符串

        ::

            >>> CheckUtil.is_general('hello_123')
            True
            >>> CheckUtil.is_general('hello 123')
            False
        """
        if not value:
            return False
        return bool(CheckUtil._RE_GENERAL.match(value))

    @staticmethod
    def is_general_with_chinese(value: str) -> bool:
        """
        校验是否为含中文的通用字符串（中文、字母、数字、下划线）。

        :param value: 待校验的字符串
        :return: 是否为含中文通用字符串

        ::

            >>> CheckUtil.is_general_with_chinese('你好abc_123')
            True
            >>> CheckUtil.is_general_with_chinese('hello 你好')
            False
        """
        if not value:
            return False
        return bool(CheckUtil._RE_GENERAL_WITH_CHINESE.match(value))

    @staticmethod
    def is_word(value: str) -> bool:
        """
        校验是否全部由英文字母组成（不含数字和符号）。

        :param value: 待校验的字符串
        :return: 是否全部为字母

        ::

            >>> CheckUtil.is_word('Hello')
            True
            >>> CheckUtil.is_word('Hello123')
            False
        """
        if not value:
            return False
        return bool(CheckUtil._RE_WORD.match(value))

    @staticmethod
    def is_hex(value: str) -> bool:
        """
        校验是否为合法的十六进制字符串。

        :param value: 待校验的字符串
        :return: 是否为十六进制字符串

        ::

            >>> CheckUtil.is_hex('0A1B2C')
            True
            >>> CheckUtil.is_hex('GHI')
            False
        """
        if not value:
            return False
        return bool(CheckUtil._RE_HEX.match(value))

    @staticmethod
    def is_letter(value: str) -> bool:
        """
        校验是否全部由英文字母组成。

        与 :meth:`is_word` 等价。

        :param value: 待校验的字符串
        :return: 是否全部为字母

        ::

            >>> CheckUtil.is_letter('abc')
            True
            >>> CheckUtil.is_letter('abc123')
            False
        """
        if not value:
            return False
        return bool(CheckUtil._RE_LETTER.match(value))

    @staticmethod
    def is_number(value: str) -> bool:
        """
        校验是否全部由数字组成。

        :param value: 待校验的字符串
        :return: 是否全部为数字

        ::

            >>> CheckUtil.is_number('12345')
            True
            >>> CheckUtil.is_number('123a')
            False
        """
        if not value:
            return False
        return bool(CheckUtil._RE_NUMBER.match(value))

    @staticmethod
    def is_zip_code(zip_code: str) -> bool:
        """
        校验是否为中国邮政编码（6 位数字）。

        与 :meth:`is_post_code` 等价。

        :param zip_code: 待校验的字符串
        :return: 是否为合法邮编

        ::

            >>> CheckUtil.is_zip_code('100000')
            True
            >>> CheckUtil.is_zip_code('1234')
            False
        """
        if not zip_code:
            return False
        return bool(CheckUtil._RE_ZIP_CODE.match(zip_code))

    @staticmethod
    def is_between(value: Any, min_val: Any, max_val: Any) -> bool:
        """
        校验值是否在指定范围内（包含边界）。

        支持数值、字符串、日期等可比较类型。

        :param value: 待校验的值
        :param min_val: 最小值
        :param max_val: 最大值
        :return: 是否在范围内

        ::

            >>> CheckUtil.is_between(5, 1, 10)
            True
            >>> CheckUtil.is_between('c', 'a', 'z')
            True
            >>> CheckUtil.is_between(0, 1, 10)
            False
        """
        if value is None:
            return False
        try:
            return min_val <= value <= max_val
        except TypeError:
            return False

    @staticmethod
    def has_chinese(value: str) -> bool:
        """
        判断字符串中是否包含中文字符。

        与 :meth:`is_chinese` （全部为中文）不同，此方法检测是否包含。

        :param value: 待检测的字符串
        :return: 是否包含中文

        ::

            >>> CheckUtil.has_chinese('hello你好')
            True
            >>> CheckUtil.has_chinese('hello')
            False
        """
        if not value:
            return False
        return bool(CheckUtil._RE_HAS_CHINESE.search(value))

    @staticmethod
    def has_number(value: str) -> bool:
        """
        判断字符串中是否包含数字。

        :param value: 待检测的字符串
        :return: 是否包含数字

        ::

            >>> CheckUtil.has_number('hello123')
            True
            >>> CheckUtil.has_number('hello')
            False
        """
        if not value:
            return False
        return bool(CheckUtil._RE_HAS_NUMBER.search(value))

    @staticmethod
    def is_null(obj: Any) -> bool:
        """
        判断对象是否为 ``None``。

        :param obj: 待判断的对象
        :return: 是否为 None

        ::

            >>> CheckUtil.is_null(None)
            True
            >>> CheckUtil.is_null('')
            False
        """
        return obj is None

    @staticmethod
    def is_not_null(obj: Any) -> bool:
        """
        判断对象是否不为 ``None``。

        :param obj: 待判断的对象
        :return: 是否不为 None

        ::

            >>> CheckUtil.is_not_null('hello')
            True
            >>> CheckUtil.is_not_null(None)
            False
        """
        return obj is not None

    @staticmethod
    def is_empty(value: Any) -> bool:
        """
        判断值是否为空（``None``、空字符串、空集合、空字典）。

        :param value: 待判断的值
        :return: 是否为空

        ::

            >>> CheckUtil.is_empty(None)
            True
            >>> CheckUtil.is_empty('')
            True
            >>> CheckUtil.is_empty([])
            True
            >>> CheckUtil.is_empty('hello')
            False
        """
        if value is None:
            return True
        if isinstance(value, (str, list, tuple, set, dict, frozenset)):
            return len(value) == 0
        return False

    @staticmethod
    def is_not_empty(value: Any) -> bool:
        """
        判断值是否非空。

        :param value: 待判断的值
        :return: 是否非空

        ::

            >>> CheckUtil.is_not_empty('hello')
            True
            >>> CheckUtil.is_not_empty('')
            False
        """
        return not CheckUtil.is_empty(value)

    @staticmethod
    def is_true_bool(value: Any) -> bool:
        """
        判断值是否为 ``True``。

        :param value: 待判断的值
        :return: 是否为 True

        ::

            >>> CheckUtil.is_true_bool(True)
            True
            >>> CheckUtil.is_true_bool(1)
            False
        """
        return value is True

    @staticmethod
    def is_false_bool(value: Any) -> bool:
        """
        判断值是否为 ``False``。

        :param value: 待判断的值
        :return: 是否为 False

        ::

            >>> CheckUtil.is_false_bool(False)
            True
            >>> CheckUtil.is_false_bool(0)
            False
        """
        return value is False

    # ================================================================== #
    #  validate_* 校验方法（失败抛出 ValidateException）
    # ================================================================== #

    @staticmethod
    def validate_match_regex(value: str, regex: str, error_msg: Optional[str] = None) -> None:
        """
        校验值是否匹配指定的正则表达式，失败抛出异常。

        :param value: 待校验的值
        :param regex: 正则表达式
        :param error_msg: 自定义错误消息
        :raises ValidateException: 正则不匹配时抛出
        """
        if not re.match(regex, str(value) if value is not None else ""):
            raise ValidateException(error_msg or "Value [{}] does not match regex [{}]", value, regex)

    @staticmethod
    def validate_mac(mac: str, error_msg: Optional[str] = None) -> None:
        """
        校验 MAC 地址，失败抛出异常。

        :param mac: 待校验的字符串
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_mac(mac):
            raise ValidateException(error_msg or "Invalid MAC address: [{}]", mac)

    @staticmethod
    def check_index_limit(index: int, size: int) -> int:
        """
        校验索引是否在合法范围内（``0 <= index < size``）。

        :param index: 索引值
        :param size: 集合大小
        :return: 校验通过的索引值
        :raises ValidateException: 索引越界时抛出

        ::

            >>> CheckUtil.check_index_limit(2, 5)
            2
        """
        if index < 0 or index >= size:
            raise ValidateException("Index [{}] is out of range [0, {})", index, size)
        return index

    @staticmethod
    def validate_email(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验邮箱地址，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_email(value):
            raise ValidateException(error_msg or "Invalid email: [{}]", value)

    @staticmethod
    def validate_ipv4(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验 IPv4 地址，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_ipv4(value):
            raise ValidateException(error_msg or "Invalid IPv4: [{}]", value)

    @staticmethod
    def validate_ipv6(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验 IPv6 地址，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_ipv6(value):
            raise ValidateException(error_msg or "Invalid IPv6: [{}]", value)

    @staticmethod
    def validate_url(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验 URL，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_url(value):
            raise ValidateException(error_msg or "Invalid URL: [{}]", value)

    @staticmethod
    def validate_uuid(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验 UUID，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_uuid(value):
            raise ValidateException(error_msg or "Invalid UUID: [{}]", value)

    @staticmethod
    def validate_mobile(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验手机号，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_mobile(value):
            raise ValidateException(error_msg or "Invalid mobile number: [{}]", value)

    @staticmethod
    def validate_plate_number(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验车牌号，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_plate_number(value):
            raise ValidateException(error_msg or "Invalid plate number: [{}]", value)

    @staticmethod
    def validate_car_vin(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验车辆识别码（VIN），失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_car_vin(value):
            raise ValidateException(error_msg or "Invalid car VIN: [{}]", value)

    @staticmethod
    def validate_car_driving_licence(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验驾驶证号，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_car_driving_licence(value):
            raise ValidateException(error_msg or "Invalid car driving licence: [{}]", value)

    @staticmethod
    def validate_birthday(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验生日日期，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_birthday(value):
            raise ValidateException(error_msg or "Invalid birthday: [{}]", value)

    @staticmethod
    def validate_chinese(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验是否全部为中文字符，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_chinese(value):
            raise ValidateException(error_msg or "Value is not all Chinese: [{}]", value)

    @staticmethod
    def validate_chinese_name(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验中文姓名，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_chinese_name(value):
            raise ValidateException(error_msg or "Invalid Chinese name: [{}]", value)

    @staticmethod
    def validate_credit_code(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验统一社会信用代码，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_credit_code(value):
            raise ValidateException(error_msg or "Invalid credit code: [{}]", value)

    @staticmethod
    def validate_citizen_id_number(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验身份证号，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_citizen_id(value):
            raise ValidateException(error_msg or "Invalid citizen ID number: [{}]", value)

    @staticmethod
    def validate_money(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验金额格式，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_money(value):
            raise ValidateException(error_msg or "Invalid money format: [{}]", value)

    @staticmethod
    def validate_general(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验通用字符串（``\\w+``），失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_general(value):
            raise ValidateException(error_msg or "Invalid general string: [{}]", value)

    @staticmethod
    def validate_general_with_chinese(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验含中文通用字符串，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_general_with_chinese(value):
            raise ValidateException(error_msg or "Invalid general string with Chinese: [{}]", value)

    @staticmethod
    def validate_word(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验是否全部为字母，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_word(value):
            raise ValidateException(error_msg or "Value is not all letters: [{}]", value)

    @staticmethod
    def validate_hex(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验十六进制字符串，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_hex(value):
            raise ValidateException(error_msg or "Invalid hex string: [{}]", value)

    @staticmethod
    def validate_letter(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验是否全部为字母，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_letter(value):
            raise ValidateException(error_msg or "Value is not all letters: [{}]", value)

    @staticmethod
    def validate_number(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验是否全部为数字，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_number(value):
            raise ValidateException(error_msg or "Value is not all digits: [{}]", value)

    @staticmethod
    def validate_zip_code(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验邮编，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_zip_code(value):
            raise ValidateException(error_msg or "Invalid zip code: [{}]", value)

    @staticmethod
    def validate_between(value: Any, min_val: Any, max_val: Any, error_msg: Optional[str] = None) -> None:
        """
        校验值是否在范围内，失败抛出异常。

        :param value: 待校验的值
        :param min_val: 最小值
        :param max_val: 最大值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_between(value, min_val, max_val):
            raise ValidateException(error_msg or "Value [{}] is not between [{}] and [{}]", value, min_val, max_val)

    @staticmethod
    def validate_not_empty(value: Any, error_msg: Optional[str] = None) -> None:
        """
        校验值是否非空，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if CheckUtil.is_empty(value):
            raise ValidateException(error_msg or "Value must not be empty")

    @staticmethod
    def validate_not_null(value: Any, error_msg: Optional[str] = None) -> None:
        """
        校验值是否非 ``None``，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if CheckUtil.is_null(value):
            raise ValidateException(error_msg or "Value must not be null")

    @staticmethod
    def validate_null(value: Any, error_msg: Optional[str] = None) -> None:
        """
        校验值是否为 ``None``，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_null(value):
            raise ValidateException(error_msg or "Value must be null, but got [{}]", value)

    @staticmethod
    def validate_empty(value: Any, error_msg: Optional[str] = None) -> None:
        """
        校验值是否为空，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_empty(value):
            raise ValidateException(error_msg or "Value must be empty, but got [{}]", value)

    @staticmethod
    def validate_true(value: Any, error_msg: Optional[str] = None) -> None:
        """
        校验值是否为 ``True``，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_true_bool(value):
            raise ValidateException(error_msg or "Value must be True, but got [{}]", value)

    @staticmethod
    def validate_false(value: Any, error_msg: Optional[str] = None) -> None:
        """
        校验值是否为 ``False``，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not CheckUtil.is_false_bool(value):
            raise ValidateException(error_msg or "Value must be False, but got [{}]", value)

    @staticmethod
    def validate_equal(obj1: Any, obj2: Any, error_msg: Optional[str] = None) -> None:
        """
        校验两个对象是否相等，失败抛出异常。

        :param obj1: 第一个对象
        :param obj2: 第二个对象
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not ObjectUtil.equals(obj1, obj2):
            raise ValidateException(error_msg or "Values not equal: [{}] and [{}]", obj1, obj2)

    @staticmethod
    def validate_not_equal(obj1: Any, obj2: Any, error_msg: Optional[str] = None) -> None:
        """
        校验两个对象是否不相等，失败抛出异常。

        :param obj1: 第一个对象
        :param obj2: 第二个对象
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if ObjectUtil.equals(obj1, obj2):
            raise ValidateException(error_msg or "Values must not be equal: [{}]", obj1)

    @staticmethod
    def validate_not_empty_and_equal(value: Any, obj: Any, error_msg: Optional[str] = None) -> None:
        """
        校验值非空且与指定对象相等，失败抛出异常。

        :param value: 待校验的值
        :param obj: 期望相等的对象
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        CheckUtil.validate_not_empty(value, error_msg)
        CheckUtil.validate_equal(value, obj, error_msg)

    @staticmethod
    def validate_not_empty_and_not_equal(value: Any, obj: Any, error_msg: Optional[str] = None) -> None:
        """
        校验值非空且与指定对象不相等，失败抛出异常。

        :param value: 待校验的值
        :param obj: 期望不相等的对象
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        CheckUtil.validate_not_empty(value, error_msg)
        CheckUtil.validate_not_equal(value, obj, error_msg)

    @staticmethod
    def validate_upper_case(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验字符串是否全部为大写，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not value or not value.isupper():
            raise ValidateException(error_msg or "Value must be upper case: [{}]", value)

    @staticmethod
    def validate_lower_case(value: str, error_msg: Optional[str] = None) -> None:
        """
        校验字符串是否全部为小写，失败抛出异常。

        :param value: 待校验的值
        :param error_msg: 自定义错误消息
        :raises ValidateException: 校验失败时抛出
        """
        if not value or not value.islower():
            raise ValidateException(error_msg or "Value must be lower case: [{}]", value)

    @staticmethod
    def is_phone_number(value: str) -> bool:
        """验证手机号（严格正则，别名 is_mobile）。

        :param value: 手机号字符串
        :return: 是否为有效手机号
        """
        return CheckUtil.is_mobile(value)

    @staticmethod
    def is_bank_card(card_no: str) -> bool:
        """验证银行卡号（Luhn 算法）。

        银行卡号长度通常为 16-19 位，使用 Luhn 算法校验。

        :param card_no: 银行卡号
        :return: 是否为有效银行卡号

        ::

            CheckUtil.is_bank_card("6222020200011111111") -> bool
        """
        if not card_no or not card_no.isdigit():
            return False
        if len(card_no) < 13 or len(card_no) > 19:
            return False
        # Luhn 算法
        digits = [int(d) for d in card_no]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits)
        for d in even_digits:
            total += sum(divmod(d * 2, 10))
        return total % 10 == 0

    @staticmethod
    def is_date(value: str) -> bool:
        """验证日期格式。

        支持格式：YYYY-MM-DD、YYYY/MM/DD、YYYYMMDD、YYYY.MM.DD。

        :param value: 日期字符串
        :return: 是否为有效日期格式
        """
        import re
        from datetime import datetime

        patterns = [
            (r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}$", ["%Y-%m-%d", "%Y/%m/%d"]),
            (r"^\d{4}\.\d{1,2}\.\d{1,2}$", ["%Y.%m.%d"]),
            (r"^\d{8}$", ["%Y%m%d"]),
        ]
        for pattern, fmts in patterns:
            if re.match(pattern, value):
                for fmt in fmts:
                    try:
                        datetime.strptime(value, fmt)
                        return True
                    except ValueError:
                        continue
        return False

    @staticmethod
    def is_ip(value: str) -> bool:
        """验证 IP 地址（兼容 IPv4/IPv6）。

        :param value: IP 地址字符串
        :return: 是否为有效 IP 地址
        """
        return CheckUtil.is_ipv4(value) or CheckUtil.is_ipv6(value)

    @staticmethod
    def is_unicode(value: str) -> bool:
        """验证字符串是否为有效的 Unicode 字符串。

        Python 3 的 str 本身就是 Unicode，此方法检查字符串是否包含
        有效的 Unicode 字符（无代理对等非法字符）。

        :param value: 字符串
        :return: 是否为有效 Unicode 字符串
        """
        if value is None:
            return False
        try:
            value.encode("utf-8")
            return True
        except (UnicodeEncodeError, UnicodeDecodeError):
            return False

    @staticmethod
    def dpd_check_digit(digits: str) -> str:
        """计算 DPD 包裹单校验位。

        DPD 校验算法：从右到左，偶数位乘 3，奇数位乘 1，求和后取模 10。

        :param digits: 14 位数字
        :return: 校验位字符串（1 位数字）
        :raises ValueError: 输入不合法时

        ::

            digit = CheckUtil.dpd_check_digit("01234567890123")
        """
        if not digits or not digits.isdigit():
            raise ValueError("输入必须为纯数字字符串")
        weights = [3, 1] * (len(digits) // 2 + 1)
        total = 0
        for i, ch in enumerate(reversed(digits)):
            total += int(ch) * weights[i]
        check = (10 - (total % 10)) % 10
        return str(check)
