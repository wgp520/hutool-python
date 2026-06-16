import base64

from hutool import SecureUtil


class TestSecureUtil:
    def test_aes_generate_key(self):
        key = SecureUtil.generate_aes_key(128)
        assert isinstance(key, bytes)
        assert len(key) == 16

    def test_aes_encrypt_decrypt(self):
        key = SecureUtil.generate_aes_key(128)
        data = b"Hello, World!"
        encrypted = SecureUtil.encrypt_aes(data, key)
        decrypted = SecureUtil.decrypt_aes(encrypted, key)
        assert decrypted == data

    def test_aes_encrypt_decrypt_str(self):
        key = SecureUtil.generate_aes_key(128)
        data = b"Hello, World!"
        encrypted = SecureUtil.encrypt_aes(data, key)
        decrypted = SecureUtil.decrypt_aes(encrypted, key)
        assert decrypted.decode("utf-8") == "Hello, World!"

    def test_aes_256(self):
        key = SecureUtil.generate_aes_key(256)
        assert len(key) == 32
        data = b"Test data for AES-256"
        encrypted = SecureUtil.encrypt_aes(data, key)
        decrypted = SecureUtil.decrypt_aes(encrypted, key)
        assert decrypted == data

    def test_rsa_generate_key_pair(self):
        pub, priv = SecureUtil.generate_rsa_key_pair(2048)
        assert pub is not None
        assert priv is not None

    def test_rsa_encrypt_decrypt(self):
        pub, priv = SecureUtil.generate_rsa_key_pair(2048)
        data = b"Hello RSA"
        encrypted = SecureUtil.encrypt_rsa(data, pub)
        decrypted = SecureUtil.decrypt_rsa(encrypted, priv)
        assert decrypted == data

    def test_rsa_sign_verify(self):
        pub, priv = SecureUtil.generate_rsa_key_pair(2048)
        data = b"sign me"
        signature = SecureUtil.sign_with_rsa(data, priv)
        assert SecureUtil.verify_with_rsa(data, signature, pub) is True
        assert SecureUtil.verify_with_rsa(b"other data", signature, pub) is False

    def test_des_generate_key(self):
        key = SecureUtil.generate_des_key()
        assert isinstance(key, bytes)

    def test_des_encrypt_decrypt(self):
        key = SecureUtil.generate_des_key()
        data = b"Test DES"
        encrypted = SecureUtil.encrypt_des(data, key)
        decrypted = SecureUtil.decrypt_des(encrypted, key)
        assert decrypted == data

    # ── 凯撒密码 ──────────────────────────────────────────────

    def test_caesar_encode_basic(self):
        """测试凯撒密码加密（交替大小写表，偏移2步 = 标准字母表偏移1位）"""
        result = SecureUtil.caesar_encode("Hello", 2)
        assert result == "Ifmmp"

    def test_caesar_decode_basic(self):
        """测试凯撒密码解密"""
        result = SecureUtil.caesar_decode("Ifmmp", 2)
        assert result == "Hello"

    def test_caesar_roundtrip(self):
        """测试凯撒密码加解密往返"""
        original = "Hello, World! 123"
        encoded = SecureUtil.caesar_encode(original, 5)
        decoded = SecureUtil.caesar_decode(encoded, 5)
        assert decoded == original

    def test_caesar_preserves_non_letter(self):
        """测试非字母字符不变"""
        assert SecureUtil.caesar_encode("123!@#", 3) == "123!@#"

    def test_caesar_large_offset(self):
        """测试大偏移量（环绕）"""
        result = SecureUtil.caesar_encode("abc", 52)
        assert result == "abc"

    def test_generate_key_aes(self):
        key = SecureUtil.generate_key("AES", 128)
        assert len(key) == 16

    def test_generate_key_des(self):
        key = SecureUtil.generate_key("DES")
        assert len(key) == 8

    def test_md5_convenience(self):
        result = SecureUtil.md5("Hello")
        assert isinstance(result, str)
        assert len(result) == 32

    def test_sha1_convenience(self):
        result = SecureUtil.sha1("Hello")
        assert isinstance(result, str)
        assert len(result) == 40

    def test_sha256_convenience(self):
        result = SecureUtil.sha256("Hello")
        assert isinstance(result, str)
        assert len(result) == 64

    def test_hmac_md5_convenience(self):
        result = SecureUtil.hmac_md5("data", "key")
        assert isinstance(result, str)

    def test_hmac_sha1_convenience(self):
        result = SecureUtil.hmac_sha1("data", "key")
        assert isinstance(result, str)

    def test_hmac_sha256_convenience(self):
        result = SecureUtil.hmac_sha256("data", "key")
        assert isinstance(result, str)

    def test_pbkdf2(self):
        result = SecureUtil.pbkdf2("password", "salt")
        assert isinstance(result, bytes)
        assert len(result) == 32

    def test_decode_hex(self):
        data = b"Hello"
        hex_str = data.hex()
        assert SecureUtil.decode(hex_str) == data

    def test_decode_base64(self):
        data = b"Hello"
        b64 = base64.b64encode(data).decode()
        assert SecureUtil.decode(b64) == data

    def test_sign_params(self):
        params = {"a": "1", "b": "2"}
        result = SecureUtil.sign_params(params, "secret")
        assert isinstance(result, str)
        assert len(result) > 0
