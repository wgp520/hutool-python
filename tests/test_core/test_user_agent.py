"""Tests for UserAgentUtil."""

from hutool import UserAgentUtil


class TestUserAgentUtil:
    def test_chrome_starts_with_mozilla(self):
        ua = UserAgentUtil.chrome()
        assert ua.startswith("Mozilla/5.0")
        assert "Chrome/" in ua or "CriOS/" in ua  # iOS uses CriOS

    def test_firefox_starts_with_mozilla(self):
        ua = UserAgentUtil.firefox()
        assert ua.startswith("Mozilla/5.0")
        assert "Firefox/" in ua

    def test_safari_starts_with_mozilla(self):
        ua = UserAgentUtil.safari()
        assert ua.startswith("Mozilla/5.0")
        assert "Safari/" in ua

    def test_opera_starts_with_opera(self):
        ua = UserAgentUtil.opera()
        assert ua.startswith("Opera/")
        assert "Presto/" in ua

    def test_ie_contains_msie(self):
        ua = UserAgentUtil.internet_explorer()
        assert "MSIE" in ua
        assert "Mozilla/5.0" in ua

    def test_edge_contains_edg(self):
        ua = UserAgentUtil.edge()
        assert "Edg/" in ua
        assert "Chrome/" in ua

    def test_user_agent_returns_string(self):
        ua = UserAgentUtil.user_agent()
        assert isinstance(ua, str)
        assert len(ua) > 0

    def test_user_agent_is_mozilla(self):
        ua = UserAgentUtil.user_agent()
        # All our UAs start with Mozilla/5.0 or Opera/
        assert ua.startswith("Mozilla/5.0") or ua.startswith("Opera/")

    def test_chrome_randomness(self):
        uas = {UserAgentUtil.chrome() for _ in range(20)}
        # Should have some variety (not all identical)
        assert len(uas) > 1

    def test_firefox_randomness(self):
        uas = {UserAgentUtil.firefox() for _ in range(20)}
        assert len(uas) > 1
