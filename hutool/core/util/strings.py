"""
Java Hutool StrUtil 的 Python 移植版。

包含字符和字符串工具类：CharPool、CharUtil、CharSequenceUtil、StrPool、StrUtil。
"""

import array
import codecs
import re
from difflib import SequenceMatcher
from typing import Any, Callable, List, Optional, Union

__all__ = [
    "CharPool",
    "CharSequenceUtil",
    "CharUtil",
    "StrPool",
    "StrUtil",
]


# ---------------------------------------------------------------------------
# CharPool
# ---------------------------------------------------------------------------
class CharPool:
    """常用字符常量。"""

    # 空字符串 ''
    EMPTY: str = ""
    # 字符常量：空格符 ' '
    SPACE: str = " "
    # 字符常量：制表符 '\t'
    TAB: str = "\t"
    # 字符常量：点 '.'
    DOT: str = "."
    # 字符常量：斜杠 '/'
    SLASH: str = "/"
    # 字符常量：反斜杠 '\\'
    BACKSLASH: str = "\\"
    # 字符常量：回车符 '\r'
    CR: str = "\r"
    # 字符常量：换行符 '\n'
    LF: str = "\n"
    # 字符常量：减号（连接符） '-'
    DASHED: str = "-"
    # 字符常量：下划线 '_'
    UNDERLINE: str = "_"
    # 字符常量：逗号 ','
    COMMA: str = ","
    # 字符常量：花括号（左） '{'
    DELIM_START: str = "{"
    # 字符常量：花括号（右） '}'
    DELIM_END: str = "}"
    # 字符常量：中括号（左） '['
    BRACKET_START: str = "["
    # 字符常量：中括号（右） ']'
    BRACKET_END: str = "]"
    # 字符常量：双引号 '"'
    DOUBLE_QUOTES: str = '"'
    # 字符常量：单引号 '\''
    SINGLE_QUOTE: str = "'"
    # 字符常量：与 '&'
    AMP: str = "&"
    # 字符常量：冒号 ':'
    COLON: str = ":"
    # 字符常量：艾特 '@'
    AT: str = "@"


# ---------------------------------------------------------------------------
# CharUtil
# ---------------------------------------------------------------------------
class CharUtil(CharPool):
    """字符工具类。"""

    @staticmethod
    def is_ascii(ch: str) -> bool:
        """
        判断字符是否为ASCII字符（0~127）。

        :param ch: 待检查的字符
        :return: 是否为ASCII字符
        """
        return ord(ch) < 128

    @staticmethod
    def is_ascii_printable(ch: str) -> bool:
        """
        判断字符是否为可打印ASCII字符（32~126）。

        :param ch: 待检查的字符
        :return: 是否为可打印ASCII字符
        """
        return 32 <= ord(ch) < 127

    @staticmethod
    def is_ascii_control(ch: str) -> bool:
        """
        判断字符是否为ASCII控制字符（0~31和127）。

        :param ch: 待检查的字符
        :return: 是否为控制字符
        """
        ord_ch = ord(ch)
        return ord_ch < 32 or ord_ch == 127

    @staticmethod
    def is_letter(ch: str) -> bool:
        """
        判断字符是否为字母（A~Z或a~z）。

        :param ch: 待检查的字符
        :return: 是否为字母
        """
        return CharUtil.is_letter_upper(ch) or CharUtil.is_letter_lower(ch)

    @staticmethod
    def is_letter_upper(ch: str) -> bool:
        """
        判断字符是否为大写字母（A~Z）。

        :param ch: 待检查的字符
        :return: 是否为大写字母
        """
        return "A" <= ch <= "Z"

    @staticmethod
    def is_letter_lower(ch: str) -> bool:
        """
        判断字符是否为小写字母（a~z）。

        :param ch: 待检查的字符
        :return: 是否为小写字母
        """
        return "a" <= ch <= "z"

    @staticmethod
    def is_number(ch: str) -> bool:
        """
        判断字符是否为数字（0~9）。

        :param ch: 待检查的字符
        :return: 是否为数字
        """
        return "0" <= ch <= "9"

    @staticmethod
    def is_hex_char(ch: str) -> bool:
        """
        判断字符是否为十六进制字符（0~9, a~f, A~F）。

        :param ch: 待检查的字符
        :return: 是否为十六进制字符
        """
        return CharUtil.is_number(ch) or ("a" <= ch <= "f") or ("A" <= ch <= "F")

    @staticmethod
    def is_letter_or_number(ch: str) -> bool:
        """
        判断字符是否为字母或数字（A~Z, a~z, 0~9）。

        :param ch: 待检查的字符
        :return: 是否为字母或数字
        """
        return CharUtil.is_letter(ch) or CharUtil.is_number(ch)

    @staticmethod
    def is_blank_char(ch: str) -> bool:
        """
        判断字符是否为空白字符。
        空白字符包括空格、制表符、全角空格和不间断空格。

        :param ch: 待检查的字符
        :return: 是否为空白字符
        """
        return ch.isspace() or ch == "﻿" or ch == "‪" or ch == "\x00" or ch == "ㅤ" or ch == "⠀" or ch == "᠎"

    @staticmethod
    def is_emoji(ch: str) -> bool:
        """
        判断字符是否为表情符号。

        :param ch: 待检查的字符
        :return: 是否为表情符号
        """
        ord_ch = ord(ch)
        return not (
            ord_ch == 0x0
            or ord_ch == 0x9
            or ord_ch == 0xA
            or ord_ch == 0xD
            or 0x20 <= ord_ch <= 0xD7FF
            or 0xE000 <= ord_ch <= 0xFFFD
            or 0x100000 <= ord_ch <= 0x10FFFF
        )

    @staticmethod
    def is_file_separator(ch: str) -> bool:
        """
        判断字符是否为文件分隔符（'/' 或 '\\'）。

        :param ch: 待检查的字符
        :return: 是否为文件分隔符
        """
        return ch == CharPool.SLASH or ch == CharPool.BACKSLASH

    @staticmethod
    def equals(ch1: str, ch2: str, case_insensitive: bool) -> bool:
        """
        比较两个字符是否相等。

        :param ch1: 第一个字符
        :param ch2: 第二个字符
        :param case_insensitive: 是否忽略大小写
        :return: 两个字符是否相等
        """
        if case_insensitive:
            return ch1.lower() == ch2.lower()
        return ch1 == ch2

    @staticmethod
    def digit16(ch: str) -> str:
        """
        获取字符的十六进制值。

        :param ch: 待转换的字符
        :return: 十六进制字符串表示
        """
        return hex(ord(ch))

    @staticmethod
    def to_close_char(ch: str) -> str:
        """
        将字母或数字转换为带圈字符形式。

        Examples::

            '1' -> '①' (①)
            'A' -> 'Ⓐ' (Ⓐ)
            'a' -> 'ⓐ' (ⓐ)

        如果字符不支持转换，则返回原字符。

        :param ch: 待转换的字符
        :return: 带圈字符，不支持时返回原字符
        """
        result = ord(ch)
        if "1" <= ch <= "9":
            result = ord("①") + result - ord("1")
        elif "A" <= ch <= "Z":
            result = ord("Ⓐ") + result - ord("A")
        elif "a" <= ch <= "z":
            result = ord("ⓐ") + result - ord("a")
        return chr(result)

    @staticmethod
    def to_close_by_number(number: int) -> str:
        """
        将数字（1~20）转换为带圈数字形式。

        Examples::

            1  -> '①' (①)
            12 -> '⑫' (⑫)
            20 -> '⑳' (⑳)

        :param number: 待转换的数字（必须在1~20范围内）
        :return: 带圈数字字符
        :raises ValueError: 数字不在[1, 20]范围内时抛出异常
        """
        if number < 1 or number > 20:
            raise ValueError("Number must be [1-20]")
        return chr(ord("①") + number - 1)


# ---------------------------------------------------------------------------
# CharSequenceUtil
# ---------------------------------------------------------------------------
class CharSequenceUtil:
    """
    CharSequence 工具类，提供常用的字符串操作。
    """

    # ------------------------------------------------------------------
    # Blank / empty checks
    # ------------------------------------------------------------------

    @staticmethod
    def is_blank(string: Optional[str]) -> bool:
        """
        判断字符串是否为空白。当字符串为 None、空字符串（``""``）
        或全部由空白字符组成时，视为空白。

        :param string: 待检查的字符串
        :return: 是否为空白字符串
        """
        if CharSequenceUtil.is_empty(string):
            return True
        for char in string:
            if not CharUtil.is_blank_char(char):
                return False
        return True

    @staticmethod
    def is_not_blank(string: Optional[str]) -> bool:
        """
        判断字符串是否不为空白（与 :meth:`is_blank` 相反）。

        :param string: 待检查的字符串
        :return: 是否不为空白字符串
        """
        return not CharSequenceUtil.is_blank(string)

    @staticmethod
    def has_blank(*strings: Optional[str]) -> bool:
        """
        判断给定的多个字符串中是否存在空白字符串。
        当 *strings* 为空或其中任一元素为空白时返回 True。

        :param strings: 一个或多个待检查的字符串
        :return: 是否存在空白字符串
        """
        if not strings:
            return True
        for string in strings:
            if CharSequenceUtil.is_blank(string):
                return True
        return False

    @staticmethod
    def is_all_blank(*strings: Optional[str]) -> bool:
        """
        判断给定的多个字符串是否全部为空白。
        当 *strings* 为空或所有元素均为空白时返回 True。

        :param strings: 一个或多个待检查的字符串
        :return: 是否全部为空白字符串
        """
        if not strings:
            return True
        for string in strings:
            if CharSequenceUtil.is_not_blank(string):
                return False
        return True

    @staticmethod
    def is_empty(string: Optional[str]) -> bool:
        """
        判断字符串是否为空（None 或 ``""``）。

        :param string: 待检查的字符串
        :return: 是否为 None 或空字符串
        """
        return string is None or len(string) == 0

    @staticmethod
    def is_not_empty(string: Optional[str]) -> bool:
        """
        判断字符串是否不为空（与 :meth:`is_empty` 相反）。

        :param string: 待检查的字符串
        :return: 是否不为 None 且不为空
        """
        return not CharSequenceUtil.is_empty(string)

    @staticmethod
    def empty_if_none(string: Optional[str]) -> str:
        """
        如果 *string* 为 None 则返回空字符串，否则返回原字符串。

        :param string: 待检查的字符串
        :return: 原字符串或 ``""``
        """
        return CharSequenceUtil.none_to_empty(string)

    @staticmethod
    def none_to_empty(string: Optional[str]) -> str:
        """
        将 None 转换为空字符串。

        :param string: 待转换的字符串
        :return: *string* 为 None 时返回 ``""``，否则返回原字符串
        """
        return CharSequenceUtil.none_to_default(string, CharPool.EMPTY)

    @staticmethod
    def none_to_default(string: Optional[str], default: str) -> str:
        """
        如果 *string* 为 None 则返回 *default*，否则返回 str(*string*)。

        :param string: 待转换的字符串
        :param default: 默认值
        :return: 字符串本身或默认值
        """
        return default if string is None else str(string)

    @staticmethod
    def empty_to_default(string: Optional[str], default: str) -> str:
        """
        如果 *string* 为 None 或 ``""`` 则返回 *default*，否则返回 str(*string*)。

        :param string: 待转换的字符串
        :param default: 默认值
        :return: 字符串本身或默认值
        """
        return default if CharSequenceUtil.is_empty(string) else str(string)

    @staticmethod
    def blank_to_default(string: Optional[str], default: str) -> str:
        """
        如果 *string* 为 None、空字符串或空白字符串则返回 *default*，否则返回 str(*string*)。

        :param string: 待转换的字符串
        :param default: 默认值
        :return: 字符串本身或默认值
        """
        return default if CharSequenceUtil.is_blank(string) else str(string)

    @staticmethod
    def empty_to_none(string: Optional[str]) -> Optional[str]:
        """
        将空字符串转换为 None。

        :param string: 待转换的字符串
        :return: *string* 为空时返回 None，否则返回原字符串
        """
        return None if CharSequenceUtil.is_empty(string) else str(string)

    @staticmethod
    def has_empty(*strings: Optional[str]) -> bool:
        """
        判断给定的多个字符串中是否存在空字符串（None 或 ``""``）。
        当 *strings* 为空或其中任一元素为空时返回 True。

        :param strings: 一个或多个待检查的字符串
        :return: 是否存在空字符串
        """
        if not strings:
            return True
        for string in strings:
            if CharSequenceUtil.is_empty(string):
                return True
        return False

    @staticmethod
    def is_all_empty(*strings: Optional[str]) -> bool:
        """
        判断给定的多个字符串是否全部为空。
        当 *strings* 为空或所有元素均为空时返回 True。

        :param strings: 一个或多个待检查的字符串
        :return: 是否全部为空字符串
        """
        if not strings:
            return True
        for string in strings:
            if CharSequenceUtil.is_not_empty(string):
                return False
        return True

    @staticmethod
    def is_all_not_empty(*strings: Optional[str]) -> bool:
        """
        判断给定的多个字符串是否全部不为空。

        :param strings: 一个或多个待检查的字符串
        :return: 是否没有空字符串
        """
        return not CharSequenceUtil.has_empty(*strings)

    @staticmethod
    def is_all_not_blank(*strings: Optional[str]) -> bool:
        """
        判断给定的多个字符串是否全部不为空白。

        :param strings: 一个或多个待检查的字符串
        :return: 是否没有空白字符串
        """
        return not CharSequenceUtil.has_blank(*strings)

    @staticmethod
    def is_none_or_undefined(string: Optional[str]) -> bool:
        """
        判断 *string* 是否为 None、``""``、``"None"`` 或 ``"undefined"``。

        :param string: 待检查的字符串
        :return: 是否匹配哨兵值
        """
        if string is None:
            return True
        return CharSequenceUtil.is_none_or_undefined_str(string)

    @staticmethod
    def is_empty_or_undefined(string: Optional[str]) -> bool:
        """
        判断 *string* 是否为空或等于 ``"None"`` / ``"undefined"``。

        :param string: 待检查的字符串
        :return: 是否为空或哨兵值
        """
        if CharSequenceUtil.is_empty(string):
            return True
        return CharSequenceUtil.is_none_or_undefined_str(string)

    @staticmethod
    def is_blank_or_undefined(string: Optional[str]) -> bool:
        """
        判断 *string* 是否为空白或等于 ``"None"`` / ``"undefined"``。

        :param string: 待检查的字符串
        :return: 是否为空白或哨兵值
        """
        if CharSequenceUtil.is_blank(string):
            return True
        return CharSequenceUtil.is_none_or_undefined_str(string)

    @staticmethod
    def is_none_or_undefined_str(string: str) -> bool:
        """
        不做 None 检查，直接判断 *string* 去除空白后是否等于 ``"None"`` 或 ``"undefined"``。

        :param string: 待检查的字符串
        :return: 是否为 ``"None"`` 或 ``"undefined"``
        """
        str_string = str(string).strip()
        return str_string == StrPool.NONE or str_string == "undefined"

    # ------------------------------------------------------------------
    # Trim
    # ------------------------------------------------------------------

    @staticmethod
    def trim(
        string: Optional[str],
        mode: int = 0,
        predicate: Callable[[str], bool] = CharUtil.is_blank_char,
    ) -> Optional[str]:
        """
        根据 *predicate* 从字符串的头部和/或尾部裁剪字符。

        :param string: 待裁剪的字符串
        :param mode: ``-1`` = 仅裁剪头部，``0`` = 两端都裁剪，``1`` = 仅裁剪尾部
        :param predicate: 返回 True 时表示该字符应被移除的函数
        :return: 裁剪后的字符串，*string* 为 None 时返回 None
        """
        result: Optional[str]
        if string is None:
            result = None
        else:
            length = len(string)
            start = 0
            end = length
            if mode <= 0:
                while start < end and predicate(string[start]):
                    start += 1
            if mode >= 0:
                while start < end and predicate(string[end - 1]):
                    end -= 1
            if start > 0 or end < length:
                result = str(string)[start:end]
            else:
                result = str(string)
        return result

    @staticmethod
    def trim_to_empty(string: Optional[str]) -> str:
        """
        裁剪两端空白。*string* 为 None 时返回 ``""``。

        :param string: 待裁剪的字符串
        :return: 裁剪后的字符串或 ``""``
        """
        return CharPool.EMPTY if string is None else CharSequenceUtil.trim(string)  # type: ignore[return-value]

    @staticmethod
    def trim_to_none(string: Optional[str]) -> Optional[str]:
        """
        裁剪两端空白。*string* 为 None 或结果为空字符串时返回 None。

        :param string: 待裁剪的字符串
        :return: 裁剪后的字符串或 None
        """
        trim_str = CharSequenceUtil.trim(string)
        return None if trim_str == CharPool.EMPTY else trim_str

    @staticmethod
    def trim_start(string: Optional[str]) -> Optional[str]:
        """
        仅裁剪字符串头部的空白。

        :param string: 待裁剪的字符串
        :return: 裁剪后的字符串，*string* 为 None 时返回 None
        """
        return CharSequenceUtil.trim(string, mode=-1)

    @staticmethod
    def trim_end(string: Optional[str]) -> Optional[str]:
        """
        仅裁剪字符串尾部的空白。

        :param string: 待裁剪的字符串
        :return: 裁剪后的字符串，*string* 为 None 时返回 None
        """
        return CharSequenceUtil.trim(string, mode=1)

    # ------------------------------------------------------------------
    # Starts / ends with
    # ------------------------------------------------------------------

    @staticmethod
    def start_with(
        string: Optional[str],
        prefix: Optional[str],
        ignore_case: bool = False,
        ignore_equals: bool = False,
    ) -> bool:
        """
        判断 *string* 是否以 *prefix* 开头。

        :param string: 待检查的字符串
        :param prefix: 前缀
        :param ignore_case: 是否忽略大小写
        :param ignore_equals: 字符串相等时是否返回 False
        :return: 是否以指定前缀开头
        """
        if string is None or prefix is None:
            if ignore_equals:
                return False
            return string is None and prefix is None

        if ignore_case:
            is_start = string.lower().startswith(prefix.lower())
        else:
            is_start = string.startswith(prefix)

        if is_start:
            if ignore_equals:
                return not CharSequenceUtil.equals(string, prefix, ignore_case)
            return True
        return False

    @staticmethod
    def start_with_ignore_equals(string: Optional[str], prefix: Optional[str]) -> bool:
        """
        判断 *string* 是否以 *prefix* 开头且不相等。

        :param string: 待检查的字符串
        :param prefix: 前缀
        :return: 是否以指定前缀开头且两者不同
        """
        return CharSequenceUtil.start_with(string, prefix, ignore_case=False, ignore_equals=True)

    @staticmethod
    def start_with_ignore_case(string: Optional[str], prefix: Optional[str]) -> bool:
        """
        判断 *string* 是否以 *prefix* 开头，忽略大小写。

        :param string: 待检查的字符串
        :param prefix: 前缀
        :return: 是否以指定前缀开头（不区分大小写）
        """
        return CharSequenceUtil.start_with(string, prefix, ignore_case=True)

    @staticmethod
    def start_with_any(string: Optional[str], *prefixes: Optional[str]) -> bool:
        """
        判断 *string* 是否以给定的任一 *prefixes* 开头。

        :param string: 待检查的字符串
        :param prefixes: 前缀列表
        :return: 是否匹配任一前缀
        """
        if CharSequenceUtil.is_empty(string) or not prefixes:
            return False
        for prefix in prefixes:
            if CharSequenceUtil.start_with(string, prefix, ignore_case=False):
                return True
        return False

    @staticmethod
    def start_with_any_ignore_case(string: Optional[str], *prefixes: Optional[str]) -> bool:
        """
        判断 *string* 是否以给定的任一 *prefixes* 开头，忽略大小写。

        :param string: 待检查的字符串
        :param prefixes: 前缀列表
        :return: 是否匹配任一前缀（不区分大小写）
        """
        if CharSequenceUtil.is_empty(string) or not prefixes:
            return False
        for prefix in prefixes:
            if CharSequenceUtil.start_with(string, prefix, ignore_case=True):
                return True
        return False

    @staticmethod
    def end_with(
        string: Optional[str],
        suffix: Optional[str],
        ignore_case: bool = False,
        ignore_equals: bool = False,
    ) -> bool:
        """
        判断 *string* 是否以 *suffix* 结尾。

        :param string: 待检查的字符串
        :param suffix: 后缀
        :param ignore_case: 是否忽略大小写
        :param ignore_equals: 字符串相等时是否返回 False
        :return: 是否以指定后缀结尾
        """
        if string is None or suffix is None:
            if ignore_equals:
                return False
            return string is None and suffix is None

        if ignore_case:
            is_end = string.lower().endswith(suffix.lower())
        else:
            is_end = string.endswith(suffix)

        if is_end:
            if ignore_equals:
                return not CharSequenceUtil.equals(string, suffix, ignore_case)
            return True
        return False

    @staticmethod
    def end_with_ignore_equals(string: Optional[str], suffix: Optional[str]) -> bool:
        """
        判断 *string* 是否以 *suffix* 结尾且不相等。

        :param string: 待检查的字符串
        :param suffix: 后缀
        :return: 是否以指定后缀结尾且两者不同
        """
        return CharSequenceUtil.end_with(string, suffix, ignore_case=False, ignore_equals=True)

    @staticmethod
    def end_with_ignore_case(string: Optional[str], prefix: Optional[str]) -> bool:
        """
        判断 *string* 是否以 *prefix* 结尾，忽略大小写。

        :param string: 待检查的字符串
        :param prefix: 后缀
        :return: 是否以指定后缀结尾（不区分大小写）
        """
        return CharSequenceUtil.end_with(string, prefix, ignore_case=True)

    @staticmethod
    def end_with_any(string: Optional[str], *prefixes: Optional[str]) -> bool:
        """
        判断 *string* 是否以给定的任一 *prefixes* 结尾。

        :param string: 待检查的字符串
        :param prefixes: 后缀列表
        :return: 是否匹配任一后缀
        """
        if CharSequenceUtil.is_empty(string) or not prefixes:
            return False
        for prefix in prefixes:
            if CharSequenceUtil.end_with(string, prefix, ignore_case=False):
                return True
        return False

    @staticmethod
    def end_with_any_ignore_case(string: Optional[str], *prefixes: Optional[str]) -> bool:
        """
        判断 *string* 是否以给定的任一 *prefixes* 结尾，忽略大小写。

        :param string: 待检查的字符串
        :param prefixes: 后缀列表
        :return: 是否匹配任一后缀（不区分大小写）
        """
        if CharSequenceUtil.is_empty(string) or not prefixes:
            return False
        for prefix in prefixes:
            if CharSequenceUtil.end_with(string, prefix, ignore_case=True):
                return True
        return False

    # ------------------------------------------------------------------
    # Contains
    # ------------------------------------------------------------------

    @staticmethod
    def contains(string: Optional[str], search: Optional[str]) -> bool:
        """
        判断 *string* 是否包含 *search*。

        :param string: 待搜索的字符串
        :param search: 待查找的子串
        :return: 是否包含该子串
        """
        if string is None or search is None:
            return False
        return search in string

    @staticmethod
    def contains_any(string: Optional[str], *test_strings: Optional[str]) -> bool:
        """
        判断 *string* 是否包含给定的任一子串。

        :param string: 待搜索的字符串
        :param test_strings: 待查找的子串列表
        :return: 是否包含任一子串
        """
        return CharSequenceUtil.get_contains_str(string, *test_strings) is not None

    @staticmethod
    def contains_all(string: Optional[str], *test_strings: Optional[str]) -> bool:
        """
        判断 *string* 是否包含所有给定的子串。

        :param string: 待搜索的字符串
        :param test_strings: 待查找的子串列表
        :return: 是否包含所有子串
        """
        if CharSequenceUtil.is_blank(string) or not test_strings:
            return False
        for test_string in test_strings:
            if not CharSequenceUtil.contains(string, test_string):
                return False
        return True

    @staticmethod
    def contains_blank(string: Optional[str]) -> bool:
        """
        判断 *string* 是否包含空白字符。
        *string* 为 None 或空字符串时返回 False。

        :param string: 待检查的字符串
        :return: 是否包含空白字符
        """
        if CharSequenceUtil.is_empty(string):
            return False
        for char in string:
            if CharUtil.is_blank_char(char):
                return True
        return False

    @staticmethod
    def get_contains_str(string: Optional[str], *test_strings: Optional[str]) -> Optional[str]:
        """
        查找 *test_strings* 中第一个被 *string* 包含的子串。

        :param string: 待搜索的字符串
        :param test_strings: 待查找的子串列表
        :return: 第一个匹配的子串，或 None
        """
        if CharSequenceUtil.is_empty(string) or not test_strings:
            return None
        for test_string in test_strings:
            if CharSequenceUtil.contains(string, test_string):
                return test_string
        return None

    @staticmethod
    def contains_ignore_case(string: Optional[str], test_string: Optional[str]) -> bool:
        """
        判断 *string* 是否包含 *test_string*，忽略大小写。
        两者均为 None 时返回 True。

        :param string: 待搜索的字符串
        :param test_string: 待查找的子串
        :return: 是否包含该子串（不区分大小写）
        """
        if string is None:
            return test_string is None
        return CharSequenceUtil.index_of(string, test_string, ignore_case=True) > -1

    @staticmethod
    def contains_any_ignore_case(string: Optional[str], *test_strings: Optional[str]) -> bool:
        """
        判断 *string* 是否包含给定的任一子串，忽略大小写。

        :param string: 待搜索的字符串
        :param test_strings: 待查找的子串列表
        :return: 是否包含任一子串（不区分大小写）
        """
        return CharSequenceUtil.get_contains_str_ignore_case(string, *test_strings) is not None

    @staticmethod
    def get_contains_str_ignore_case(string: Optional[str], *test_strings: Optional[str]) -> Optional[str]:
        """
        查找 *test_strings* 中第一个被 *string* 包含的子串，忽略大小写。

        :param string: 待搜索的字符串
        :param test_strings: 待查找的子串列表
        :return: 第一个匹配的子串，或 None
        """
        if CharSequenceUtil.is_empty(string) or not test_strings:
            return None
        for test_string in test_strings:
            if CharSequenceUtil.contains_ignore_case(string, test_string):
                return test_string
        return None

    # ------------------------------------------------------------------
    # Index of
    # ------------------------------------------------------------------

    @staticmethod
    def index_of(
        text: Optional[str],
        search_string: Optional[str],
        start: Optional[int] = None,
        end: Optional[int] = None,
        ignore_case: bool = False,
    ) -> int:
        """
        在 *text* 的可选范围 [start, end) 内查找 *search_string* 的索引。

        :param text: 待搜索的字符串
        :param search_string: 待查找的子串
        :param start: 可选的起始位置
        :param end: 可选的结束位置
        :param ignore_case: 是否忽略大小写
        :return: 索引值，未找到时返回 -1
        """
        if CharSequenceUtil.is_empty(text) or CharSequenceUtil.is_empty(search_string):
            if CharSequenceUtil.equals(text, search_string):
                return 0
            return -1
        if ignore_case:
            text = text.lower()
            search_string = search_string.lower()
        return text.find(search_string, start, end)

    @staticmethod
    def index_of_ignore_case(
        text: Optional[str],
        search_string: Optional[str],
        start: Optional[int] = None,
        end: Optional[int] = None,
    ) -> int:
        """
        在 *text* 中查找 *search_string* 的索引，忽略大小写。

        :param text: 待搜索的字符串
        :param search_string: 待查找的子串
        :param start: 可选的起始位置
        :param end: 可选的结束位置
        :return: 索引值，未找到时返回 -1
        """
        return CharSequenceUtil.index_of(text, search_string, start=start, end=end, ignore_case=True)

    @staticmethod
    def last_index_of(
        text: Optional[str],
        search_string: Optional[str],
        start: Optional[int] = None,
        end: Optional[int] = None,
        ignore_case: bool = False,
    ) -> int:
        """
        在 *text* 的可选范围 [start, end) 内查找 *search_string* 最后一次出现的索引。

        :param text: 待搜索的字符串
        :param search_string: 待查找的子串
        :param start: 可选的起始位置
        :param end: 可选的结束位置
        :param ignore_case: 是否忽略大小写
        :return: 索引值，未找到时返回 -1
        """
        if CharSequenceUtil.is_empty(text) or CharSequenceUtil.is_empty(search_string):
            if CharSequenceUtil.equals(text, search_string):
                return 0
            return -1
        if ignore_case:
            text = text.lower()
            search_string = search_string.lower()
        return text.rfind(search_string, start, end)

    @staticmethod
    def last_index_of_ignore_case(
        text: Optional[str],
        search_string: Optional[str],
        start: Optional[int] = None,
        end: Optional[int] = None,
    ) -> int:
        """
        在 *text* 中查找 *search_string* 最后一次出现的索引，忽略大小写。

        :param text: 待搜索的字符串
        :param search_string: 待查找的子串
        :param start: 可选的起始位置
        :param end: 可选的结束位置
        :return: 索引值，未找到时返回 -1
        """
        return CharSequenceUtil.last_index_of(text, search_string, start, end, ignore_case=True)

    @staticmethod
    def ordinal_index_of(text: Optional[str], search_string: Optional[str], ordinal: int) -> int:
        """
        返回 *search_string* 在 *text* 中第 *ordinal* 次出现的索引。

        :param text: 待搜索的字符串
        :param search_string: 待查找的子串
        :param ordinal: 出现次数（从1开始）
        :return: 索引值，未找到时返回 -1
        """
        if text is None or search_string is None or ordinal <= 0:
            return -1
        if len(search_string) == 0:
            return 0
        found = 0
        index = -1
        for _ in range(ordinal):
            index = CharSequenceUtil.index_of(text, search_string, start=found)
            if index < 0:
                return index
            found = index + 1
        return index

    # ------------------------------------------------------------------
    # Remove
    # ------------------------------------------------------------------

    @staticmethod
    def remove_all(string: Optional[str], string_to_remove: Optional[str]) -> Optional[str]:
        """
        从 *string* 中移除所有 *string_to_remove* 的出现。

        :param string: 源字符串
        :param string_to_remove: 待移除的子串
        :return: 移除后的字符串
        """
        if CharSequenceUtil.is_empty(string) or CharSequenceUtil.is_empty(string_to_remove):
            return string
        return string.replace(string_to_remove, CharPool.EMPTY)  # type: ignore[union-attr]

    @staticmethod
    def remove_any(string: Optional[str], *strings_to_remove: Optional[str]) -> Optional[str]:
        """
        从 *string* 中移除 *strings_to_remove* 中每个子串的所有出现。

        :param string: 源字符串
        :param strings_to_remove: 待移除的子串列表
        :return: 移除后的字符串
        """
        result = string
        if CharSequenceUtil.is_not_empty(string):
            for string_to_remove in strings_to_remove:
                result = CharSequenceUtil.remove_all(result, string_to_remove)
        return result

    @staticmethod
    def remove_all_line_breaks(string: Optional[str]) -> Optional[str]:
        """
        从 *string* 中移除所有换行符（``\\r`` 和 ``\\n``）。

        :param string: 源字符串
        :return: 不含换行符的字符串
        """
        return CharSequenceUtil.remove_any(string, CharPool.CR, CharPool.LF)

    @staticmethod
    def remove_pre_and_lower_first(string: Optional[str], pre_or_length: Union[int, str]) -> Optional[str]:
        """
        从 *string* 中移除前缀，并将剩余字符串的首字母小写。

        :param string: 源字符串
        :param pre_or_length: 要移除的前缀字符串，或从头部移除的字符数
        :return: 处理后的字符串，*string* 为 None 时返回 None
        """
        if isinstance(pre_or_length, str):
            return CharSequenceUtil.lower_first(CharSequenceUtil.remove_prefix(string, pre_or_length))
        if string is None:
            return None
        if len(string) > pre_or_length:
            first = string[pre_or_length].lower()
            if len(string) > pre_or_length + 1:
                start_index = pre_or_length + 1
                return first + string[start_index:]
            return first
        return string

    @staticmethod
    def remove_prefix(string: Optional[str], prefix: Optional[str]) -> Optional[str]:
        """
        如果 *string* 以 *prefix* 开头则移除该前缀。

        :param string: 源字符串
        :param prefix: 待移除的前缀
        :return: 移除前缀后的字符串
        """
        if CharSequenceUtil.is_empty(string) or CharSequenceUtil.is_empty(prefix):
            return string
        if CharSequenceUtil.start_with(string, prefix):
            return CharSequenceUtil.sub_suf(string, len(prefix))  # type: ignore[arg-type]
        return string

    @staticmethod
    def remove_prefix_ignore_case(string: Optional[str], prefix: Optional[str]) -> Optional[str]:
        """
        如果 *string* 以 *prefix* 开头则移除该前缀（忽略大小写）。

        :param string: 源字符串
        :param prefix: 待移除的前缀
        :return: 移除前缀后的字符串
        """
        if CharSequenceUtil.is_empty(string) or CharSequenceUtil.is_empty(prefix):
            return string
        if CharSequenceUtil.start_with_ignore_case(string, prefix):
            return CharSequenceUtil.sub_suf(string, len(prefix))  # type: ignore[arg-type]
        return string

    @staticmethod
    def remove_suffix(string: Optional[str], suffix: Optional[str]) -> Optional[str]:
        """
        如果 *string* 以 *suffix* 结尾则移除该后缀。

        :param string: 源字符串
        :param suffix: 待移除的后缀
        :return: 移除后缀后的字符串
        """
        if CharSequenceUtil.is_empty(string) or CharSequenceUtil.is_empty(suffix):
            return string
        if CharSequenceUtil.end_with(string, suffix):
            return CharSequenceUtil.sub_pre(string, len(suffix))  # type: ignore[arg-type]
        return string

    @staticmethod
    def remove_suffix_and_lower_first(string: Optional[str], suffix: Optional[str]) -> Optional[str]:
        """
        从 *string* 中移除后缀并将首字母小写。

        :param string: 源字符串
        :param suffix: 待移除的后缀
        :return: 处理后的字符串
        """
        return CharSequenceUtil.lower_first(CharSequenceUtil.remove_suffix(string, suffix))

    @staticmethod
    def remove_suffix_ignore_case(string: Optional[str], suffix: Optional[str]) -> Optional[str]:
        """
        如果 *string* 以 *suffix* 结尾则移除该后缀（忽略大小写）。

        :param string: 源字符串
        :param suffix: 待移除的后缀
        :return: 移除后缀后的字符串
        """
        if CharSequenceUtil.is_empty(string) or CharSequenceUtil.is_empty(suffix):
            return string
        if CharSequenceUtil.end_with_ignore_case(string, suffix):
            return CharSequenceUtil.sub_pre(string, len(suffix))  # type: ignore[arg-type]
        return string

    # ------------------------------------------------------------------
    # Clean / strip
    # ------------------------------------------------------------------

    @staticmethod
    def clean_blank(string: Optional[str]) -> Optional[str]:
        """
        移除 *string* 中的所有空白字符。

        :param string: 源字符串
        :return: 不含空白字符的字符串
        """
        return CharSequenceUtil.filter(string, lambda char: not CharUtil.is_blank_char(char))

    @staticmethod
    def strip(string: Optional[str], prefix: str, suffix: Optional[str] = None) -> Optional[str]:
        """
        从 *string* 头部去除 *prefix*，尾部去除 *suffix*。
        若 *suffix* 为 None，则两端均去除 *prefix*。

        :param string: 源字符串
        :param prefix: 待去除的前缀
        :param suffix: 待去除的后缀（默认为 *prefix*）
        :return: 去除后的字符串
        """
        if suffix is None:
            if CharSequenceUtil.equals(string, prefix):
                return CharPool.EMPTY
            suffix = prefix

        if CharSequenceUtil.is_empty(string):
            return string
        from_index = 0
        to_index = len(string)
        if CharSequenceUtil.start_with(string, prefix):
            from_index = len(prefix)
        if CharSequenceUtil.end_with(string, suffix):
            to_index -= len(suffix)
        return string[from_index:to_index]

    @staticmethod
    def strip_ignore_case(string: Optional[str], prefix: str, suffix: Optional[str] = None) -> Optional[str]:
        """
        从 *string* 头部去除 *prefix*，尾部去除 *suffix*，忽略大小写。

        :param string: 源字符串
        :param prefix: 待去除的前缀
        :param suffix: 待去除的后缀（默认为 *prefix*）
        :return: 去除后的字符串
        """
        if suffix is None:
            if CharSequenceUtil.equals_ignore_case(string, prefix):
                return CharPool.EMPTY
            suffix = prefix

        if CharSequenceUtil.is_empty(string):
            return string
        from_index = 0
        to_index = len(string)
        if CharSequenceUtil.start_with_ignore_case(string, prefix):
            from_index = len(prefix)
        if CharSequenceUtil.end_with_ignore_case(string, suffix):
            to_index -= len(suffix)
        return string[from_index:to_index]

    # ------------------------------------------------------------------
    # Add prefix / suffix if missing
    # ------------------------------------------------------------------

    @staticmethod
    def add_prefix_if_not(string: Optional[str], prefix: Optional[str]) -> Optional[str]:
        """
        如果 *string* 不以 *prefix* 开头则添加该前缀。

        :param string: 源字符串
        :param prefix: 待添加的前缀
        :return: 确保有前缀的字符串
        """
        return CharSequenceUtil.prepend_if_missing(string, prefix, prefix)

    @staticmethod
    def add_suffix_if_not(string: Optional[str], suffix: Optional[str]) -> Optional[str]:
        """
        如果 *string* 不以 *suffix* 结尾则添加该后缀。

        :param string: 源字符串
        :param suffix: 待添加的后缀
        :return: 确保有后缀的字符串
        """
        return CharSequenceUtil.append_if_missing(string, suffix, suffix)

    # ------------------------------------------------------------------
    # Cut
    # ------------------------------------------------------------------

    @staticmethod
    def cut(string: Optional[str], part_length: int) -> List[str]:
        """
        将 *string* 按 *part_length* 个字符一组进行分割。

        :param string: 源字符串
        :param part_length: 每组的长度
        :return: 分割后的字符串列表
        """
        if string is None:
            return []
        length = len(string)
        if length < part_length:
            return [string]
        part = (length // part_length) if length % part_length == 0 else (length // part_length + 1)
        result: List[str] = []
        for i in range(part):
            start = i * part_length
            end = length if i == part - 1 else (part_length + i * part_length)
            result.append(string[start:end])
        return result

    # ------------------------------------------------------------------
    # Equals
    # ------------------------------------------------------------------

    @staticmethod
    def equals(string1: Optional[str], string2: Optional[str], ignore_case: bool = False) -> bool:
        """
        比较两个字符串是否相等。

        :param string1: 第一个字符串
        :param string2: 第二个字符串
        :param ignore_case: 是否忽略大小写
        :return: 两个字符串是否相等（或均为 None）
        """
        if string1 is None:
            return string2 is None
        if string2 is None:
            return False
        if ignore_case:
            return string1.lower() == string2.lower()
        return string1 == string2

    @staticmethod
    def equals_ignore_case(string1: Optional[str], string2: Optional[str]) -> bool:
        """
        比较两个字符串是否相等，忽略大小写。

        :param string1: 第一个字符串
        :param string2: 第二个字符串
        :return: 两个字符串是否相等（不区分大小写）
        """
        return CharSequenceUtil.equals(string1, string2, ignore_case=True)

    # ------------------------------------------------------------------
    # Append / prepend if missing
    # ------------------------------------------------------------------

    @staticmethod
    def append_if_missing(
        string: Optional[str], suffix: Optional[str], *suffixes: Optional[str], ignore_case: bool = False
    ) -> Optional[str]:
        """
        如果 *string* 不以指定后缀结尾，则追加 *suffix*。

        :param string: 源字符串
        :param suffix: 待追加的后缀
        :param suffixes: 额外的待检查后缀
        :param ignore_case: 检查时是否忽略大小写
        :return: 确保有后缀的字符串
        """
        if (
            string is None
            or CharSequenceUtil.is_empty(suffix)
            or CharSequenceUtil.end_with(string, suffix, ignore_case=ignore_case)
        ):
            return string
        if suffixes:
            for s in suffixes:
                if CharSequenceUtil.end_with(string, s, ignore_case):
                    return string
        return string + suffix  # type: ignore[operator]

    @staticmethod
    def append_if_missing_ignore_case(
        string: Optional[str], suffix: Optional[str], *suffixes: Optional[str]
    ) -> Optional[str]:
        """
        如果 *string* 不以 *suffix* 结尾则追加（忽略大小写）。

        :param string: 源字符串
        :param suffix: 待追加的后缀
        :param suffixes: 额外的待检查后缀
        :return: 确保有后缀的字符串
        """
        return CharSequenceUtil.append_if_missing(string, suffix, *suffixes, ignore_case=True)

    @staticmethod
    def prepend_if_missing(
        string: Optional[str], prefix: Optional[str], *prefixes: Optional[str], ignore_case: bool = False
    ) -> Optional[str]:
        """
        如果 *string* 不以指定前缀开头，则前置 *prefix*。

        :param string: 源字符串
        :param prefix: 待前置的前缀
        :param prefixes: 额外的待检查前缀
        :param ignore_case: 检查时是否忽略大小写
        :return: 确保有前缀的字符串
        """
        if (
            string is None
            or CharSequenceUtil.is_empty(prefix)
            or CharSequenceUtil.start_with(string, prefix, ignore_case=ignore_case)
        ):
            return string
        if prefixes:
            for p in prefixes:
                if CharSequenceUtil.start_with(string, p, ignore_case):
                    return string
        return prefix + string  # type: ignore[operator]

    @staticmethod
    def prepend_if_missing_ignore_case(
        string: Optional[str], prefix: Optional[str], *prefixes: Optional[str]
    ) -> Optional[str]:
        """
        如果 *string* 不以 *prefix* 开头则前置（忽略大小写）。

        :param string: 源字符串
        :param prefix: 待前置的前缀
        :param prefixes: 额外的待检查前缀
        :return: 确保有前缀的字符串
        """
        return CharSequenceUtil.prepend_if_missing(string, prefix, *prefixes, ignore_case=True)

    # ------------------------------------------------------------------
    # Upper / lower first
    # ------------------------------------------------------------------

    @staticmethod
    def upper_first_and_add_pre(string: Optional[str], pre_string: Optional[str]) -> Optional[str]:
        """
        将 *string* 首字母大写并前置 *pre_string*。

        :param string: 源字符串
        :param pre_string: 待前置的前缀
        :return: 处理后的字符串，任一参数为 None 时返回 None
        """
        if string is None or pre_string is None:
            return None
        return pre_string + CharSequenceUtil.upper_first(string)  # type: ignore[operator]

    @staticmethod
    def upper_first(string: Optional[str]) -> Optional[str]:
        """
        将 *string* 的首字母大写。

        :param string: 源字符串
        :return: 首字母大写后的字符串
        """
        if string is None:
            return None
        if len(string) > 0:
            first_char = string[0]
            if CharUtil.is_letter_lower(first_char):
                return first_char.upper() + CharSequenceUtil.sub_suf(string, 1)
        return string

    @staticmethod
    def lower_first(string: Optional[str]) -> Optional[str]:
        """
        将 *string* 的首字母小写。

        :param string: 源字符串
        :return: 首字母小写后的字符串
        """
        if string is None:
            return None
        if len(string) > 0:
            first_char = string[0]
            if CharUtil.is_letter_upper(first_char):
                return first_char.lower() + CharSequenceUtil.sub_suf(string, 1)
        return string

    # ------------------------------------------------------------------
    # Filter
    # ------------------------------------------------------------------

    @staticmethod
    def filter(string: Optional[str], filter_func: Callable[[str], bool]) -> Optional[str]:
        """
        使用 *filter_func* 过滤 *string* 中的字符。仅保留
        *filter_func* 返回 True 的字符。

        :param string: 源字符串
        :param filter_func: 过滤函数
        :return: 过滤后的字符串
        """
        if string is None or filter_func is None:
            return string
        return "".join([char for char in string if filter_func(char)])

    # ------------------------------------------------------------------
    # Substring helpers (used internally)
    # ------------------------------------------------------------------

    @staticmethod
    def sub_suf(string: Optional[str], from_index: int) -> Optional[str]:
        """
        返回从 *from_index* 到末尾的子串。

        :param string: 源字符串
        :param from_index: 起始索引（包含）
        :return: 子串，*string* 为 None 时返回 None
        """
        if string is None:
            return None
        if from_index < 0:
            from_index = 0
        if from_index >= len(string):
            return ""
        return string[from_index:]

    @staticmethod
    def sub_pre(string: Optional[str], to_index: int) -> Optional[str]:
        """
        返回从开头到末尾减去 *to_index* 个字符处的子串。

        :param string: 源字符串
        :param to_index: 从末尾排除的字符数
        :return: 子串，*string* 为 None 时返回 None
        """
        if string is None:
            return None
        length = len(string)
        end = length - to_index
        if end <= 0:
            return ""
        return string[:end]

    # ======================================================================
    # NEW METHODS ported from Java Hutool
    # ======================================================================

    # ------------------------------------------------------------------
    # Substring operations
    # ------------------------------------------------------------------

    @staticmethod
    def sub(string: Optional[str], start: int, end: Optional[int] = None) -> Optional[str]:
        """
        提取子串，支持从末尾开始计数的负索引（类似 Python 切片）。

        :param string: 源字符串
        :param start: 起始索引（包含）。负值表示从末尾开始计数。
        :param end: 结束索引（不包含）。负值表示从末尾开始计数。
            为 None 时返回到字符串末尾。
        :return: 子串，*string* 为 None 时返回 None
        """
        if string is None:
            return None
        length = len(string)
        if start < 0:
            start += length
        if start < 0:
            start = 0
        if end is None:
            end = length
        if end < 0:
            end += length
        if end < 0:
            end = 0
        if start >= end:
            return ""
        return string[start:end]

    @staticmethod
    def sub_before(string: Optional[str], separator: str, is_last: bool = False) -> Optional[str]:
        """
        返回第一个（或最后一个）*separator* 出现之前的子串。

        未找到 *separator* 时返回整个字符串。

        :param string: 源字符串
        :param separator: 分隔符字符串
        :param is_last: 是否使用最后一个分隔符
        :return: 分隔符之前的子串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        if CharSequenceUtil.is_empty(separator):
            return string
        if is_last:
            pos = string.rfind(separator)  # type: ignore[union-attr]
        else:
            pos = string.find(separator)  # type: ignore[union-attr]
        if pos < 0:
            return string
        return string[:pos]  # type: ignore[index]

    @staticmethod
    def sub_after(string: Optional[str], separator: str, is_last: bool = False) -> Optional[str]:
        """
        返回第一个（或最后一个）*separator* 出现之后的子串。

        未找到 *separator* 时返回整个字符串。

        :param string: 源字符串
        :param separator: 分隔符字符串
        :param is_last: 是否使用最后一个分隔符
        :return: 分隔符之后的子串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        if CharSequenceUtil.is_empty(separator):
            return string
        if is_last:
            pos = string.rfind(separator)  # type: ignore[union-attr]
        else:
            pos = string.find(separator)  # type: ignore[union-attr]
        if pos < 0:
            return string
        return string[pos + len(separator) :]  # type: ignore[index]

    @staticmethod
    def sub_between(string: Optional[str], prefix: str, suffix: str) -> Optional[str]:
        """
        返回 *string* 中第一个 *prefix* 之后、下一个 *suffix* 之前的文本。

        *string* 为 None/空，或找不到 *prefix*/*suffix* 时返回 None。

        :param string: 源字符串
        :param prefix: 前标记
        :param suffix: 后标记
        :return: *prefix* 和 *suffix* 之间的文本，或 None
        """
        if CharSequenceUtil.is_empty(string) or CharSequenceUtil.is_empty(prefix) or CharSequenceUtil.is_empty(suffix):
            return None

        start = string.find(prefix)  # type: ignore[union-attr]
        if start < 0:
            return None
        start += len(prefix)
        end = string.find(suffix, start)  # type: ignore[union-attr]
        if end < 0:
            return None
        return string[start:end]  # type: ignore[index]

    @staticmethod
    def sub_between_all(string: Optional[str], prefix: str, suffix: str) -> List[str]:
        """
        返回 *string* 中所有 *prefix* 和 *suffix* 之间的不重叠子串。

        :param string: 源字符串
        :param prefix: 前标记
        :param suffix: 后标记
        :return: *prefix* 和 *suffix* 之间的子串列表
        """
        if CharSequenceUtil.is_empty(string) or CharSequenceUtil.is_empty(prefix) or CharSequenceUtil.is_empty(suffix):
            return []

        result: List[str] = []
        remaining = string
        while True:
            piece = CharSequenceUtil.sub_between(remaining, prefix, suffix)
            if piece is None:
                break
            result.append(piece)
            # advance past this match
            idx = remaining.find(prefix + piece + suffix)  # type: ignore[union-attr]
            if idx < 0:
                break
            remaining = remaining[idx + len(prefix) + len(piece) + len(suffix) :]  # type: ignore[index]
        return result

    # ------------------------------------------------------------------
    # Count
    # ------------------------------------------------------------------

    @staticmethod
    def count(
        string: Optional[str],
        char_or_start: str,
        end: Optional[str] = None,
    ) -> int:
        """
        统计字符或子串的出现次数。

        两种调用方式（与 Java Hutool 对齐）：

        - ``count(str, char)`` -- 统计 *char* 在 *str* 中出现的次数。
        - ``count(str, start, end)`` -- 统计 *str* 中 *start* 和 *end* 标记之间的子串数量。

        :param string: 源字符串
        :param char_or_start: 待统计的字符/子串，或当提供 *end* 时作为起始标记
        :param end: 结束标记。提供时 *char_or_start* 视为起始标记
        :return: 统计次数
        """
        if CharSequenceUtil.is_empty(string):
            return 0
        if end is not None:
            # count between markers
            count_val = 0
            remaining = string
            while True:
                sub_piece = CharSequenceUtil.sub_between(remaining, char_or_start, end)
                if sub_piece is None:
                    break
                count_val += 1
                idx = remaining.find(char_or_start + sub_piece + end)  # type: ignore[union-attr]
                if idx < 0:
                    break
                remaining = remaining[idx + len(char_or_start) + len(sub_piece) + len(end) :]  # type: ignore[index]
            return count_val
        return string.count(char_or_start)  # type: ignore[union-attr]

    # ------------------------------------------------------------------
    # Replace
    # ------------------------------------------------------------------

    @staticmethod
    def replace(string: Optional[str], search_str: str, replacement: str, count: int = -1) -> Optional[str]:
        """
        将 *string* 中的 *search_str* 替换为 *replacement*。

        :param string: 源字符串
        :param search_str: 待查找的字符串
        :param replacement: 替换字符串
        :param count: 最大替换次数。``-1`` 表示全部替换（默认）
        :return: 替换后的字符串
        """
        if CharSequenceUtil.is_empty(string) or CharSequenceUtil.is_empty(search_str):
            return string
        if count == -1:
            return string.replace(search_str, replacement)  # type: ignore[union-attr]
        return string.replace(search_str, replacement, count)  # type: ignore[union-attr]

    @staticmethod
    def replace_chars(string: Optional[str], chars: str, replacement: str) -> Optional[str]:
        """
        将 *string* 中出现在 *chars* 里的每个字符替换为 *replacement*。

        :param string: 源字符串
        :param chars: 包含待替换字符的字符串
        :param replacement: 每个匹配字符的替换字符串
        :return: 替换后的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        result = string
        for ch in chars:
            result = result.replace(ch, replacement)  # type: ignore[union-attr]
        return result

    @staticmethod
    def replace_first(string: Optional[str], regex: str, replacement: str) -> Optional[str]:
        """
        替换 *string* 中 *regex* 的第一个匹配项为 *replacement*。

        :param string: 源字符串
        :param regex: 正则表达式模式
        :param replacement: 替换字符串（可包含反向引用如 ``\\1``）
        :return: 替换第一个正则匹配后的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        return re.sub(regex, replacement, string, count=1)  # type: ignore[arg-type]

    @staticmethod
    def replace_all(string: Optional[str], regex: str, replacement: str) -> Optional[str]:
        """
        替换 *string* 中 *regex* 的所有匹配项为 *replacement*。

        :param string: 源字符串
        :param regex: 正则表达式模式
        :param replacement: 替换字符串（可包含反向引用如 ``\\1``）
        :return: 替换所有正则匹配后的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        return re.sub(regex, replacement, string)  # type: ignore[arg-type]

    # ------------------------------------------------------------------
    # Join
    # ------------------------------------------------------------------

    @staticmethod
    def join(sep: str, *args: Any) -> str:
        """
        将 *args* 用 *sep* 连接成一个字符串。

        每个元素通过 ``str()`` 转换为字符串。None 值表示为 ``""``。

        :param sep: 分隔符
        :param args: 待连接的值
        :return: 连接后的字符串
        """
        parts = []
        for arg in args:
            if arg is None:
                parts.append("")
            elif isinstance(arg, (list, tuple)):
                for item in arg:
                    parts.append("" if item is None else str(item))
            else:
                parts.append(str(arg))
        return sep.join(parts)

    @staticmethod
    def join_array(array: list, conjunction: str) -> str:
        """
        将 *array* 的元素用 *conjunction* 连接成一个字符串。

        :param array: 待连接的值列表
        :param conjunction: 分隔符
        :return: 连接后的字符串
        """
        if not array:
            return ""
        return conjunction.join(str(item) for item in array)

    # ------------------------------------------------------------------
    # Split
    # ------------------------------------------------------------------

    @staticmethod
    def split(
        string: Optional[str],
        separator: str,
        limit: int = -1,
        is_trim: bool = False,
        ignore_empty: bool = False,
    ) -> List[str]:
        """
        按 *separator* 分割 *string*，支持可选的裁剪和空元素移除。

        :param string: 源字符串
        :param separator: 分隔符字符串
        :param limit: 最大分割份数（类似 ``str.split(sep, n)``）。``-1`` 表示不限制
        :param is_trim: 是否裁剪每个部分
        :param ignore_empty: 是否移除空部分
        :return: 分割后的字符串列表
        """
        if CharSequenceUtil.is_empty(string):
            return []

        if limit == -1:
            parts = string.split(separator)  # type: ignore[union-attr]
        else:
            parts = string.split(separator, limit)  # type: ignore[union-attr]

        if is_trim:
            parts = [p.strip() for p in parts]
        if ignore_empty:
            parts = [p for p in parts if p != ""]
        return parts

    # ------------------------------------------------------------------
    # Pad
    # ------------------------------------------------------------------

    @staticmethod
    def pad(string: Optional[str], size: int, pad_str: str = " ", is_right: bool = True) -> str:
        """
        使用 *pad_str* 将 *string* 填充到 *size* 个字符。

        如果字符串已经至少 *size* 个字符，则原样返回。

        :param string: 源字符串
        :param size: 目标长度
        :param pad_str: 填充字符串（默认 ``" "``）
        :param is_right: True = 右侧填充（左对齐），False = 左侧填充（右对齐）
        :return: 填充后的字符串
        """
        if string is None:
            string = ""
        if len(pad_str) == 0:
            pad_str = " "
        if is_right:
            return string.ljust(size, pad_str)
        return string.rjust(size, pad_str)

    @staticmethod
    def center(string: Optional[str], size: int, pad_str: str = " ") -> str:
        """
        使用 *pad_str* 将 *string* 居中对齐到 *size* 个字符。

        :param string: 源字符串
        :param size: 目标长度
        :param pad_str: 填充字符串（默认 ``" "``）
        :return: 居中对齐后的字符串
        """
        if string is None:
            string = ""
        if len(pad_str) == 0:
            pad_str = " "
        return string.center(size, pad_str)

    # ------------------------------------------------------------------
    # Repeat
    # ------------------------------------------------------------------

    @staticmethod
    def repeat(string: Optional[str], count: int) -> str:
        """
        将 *string* 重复 *count* 次。

        :param string: 待重复的字符串
        :param count: 重复次数
        :return: 重复后的字符串
        """
        if CharSequenceUtil.is_empty(string) or count <= 0:
            return ""
        return string * count  # type: ignore[operator]

    @staticmethod
    def repeat_and_join(string: Optional[str], count: int, conjunction: str) -> str:
        """
        将 *string* 重复 *count* 次，每次重复之间用 *conjunction* 连接。

        :param string: 待重复的字符串
        :param count: 重复次数
        :param conjunction: 重复之间的分隔符
        :return: 重复并连接后的字符串
        """
        if CharSequenceUtil.is_empty(string) or count <= 0:
            return ""
        return conjunction.join([string] * count)  # type: ignore[list-item]

    # ------------------------------------------------------------------
    # Naming conversions
    # ------------------------------------------------------------------

    @staticmethod
    def to_camel_case(string: Optional[str]) -> Optional[str]:
        """
        将字符串转换为 camelCase（驼峰命名法）。

        支持 ``snake_case``、``kebab-case`` 和空格分隔的输入。

        Examples::

            "hello_world"  -> "helloWorld"
            "hello-world"  -> "helloWorld"
            "HELLO_WORLD"  -> "helloWorld"

        :param string: 源字符串
        :return: 驼峰命名的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string

        # split on underscores, hyphens, and spaces
        words = re.split(r"[_\- ]+", string)  # type: ignore[arg-type]
        if not words:
            return string

        result = words[0].lower()
        for word in words[1:]:
            if word:
                result += word[0].upper() + word[1:].lower()
        return result

    @staticmethod
    def to_snake_case(string: Optional[str]) -> Optional[str]:
        """
        将字符串转换为 snake_case（蛇形命名法）。

        支持 ``camelCase``、``PascalCase``、``kebab-case`` 和空格分隔的输入。

        Examples::

            "helloWorld"   -> "hello_world"
            "HelloWorld"   -> "hello_world"
            "hello-world"  -> "hello_world"

        :param string: 源字符串
        :return: 蛇形命名的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string

        # Replace hyphens and spaces with underscores
        s = re.sub(r"[\- ]+", "_", string)  # type: ignore[arg-type]

        # Insert underscore before uppercase letters preceded by lowercase
        s = re.sub(r"([a-z])([A-Z])", r"\1_\2", s)
        # Insert underscore between consecutive uppercase and following
        # lowercase (e.g. "HTMLParser" -> "HTML_Parser")
        s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)

        return s.lower()

    @staticmethod
    def to_under_score_case(string: Optional[str]) -> Optional[str]:
        """
        :meth:`to_snake_case` 的别名。

        :param string: 源字符串
        :return: 蛇形命名的字符串
        """
        return CharSequenceUtil.to_snake_case(string)

    # ------------------------------------------------------------------
    # Similarity
    # ------------------------------------------------------------------

    @staticmethod
    def similar(str1: Optional[str], str2: Optional[str], is_ignore_case: bool = False) -> float:
        """
        使用 Python 的 ``difflib.SequenceMatcher`` 计算两个字符串的相似度。
        返回 [0.0, 1.0] 之间的浮点数。

        :param str1: 第一个字符串
        :param str2: 第二个字符串
        :param is_ignore_case: 是否忽略大小写
        :return: 相似度比率（0.0 到 1.0）
        """
        if str1 is None and str2 is None:
            return 1.0
        if str1 is None or str2 is None:
            return 0.0
        s1 = str1.lower() if is_ignore_case else str1
        s2 = str2.lower() if is_ignore_case else str2
        return SequenceMatcher(None, s1, s2).ratio()

    # ------------------------------------------------------------------
    # Format with map
    # ------------------------------------------------------------------

    @staticmethod
    def format_with_map(template: str, map_: dict, ignore_null: bool = False) -> str:
        """
        通过将 ``{key}`` 占位符替换为 *map_* 中的值来格式化 *template*。

        如果 *ignore_null* 为 False 且键不存在，占位符保持不变。
        如果 *ignore_null* 为 True，缺失的键将被替换为空字符串。

        :param template: 包含 ``{key}`` 占位符的模板字符串
        :param map_: 映射键到替换值的字典
        :param ignore_null: 为 True 时，缺失的键替换为 ``""``
        :return: 格式化后的字符串
        """

        def _replacer(match: re.Match) -> str:
            key = match.group(1)
            if key in map_:
                return str(map_[key])
            if ignore_null:
                return ""
            return match.group(0)

        return re.sub(r"\{(\w+)\}", _replacer, template)

    # ------------------------------------------------------------------
    # Type checks
    # ------------------------------------------------------------------

    @staticmethod
    def is_numeric(string: Optional[str]) -> bool:
        """
        判断 *string* 是否全部由数字字符组成。
        允许前导 ``-`` 号（与 Java Hutool 的 ``StrUtil.isNumeric`` 对齐）。

        :param string: 待检查的字符串
        :return: 是否为数字字符串
        """
        if CharSequenceUtil.is_empty(string):
            return False
        s = string.lstrip("-")  # type: ignore[union-attr]
        if len(s) == 0:
            return False
        return s.isdigit()

    @staticmethod
    def is_number(string: Optional[str]) -> bool:
        """
        判断 *string* 是否表示有效的数字（整数或浮点数）。

        :param string: 待检查的字符串
        :return: 是否为有效数字
        """
        if CharSequenceUtil.is_empty(string):
            return False
        try:
            float(string)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_alpha(string: Optional[str]) -> bool:
        """
        判断 *string* 是否全部由字母组成。

        :param string: 待检查的字符串
        :return: 是否全部为字母
        """
        if CharSequenceUtil.is_empty(string):
            return False
        return string.isalpha()  # type: ignore[union-attr]

    @staticmethod
    def is_alpha_upper(string: Optional[str]) -> bool:
        """
        判断 *string* 是否全部由大写字母组成。

        :param string: 待检查的字符串
        :return: 是否全部为大写字母
        """
        if CharSequenceUtil.is_empty(string):
            return False
        return string.isalpha() and string.isupper()  # type: ignore[union-attr]

    @staticmethod
    def is_alpha_lower(string: Optional[str]) -> bool:
        """
        判断 *string* 是否全部由小写字母组成。

        :param string: 待检查的字符串
        :return: 是否全部为小写字母
        """
        if CharSequenceUtil.is_empty(string):
            return False
        return string.isalpha() and string.islower()  # type: ignore[union-attr]

    @staticmethod
    def only_digits(string: Optional[str]) -> str:
        """
        移除字符串中所有非数字字符，仅保留数字。

        :param string: 源字符串
        :return: 仅包含数字的字符串，输入为 None 时返回空字符串
        """
        if CharSequenceUtil.is_empty(string):
            return ""
        return re.sub(r"[^0-9]", "", string)  # type: ignore[arg-type]

    @staticmethod
    def de_umlaut(text: str) -> str:
        """
        将德语变音符号（äöüß等）转换为 ASCII 等价形式。

        例如 ``ä`` → ``ae``，``ö`` → ``oe``，``ü`` → ``ue``，``ß`` → ``ss``。

        :param text: 包含德语变音符号的文本
        :return: 转换后的 ASCII 文本
        :raises ValueError: 文本无法转换为 ASCII 时
        """
        import unicodedata as _ud

        _replacements = {
            "ä": "ae",  # ä
            "ö": "oe",  # ö
            "ü": "ue",  # ü
            "Ä": "Ae",  # Ä
            "Ö": "Oe",  # Ö
            "Ü": "Ue",  # Ü
            "ß": "ss",  # ß
        }
        for src, dst in _replacements.items():
            text = text.replace(src, dst)
        # 使用 NFKD 分解并去除组合字符
        text = _ud.normalize("NFKD", text)
        return text.encode("ascii", "ignore").decode("ascii")

    # ------------------------------------------------------------------
    # 全角半角转换
    # ------------------------------------------------------------------

    @staticmethod
    def full_to_half_width(text: str) -> str:
        """
        将全角字符转换为半角字符。

        仅转换 ASCII 可见字符范围（0x21~0x7E）和全角空格（0x3000）。

        Examples::

            "ＨｅｌｌｏＷｏｒｌｄ" -> "HelloWorld"
            "１２３" -> "123"

        :param text: 包含全角字符的文本
        :return: 转换后的半角文本
        """
        _FULL2HALF = dict((i + 0xFEE0, i) for i in range(0x21, 0x7F))
        _FULL2HALF[0x3000] = 0x20
        return text.translate(_FULL2HALF)

    @staticmethod
    def half_to_full_width(text: str) -> str:
        """
        将半角字符转换为全角字符。

        仅转换 ASCII 可见字符范围（0x21~0x7E）和空格（0x20）。

        Examples::

            "Hello" -> "Ｈｅｌｌｏ"
            "123" -> "１２３"

        :param text: 包含半角字符的文本
        :return: 转换后的全角文本
        """
        _HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
        _HALF2FULL[0x20] = 0x3000
        return text.translate(_HALF2FULL)

    # ------------------------------------------------------------------
    # Levenshtein 编辑距离
    # ------------------------------------------------------------------

    @staticmethod
    def levenshtein_distance(s: str, t: str) -> int:
        """
        计算两个字符串的 Levenshtein 编辑距离。

        编辑距离是指将一个字符串变换为另一个字符串所需的最少
        单字符编辑（插入、删除、替换）操作数。

        :param s: 第一个字符串
        :param t: 第二个字符串
        :return: 编辑距离（非负整数）
        """
        m, n = len(s), len(t)
        if m == 0:
            return n
        if n == 0:
            return m

        # 使用两行滚动数组优化空间
        prev = list(range(n + 1))
        curr = [0] * (n + 1)

        for i in range(m):
            curr[0] = i + 1
            for j in range(n):
                cost = 0 if s[i] == t[j] else 1
                curr[j + 1] = min(
                    curr[j] + 1,  # 插入
                    prev[j + 1] + 1,  # 删除
                    prev[j] + cost,  # 替换
                )
            prev, curr = curr, prev

        return prev[n]

    # ------------------------------------------------------------------
    # 中文字符/标点过滤
    # ------------------------------------------------------------------

    @staticmethod
    def filter_chinese(text: str) -> str:
        """
        移除字符串中的所有中文字符（Unicode 范围 ``\\u4e00-\\u9fa5``）。

        :param text: 源字符串
        :return: 移除中文字符后的字符串
        """
        return re.sub(r"[一-龥]", "", text)

    @staticmethod
    def filter_chinese_punctuations(text: str) -> str:
        """
        移除字符串中的中英文标点符号和多余空白。

        移除范围包括：英文标点 ``!@#$%^&*()`` 等，中文标点
        ``！，。？、（）：；《》""`` 等，以及制表符。

        :param text: 源字符串
        :return: 移除标点后的字符串
        """
        return re.sub(
            r"[+.!/_,$%^*(\"\'\-]+|"
            r"[、-〃〈-】〔-〟〽゠・！-／"
            r"：-＠［-｀｛-･ -⁯⸀-⹿"
            r"¡-¿‐-‧‰-⁞]+",
            "",
            text,
        )

    @staticmethod
    def left_space_count(text: str) -> int:
        """
        计算字符串前导空白字符数。

        空格计 1，Tab 计 4。

        :param text: 待检查的字符串
        :return: 前导空白字符数（等效空格数）

        ::

            >>> StrUtil.left_space_count('  hello')
            2
            >>> StrUtil.left_space_count('\\thello')
            4
        """
        count = 0
        for ch in text:
            if ch == " ":
                count += 1
            elif ch == "\t":
                count += 4
            else:
                break
        return count

    @staticmethod
    def find_all_indices(text: str, sub: str) -> List[int]:
        """
        查找子串在文本中所有出现的起始索引。

        无匹配时返回空列表。

        :param text: 待搜索的文本
        :param sub: 待查找的子串
        :return: 起始索引列表

        ::

            >>> StrUtil.find_all_indices('abcabc', 'b')
            [1, 4]
            >>> StrUtil.find_all_indices('abcabc', 'x')
            []
        """
        if CharSequenceUtil.is_empty(text) or CharSequenceUtil.is_empty(sub):
            return []
        indices: List[int] = []
        start = 0
        while True:
            idx = text.find(sub, start)
            if idx == -1:
                break
            indices.append(idx)
            start = idx + len(sub)
        return indices

    # ------------------------------------------------------------------
    # 比较与判断
    # ------------------------------------------------------------------

    @staticmethod
    def equals_any(string: Optional[str], *candidates: Optional[str]) -> bool:
        """
        判断 *string* 是否等于候选中的任一个。

        :param string: 待比较的字符串
        :param candidates: 候选字符串
        :return: 匹配任一候选返回 True
        """
        if string is None:
            return any(c is None for c in candidates)
        return any(string == c for c in candidates)

    @staticmethod
    def equals_any_ignore_case(string: Optional[str], *candidates: Optional[str]) -> bool:
        """
        判断 *string* 是否等于候选中的任一个（忽略大小写）。

        :param string: 待比较的字符串
        :param candidates: 候选字符串
        :return: 匹配任一候选返回 True
        """
        if string is None:
            return any(c is None for c in candidates)
        lower = string.lower()
        return any(c is not None and lower == c.lower() for c in candidates)

    @staticmethod
    def equals_char_at(string: Optional[str], index: int, char: str) -> bool:
        """
        判断 *string* 的第 *index* 个字符是否为 *char*。

        :param string: 待检查的字符串
        :param index: 字符索引
        :param char: 期望的字符
        :return: 是否匹配
        """
        if string is None or index < 0 or index >= len(string):
            return False
        return string[index] == char

    @staticmethod
    def contains_only(string: Optional[str], chars: str) -> bool:
        """
        判断 *string* 是否全部由 *chars* 中的字符组成。

        :param string: 待检查的字符串
        :param chars: 允许的字符集
        :return: 是否全部由指定字符组成
        """
        if CharSequenceUtil.is_empty(string):
            return False
        char_set = set(chars)
        return all(c in char_set for c in string)

    @staticmethod
    def has_letter(string: Optional[str]) -> bool:
        """
        判断 *string* 是否包含至少一个字母。

        :param string: 待检查的字符串
        :return: 是否包含字母
        """
        if string is None:
            return False
        return any(c.isalpha() for c in string)

    @staticmethod
    def is_sub_equals(
        string: Optional[str],
        sub: Optional[str],
        from_index: int = 0,
        ignore_case: bool = False,
    ) -> bool:
        """
        判断从 *from_index* 开始的子串是否等于 *sub*。

        :param string: 待检查的字符串
        :param sub: 期望的子串
        :param from_index: 起始索引
        :param ignore_case: 是否忽略大小写
        :return: 是否匹配
        """
        if string is None or sub is None:
            return string is None and sub is None
        if from_index < 0 or from_index > len(string):
            return False
        actual = string[from_index : from_index + len(sub)]
        if ignore_case:
            return actual.lower() == sub.lower()
        return actual == sub

    @staticmethod
    def is_surround(string: Optional[str], prefix: str, suffix: str) -> bool:
        """
        判断 *string* 是否以 *prefix* 开头且以 *suffix* 结尾。

        :param string: 待检查的字符串
        :param prefix: 前缀
        :param suffix: 后缀
        :return: 是否包裹
        """
        if string is None:
            return False
        return string.startswith(prefix) and string.endswith(suffix)

    @staticmethod
    def is_wrap(string: Optional[str], wrap: str) -> bool:
        """
        判断 *string* 是否被 *wrap* 包裹（前后相同）。

        :param string: 待检查的字符串
        :param wrap: 包裹字符/串
        :return: 是否被包裹
        """
        if string is None:
            return False
        return string.startswith(wrap) and string.endswith(wrap) and len(string) >= len(wrap) * 2

    @staticmethod
    def is_lower_case(string: Optional[str]) -> bool:
        """
        判断 *string* 是否全部为小写（至少一个字母）。

        :param string: 待检查的字符串
        :return: 是否全小写
        """
        if CharSequenceUtil.is_empty(string):
            return False
        return string == string.lower() and any(c.isalpha() for c in string)

    @staticmethod
    def is_upper_case(string: Optional[str]) -> bool:
        """
        判断 *string* 是否全部为大写（至少一个字母）。

        :param string: 待检查的字符串
        :return: 是否全大写
        """
        if CharSequenceUtil.is_empty(string):
            return False
        return string == string.upper() and any(c.isalpha() for c in string)

    @staticmethod
    def is_all_char_match(string: Optional[str], match_func: Callable[[str], bool]) -> bool:
        """
        判断 *string* 的所有字符是否都满足 *match_func*。

        :param string: 待检查的字符串
        :param match_func: 匹配函数
        :return: 是否全部匹配
        """
        if CharSequenceUtil.is_empty(string):
            return False
        return all(match_func(c) for c in string)

    # ------------------------------------------------------------------
    # 公共前缀/后缀 & 比较
    # ------------------------------------------------------------------

    @staticmethod
    def common_prefix(*strings: Optional[str]) -> str:
        """
        返回多个字符串的最长公共前缀。

        :param strings: 字符串列表
        :return: 公共前缀
        """
        valid = [s for s in strings if s is not None]
        if not valid:
            return ""
        prefix = valid[0]
        for s in valid[1:]:
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ""
        return prefix

    @staticmethod
    def common_suffix(*strings: Optional[str]) -> str:
        """
        返回多个字符串的最长公共后缀。

        :param strings: 字符串列表
        :return: 公共后缀
        """
        valid = [s for s in strings if s is not None]
        if not valid:
            return ""
        suffix = valid[0]
        for s in valid[1:]:
            while not s.endswith(suffix):
                suffix = suffix[1:]
                if not suffix:
                    return ""
        return suffix

    @staticmethod
    def compare(string1: Optional[str], string2: Optional[str], null_is_greater: bool = False) -> int:
        """
        null-safe 的字符串比较。

        :param string1: 字符串1
        :param string2: 字符串2
        :param null_is_greater: None 是否视为更大
        :return: 负数/0/正数
        """
        if string1 == string2:
            return 0
        if string1 is None:
            return 1 if null_is_greater else -1
        if string2 is None:
            return -1 if null_is_greater else 1
        return (string1 > string2) - (string1 < string2)

    @staticmethod
    def compare_ignore_case(string1: Optional[str], string2: Optional[str], null_is_greater: bool = False) -> int:
        """
        null-safe 忽略大小写的字符串比较。

        :param string1: 字符串1
        :param string2: 字符串2
        :param null_is_greater: None 是否视为更大
        :return: 负数/0/正数
        """
        if string1 == string2:
            return 0
        if string1 is None:
            return 1 if null_is_greater else -1
        if string2 is None:
            return -1 if null_is_greater else 1
        s1 = string1.lower()
        s2 = string2.lower()
        return (s1 > s2) - (s1 < s2)

    @staticmethod
    def concat(*strings: Optional[str]) -> str:
        """
        拼接多个字符串，None 视为空串。

        :param strings: 字符串列表
        :return: 拼接结果
        """
        return "".join("" if s is None else s for s in strings)

    # ------------------------------------------------------------------
    # 截取与格式化
    # ------------------------------------------------------------------

    @staticmethod
    def brief(string: Optional[str], max_length: int) -> Optional[str]:
        """
        截断 *string* 到 *max_length*，超出部分用 ``...`` 替代。
        总长度不超过 *max_length*。

        :param string: 待截断的字符串
        :param max_length: 最大总长度（含省略号）
        :return: 截断后的字符串
        """
        if string is None:
            return None
        if max_length < 4:
            return string[:max_length]
        if len(string) <= max_length:
            return string
        return string[: max_length - 3] + "..."

    @staticmethod
    def max_length(string: Optional[str], max_length: int) -> Optional[str]:
        """
        强制截断 *string* 到 *max_length* 长度。

        :param string: 待截断的字符串
        :param max_length: 最大长度
        :return: 截断后的字符串
        """
        if string is None:
            return None
        if len(string) > max_length:
            return string[:max_length]
        return string

    @staticmethod
    def fix_length(string: Optional[str], fixed_length: int, pad_char: str = " ") -> str:
        """
        将 *string* 填充或截断到 *fixed_length*。

        - 长度不足时右侧用 *pad_char* 填充
        - 长度超出时截断

        :param string: 待处理的字符串
        :param fixed_length: 固定长度
        :param pad_char: 填充字符
        :return: 固定长度的字符串
        """
        if string is None:
            return pad_char * fixed_length
        if len(string) < fixed_length:
            return string.ljust(fixed_length, pad_char)
        if len(string) > fixed_length:
            return string[:fixed_length]
        return string

    @staticmethod
    def hide(string: Optional[str], start: int, end: int) -> Optional[str]:
        """
        隐藏 *string* 中 *start* 到 *end* 索引的字符，用 ``*`` 替代。

        :param string: 待处理的字符串
        :param start: 起始索引（含）
        :param end: 结束索引（不含）
        :return: 隐藏后的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        chars = list(string)
        for i in range(max(0, start), min(len(chars), end)):
            chars[i] = "*"
        return "".join(chars)

    @staticmethod
    def move(string: Optional[str], start: int, end: int, move_length: int) -> Optional[str]:
        """
        移动 *string* 中 *start* 到 *end* 区间的字符 *move_length* 位。
        正数右移，负数左移。

        :param string: 待处理的字符串
        :param start: 起始索引（含）
        :param end: 结束索引（不含）
        :param move_length: 移动长度
        :return: 移动后的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        if start < 0:
            start = 0
        if end > len(string):
            end = len(string)
        if start >= end:
            return string
        chars = list(string)
        segment = chars[start:end]
        remaining = chars[:start] + chars[end:]
        insert_pos = start + move_length
        insert_pos = max(0, min(insert_pos, len(remaining)))
        result = remaining[:insert_pos] + segment + remaining[insert_pos:]
        return "".join(result)

    @staticmethod
    def normalize(string: Optional[str]) -> Optional[str]:
        """
        合并连续空白为单个空格，并去除首尾空白。

        :param string: 待规范化的字符串
        :return: 规范化后的字符串
        """
        if string is None:
            return None
        return " ".join(string.split())

    @staticmethod
    def total_length(*strings: Optional[str]) -> int:
        """
        计算多个字符串的总长度。

        :param strings: 字符串列表
        :return: 总长度
        """
        return sum(len(s) for s in strings if s is not None)

    @staticmethod
    def indexed_format(template: str, *args: Any) -> str:
        """
        使用索引格式化模板，如 ``"{0} + {1} = {2}"``。

        :param template: 模板字符串
        :param args: 位置参数
        :return: 格式化后的字符串
        """
        result = template
        for i, arg in enumerate(args):
            result = result.replace("{" + str(i) + "}", str(arg))
        return result

    # ------------------------------------------------------------------
    # 包裹与填充
    # ------------------------------------------------------------------

    @staticmethod
    def wrap(string: Optional[str], prefix: str, suffix: Optional[str] = None) -> Optional[str]:
        """
        包裹 *string*。如果只传一个包裹参数，前后相同。

        :param string: 待包裹的字符串
        :param prefix: 前缀
        :param suffix: 后缀（默认同前缀）
        :return: 包裹后的字符串
        """
        if string is None:
            return None
        if suffix is None:
            suffix = prefix
        return prefix + string + suffix

    @staticmethod
    def wrap_if_missing(string: Optional[str], prefix: str, suffix: Optional[str] = None) -> Optional[str]:
        """
        仅在缺失时包裹 *string*。

        :param string: 待检查的字符串
        :param prefix: 前缀
        :param suffix: 后缀（默认同前缀）
        :return: 包裹后的字符串
        """
        if string is None:
            return None
        if suffix is None:
            suffix = prefix
        result = string
        if not result.startswith(prefix):
            result = prefix + result
        if not result.endswith(suffix):
            result = result + suffix
        return result

    @staticmethod
    def wrap_all(arr: Optional[list], prefix: str, suffix: Optional[str] = None) -> Optional[list]:
        """
        包裹列表中每个元素。

        :param arr: 字符串列表
        :param prefix: 前缀
        :param suffix: 后缀（默认同前缀）
        :return: 包裹后的列表
        """
        if arr is None:
            return None
        if suffix is None:
            suffix = prefix
        return [prefix + s + suffix if s is not None else s for s in arr]

    @staticmethod
    def wrap_all_if_missing(arr: Optional[list], prefix: str, suffix: Optional[str] = None) -> Optional[list]:
        """
        仅在缺失时包裹列表中每个元素。

        :param arr: 字符串列表
        :param prefix: 前缀
        :param suffix: 后缀（默认同前缀）
        :return: 包裹后的列表
        """
        if arr is None:
            return None
        if suffix is None:
            suffix = prefix
        return [CharSequenceUtil.wrap_if_missing(s, prefix, suffix) if s is not None else s for s in arr]

    @staticmethod
    def pad_after(string: Optional[str], length: int, pad_char: str = " ") -> Optional[str]:
        """
        右填充 *string* 到 *length*。

        :param string: 待填充的字符串
        :param length: 目标长度
        :param pad_char: 填充字符
        :return: 填充后的字符串
        """
        if string is None:
            return pad_char * length
        return string.ljust(length, pad_char)

    @staticmethod
    def pad_pre(string: Optional[str], length: int, pad_char: str = " ") -> Optional[str]:
        """
        左填充 *string* 到 *length*。

        :param string: 待填充的字符串
        :param length: 目标长度
        :param pad_char: 填充字符
        :return: 填充后的字符串
        """
        if string is None:
            return pad_char * length
        return string.rjust(length, pad_char)

    @staticmethod
    def repeat_by_length(string: Optional[str], length: int) -> Optional[str]:
        """
        重复 *string* 直到达到 *length* 长度（截断多余部分）。

        :param string: 待重复的字符串
        :param length: 目标长度
        :return: 重复后的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        repeat_count = (length + len(string) - 1) // len(string)
        return (string * repeat_count)[:length]

    # ------------------------------------------------------------------
    # 替换与移除
    # ------------------------------------------------------------------

    @staticmethod
    def replace_ignore_case(string: Optional[str], search_str: str, replacement: str) -> Optional[str]:
        """
        忽略大小写替换所有匹配。

        :param string: 待处理的字符串
        :param search_str: 搜索字符串
        :param replacement: 替换字符串
        :return: 替换后的字符串
        """
        if CharSequenceUtil.is_empty(string) or CharSequenceUtil.is_empty(search_str):
            return string
        pattern = re.compile(re.escape(search_str), re.IGNORECASE)
        return pattern.sub(replacement, string)

    @staticmethod
    def replace_last(string: Optional[str], regex: str, replacement: str) -> Optional[str]:
        """
        替换最后一个正则匹配。

        :param string: 待处理的字符串
        :param regex: 正则表达式
        :param replacement: 替换字符串
        :return: 替换后的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        pattern = re.compile(regex)
        matches = list(pattern.finditer(string))
        if not matches:
            return string
        last = matches[-1]
        return string[: last.start()] + replacement + string[last.end() :]

    @staticmethod
    def remove_all_prefix(string: Optional[str], prefix: Optional[str]) -> Optional[str]:
        """
        移除所有匹配的前缀（循环移除）。

        :param string: 待处理的字符串
        :param prefix: 前缀
        :return: 移除前缀后的字符串
        """
        if CharSequenceUtil.is_empty(string) or CharSequenceUtil.is_empty(prefix):
            return string
        while string.startswith(prefix):
            string = string[len(prefix) :]
        return string

    @staticmethod
    def remove_all_suffix(string: Optional[str], suffix: Optional[str]) -> Optional[str]:
        """
        移除所有匹配的后缀（循环移除）。

        :param string: 待处理的字符串
        :param suffix: 后缀
        :return: 移除后缀后的字符串
        """
        if CharSequenceUtil.is_empty(string) or CharSequenceUtil.is_empty(suffix):
            return string
        while string.endswith(suffix):
            string = string[: -len(suffix)]
        return string

    @staticmethod
    def remove_suf_and_lower_first(string: Optional[str], suffix: Optional[str]) -> Optional[str]:
        """
        移除后缀并将首字母转为小写。

        :param string: 待处理的字符串
        :param suffix: 后缀
        :return: 处理后的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        result = string
        if suffix and result.endswith(suffix):
            result = result[: -len(suffix)]
        return CharSequenceUtil.lower_first(result)

    # ------------------------------------------------------------------
    # 分割与转换
    # ------------------------------------------------------------------

    @staticmethod
    def split_trim(string: Optional[str], separator: str = ",") -> List[str]:
        """
        按 *separator* 分割 *string* 并 trim 每一部分。

        :param string: 待分割的字符串
        :param separator: 分隔符
        :return: 分割并 trim 后的列表
        """
        if CharSequenceUtil.is_empty(string):
            return []
        return [part.strip() for part in string.split(separator)]

    @staticmethod
    def strip_all(*strings: Optional[str]) -> List[Optional[str]]:
        """
        对多个字符串执行 strip。

        :param strings: 字符串列表
        :return: strip 后的列表
        """
        return [s.strip() if s is not None else None for s in strings]

    @staticmethod
    def swap_case(string: Optional[str]) -> Optional[str]:
        """
        大小写互转。

        :param string: 待转换的字符串
        :return: 转换后的字符串
        """
        if string is None:
            return None
        return string.swapcase()

    @staticmethod
    def to_symbol_case(string: Optional[str], symbol: str = "-") -> Optional[str]:
        """
        将驼峰命名转换为符号分隔命名（如 kebab-case）。

        :param string: 待转换的字符串
        :param symbol: 分隔符号
        :return: 转换后的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        # 先转下划线格式再替换
        result = re.sub(r"([A-Z])", lambda m: symbol + m.group(1).lower(), string)
        # 处理可能的前导分隔符
        result = result.lstrip(symbol)
        # 统一已有的下划线/连字符
        result = result.replace("_", symbol).replace("-", symbol)
        # 移除连续的分隔符
        while symbol * 2 in result:
            result = result.replace(symbol * 2, symbol)
        return result

    @staticmethod
    def trim_to_null(string: Optional[str]) -> Optional[str]:
        """
        trim 后如果为空返回 None。

        :param string: 待处理的字符串
        :return: trim 后的字符串或 None
        """
        if string is None:
            return None
        result = string.strip()
        return result if result else None

    # ------------------------------------------------------------------
    # 空值处理 & 杂项
    # ------------------------------------------------------------------

    @staticmethod
    def empty_if_null(string: Optional[str]) -> str:
        """
        如果 *string* 为 None，返回空串。与 :meth:`empty_if_none` 相同。

        :param string: 待检查的字符串
        :return: 非 None 的字符串
        """
        return "" if string is None else string

    @staticmethod
    def desensitized(string: Optional[str], start_len: int, end_len: int) -> Optional[str]:
        """
        脱敏：保留前 *start_len* 和后 *end_len* 个字符，中间用 ``*`` 替代。

        :param string: 待脱敏的字符串
        :param start_len: 前面保留的长度
        :param end_len: 后面保留的长度
        :return: 脱敏后的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        length = len(string)
        if start_len + end_len >= length:
            return "*" * length
        return string[:start_len] + "*" * (length - start_len - end_len) + string[length - end_len :]

    @staticmethod
    def compare_version(version1: Optional[str], version2: Optional[str]) -> int:
        """
        比较两个版本号字符串（如 "1.2.3" vs "1.2.4"）。

        :param version1: 版本号1
        :param version2: 版本号2
        :return: 负数/0/正数
        """
        if version1 == version2:
            return 0
        if version1 is None:
            return -1
        if version2 is None:
            return 1
        parts1 = version1.split(".")
        parts2 = version2.split(".")
        max_len = max(len(parts1), len(parts2))
        for i in range(max_len):
            v1 = int(parts1[i]) if i < len(parts1) else 0
            v2 = int(parts2[i]) if i < len(parts2) else 0
            if v1 != v2:
                return 1 if v1 > v2 else -1
        return 0


# ---------------------------------------------------------------------------
# StrPool
# ---------------------------------------------------------------------------
class StrPool(CharPool):
    """常用字符串常量。"""

    # 字符串常量：'None'
    NONE: str = "None"
    # 字符串常量：双点 "..",
    # 用途：作为指向上级文件夹的路径，如："../path"
    DOUBLE_DOT: str = ".."
    # 字符串常量：Windows 换行 "\r\n"
    CRLF: str = "\r\n"
    # 字符串常量：HTML 不间断空格转义 "&nbsp;"
    HTML_NBSP: str = "&nbsp;"
    # 字符串常量：HTML And 符转义 "&amp;"
    HTML_AMP: str = "&amp;"
    # 字符串常量：HTML 双引号转义 "&quot;"
    HTML_QUOTE: str = "&quot;"
    # 字符串常量：HTML 单引号转义 "&apos;"
    HTML_APOS: str = "&apos;"
    # 字符串常量：HTML 小于号转义 "&lt;"
    HTML_LT: str = "&lt;"
    # 字符串常量：HTML 大于号转义 "&gt;"
    HTML_GT: str = "&gt;"
    # 字符串常量：空 JSON "{}"
    EMPTY_JSON: str = "{}"


# ---------------------------------------------------------------------------
# StrUtil
# ---------------------------------------------------------------------------
class StrUtil(CharSequenceUtil, StrPool):
    """
    主字符串工具类。继承 :class:`CharSequenceUtil` 和 :class:`StrPool`，
    提供所有字符串操作的统一入口。
    """

    @staticmethod
    def is_blank_if_str(obj: Any) -> bool:
        """
        如果 *obj* 是字符串，判断其是否为空白。非字符串对象返回 False（None 返回 True）。

        :param obj: 待检查的对象
        :return: *obj* 为 None 或为空白字符串时返回 True
        """
        if obj is None:
            return True
        elif isinstance(obj, str):
            return CharSequenceUtil.is_blank(obj)
        return False

    @staticmethod
    def is_empty_if_str(obj: Any) -> bool:
        """
        如果 *obj* 是字符串，判断其是否为空。非字符串对象返回 False（None 返回 True）。

        :param obj: 待检查的对象
        :return: *obj* 为 None 或为空字符串时返回 True
        """
        if obj is None:
            return True
        elif isinstance(obj, str):
            return CharSequenceUtil.is_empty(obj)
        return False

    @staticmethod
    def trim(
        string: Union[List[str], str, None],
        mode: int = 0,
        predicate: Callable[[str], bool] = CharUtil.is_blank_char,
    ) -> Union[str, None]:
        """
        裁剪字符串，或就地裁剪字符串列表中的每个元素。

        :param string: 字符串或字符串列表
        :param mode: ``-1`` = 仅裁剪头部，``0`` = 两端裁剪，``1`` = 仅裁剪尾部
        :param predicate: 返回 True 时表示该字符应被移除的函数
        :return: 裁剪后的字符串或 None
        """
        if isinstance(string, str):
            return CharSequenceUtil.trim(string, mode=mode, predicate=predicate)

        if string is None:
            return None
        for i in range(len(string)):
            s = string[i]
            if s is not None:
                string[i] = CharSequenceUtil.trim(s)  # type: ignore[index]
        return None

    @staticmethod
    def to_str(obj: Any, charset: str = "utf-8") -> Optional[str]:
        """
        将 *obj* 转换为字符串。

        ``bytes``/``bytearray``/``array.array`` 使用 *charset* 解码。列表会递归转换。

        :param obj: 待转换的对象
        :param charset: 字符编码
        :return: 字符串表示
        """
        if obj is None:
            return None

        if isinstance(obj, str):
            return obj
        elif isinstance(obj, (bytes, bytearray, array.array)):
            return obj.decode(charset)
        elif isinstance(obj, memoryview):
            return obj.tobytes().decode(charset)
        elif isinstance(obj, list):
            return str(StrUtil.to_str(item, charset=charset) for item in obj)
        return str(obj)

    @staticmethod
    def to_str_or_none(obj: Any) -> Optional[str]:
        """
        将 *obj* 转换为字符串，None 输入返回 None。

        :param obj: 待转换的对象
        :return: 字符串表示或 None
        """
        return None if obj is None else str(obj)

    @staticmethod
    def reverse(string: Optional[str]) -> Optional[str]:
        """
        反转 *string*。

        :param string: 待反转的字符串
        :return: 反转后的字符串
        """
        if CharSequenceUtil.is_empty(string):
            return string
        return string[::-1]  # type: ignore[index]

    @staticmethod
    def fill_before(string: Optional[str], filled_char: str, length: int) -> Optional[str]:
        """
        使用 *filled_char* 将 *string* 左侧填充到 *length*。

        :param string: 待填充的字符串
        :param filled_char: 单个填充字符
        :param length: 目标长度
        :return: 填充后的字符串
        """
        return StrUtil.fill(string, filled_char, length, True)

    @staticmethod
    def fill_after(string: Optional[str], filled_char: str, length: int) -> Optional[str]:
        """
        使用 *filled_char* 将 *string* 右侧填充到 *length*。

        :param string: 待填充的字符串
        :param filled_char: 单个填充字符
        :param length: 目标长度
        :return: 填充后的字符串
        """
        return StrUtil.fill(string, filled_char, length, False)

    @staticmethod
    def fill(string: Optional[str], filled_char: str, length: int, is_pre: bool) -> Optional[str]:
        """
        使用 *filled_char* 将 *string* 填充到 *length*，
        可选择左侧填充（``is_pre=True``）或右侧填充（``is_pre=False``）。

        :param string: 待填充的字符串
        :param filled_char: 单个填充字符
        :param length: 目标长度
        :param is_pre: 是否左侧填充
        :return: 填充后的字符串
        :raises TypeError: *filled_char* 不是单个字符时抛出异常
        """
        if CharSequenceUtil.is_empty(filled_char):
            return string
        if len(filled_char) > 1:
            raise TypeError("The fill character must be exactly one character long")
        if string is None:
            return filled_char * length
        if is_pre:
            return string.rjust(length, filled_char)
        return string.ljust(length, filled_char)

    @staticmethod
    def format(template: str, *args: Any, **kwargs: Any) -> str:
        """
        使用 Python 的 ``str.format()`` 格式化 *template*。

        :param template: 模板字符串
        :param args: 位置参数
        :param kwargs: 关键字参数
        :return: 格式化后的字符串
        """
        return template.format(*args, **kwargs)

    @staticmethod
    def truncate_utf8(string: Optional[str], max_bytes: int) -> Optional[str]:
        """
        截断 *string* 使其 UTF-8 编码不超过 *max_bytes*。
        截断时会附加省略号（``...``）。

        :param string: 待截断的字符串
        :param max_bytes: 最大字节长度
        :return: 截断后的字符串
        """
        return StrUtil.truncate_by_byte_length(string, "utf-8", max_bytes, 4, True)

    @staticmethod
    def truncate_by_byte_length(
        string: Optional[str],
        charset: str,
        max_bytes: int,
        factor: int,
        append_dots: bool,
    ) -> Optional[str]:
        """
        截断 *string* 使其编码字节长度不超过 *max_bytes*。

        *factor* 是速度估计除数（编码中单个字符的最大字节长度）。

        :param string: 待截断的字符串
        :param charset: 字符编码
        :param max_bytes: 最大字节长度
        :param factor: 速度估计除数
        :param append_dots: 截断后是否附加 ``...``
        :return: 截断后的字符串
        """
        if string is None or len(string) * factor <= max_bytes:
            return string

        sba = string.encode(charset)
        if len(sba) <= max_bytes:
            return string

        limit_bytes = max_bytes
        if append_dots:
            limit_bytes -= len("...".encode(charset))

        bb = sba[:limit_bytes]
        decoder = codecs.getincrementaldecoder(charset)(errors="ignore")
        result = decoder.decode(bb, final=True)

        if append_dots:
            return result + "..."

        return result
