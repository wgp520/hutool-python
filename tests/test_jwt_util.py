from hutool import JWTUtil


class TestJWTUtil:
    def test_create_token(self):
        payload = {"user_id": 1, "username": "test"}
        token = JWTUtil.create_token(payload, "secret_key")
        assert isinstance(token, str)
        assert len(token) > 0
        assert "." in token

    def test_parse_token(self):
        payload = {"user_id": 1, "username": "test"}
        token = JWTUtil.create_token(payload, "secret_key")
        result = JWTUtil.parse_token(token, "secret_key")
        assert result["user_id"] == 1
        assert result["username"] == "test"

    def test_verify_valid(self):
        payload = {"user_id": 1}
        token = JWTUtil.create_token(payload, "secret_key")
        assert JWTUtil.verify(token, "secret_key") is True

    def test_verify_invalid(self):
        payload = {"user_id": 1}
        token = JWTUtil.create_token(payload, "secret_key")
        assert JWTUtil.verify(token, "wrong_key") is False

    def test_get_payload(self):
        payload = {"user_id": 1, "role": "admin"}
        token = JWTUtil.create_token(payload, "secret_key")
        result = JWTUtil.get_payload(token)
        assert result["user_id"] == 1
        assert result["role"] == "admin"

    def test_different_algorithms(self):
        payload = {"user_id": 1}
        for alg in ["HS256", "HS384", "HS512"]:
            token = JWTUtil.create_token(payload, "secret_key", algorithm=alg)
            result = JWTUtil.parse_token(token, "secret_key", algorithm=alg)
            assert result["user_id"] == 1

    def test_token_with_expiry(self):
        import time

        payload = {"user_id": 1, "exp": int(time.time()) + 1}  # expires in 1 second
        token = JWTUtil.create_token(payload, "secret_key")
        assert JWTUtil.verify(token, "secret_key") is True
        time.sleep(2)
        assert JWTUtil.verify(token, "secret_key") is False
