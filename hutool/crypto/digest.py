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

    # ------------------------------------------------------------------ #
    #  文件摘要
    # ------------------------------------------------------------------ #

    @staticmethod
    def md5_from_file(file_path: str) -> str:
        """计算文件的MD5摘要（32位十六进制）

        以8192字节为单位分块读取文件，适用于大文件。

        :param file_path: 文件路径
        :return: 32位十六进制MD5字符串
        """
        h = hashlib.new("md5")
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def sha256_from_file(file_path: str) -> str:
        """计算文件的SHA-256摘要

        以8192字节为单位分块读取文件，适用于大文件。

        :param file_path: 文件路径
        :return: 十六进制SHA-256字符串
        """
        h = hashlib.new("sha256")
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()

    # ------------------------------------------------------------------ #
    #  通用摘要工厂
    # ------------------------------------------------------------------ #

    @staticmethod
    def md5_hex_to_16(md5_hex32: str) -> str:
        """将32位MD5转换为16位MD5（取中间16位）

        :param md5_hex32: 32位MD5十六进制字符串
        :return: 16位MD5十六进制字符串
        """
        if md5_hex32 and len(md5_hex32) >= 32:
            return md5_hex32[8:24]
        return md5_hex32 or ""

    @staticmethod
    def hmac(data: Union[str, bytes], key: Union[str, bytes], algorithm: str = "sha256") -> bytes:
        """通用HMAC计算工厂方法

        :param data: 输入数据
        :param key: HMAC密钥
        :param algorithm: 摘要算法名称，如 'md5', 'sha1', 'sha256'
        :return: HMAC摘要字节数据
        """
        return DigestUtil._hmac_digest(data, key, algorithm)

    @staticmethod
    def hmac_hex(data: Union[str, bytes], key: Union[str, bytes], algorithm: str = "sha256") -> str:
        """通用HMAC计算工厂方法（返回十六进制）

        :param data: 输入数据
        :param key: HMAC密钥
        :param algorithm: 摘要算法名称
        :return: 十六进制HMAC摘要字符串
        """
        return DigestUtil._hmac_hex_digest(data, key, algorithm)

    @staticmethod
    def digest(data: Union[str, bytes], algorithm: str = "sha256") -> bytes:
        """通用摘要计算工厂方法

        :param data: 输入数据
        :param algorithm: 摘要算法名称，如 'md5', 'sha1', 'sha256', 'sha384', 'sha512'
        :return: 摘要字节数据
        """
        return DigestUtil._digest(data, algorithm)

    @staticmethod
    def digest_hex(data: Union[str, bytes], algorithm: str = "sha256") -> str:
        """通用摘要计算工厂方法（返回十六进制）

        :param data: 输入数据
        :param algorithm: 摘要算法名称
        :return: 十六进制摘要字符串
        """
        return DigestUtil._hex_digest(data, algorithm)

    # ------------------------------------------------------------------ #
    #  bcrypt
    # ------------------------------------------------------------------ #

    @staticmethod
    def bcrypt(password: Union[str, bytes]) -> str:
        """使用bcrypt算法加密密码

        :param password: 明文密码
        :return: bcrypt哈希字符串
        :raises ImportError: 未安装bcrypt库时抛出
        """
        try:
            import bcrypt as _bcrypt
        except ImportError:
            raise ImportError("需要安装 bcrypt 库: pip install bcrypt")
        pwd = DigestUtil._to_bytes(password)
        return _bcrypt.hashpw(pwd, _bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def bcrypt_check(password: Union[str, bytes], hashed: str) -> bool:
        """校验密码是否与bcrypt哈希匹配

        :param password: 明文密码
        :param hashed: bcrypt哈希字符串
        :return: 是否匹配
        :raises ImportError: 未安装bcrypt库时抛出
        """
        try:
            import bcrypt as _bcrypt
        except ImportError:
            raise ImportError("需要安装 bcrypt 库: pip install bcrypt")
        pwd = DigestUtil._to_bytes(password)
        if hashed is None:
            raise ValueError("bcrypt哈希字符串不能为空")
        return _bcrypt.checkpw(pwd, hashed.encode("utf-8"))
