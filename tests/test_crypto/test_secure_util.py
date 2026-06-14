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
