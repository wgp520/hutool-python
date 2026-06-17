"""
类型转换工具类

提供 bytes↔int、通用类型转换、中英文数字互转、全角半角互转等常用类型转换方法。
"""

from typing import Any, Optional


class ConvertUtil:
    """类型转换工具类。

    提供 ``bytes_to_int``、``int_to_bytes``、``to_str``、``convert``、
    ``number_to_chinese``、``digit_to_chinese``、``chinese_to_number``、
    ``number_to_word``、``chinese_money_to_number``、``number_to_simple``、
    ``to_sbc``、``to_dbc`` 等常用类型转换方法。
    """

    @staticmethod
    def bytes_to_int(data: bytes) -> int:
        """
        将 bytes 按大端序转换为 int。

        :param data: 字节数据
        :return: 转换后的整数

        ::

            >>> ConvertUtil.bytes_to_int(b'\\x00\\x00\\x01\\x00')
            256
            >>> ConvertUtil.bytes_to_int(b'\\xff')
            255
        """
        return int.from_bytes(data, byteorder="big", signed=False)

    @staticmethod
    def int_to_bytes(value: int, length: int = 4) -> bytes:
        """
        将 int 按大端序转换为指定长度的 bytes。

        :param value: 整数值（非负）
        :param length: 输出 bytes 的长度（字节数），默认 4
        :return: 字节数据
        :raises ValueError: value 为负数时

        ::

            >>> ConvertUtil.int_to_bytes(256, 2)
            b'\\x01\\x00'
            >>> ConvertUtil.int_to_bytes(0, 1)
            b'\\x00'
        """
        if value < 0:
            raise ValueError("value 必须为非负整数")
        return value.to_bytes(length, byteorder="big", signed=False)

    @staticmethod
    def to_str(value: Any, encoding: str = "utf-8") -> str:
        """
        安全地将值转换为字符串。

        ``bytes``/``bytearray`` 类型使用 *encoding* 解码，其他类型使用 ``str()`` 转换。

        :param value: 待转换的值
        :param encoding: 字节解码编码，默认 ``"utf-8"``
        :return: 字符串

        ::

            >>> ConvertUtil.to_str(b'hello')
            'hello'
            >>> ConvertUtil.to_str(123)
            '123'
            >>> ConvertUtil.to_str(None)
            ''
        """
        if value is None:
            return ""
        if isinstance(value, (bytes, bytearray)):
            return value.decode(encoding)
        return str(value)

    @staticmethod
    def convert(value: Any, target_type: type) -> Any:
        """
        将值转换为指定类型。

        支持常见类型：``int``、``float``、``str``、``bool``、``list``、``tuple``、``set``。
        ``None`` 输入返回 ``target_type()`` 的默认值。

        :param value: 待转换的值
        :param target_type: 目标类型
        :return: 转换后的值
        :raises ValueError: 无法转换时

        ::

            >>> ConvertUtil.convert('123', int)
            123
            >>> ConvertUtil.convert(3.14, str)
            '3.14'
            >>> ConvertUtil.convert(None, str)
            ''
        """
        if value is None:
            if target_type in (int, float):
                return target_type(0)
            return target_type()
        if isinstance(value, target_type):
            return value
        return target_type(value)

    # ------------------------------------------------------------------
    # 中文 / 数字 / 金额 转换
    # ------------------------------------------------------------------

    _SIMPLE_DIGITS = "零一二三四五六七八九"
    _FORMAL_DIGITS = "零壹贰叁肆伍陆柒捌玖"

    @staticmethod
    def number_to_chinese(number: float) -> str:
        """
        将数字转换为中文小写数字（一二三……）。

        支持负数和小数，整数部分逐位转换，小数部分逐位读出。

        :param number: 待转换的数字
        :return: 中文小写数字字符串

        ::

            >>> ConvertUtil.number_to_chinese(123)
            '一百二十三'
            >>> ConvertUtil.number_to_chinese(-5)
            '负五'
            >>> ConvertUtil.number_to_chinese(3.14)
            '三点一四'
        """
        return ConvertUtil._number_to_chinese_impl(number, ConvertUtil._SIMPLE_DIGITS)

    @staticmethod
    def digit_to_chinese(number: float) -> str:
        """
        将数字转换为中文大写数字（壹贰叁……）。

        支持负数和小数，整数部分逐位转换，小数部分逐位读出。

        :param number: 待转换的数字
        :return: 中文大写数字字符串

        ::

            >>> ConvertUtil.digit_to_chinese(123)
            '壹佰贰拾叁'
            >>> ConvertUtil.digit_to_chinese(-5)
            '负伍'
        """
        return ConvertUtil._number_to_chinese_impl(number, ConvertUtil._FORMAL_DIGITS)

    # -- internal helpers --------------------------------------------------

    @staticmethod
    def _number_to_chinese_impl(number: float, digits: str) -> str:
        """内部实现：根据 *digits* 映射表将数字转为中文。"""
        if number < 0:
            return "负" + ConvertUtil._number_to_chinese_impl(-number, digits)

        # 分离整数和小数部分
        str_num = str(number)
        if "." in str_num:
            int_part, dec_part = str_num.split(".", 1)
        else:
            int_part, dec_part = str_num, ""

        int_val = int(int_part)

        # 中文单位
        units_simple = ["", "十", "百", "千"]
        units_formal = ["", "拾", "佰", "仟"]
        units = units_formal if digits is ConvertUtil._FORMAL_DIGITS else units_simple
        big_units_simple = ["", "万", "亿"]
        big_units_formal = ["", "萬", "億"]
        big_units = big_units_formal if digits is ConvertUtil._FORMAL_DIGITS else big_units_simple

        if int_val == 0:
            result = digits[0]
        else:
            result = ""
            str_int = str(int_val)
            # 按4位一组分组
            groups: list[str] = []
            while str_int:
                groups.insert(0, str_int[-4:])
                str_int = str_int[:-4]

            for gi, group in enumerate(groups):
                group_str = ""
                has_nonzero = False
                zero_buf = False
                for ci, ch in enumerate(group):
                    d = int(ch)
                    pos = len(group) - 1 - ci  # 位权索引
                    if d == 0:
                        zero_buf = True
                    else:
                        if zero_buf:
                            group_str += digits[0]
                            zero_buf = False
                        group_str += digits[d] + units[pos]
                        has_nonzero = True
                if has_nonzero:
                    big_idx = len(groups) - 1 - gi
                    group_str += big_units[big_idx]
                    result += group_str

            # 避免"一十"开头时多余的"一"
            if digits is ConvertUtil._SIMPLE_DIGITS and result.startswith("一十"):
                result = result[1:]

        # 小数部分
        if dec_part:
            result += "点"
            for ch in dec_part:
                result += digits[int(ch)]

        return result

    @staticmethod
    def chinese_to_number(chinese_str: str) -> float:
        """
        将中文数字字符串转回阿拉伯数字。

        同时支持小写（一二三……）和大写（壹贰叁……）中文数字。

        :param chinese_str: 中文数字字符串
        :return: 对应的数字

        ::

            >>> ConvertUtil.chinese_to_number('一百二十三')
            123
            >>> ConvertUtil.chinese_to_number('壹佰贰拾叁')
            123
            >>> ConvertUtil.chinese_to_number('负五')
            -5
            >>> ConvertUtil.chinese_to_number('三点一四')
            3.14
        """
        if not chinese_str:
            raise ValueError("输入不能为空")

        negative = False
        s = chinese_str
        if s.startswith("负"):
            negative = True
            s = s[1:]

        # 构建字符到数字的映射
        char_map: dict[str, int] = {}
        for i, ch in enumerate(ConvertUtil._SIMPLE_DIGITS):
            char_map[ch] = i
        for i, ch in enumerate(ConvertUtil._FORMAL_DIGITS):
            char_map[ch] = i

        # 单位映射
        unit_map: dict[str, int] = {
            "十": 10,
            "拾": 10,
            "百": 100,
            "佰": 100,
            "千": 1000,
            "仟": 1000,
            "万": 10000,
            "萬": 10000,
            "亿": 100000000,
            "億": 100000000,
        }

        if "点" in s:
            int_part, dec_part = s.split("点", 1)
        else:
            int_part, dec_part = s, ""

        # 解析整数部分
        current = 0
        section = 0

        for ch in int_part:
            if ch in char_map:
                current = char_map[ch]
            elif ch in unit_map:
                u = unit_map[ch]
                if u >= 10000:
                    # 万 / 亿：先累加 current 到 section，再乘大单位
                    section = (section + current) * u
                    current = 0
                else:
                    section += current * u if current else u
                    current = 0
            else:
                raise ValueError(f"无法识别的字符: {ch}")

        int_val = section + current
        if int_val == 0 and int_part and all(ch in unit_map for ch in int_part):
            # 纯单位情况（如 "十万"），section 已正确计算
            int_val = section

        # 解析小数部分
        dec_val = 0.0
        if dec_part:
            dec_str = ""
            for ch in dec_part:
                if ch in char_map:
                    dec_str += str(char_map[ch])
                else:
                    raise ValueError(f"小数部分包含无法识别的字符: {ch}")
            dec_val = float("0." + dec_str)

        result = int_val + dec_val
        return -result if negative else result

    # ------------------------------------------------------------------
    # 英文数字 / 金额
    # ------------------------------------------------------------------

    _ONES = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
    ]
    _TENS = [
        "",
        "",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety",
    ]

    @staticmethod
    def number_to_word(number: int) -> str:
        """
        将非负整数（0–9999）转换为英文单词。

        :param number: 0 到 9999 之间的整数
        :return: 英文单词
        :raises ValueError: 超出支持范围或为负数时

        ::

            >>> ConvertUtil.number_to_word(0)
            'zero'
            >>> ConvertUtil.number_to_word(123)
            'one hundred twenty-three'
            >>> ConvertUtil.number_to_word(2024)
            'two thousand twenty-four'
        """
        if not isinstance(number, int) or number < 0:
            raise ValueError("仅支持非负整数")
        if number > 9999:
            raise ValueError("仅支持 0-9999 范围的数字")

        if number < 20:
            return ConvertUtil._ONES[number]

        if number < 100:
            t, o = divmod(number, 10)
            return ConvertUtil._TENS[t] + (f"-{ConvertUtil._ONES[o]}" if o else "")

        if number < 1000:
            h, rem = divmod(number, 100)
            word = f"{ConvertUtil._ONES[h]} hundred"
            if rem:
                word += f" {ConvertUtil.number_to_word(rem)}"
            return word

        # 1000–9999
        th, rem = divmod(number, 1000)
        word = f"{ConvertUtil._ONES[th]} thousand"
        if rem:
            word += f" {ConvertUtil.number_to_word(rem)}"
        return word

    @staticmethod
    def chinese_money_to_number(money_str: str) -> int:
        """
        将中文金额字符串转换为整数。

        支持小写（零一二三四五六七八九十百千万亿）和大写
        （零壹贰叁肆伍陆柒捌玖拾佰仟萬億）。

        :param money_str: 中文金额字符串
        :return: 对应的整数

        ::

            >>> ConvertUtil.chinese_money_to_number('壹佰贰拾叁')
            123
            >>> ConvertUtil.chinese_money_to_number('一万二千三百四十五')
            12345
            >>> ConvertUtil.chinese_money_to_number('叁萬伍仟')
            35000
        """
        if not money_str:
            raise ValueError("输入不能为空")
        return int(ConvertUtil.chinese_to_number(money_str))

    # ------------------------------------------------------------------
    # 数字缩写 / 全角半角
    # ------------------------------------------------------------------

    @staticmethod
    def number_to_simple(number: float, precision: int = 1) -> str:
        """
        将大数字缩写为带单位的简短形式。

        支持 K（千）、M（百万）、B（十亿）。

        :param number: 待缩写的数字
        :param precision: 小数精度，默认 1
        :return: 缩写后的字符串

        ::

            >>> ConvertUtil.number_to_simple(1234)
            '1.2K'
            >>> ConvertUtil.number_to_simple(3400000)
            '3.4M'
            >>> ConvertUtil.number_to_simple(5600000000)
            '5.6B'
            >>> ConvertUtil.number_to_simple(42)
            '42'
        """
        abs_num = abs(number)
        sign = "-" if number < 0 else ""

        if abs_num >= 1_000_000_000:
            value = abs_num / 1_000_000_000
            suffix = "B"
        elif abs_num >= 1_000_000:
            value = abs_num / 1_000_000
            suffix = "M"
        elif abs_num >= 1_000:
            value = abs_num / 1_000
            suffix = "K"
        else:
            # 小于 1000 直接返回
            if isinstance(number, int) or number == int(number):
                return f"{sign}{int(abs_num)}"
            return f"{sign}{abs_num}"

        rounded = round(value, precision)
        # 如果四舍五入后刚好进位到整数（如 999.95K → 1000.0K），保留一位小数
        formatted = f"{rounded:.{precision}f}"
        # 去掉末尾多余的零，但保留至少一位小数
        if "." in formatted:
            formatted = formatted.rstrip("0").rstrip(".")
            if "." not in formatted:
                formatted += ".0" if precision > 0 else ""
        return f"{sign}{formatted}{suffix}"

    @staticmethod
    def to_sbc(s: str) -> str:
        """
        将半角字符转换为全角字符。

        ASCII 可见字符 ``0x21–0x7E`` 映射为 ``0xFF01–0xFF5E``，
        空格 ``0x20`` 映射为 ``0x3000``。

        :param s: 输入字符串
        :return: 全角字符串

        ::

            >>> ConvertUtil.to_sbc('ABC')
            'ＡＢＣ'
            >>> ConvertUtil.to_sbc('123')
            '１２３'
            >>> ConvertUtil.to_sbc(' ')
            '　'
        """
        result: list[str] = []
        for ch in s:
            code = ord(ch)
            if code == 0x20:
                result.append("　")
            elif 0x21 <= code <= 0x7E:
                result.append(chr(code + 0xFEE0))
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def to_dbc(s: str) -> str:
        """
        将全角字符转换为半角字符。

        ``0xFF01–0xFF5E`` 映射为 ASCII ``0x21–0x7E``，
        ``0x3000``（全角空格）映射为普通空格 ``0x20``。

        :param s: 输入字符串
        :return: 半角字符串

        ::

            >>> ConvertUtil.to_dbc('ＡＢＣ')
            'ABC'
            >>> ConvertUtil.to_dbc('１２３')
            '123'
            >>> ConvertUtil.to_dbc('　')
            ' '
        """
        result: list[str] = []
        for ch in s:
            code = ord(ch)
            if code == 0x3000:
                result.append(" ")
            elif 0xFF01 <= code <= 0xFF5E:
                result.append(chr(code - 0xFEE0))
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def dict_to_tabular(data: dict, headers: Optional[list] = None) -> list:
        """将 dict of dict 转换为二维列表（表格形式）。

        :param data: 字典的字典，如 ``{"row1": {"a": 1, "b": 2}, "row2": {"a": 3, "b": 4}}``
        :param headers: 表头列表，为 None 时自动从第一个值中提取键
        :return: 二维列表，第一行为表头

        ::

            data = {"r1": {"a": 1, "b": 2}, "r2": {"a": 3, "b": 4}}
            table = ConvertUtil.dict_to_tabular(data)
            assert table[0] == ["a", "b"]
            assert table[1] == [1, 2]
        """
        if not data:
            return []
        first_value = next(iter(data.values()))
        if headers is None:
            headers = list(first_value.keys()) if isinstance(first_value, dict) else ["value"]
        result = [list(headers)]
        for key, value in data.items():
            if isinstance(value, dict):
                row = [value.get(h, "") for h in headers]
            else:
                row = [value]
            result.append(row)
        return result

    @staticmethod
    def list_to_tabular(data: list, headers: Optional[list] = None) -> list:
        """将 list of dict 转换为二维列表（表格形式）。

        :param data: 字典列表
        :param headers: 表头列表，为 None 时自动从第一个 dict 中提取键
        :return: 二维列表，第一行为表头

        ::

            data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
            table = ConvertUtil.list_to_tabular(data)
            assert table[0] == ["name", "age"]
            assert table[1] == ["Alice", 30]
        """
        if not data:
            return []
        first = data[0]
        if headers is None:
            headers = list(first.keys()) if isinstance(first, dict) else ["value"]
        result = [list(headers)]
        for item in data:
            if isinstance(item, dict):
                row = [item.get(h, "") for h in headers]
            else:
                row = [item]
            result.append(row)
        return result
