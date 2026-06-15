from hutool import DigestUtil


class TestDigestUtil:
    def test_md5(self):
        result = DigestUtil.md5("hello")
        assert isinstance(result, bytes)
        assert len(result) == 16

    def test_md5_hex(self):
        result = DigestUtil.md5_hex("hello")
        assert isinstance(result, str)
        assert len(result) == 32

    def test_md5_hex16(self):
        result = DigestUtil.md5_hex16("hello")
        assert isinstance(result, str)
        assert len(result) == 16

    def test_sha1(self):
        result = DigestUtil.sha1("hello")
        assert isinstance(result, bytes)
        assert len(result) == 20

    def test_sha1_hex(self):
        result = DigestUtil.sha1_hex("hello")
        assert isinstance(result, str)
        assert len(result) == 40

    def test_sha256(self):
        result = DigestUtil.sha256("hello")
        assert isinstance(result, bytes)
        assert len(result) == 32

    def test_sha256_hex(self):
        result = DigestUtil.sha256_hex("hello")
        assert isinstance(result, str)
        assert len(result) == 64

    def test_sha384(self):
        result = DigestUtil.sha384("hello")
        assert isinstance(result, bytes)
        assert len(result) == 48

    def test_sha512(self):
        result = DigestUtil.sha512("hello")
        assert isinstance(result, bytes)
        assert len(result) == 64

    def test_hmac_md5(self):
        result = DigestUtil.hmac_md5("hello", "secret")
        assert isinstance(result, bytes)

    def test_hmac_md5_hex(self):
        result = DigestUtil.hmac_md5_hex("hello", "secret")
        assert isinstance(result, str)

    def test_hmac_sha1(self):
        result = DigestUtil.hmac_sha1("hello", "secret")
        assert isinstance(result, bytes)

    def test_hmac_sha256(self):
        result = DigestUtil.hmac_sha256("hello", "secret")
        assert isinstance(result, bytes)

    def test_hmac_sha256_hex(self):
        result = DigestUtil.hmac_sha256_hex("hello", "secret")
        assert isinstance(result, str)
        assert len(result) == 64

    def test_known_md5(self):
        # MD5("hello") = 5d41402abc4b2a76b9719d911017c592
        assert DigestUtil.md5_hex("hello") == "5d41402abc4b2a76b9719d911017c592"

    def test_known_sha256(self):
        # SHA256("hello") = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
        assert DigestUtil.sha256_hex("hello") == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

    def test_bytes_input(self):
        result = DigestUtil.md5_hex(b"hello")
        assert result == "5d41402abc4b2a76b9719d911017c592"
