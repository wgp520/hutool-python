from hutool import SensitiveUtil


class TestSensitiveUtil:
    def test_init_and_contains(self):
        SensitiveUtil.init(["bad", "evil", "naughty"])
        assert SensitiveUtil.contains("this is a bad word") is True
        assert SensitiveUtil.contains("this is good") is False

    def test_find_first(self):
        SensitiveUtil.init(["bad", "evil"])
        result = SensitiveUtil.find_first("this is a bad evil word")
        assert result == "bad"

    def test_find_all(self):
        SensitiveUtil.init(["bad", "evil"])
        result = SensitiveUtil.find_all("this is a bad evil word")
        assert "bad" in result
        assert "evil" in result

    def test_replace(self):
        SensitiveUtil.init(["bad", "evil"])
        result = SensitiveUtil.replace("this is a bad evil word")
        assert "bad" not in result
        assert "evil" not in result
        assert "***" in result

    def test_replace_custom_char(self):
        SensitiveUtil.init(["bad"])
        result = SensitiveUtil.replace("this is a bad word", replace_char="#")
        assert "bad" not in result
        assert "###" in result

    def test_empty_text(self):
        SensitiveUtil.init(["bad"])
        assert SensitiveUtil.contains("") is False
        assert SensitiveUtil.replace("") == ""

    def test_no_sensitive_words(self):
        SensitiveUtil.init(["bad", "evil"])
        assert SensitiveUtil.contains("hello world") is False
        assert SensitiveUtil.replace("hello world") == "hello world"

    def test_multiple_occurrences(self):
        SensitiveUtil.init(["bad"])
        result = SensitiveUtil.find_all("bad bad bad")
        assert len(result) == 3
