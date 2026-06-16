import re
from typing import List


class UnicodeUtil:
    """Unicode工具类"""

    @staticmethod
    def to_unicode(string: str) -> str:
        """字符串转Unicode，如 "中文" -> "\\u4e2d\\u6587"

        :param string: 原始字符串
        :return: Unicode转义后的字符串
        """
        return string.encode("unicode_escape").decode("ascii")

    @staticmethod
    def from_unicode(unicode_str: str) -> str:
        """Unicode转字符串，如 "\\u4e2d\\u6587" -> "中文"

        :param unicode_str: Unicode转义字符串
        :return: 解码后的原始字符串
        """
        return unicode_str.encode("ascii").decode("unicode_escape")

    @staticmethod
    def escape(content: str) -> str:
        """转义非ASCII字符为Unicode

        将字符串中所有非ASCII字符转换为 \\uXXXX 格式的Unicode转义序列，
        ASCII字符保持不变。

        :param content: 原始字符串
        :return: 转义后的字符串
        """
        result: List[str] = []
        for ch in content:
            if ord(ch) > 127:
                result.append(f"\\u{ord(ch):04x}")
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def unescape(content: str) -> str:
        """反转义Unicode字符

        将字符串中的 \\uXXXX 格式的Unicode转义序列还原为实际字符，
        同时支持 \\uXXXXX 等五位及以上的Unicode码点。

        :param content: 包含Unicode转义序列的字符串
        :return: 还原后的原始字符串
        """

        def _replace(match: re.Match) -> str:
            return chr(int(match.group(1), 16))

        return re.sub(r"\\u([0-9a-fA-F]{4,})", _replace, content)

    @staticmethod
    def to_string(unicode_str: str) -> str:
        """Unicode 转义字符串还原为中文等字符。

        将 ``\\uXXXX`` 格式的序列转为实际字符。
        与 :meth:`unescape` 功能相同。

        :param unicode_str: Unicode 转义字符串
        :return: 还原后的字符串
        """
        return UnicodeUtil.unescape(unicode_str)

    @staticmethod
    def to_unicode_string(s: str) -> str:
        """将字符串转为 Unicode 转义格式。

        非 ASCII 字符转为 ``\\uXXXX``，ASCII 字符保持不变。
        与 :meth:`escape` 功能相同。

        :param s: 原始字符串
        :return: Unicode 转义后的字符串
        """
        return UnicodeUtil.escape(s)
