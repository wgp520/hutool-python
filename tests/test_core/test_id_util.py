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
