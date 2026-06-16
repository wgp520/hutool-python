from hutool import JWTUtil


class TestJWTUtil:
    SECRET = "test_secret_key"

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

    def test_create_token_with_expire(self):
        token = JWTUtil.create_token_with_expire({"user": "test"}, self.SECRET, 3600)
        assert isinstance(token, str)
        payload = JWTUtil.parse_token(token, self.SECRET)
        assert payload["user"] == "test"
        assert "exp" in payload

    def test_parse_header(self):
        token = JWTUtil.create_token({"user": "test"}, self.SECRET)
        header = JWTUtil.parse_header(token)
        assert isinstance(header, dict)
        assert "alg" in header

    def test_is_expired_not(self):
        token = JWTUtil.create_token_with_expire({"user": "test"}, self.SECRET, 3600)
        assert JWTUtil.is_expired(token) is False

    def test_is_expired_yes(self):
        token = JWTUtil.create_token_with_expire({"user": "test"}, self.SECRET, -1)
        assert JWTUtil.is_expired(token) is True

    def test_get_claim(self):
        token = JWTUtil.create_token({"user": "test", "role": "admin"}, self.SECRET)
        assert JWTUtil.get_claim(token, "user") == "test"
        assert JWTUtil.get_claim(token, "role") == "admin"
        assert JWTUtil.get_claim(token, "nonexistent") is None

    def test_generate_key(self):
        key = JWTUtil.generate_key("HS256")
        assert isinstance(key, bytes)
        assert len(key) == 32

    def test_generate_key_384(self):
        key = JWTUtil.generate_key("HS384")
        assert len(key) == 48

    def test_create_token_with_claims(self):
        token = JWTUtil.create_token_with_claims(
            self.SECRET,
            issuer="test_iss",
            subject="test_sub",
            expire_seconds=3600,
            custom_field="value",
        )
        payload = JWTUtil.get_payload(token)
        assert payload["iss"] == "test_iss"
        assert payload["sub"] == "test_sub"
        assert payload["custom_field"] == "value"
        assert "exp" in payload
        assert "iat" in payload
