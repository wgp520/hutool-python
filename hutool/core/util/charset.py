"""字符集工具类"""

from __future__ import annotations

import locale
import sys


class CharsetUtil:
    """字符集工具类，提供字符集转换和常量定义。"""

    UTF_8 = "utf-8"
    """UTF-8 字符集"""
    GBK = "gbk"
    """GBK 字符集"""
    ISO_8859_1 = "iso-8859-1"
    """ISO-8859-1 字符集"""
    US_ASCII = "us-ascii"
    """US-ASCII 字符集"""

    @staticmethod
    def charset(charset_name: str) -> str:
        """
        获取字符集名称，为 None 时返回 UTF-8。

        :param charset_name: 字符集名称
        :return: 处理后的字符集名称（小写）
        """
        if charset_name is None:
            return CharsetUtil.UTF_8
        return charset_name.lower()

    @staticmethod
    def default_charset() -> str:
        """
        获取系统默认字符集。

        :return: 系统默认字符集名称
        """
        # 优先使用preferredencoding，回退到locale
        encoding = sys.getdefaultencoding()
        if encoding:
            return encoding
        loc = locale.getpreferredencoding(False)
        return loc if loc else CharsetUtil.UTF_8

    @staticmethod
    def convert(source: bytes, src_charset: str, dest_charset: str) -> bytes:
        """
        将字节数据从源字符集转为目标字符集。

        :param source: 待转码的字节数据
        :param src_charset: 源字符集
        :param dest_charset: 目标字符集
        :return: 转码后的字节数据
        :raises UnicodeDecodeError: 源数据无法用 src_charset 解码时
        :raises UnicodeEncodeError: 文本无法用 dest_charset 编码时
        """
        if src_charset is None:
            src_charset = CharsetUtil.UTF_8
        if dest_charset is None:
            dest_charset = CharsetUtil.UTF_8
        text = source.decode(src_charset)
        return text.encode(dest_charset)

    @staticmethod
    def convert_str(source: str, src_charset: str, dest_charset: str) -> str:
        """
        将字符串从源字符集转码为目标字符集。

        :param source: 待转码的字符串
        :param src_charset: 源字符集
        :param dest_charset: 目标字符集
        :return: 转码后的字符串
        :raises UnicodeEncodeError: 字符串无法用 src_charset 编码时
        :raises UnicodeDecodeError: 字节无法用 dest_charset 解码时
        """
        if src_charset is None:
            src_charset = CharsetUtil.UTF_8
        if dest_charset is None:
            dest_charset = CharsetUtil.UTF_8
        byte_data = source.encode(src_charset)
        return byte_data.decode(dest_charset)

    @staticmethod
    def clean_bom(content: str) -> str:
        """
        清理字符串开头的 BOM 标记（``\\ufeff``）。

        :param content: 待清理的字符串
        :return: 去除 BOM 后的字符串
        """
        # UTF-8 BOM:
        if content and content[0] == "﻿":
            return content[1:]
        return content

    @staticmethod
    def clean_invalid(content: str) -> str:
        """
        清除字符串中的无效控制字符（ASCII 0x00~0x1F 中除 \\t、\\n、\\r 以外的字符）。

        :param content: 待清理的字符串
        :return: 清除无效字符后的字符串
        """
        if not content:
            return content or ""
        # 保留 \t(0x09) \n(0x0A) \r(0x0D)，清除其余 0x00~0x1F 控制字符
        return "".join(ch for ch in content if ord(ch) >= 0x20 or ch in ("\t", "\n", "\r"))

    @staticmethod
    def parse(charset_name: str) -> str:
        """解析字符集名称，None 或空时返回 UTF-8。

        :param charset_name: 字符集名称
        :return: 字符集名称（小写）
        """
        if not charset_name:
            return CharsetUtil.UTF_8
        return charset_name.lower().strip()

    @staticmethod
    def convert_file(src_file: str, dest_file: str, src_charset: str, dest_charset: str) -> str:
        """转换文件字符集。

        :param src_file: 源文件路径
        :param dest_file: 目标文件路径
        :param src_charset: 源字符集
        :param dest_charset: 目标字符集
        :return: 目标文件路径
        """
        with open(src_file, "rb") as f:
            content = f.read()
        converted = CharsetUtil.convert(content, src_charset, dest_charset)
        with open(dest_file, "wb") as f:
            f.write(converted)
        return dest_file

    @staticmethod
    def system_charset_name() -> str:
        """获取系统字符集名称。

        :return: 系统字符集名称
        """
        return sys.getdefaultencoding() or CharsetUtil.UTF_8

    @staticmethod
    def default_charset_name() -> str:
        """获取默认字符集名称（同 system_charset_name）。

        :return: 默认字符集名称
        """
        return CharsetUtil.system_charset_name()

    @staticmethod
    def detect_charset(data: bytes) -> str:
        """简单检测字节数据的字符集。

        通过检查 BOM 标记判断编码，无法判断时返回 UTF-8。

        :param data: 字节数据
        :return: 检测到的字符集名称
        """
        if data[:3] == b"\xef\xbb\xbf":
            return "utf-8-sig"
        if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
            return "utf-16"
        if data[:4] in (b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff"):
            return "utf-32"
        return CharsetUtil.UTF_8
