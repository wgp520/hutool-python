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
