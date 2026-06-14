import hashlib
import hmac
from typing import Union


class DigestUtil:
    """摘要工具类

    提供常用的摘要（哈希）算法封装，包括：
    - MD5 / SHA-1 / SHA-256 / SHA-384 / SHA-512
    - HMAC-MD5 / HMAC-SHA1 / HMAC-SHA256
    所有方法同时支持 str 和 bytes 输入。
    """

    # ------------------------------------------------------------------ #
    #  内部辅助
    # ------------------------------------------------------------------ #

    @staticmethod
    def _to_bytes(data: Union[str, bytes]) -> bytes:
        """
        将输入统一转为 bytes。

        :param data: 字符串或字节数据
        :return: 字节数据
        """
        if isinstance(data, str):
            return data.encode("utf-8")
        return data

    @staticmethod
    def _digest(data: Union[str, bytes], algorithm: str) -> bytes:
        """
        通用摘要计算，返回原始 bytes。

        :param data: 输入数据
        :param algorithm: 摘要算法名称
        :return: 摘要字节数据
        """
        return hashlib.new(algorithm, DigestUtil._to_bytes(data)).digest()

    @staticmethod
    def _hex_digest(data: Union[str, bytes], algorithm: str) -> str:
        """
        通用摘要计算，返回十六进制字符串。

        :param data: 输入数据
        :param algorithm: 摘要算法名称
        :return: 十六进制摘要字符串
        """
        return hashlib.new(algorithm, DigestUtil._to_bytes(data)).hexdigest()

    # ------------------------------------------------------------------ #
    #  MD5
    # ------------------------------------------------------------------ #

    @staticmethod
    def md5(data: Union[str, bytes]) -> bytes:
        """
        计算MD5摘要，返回原始bytes。

        :param data: 输入数据
        :return: MD5摘要字节数据
        """
        return DigestUtil._digest(data, "md5")

    @staticmethod
    def md5_hex(data: Union[str, bytes]) -> str:
        """
        计算MD5摘要，返回32位十六进制字符串。

        :param data: 输入数据
        :return: 32位十六进制MD5字符串
        """
        return DigestUtil._hex_digest(data, "md5")

    @staticmethod
    def md5_hex16(data: Union[str, bytes]) -> str:
        """
        计算MD5摘要，返回16位十六进制字符串（取32位结果的中间16位）。

        :param data: 输入数据
        :return: 16位十六进制MD5字符串
        """
        return DigestUtil.md5_hex(data)[8:24]

    # ------------------------------------------------------------------ #
    #  SHA-1
    # ------------------------------------------------------------------ #

    @staticmethod
    def sha1(data: Union[str, bytes]) -> bytes:
        """
        计算SHA-1摘要，返回原始bytes。

        :param data: 输入数据
        :return: SHA-1摘要字节数据
        """
        return DigestUtil._digest(data, "sha1")

    @staticmethod
    def sha1_hex(data: Union[str, bytes]) -> str:
        """
        计算SHA-1摘要，返回十六进制字符串。

        :param data: 输入数据
        :return: 十六进制SHA-1字符串
        """
        return DigestUtil._hex_digest(data, "sha1")

    # ------------------------------------------------------------------ #
    #  SHA-256
    # ------------------------------------------------------------------ #

    @staticmethod
    def sha256(data: Union[str, bytes]) -> bytes:
        """
        计算SHA-256摘要，返回原始bytes。

        :param data: 输入数据
        :return: SHA-256摘要字节数据
        """
        return DigestUtil._digest(data, "sha256")

    @staticmethod
    def sha256_hex(data: Union[str, bytes]) -> str:
        """
        计算SHA-256摘要，返回十六进制字符串。

        :param data: 输入数据
        :return: 十六进制SHA-256字符串
        """
        return DigestUtil._hex_digest(data, "sha256")

    # ------------------------------------------------------------------ #
    #  SHA-384
    # ------------------------------------------------------------------ #

    @staticmethod
    def sha384(data: Union[str, bytes]) -> bytes:
        """
        计算SHA-384摘要，返回原始bytes。

        :param data: 输入数据
        :return: SHA-384摘要字节数据
        """
        return DigestUtil._digest(data, "sha384")

    @staticmethod
    def sha384_hex(data: Union[str, bytes]) -> str:
        """
        计算SHA-384摘要，返回十六进制字符串。

        :param data: 输入数据
        :return: 十六进制SHA-384字符串
        """
        return DigestUtil._hex_digest(data, "sha384")

    # ------------------------------------------------------------------ #
    #  SHA-512
    # ------------------------------------------------------------------ #

    @staticmethod
    def sha512(data: Union[str, bytes]) -> bytes:
        """
        计算SHA-512摘要，返回原始bytes。

        :param data: 输入数据
        :return: SHA-512摘要字节数据
        """
        return DigestUtil._digest(data, "sha512")

    @staticmethod
    def sha512_hex(data: Union[str, bytes]) -> str:
        """
        计算SHA-512摘要，返回十六进制字符串。

        :param data: 输入数据
        :return: 十六进制SHA-512字符串
        """
        return DigestUtil._hex_digest(data, "sha512")

    # ------------------------------------------------------------------ #
    #  HMAC
    # ------------------------------------------------------------------ #

    @staticmethod
    def _hmac_digest(data: Union[str, bytes], key: Union[str, bytes], algorithm: str) -> bytes:
        """
        通用HMAC计算，返回原始bytes。

        :param data: 输入数据
        :param key: HMAC密钥
        :param algorithm: 摘要算法名称
        :return: HMAC摘要字节数据
        """
        return hmac.new(
            DigestUtil._to_bytes(key),
            DigestUtil._to_bytes(data),
            algorithm,
        ).digest()

    @staticmethod
    def _hmac_hex_digest(data: Union[str, bytes], key: Union[str, bytes], algorithm: str) -> str:
        """
        通用HMAC计算，返回十六进制字符串。

        :param data: 输入数据
        :param key: HMAC密钥
        :param algorithm: 摘要算法名称
        :return: 十六进制HMAC摘要字符串
        """
        return hmac.new(
            DigestUtil._to_bytes(key),
            DigestUtil._to_bytes(data),
            algorithm,
        ).hexdigest()

    # HMAC-MD5

    @staticmethod
    def hmac_md5(data: Union[str, bytes], key: Union[str, bytes]) -> bytes:
        """
        HMAC-MD5计算，返回原始bytes。

        :param data: 输入数据
        :param key: HMAC密钥
        :return: HMAC-MD5摘要字节数据
        """
        return DigestUtil._hmac_digest(data, key, "md5")

    @staticmethod
    def hmac_md5_hex(data: Union[str, bytes], key: Union[str, bytes]) -> str:
        """
        HMAC-MD5计算，返回十六进制字符串。

        :param data: 输入数据
        :param key: HMAC密钥
        :return: 十六进制HMAC-MD5字符串
        """
        return DigestUtil._hmac_hex_digest(data, key, "md5")

    # HMAC-SHA1

    @staticmethod
    def hmac_sha1(data: Union[str, bytes], key: Union[str, bytes]) -> bytes:
        """
        HMAC-SHA1计算，返回原始bytes。

        :param data: 输入数据
        :param key: HMAC密钥
        :return: HMAC-SHA1摘要字节数据
        """
        return DigestUtil._hmac_digest(data, key, "sha1")

    @staticmethod
    def hmac_sha1_hex(data: Union[str, bytes], key: Union[str, bytes]) -> str:
        """
        HMAC-SHA1计算，返回十六进制字符串。

        :param data: 输入数据
        :param key: HMAC密钥
        :return: 十六进制HMAC-SHA1字符串
        """
        return DigestUtil._hmac_hex_digest(data, key, "sha1")

    # HMAC-SHA256

    @staticmethod
    def hmac_sha256(data: Union[str, bytes], key: Union[str, bytes]) -> bytes:
        """
        HMAC-SHA256计算，返回原始bytes。

        :param data: 输入数据
        :param key: HMAC密钥
        :return: HMAC-SHA256摘要字节数据
        """
        return DigestUtil._hmac_digest(data, key, "sha256")

    @staticmethod
    def hmac_sha256_hex(data: Union[str, bytes], key: Union[str, bytes]) -> str:
        """
        HMAC-SHA256计算，返回十六进制字符串。

        :param data: 输入数据
        :param key: HMAC密钥
        :return: 十六进制HMAC-SHA256字符串
        """
        return DigestUtil._hmac_hex_digest(data, key, "sha256")
