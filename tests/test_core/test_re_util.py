from hutool import ReUtil


class TestReUtil:
    def test_is_match(self):
        assert ReUtil.is_match(r"\d+", "123") is True
        assert ReUtil.is_match(r"\d+", "abc") is False

    def test_contains(self):
        assert ReUtil.contains(r"\d+", "abc123def") is True
        assert ReUtil.contains(r"\d+", "abcdef") is False

    def test_get(self):
        result = ReUtil.get(r"\d+", "abc123def")
        assert result == "123"

    def test_get_group(self):
        result = ReUtil.get(r"(\d+)", "abc123def", group_index=1)
        assert result == "123"

    def test_get_all(self):
        result = ReUtil.get_all(r"\d+", "abc123def456")
        assert result == ["123", "456"]

    def test_match_all(self):
        result = ReUtil.match_all(r"\d+", "abc123def456")
        assert result == ["123", "456"]

    def test_replace_all(self):
        result = ReUtil.replace_all("abc123def456", r"\d+", "X")
        assert result == "abcXdefX"

    def test_replace_first(self):
        result = ReUtil.replace_first("abc123def456", r"\d+", "X")
        assert result == "abcXdef456"

    def test_count(self):
        assert ReUtil.count(r"\d+", "abc123def456") == 2

    def test_split(self):
        result = ReUtil.split("abc123def456ghi", r"\d+")
        assert result == ["abc", "def", "ghi"]

    def test_del_all(self):
        result = ReUtil.del_all(r"\d+", "abc123def456")
        assert result == "abcdef"

    def test_escape(self):
        result = ReUtil.escape("[test]")
        assert "[" in result and "]" in result
