from hutool import VersionUtil


class TestVersionUtil:
    def test_compare(self):
        assert VersionUtil.compare("1.0.0", "1.0.1") == -1
        assert VersionUtil.compare("1.0.1", "1.0.0") == 1
        assert VersionUtil.compare("1.0.0", "1.0.0") == 0

    def test_is_greater(self):
        assert VersionUtil.is_greater("1.0.1", "1.0.0") is True
        assert VersionUtil.is_greater("1.0.0", "1.0.1") is False

    def test_is_lower(self):
        assert VersionUtil.is_lower("1.0.0", "1.0.1") is True
        assert VersionUtil.is_lower("1.0.1", "1.0.0") is False

    def test_get_main_version(self):
        result = VersionUtil.get_main_version("1.2.3.4")
        assert result == "1"

    def test_compare_multi_part(self):
        assert VersionUtil.compare("1.0.0", "2.0.0") == -1
        assert VersionUtil.compare("1.1.0", "1.0.0") == 1
