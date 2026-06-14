"""编解码工具类，提供Base64、Base32等编解码功能"""

import base64

__all__ = ("Base32", "Base64")


class Base64:
    """Base64编解码工具类"""

    @staticmethod
    def encode(data: bytes) -> str:
        """
        编码字节数据为Base64字符串

        :param data: 待编码的字节数据
        :return: Base64编码字符串
        """
        if data is None:
            raise ValueError("待编码数据不能为None")
        return base64.b64encode(data).decode("ascii")

    @staticmethod
    def encode_str(data: str, charset: str = "utf-8") -> str:
        """
        编码字符串为Base64字符串

        :param data: 待编码的字符串
        :param charset: 字符编码，默认utf-8
        :return: Base64编码字符串
        """
        if data is None:
            raise ValueError("待编码字符串不能为None")
        return base64.b64encode(data.encode(charset)).decode("ascii")

    @staticmethod
    def decode(base64_str: str) -> bytes:
        """
        解码Base64字符串为字节数据

        :param base64_str: Base64编码字符串
        :return: 解码后的字节数据
        """
        if base64_str is None:
            raise ValueError("Base64字符串不能为None")
        return base64.b64decode(base64_str)

    @staticmethod
    def decode_str(base64_str: str, charset: str = "utf-8") -> str:
        """
        解码Base64字符串为字符串

        :param base64_str: Base64编码字符串
        :param charset: 字符编码，默认utf-8
        :return: 解码后的字符串
        """
        if base64_str is None:
            raise ValueError("Base64字符串不能为None")
        return base64.b64decode(base64_str).decode(charset)

    @staticmethod
    def encode_url_safe(data: bytes) -> str:
        """
        编码为URL安全的Base64字符串（使用-和_代替+和/）

        :param data: 待编码的字节数据
        :return: URL安全的Base64编码字符串
        """
        if data is None:
            raise ValueError("待编码数据不能为None")
        return base64.urlsafe_b64encode(data).decode("ascii")

    @staticmethod
    def decode_url_safe(base64_str: str) -> bytes:
        """
        解码URL安全的Base64字符串

        :param base64_str: URL安全的Base64编码字符串
        :return: 解码后的字节数据
        """
        if base64_str is None:
            raise ValueError("Base64字符串不能为None")
        return base64.urlsafe_b64decode(base64_str)


class Base32:
    """Base32编解码工具类"""

    @staticmethod
    def encode(data: bytes) -> str:
        """
        编码字节数据为Base32字符串

        :param data: 待编码的字节数据
        :return: Base32编码字符串
        """
        if data is None:
            raise ValueError("待编码数据不能为None")
        return base64.b32encode(data).decode("ascii")

    @staticmethod
    def decode(base32_str: str) -> bytes:
        """
        解码Base32字符串为字节数据

        :param base32_str: Base32编码字符串
        :return: 解码后的字节数据
        """
        if base32_str is None:
            raise ValueError("Base32字符串不能为None")
        return base64.b32decode(base32_str)
