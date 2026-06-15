from hutool import IdUtil


class TestIdUtil:
    def test_random_uuid(self):
        result = IdUtil.random_uuid()
        assert len(result) == 36
        assert result.count("-") == 4

    def test_simple_uuid(self):
        result = IdUtil.simple_uuid()
        assert len(result) == 32
        assert "-" not in result

    def test_fast_uuid(self):
        result = IdUtil.fast_uuid()
        assert len(result) == 36

    def test_fast_simple_uuid(self):
        result = IdUtil.fast_simple_uuid()
        assert len(result) == 32

    def test_nano_id(self):
        result = IdUtil.nano_id()
        assert isinstance(result, str)
        assert len(result) == 21

    def test_nano_id_custom_size(self):
        result = IdUtil.nano_id(size=10)
        assert len(result) == 10

    def test_snowflake_id(self):
        result = IdUtil.snowflake_id()
        assert isinstance(result, int)
        assert result > 0

    def test_snowflake_id_uniqueness(self):
        ids = {IdUtil.snowflake_id() for _ in range(100)}
        assert len(ids) == 100

    def test_object_id(self):
        result = IdUtil.object_id()
        assert len(result) == 24
        int(result, 16)  # should be valid hex

    # ── unique_machine_id ───────────────────────────────────

    def test_unique_machine_id_returns_int(self):
        """测试返回整数类型"""
        result = IdUtil.unique_machine_id()
        assert isinstance(result, int)

    def test_unique_machine_id_positive(self):
        """测试返回正数"""
        result = IdUtil.unique_machine_id()
        assert result > 0

    def test_unique_machine_id_uniqueness(self):
        """测试多次调用返回不同值"""
        ids = {IdUtil.unique_machine_id() for _ in range(100)}
        assert len(ids) == 100

    # ── guid128 ─────────────────────────────────────────────

    def test_guid128_length(self):
        """测试返回 26 字符"""
        result = IdUtil.guid128()
        assert len(result) == 26

    def test_guid128_uniqueness(self):
        """测试唯一性"""
        ids = {IdUtil.guid128() for _ in range(100)}
        assert len(ids) == 100

    def test_guid128_with_salt(self):
        """测试带盐值"""
        result = IdUtil.guid128(salt="my_salt")
        assert len(result) == 26
        result2 = IdUtil.guid128(salt="my_salt")
        assert len(result2) == 26

    def test_guid128_format(self):
        """测试格式（应只包含 Crockford Base32 字符）"""
        valid_chars = set("0123456789ABCDEFGHJKMNPQRSTVWXYZ")
        result = IdUtil.guid128()
        assert all(c in valid_chars for c in result)
