"""字符集工具类"""

from __future__ import annotations

import locale
import sys


class CharsetUtil:
    """字符集工具类"""

    UTF_8 = "utf-8"
    GBK = "gbk"
    ISO_8859_1 = "iso-8859-1"
    US_ASCII = "us-ascii"

    @staticmethod
    def charset(charset_name: str) -> str:
        """获取字符集名称，None返回UTF-8"""
        if charset_name is None:
            return CharsetUtil.UTF_8
        return charset_name.lower()

    @staticmethod
    def default_charset() -> str:
        """获取系统默认字符集"""
        # 优先使用preferredencoding，回退到locale
        encoding = sys.getdefaultencoding()
        if encoding:
            return encoding
        loc = locale.getpreferredencoding(False)
        return loc if loc else CharsetUtil.UTF_8

    @staticmethod
    def convert(source: bytes, src_charset: str, dest_charset: str) -> bytes:
        """字节数据转码"""
        if src_charset is None:
            src_charset = CharsetUtil.UTF_8
        if dest_charset is None:
            dest_charset = CharsetUtil.UTF_8
        text = source.decode(src_charset)
        return text.encode(dest_charset)

    @staticmethod
    def convert_str(source: str, src_charset: str, dest_charset: str) -> str:
        """字符串转码"""
        if src_charset is None:
            src_charset = CharsetUtil.UTF_8
        if dest_charset is None:
            dest_charset = CharsetUtil.UTF_8
        byte_data = source.encode(src_charset)
        return byte_data.decode(dest_charset)

    @staticmethod
    def clean_bom(content: str) -> str:
        """清理BOM头"""
        # UTF-8 BOM:
        if content and content[0] == "﻿":
            return content[1:]
        return content
