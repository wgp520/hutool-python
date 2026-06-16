import base64
import hashlib
import hmac as hmac_mod
import os
from typing import Optional, Tuple, Union

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class SecureUtil:
    """加密工具类

    提供常用对称/非对称加密算法封装：
    - AES（CBC/ECB/CTR）
    - DES（CBC/ECB）
    - RSA（加密/解密/签名/验签）
    """

    _CAESAR_TABLE = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"

    # ------------------------------------------------------------------ #
    #  内部辅助
    # ------------------------------------------------------------------ #

    @staticmethod
    def _ensure_bytes(data: Union[str, bytes]) -> bytes:
        """
        将输入统一转为 bytes。

        :param data: 字符串或字节数据
        :return: 字节数据
        """
        if isinstance(data, str):
            return data.encode("utf-8")
        return data

    # ------------------------------------------------------------------ #
    #  AES
    # ------------------------------------------------------------------ #

    @staticmethod
    def generate_aes_key(key_size: int = 128) -> bytes:
        """生成AES密钥

        :param key_size: 密钥位数，支持 128、192、256
        :return: 随机密钥 bytes
        """
        if key_size not in (128, 192, 256):
            raise ValueError("AES密钥长度必须为128、192或256位")
        return os.urandom(key_size // 8)

    @staticmethod
    def encrypt_aes(data: bytes, key: bytes, mode: str = "CBC", iv: Optional[bytes] = None) -> bytes:
        """AES加密

        :param data: 待加密数据（明文）
        :param key: AES密钥（16/24/32字节）
        :param mode: 加密模式，支持 CBC / ECB / CTR
        :param iv: 初始化向量（CBC/CTR模式必填，ECB模式忽略）
        :return: 密文 bytes（CBC/CTR模式前16字节为IV）
        """
        if len(key) not in (16, 24, 32):
            raise ValueError("AES密钥长度必须为16、24或32字节")

        mode_upper = mode.upper()
        if mode_upper == "CBC":
            if iv is None:
                iv = os.urandom(16)
            cipher_mode = modes.CBC(iv)
        elif mode_upper == "ECB":
            iv = b""
            cipher_mode = modes.ECB()
        elif mode_upper == "CTR":
            if iv is None:
                iv = os.urandom(16)
            cipher_mode = modes.CTR(iv)
        else:
            raise ValueError(f"不支持的AES模式: {mode}")

        # PKCS7 填充（CTR模式无需填充）
        if mode_upper != "CTR":
            padder = sym_padding.PKCS7(128).padder()
            data = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), cipher_mode, backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()

        # 将IV/nonce拼接在密文前（ECB模式除外）
        if mode_upper == "ECB":
            return ciphertext
        return iv + ciphertext

    @staticmethod
    def decrypt_aes(data: bytes, key: bytes, mode: str = "CBC", iv: Optional[bytes] = None) -> bytes:
        """AES解密

        :param data: 密文 bytes（如果未提供iv，CBC/CTR模式会从前16字节读取IV）
        :param key: AES密钥
        :param mode: 加密模式，支持 CBC / ECB / CTR
        :param iv: 初始化向量（可选，不提供时从密文前缀读取）
        :return: 解密后的明文 bytes
        """
        if len(key) not in (16, 24, 32):
            raise ValueError("AES密钥长度必须为16、24或32字节")

        mode_upper = mode.upper()
        if mode_upper == "CBC":
            if iv is None:
                iv, data = data[:16], data[16:]
            cipher_mode = modes.CBC(iv)
        elif mode_upper == "ECB":
            cipher_mode = modes.ECB()
        elif mode_upper == "CTR":
            if iv is None:
                iv, data = data[:16], data[16:]
            cipher_mode = modes.CTR(iv)
        else:
            raise ValueError(f"不支持的AES模式: {mode}")

        cipher = Cipher(algorithms.AES(key), cipher_mode, backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(data) + decryptor.finalize()

        # 去除PKCS7填充（CTR模式无需去除）
        if mode_upper != "CTR":
            unpadder = sym_padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(plaintext) + unpadder.finalize()

        return plaintext

    # ------------------------------------------------------------------ #
    #  DES
    # ------------------------------------------------------------------ #

    @staticmethod
    def generate_des_key() -> bytes:
        """
        生成DES密钥（8字节）。

        :return: 随机DES密钥 bytes
        """
        return os.urandom(8)

    @staticmethod
    def encrypt_des(data: bytes, key: bytes, mode: str = "CBC", iv: Optional[bytes] = None) -> bytes:
        """DES加密

        :param data: 待加密数据
        :param key: DES密钥（8字节）
        :param mode: 加密模式，支持 CBC / ECB
        :param iv: 初始化向量（CBC模式必填或自动生成）
        :return: 密文 bytes（CBC模式前8字节为IV）
        """
        if len(key) != 8:
            raise ValueError("DES密钥长度必须为8字节")

        mode_upper = mode.upper()
        if mode_upper == "CBC":
            if iv is None:
                iv = os.urandom(8)
            cipher_mode = modes.CBC(iv)
        elif mode_upper == "ECB":
            iv = b""
            cipher_mode = modes.ECB()
        else:
            raise ValueError(f"不支持的DES模式: {mode}")

        # PKCS7 填充（DES块大小64位=8字节）
        padder = sym_padding.PKCS7(64).padder()
        data = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.TripleDES(key * 3 if len(key) == 8 else key), cipher_mode, backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()

        if mode_upper == "ECB":
            return ciphertext
        return iv + ciphertext

    @staticmethod
    def decrypt_des(data: bytes, key: bytes, mode: str = "CBC", iv: Optional[bytes] = None) -> bytes:
        """DES解密

        :param data: 密文 bytes（如果未提供iv，CBC模式会从前8字节读取IV）
        :param key: DES密钥（8字节）
        :param mode: 加密模式，支持 CBC / ECB
        :param iv: 初始化向量（可选）
        :return: 解密后的明文 bytes
        """
        if len(key) != 8:
            raise ValueError("DES密钥长度必须为8字节")

        mode_upper = mode.upper()
        if mode_upper == "CBC":
            if iv is None:
                iv, data = data[:8], data[8:]
            cipher_mode = modes.CBC(iv)
        elif mode_upper == "ECB":
            cipher_mode = modes.ECB()
        else:
            raise ValueError(f"不支持的DES模式: {mode}")

        cipher = Cipher(algorithms.TripleDES(key * 3 if len(key) == 8 else key), cipher_mode, backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(data) + decryptor.finalize()

        unpadder = sym_padding.PKCS7(64).unpadder()
        plaintext = unpadder.update(plaintext) + unpadder.finalize()

        return plaintext

    # ------------------------------------------------------------------ #
    #  RSA
    # ------------------------------------------------------------------ #

    @staticmethod
    def generate_rsa_key_pair(key_size: int = 2048) -> Tuple[bytes, bytes]:
        """生成RSA密钥对

        :param key_size: 密钥位数，默认2048
        :return: (public_key_pem, private_key_pem) 元组
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend(),
        )
        public_key = private_key.public_key()

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return public_pem, private_pem

    @staticmethod
    def encrypt_rsa(data: bytes, public_key_pem: bytes) -> bytes:
        """RSA公钥加密

        :param data: 待加密数据（长度受密钥大小限制）
        :param public_key_pem: PEM格式公钥
        :return: 密文 bytes
        """
        public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
        ciphertext = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return ciphertext

    @staticmethod
    def decrypt_rsa(data: bytes, private_key_pem: bytes) -> bytes:
        """RSA私钥解密

        :param data: 密文 bytes
        :param private_key_pem: PEM格式私钥
        :return: 明文 bytes
        """
        private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())
        plaintext = private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return plaintext

    @staticmethod
    def sign_with_rsa(data: bytes, private_key_pem: bytes) -> bytes:
        """RSA私钥签名

        :param data: 待签名数据
        :param private_key_pem: PEM格式私钥
        :return: 签名 bytes
        """
        private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())
        signature = private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return signature

    @staticmethod
    def verify_with_rsa(data: bytes, signature: bytes, public_key_pem: bytes) -> bool:
        """RSA公钥验签

        :param data: 原始数据
        :param signature: 签名 bytes
        :param public_key_pem: PEM格式公钥
        :return: 验签是否通过
        """
        public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
        try:
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------ #
    #  凯撒密码
    # ------------------------------------------------------------------ #

    @staticmethod
    def caesar_encode(message: str, offset: int) -> str:
        """
        凯撒密码加密。

        仅对 ``A-Za-z`` 字母字符进行移位，其他字符保持不变。
        使用交替大小写的字母表（AaBbCc...Zz，共 52 个字符）。

        Examples::

            caesar_encode("Hello", 1) -> "Ifmmp"

        :param message: 明文
        :param offset: 移位量（正整数）
        :return: 密文
        """
        table = SecureUtil._CAESAR_TABLE
        length = len(table)
        chars = []
        for ch in message:
            if ch in table:
                idx = table.index(ch)
                chars.append(table[(idx + offset) % length])
            else:
                chars.append(ch)
        return "".join(chars)

    @staticmethod
    def caesar_decode(message: str, offset: int) -> str:
        """
        凯撒密码解密。

        与 :meth:`caesar_encode` 配对使用。

        Examples::

            caesar_decode("Ifmmp", 1) -> "Hello"

        :param message: 密文
        :param offset: 移位量（与加密时相同）
        :return: 明文
        """
        return SecureUtil.caesar_encode(message, -offset)

    # ------------------------------------------------------------------ #
    #  对称密钥生成
    # ------------------------------------------------------------------ #

    @staticmethod
    def generate_key(algorithm: str = "AES", key_size: int = 128) -> bytes:
        """生成对称加密密钥

        :param algorithm: 算法名称，支持 'AES', 'DES', 'DESede'
        :param key_size: 密钥位数
        :return: 随机密钥 bytes
        """
        algo_upper = algorithm.upper()
        if algo_upper == "AES":
            if key_size not in (128, 192, 256):
                raise ValueError("AES密钥长度必须为128、192或256位")
            return os.urandom(key_size // 8)
        elif algo_upper == "DES":
            return os.urandom(8)
        elif algo_upper in ("DESEDE", "3DES", "TRIPLEDES"):
            return os.urandom(24)
        else:
            raise ValueError(f"不支持的算法: {algorithm}")

    @staticmethod
    def desede(key: bytes, mode: str = "CBC") -> Tuple:
        """TripleDES加密解密快捷方法

        返回一个元组 ``(encrypt_func, decrypt_func)``，每个函数接受
        ``data: bytes`` 和可选 ``iv: bytes`` 参数。

        :param key: TripleDES密钥（24字节）
        :param mode: 加密模式
        :return: (encrypt_func, decrypt_func) 元组
        """
        if len(key) != 24:
            raise ValueError("TripleDES密钥长度必须为24字节")

        def _encrypt(data: bytes, iv: Optional[bytes] = None) -> bytes:
            return SecureUtil.encrypt_aes(data, key, mode=mode, iv=iv)

        def _decrypt(data: bytes, iv: Optional[bytes] = None) -> bytes:
            return SecureUtil.decrypt_aes(data, key, mode=mode, iv=iv)

        return _encrypt, _decrypt

    # ------------------------------------------------------------------ #
    #  摘要便捷方法
    # ------------------------------------------------------------------ #

    @staticmethod
    def md5(data: Union[str, bytes]) -> str:
        """MD5摘要便捷方法（返回十六进制）

        :param data: 输入数据
        :return: MD5十六进制字符串
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        return hashlib.md5(data).hexdigest()

    @staticmethod
    def sha1(data: Union[str, bytes]) -> str:
        """SHA-1摘要便捷方法

        :param data: 输入数据
        :return: SHA-1十六进制字符串
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        return hashlib.sha1(data).hexdigest()

    @staticmethod
    def sha256(data: Union[str, bytes]) -> str:
        """SHA-256摘要便捷方法

        :param data: 输入数据
        :return: SHA-256十六进制字符串
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    # ------------------------------------------------------------------ #
    #  HMAC便捷方法
    # ------------------------------------------------------------------ #

    @staticmethod
    def hmac_md5(data: Union[str, bytes], key: Union[str, bytes]) -> str:
        """HMAC-MD5便捷方法

        :param data: 输入数据
        :param key: HMAC密钥
        :return: HMAC-MD5十六进制字符串
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        if isinstance(key, str):
            key = key.encode("utf-8")
        return hmac_mod.new(key, data, "md5").hexdigest()

    @staticmethod
    def hmac_sha1(data: Union[str, bytes], key: Union[str, bytes]) -> str:
        """HMAC-SHA1便捷方法

        :param data: 输入数据
        :param key: HMAC密钥
        :return: HMAC-SHA1十六进制字符串
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        if isinstance(key, str):
            key = key.encode("utf-8")
        return hmac_mod.new(key, data, "sha1").hexdigest()

    @staticmethod
    def hmac_sha256(data: Union[str, bytes], key: Union[str, bytes]) -> str:
        """HMAC-SHA256便捷方法

        :param data: 输入数据
        :param key: HMAC密钥
        :return: HMAC-SHA256十六进制字符串
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        if isinstance(key, str):
            key = key.encode("utf-8")
        return hmac_mod.new(key, data, "sha256").hexdigest()

    # ------------------------------------------------------------------ #
    #  密钥派生
    # ------------------------------------------------------------------ #

    @staticmethod
    def pbkdf2(
        password: Union[str, bytes], salt: Union[str, bytes], iterations: int = 10000, key_length: int = 32
    ) -> bytes:
        """PBKDF2密钥派生

        :param password: 密码
        :param salt: 盐值
        :param iterations: 迭代次数
        :param key_length: 输出密钥长度
        :return: 派生密钥 bytes
        """
        if isinstance(password, str):
            password = password.encode("utf-8")
        if isinstance(salt, str):
            salt = salt.encode("utf-8")
        return hashlib.pbkdf2_hmac("sha256", password, salt, iterations, dklen=key_length)

    # ------------------------------------------------------------------ #
    #  编码检测与解码
    # ------------------------------------------------------------------ #

    @staticmethod
    def decode(data: Union[str, bytes]) -> bytes:
        """自动检测并解码（Hex或Base64）

        先尝试Hex解码，失败则尝试Base64解码。

        :param data: Hex或Base64编码的数据
        :return: 解码后的 bytes
        """
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        # 尝试Hex解码
        try:
            return bytes.fromhex(data)
        except ValueError:
            pass
        # 尝试Base64解码
        return base64.b64decode(data)

    # ------------------------------------------------------------------ #
    #  参数签名
    # ------------------------------------------------------------------ #

    @staticmethod
    def sign_params(params: dict, secret: str, algorithm: str = "sha256") -> str:
        """参数签名

        将参数按键名排序拼接后，使用指定算法与密钥进行签名。

        :param params: 参数字典
        :param secret: 密钥
        :param algorithm: 签名算法
        :return: 签名字符串
        """
        sorted_keys = sorted(params.keys())
        parts = []
        for k in sorted_keys:
            v = params[k]
            if v is not None:
                parts.append(f"{k}={v}")
        sign_str = "&".join(parts) + "&secret=" + secret

        algo = algorithm.lower()
        if algo.startswith("hmac_"):
            hash_name = algo[5:]
            if isinstance(sign_str, str):
                sign_str = sign_str.encode("utf-8")
            if isinstance(secret, str):
                secret = secret.encode("utf-8")
            return hmac_mod.new(secret, sign_str, hash_name).hexdigest()
        else:
            return getattr(hashlib, algo)(sign_str.encode("utf-8")).hexdigest()
