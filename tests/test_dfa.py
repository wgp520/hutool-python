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

    def setup_method(self):
        SensitiveUtil.init(["bad", "worse", "terrible"])

    def test_is_inited(self):
        assert SensitiveUtil.is_inited() is True

    def test_contains(self):
        assert SensitiveUtil.contains("this is bad") is True
        assert SensitiveUtil.contains("this is good") is False

    def test_set_char_filter(self):
        SensitiveUtil.set_char_filter(lambda t: t.replace(" ", ""))
        assert SensitiveUtil.contains("b a d") is True
        SensitiveUtil.set_char_filter(None)

    def test_contains_sensitive_str(self):
        assert SensitiveUtil.contains_sensitive("this is bad") is True

    def test_contains_sensitive_list(self):
        assert SensitiveUtil.contains_sensitive(["good", "bad"]) is True
        assert SensitiveUtil.contains_sensitive(["good", "ok"]) is False

    def test_contains_sensitive_dict(self):
        assert SensitiveUtil.contains_sensitive({"key": "bad value"}) is True
        assert SensitiveUtil.contains_sensitive({"key": "good"}) is False

    def test_get_found_first_sensitive(self):
        result = SensitiveUtil.get_found_first_sensitive("this is bad stuff")
        assert isinstance(result, dict)
        assert result.get("word") == "bad"
        assert "start" in result
        assert "end" in result

    def test_get_found_first_sensitive_none(self):
        result = SensitiveUtil.get_found_first_sensitive("clean text")
        assert result == {}

    def test_get_found_all_sensitive(self):
        result = SensitiveUtil.get_found_all_sensitive("bad and worse")
        assert isinstance(result, list)
        assert len(result) == 2

    def test_init_from_delimited(self):
        SensitiveUtil.init_from_delimited("a,b,c", ",")
        assert SensitiveUtil.contains("a") is True
        assert SensitiveUtil.contains("d") is False
