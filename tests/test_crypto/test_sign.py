from hutool import SignUtil


class TestSignUtil:
    def test_sign_params(self):
        params = {"a": "1", "b": "2", "c": "3"}
        result = SignUtil.sign_params(params, "secret", algorithm="md5")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_sort_sign(self):
        params = {"c": "3", "a": "1", "b": "2"}
        result = SignUtil.sort_sign(params, "secret")
        assert isinstance(result, str)

    def test_sign_deterministic(self):
        params = {"a": "1", "b": "2"}
        result1 = SignUtil.sign_params(params, "secret", algorithm="md5")
        result2 = SignUtil.sign_params(params, "secret", algorithm="md5")
        assert result1 == result2

    def test_sign_different_secret(self):
        params = {"a": "1"}
        result1 = SignUtil.sign_params(params, "secret1", algorithm="md5")
        result2 = SignUtil.sign_params(params, "secret2", algorithm="md5")
        assert result1 != result2

    def test_sign_params_md5(self):
        params = {"a": "1", "b": "2"}
        result = SignUtil.sign_params_md5(params, "secret")
        assert result == SignUtil.sign_params(params, "secret", "md5")

    def test_sign_params_sha1(self):
        params = {"a": "1"}
        result = SignUtil.sign_params_sha1(params, "secret")
        assert result == SignUtil.sign_params(params, "secret", "sha1")

    def test_sign_params_sha256(self):
        params = {"a": "1"}
        result = SignUtil.sign_params_sha256(params, "secret")
        assert result == SignUtil.sign_params(params, "secret", "sha256")

    def test_sign_params_hmac_md5(self):
        params = {"a": "1"}
        result = SignUtil.sign_params_hmac_md5(params, "secret")
        assert result == SignUtil.sign_params(params, "secret", "hmac_md5")

    def test_sign_params_hmac_sha1(self):
        params = {"a": "1"}
        result = SignUtil.sign_params_hmac_sha1(params, "secret")
        assert result == SignUtil.sign_params(params, "secret", "hmac_sha1")

    def test_sign_params_hmac_sha256(self):
        params = {"a": "1"}
        result = SignUtil.sign_params_hmac_sha256(params, "secret")
        assert result == SignUtil.sign_params(params, "secret", "hmac_sha256")
