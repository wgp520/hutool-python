from hutool import RuntimeUtil
from hutool import SystemUtil


class TestSystemUtil:
    def test_get(self):
        result = SystemUtil.get("PATH")
        assert result is not None
        assert isinstance(result, str)

    def test_get_with_default(self):
        result = SystemUtil.get("nonexistent.key", "default_value")
        assert result == "default_value"

    def test_get_all(self):
        result = SystemUtil.get_all()
        assert isinstance(result, dict)
        assert len(result) > 0


class TestRuntimeUtil:
    def test_get_pid(self):
        pid = RuntimeUtil.get_pid()
        assert isinstance(pid, int)
        assert pid > 0

    def test_get_memory_info(self):
        info = RuntimeUtil.get_memory_info()
        assert isinstance(info, dict)

    def test_get_available_processors(self):
        count = RuntimeUtil.get_available_processors()
        assert isinstance(count, int)
        assert count > 0
