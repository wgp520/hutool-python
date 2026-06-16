"""Base32 编解码工具类"""

import base64

# Base32 Extended Hex 字母表
_HEX_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUV"
_HEX_DECODE_MAP = {c: i for i, c in enumerate(_HEX_ALPHABET)}


def _b32hex_encode(data: bytes) -> str:
    """手动实现 Base32 Hex 编码。"""
    result = []
    for i in range(0, len(data), 5):
        chunk = data[i : i + 5]
        # 将最多 5 字节转为 40 位整数
        n = 0
        for b in chunk:
            n = (n << 8) | b
        # 计算填充位数
        pad_bits = (5 - len(chunk)) * 8
        n <<= pad_bits
        # 提取 8 个 5-bit 组
        num_groups = (len(chunk) * 8 + 4) // 5
        for j in range(num_groups):
            shift = 35 - j * 5
            idx = (n >> shift) & 0x1F
            result.append(_HEX_ALPHABET[idx])
    return "".join(result)


def _b32hex_decode(s: str) -> bytes:
    """手动实现 Base32 Hex 解码。"""
    s = s.rstrip("=").upper()
    result = bytearray()
    for i in range(0, len(s), 8):
        chunk = s[i : i + 8]
        n = 0
        for c in chunk:
            n = (n << 5) | _HEX_DECODE_MAP[c]
        # 每组 8 字符 = 40 bits = 5 bytes
        num_bytes = (len(chunk) * 5) // 8
        for j in range(num_bytes):
            shift = 32 - j * 8
            result.append((n >> shift) & 0xFF)
    return bytes(result)


class Base32Util:
    """Base32 编解码工具类。"""

    @staticmethod
    def encode(data) -> str:
        """Base32 编码。

        :param data: 待编码的 bytes 或 str
        :return: Base32 编码字符串
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        return base64.b32encode(data).decode("ascii")

    @staticmethod
    def decode(base32_str: str) -> bytes:
        """Base32 解码。

        :param base32_str: Base32 编码字符串
        :return: 解码后的 bytes
        """
        return base64.b32decode(base32_str)

    @staticmethod
    def encode_hex(data) -> str:
        """Base32 Hex 编码（使用扩展十六进制字母表）。

        :param data: 待编码的 bytes 或 str
        :return: Base32 Hex 编码字符串
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        return _b32hex_encode(data)

    @staticmethod
    def decode_hex(base32_hex_str: str) -> bytes:
        """Base32 Hex 解码。

        :param base32_hex_str: Base32 Hex 编码字符串
        :return: 解码后的 bytes
        """
        return _b32hex_decode(base32_hex_str)

    @staticmethod
    def decode_str_hex(base32_hex_str: str, charset: str = "utf-8") -> str:
        """Base32 Hex 解码为字符串。

        :param base32_hex_str: Base32 Hex 编码字符串
        :param charset: 字符集，默认 ``"utf-8"``
        :return: 解码后的字符串
        """
        return _b32hex_decode(base32_hex_str).decode(charset)
