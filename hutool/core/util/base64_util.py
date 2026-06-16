"""Base64 编解码工具类"""

import base64
import re


class Base64Util:
    """Base64 编解码工具类。"""

    @staticmethod
    def encode(data):
        """Base64 编码。

        :param data: 待编码的 bytes 或 str
        :return: Base64 编码的 bytes
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        return base64.b64encode(data)

    @staticmethod
    def encode_str(s: str, charset: str = "utf-8") -> str:
        """将字符串进行 Base64 编码，返回字符串。

        :param s: 待编码的字符串
        :param charset: 字符集，默认 ``"utf-8"``
        :return: Base64 编码字符串
        """
        return base64.b64encode(s.encode(charset)).decode("ascii")

    @staticmethod
    def encode_url_safe(data) -> bytes:
        """URL 安全的 Base64 编码。

        :param data: 待编码的 bytes 或 str
        :return: URL 安全的 Base64 编码 bytes
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        return base64.urlsafe_b64encode(data)

    @staticmethod
    def encode_without_padding(data) -> bytes:
        """Base64 编码（不含填充字符 ``=``）。

        :param data: 待编码的 bytes 或 str
        :return: 不含填充的 Base64 编码 bytes
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        return base64.b64encode(data).rstrip(b"=")

    @staticmethod
    def encode_from_file(file_path: str) -> str:
        """读取文件并进行 Base64 编码。

        :param file_path: 文件路径
        :return: Base64 编码字符串
        """
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")

    @staticmethod
    def encode_from_stream(stream) -> str:
        """从流中读取并进行 Base64 编码。

        :param stream: 可读的二进制流
        :return: Base64 编码字符串
        """
        data = stream.read()
        if isinstance(data, str):
            data = data.encode("utf-8")
        return base64.b64encode(data).decode("ascii")

    @staticmethod
    def decode(base64_str):
        """Base64 解码。

        :param base64_str: Base64 编码的字符串或 bytes
        :return: 解码后的 bytes
        """
        if isinstance(base64_str, str):
            base64_str = base64_str.encode("ascii")
        return base64.b64decode(base64_str)

    @staticmethod
    def decode_str(base64_str: str, charset: str = "utf-8") -> str:
        """Base64 解码为字符串。

        :param base64_str: Base64 编码字符串
        :param charset: 字符集，默认 ``"utf-8"``
        :return: 解码后的字符串
        """
        return base64.b64decode(base64_str.encode("ascii")).decode(charset)

    @staticmethod
    def decode_str_gbk(base64_str: str) -> str:
        """Base64 解码为 GBK 字符串。

        :param base64_str: Base64 编码字符串
        :return: GBK 解码后的字符串
        """
        return base64.b64decode(base64_str.encode("ascii")).decode("gbk")

    @staticmethod
    def decode_to_file(base64_str: str, file_path: str) -> None:
        """Base64 解码并写入文件。

        :param base64_str: Base64 编码字符串
        :param file_path: 目标文件路径
        """
        data = base64.b64decode(base64_str.encode("ascii"))
        with open(file_path, "wb") as f:
            f.write(data)

    @staticmethod
    def is_base64(s: str) -> bool:
        """判断字符串是否为有效的 Base64 编码。

        :param s: 待检查的字符串
        :return: 是否为有效 Base64
        """
        if not s:
            return False
        # 基本格式检查
        if not re.match(r"^[A-Za-z0-9+/]*={0,2}$", s):
            return False
        if len(s) % 4 != 0:
            return False
        try:
            base64.b64decode(s)
            return True
        except Exception:
            return False
