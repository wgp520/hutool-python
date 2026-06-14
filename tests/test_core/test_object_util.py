from hutool import ObjectUtil


class TestObjectUtil:
    def test_equals(self):
        assert ObjectUtil.equals("abc", "abc") is True
        assert ObjectUtil.equals("abc", "def") is False
        assert ObjectUtil.equals(None, None) is True

    def test_not_equal(self):
        assert ObjectUtil.not_equal("abc", "def") is True

    def test_is_null(self):
        assert ObjectUtil.is_null(None) is True
        assert ObjectUtil.is_null("") is False

    def test_is_not_null(self):
        assert ObjectUtil.is_not_null("") is True
        assert ObjectUtil.is_not_null(None) is False

    def test_is_empty(self):
        assert ObjectUtil.is_empty(None) is True
        assert ObjectUtil.is_empty("") is True
        assert ObjectUtil.is_empty([]) is True
        assert ObjectUtil.is_empty({}) is True
        assert ObjectUtil.is_empty("abc") is False

    def test_is_not_empty(self):
        assert ObjectUtil.is_not_empty("abc") is True

    def test_default_if_null(self):
        assert ObjectUtil.default_if_null(None, "default") == "default"
        assert ObjectUtil.default_if_null("value", "default") == "value"

    def test_default_if_empty(self):
        assert ObjectUtil.default_if_empty("", "default") == "default"
        assert ObjectUtil.default_if_empty("value", "default") == "value"

    def test_length(self):
        assert ObjectUtil.length("abc") == 3
        assert ObjectUtil.length([1, 2]) == 2
        assert ObjectUtil.length(None) == 0

    def test_contains(self):
        assert ObjectUtil.contains("abc", "b") is True
        assert ObjectUtil.contains([1, 2, 3], 2) is True

    def test_is_basic_type(self):
        assert ObjectUtil.is_basic_type(1) is True
        assert ObjectUtil.is_basic_type("str") is True
        assert ObjectUtil.is_basic_type([1]) is False

    def test_has_null(self):
        assert ObjectUtil.has_null(1, None, 3) is True
        assert ObjectUtil.has_null(1, 2, 3) is False

    def test_has_empty(self):
        assert ObjectUtil.has_empty("", "abc") is True
        assert ObjectUtil.has_empty("abc", "def") is False

    def test_to_string(self):
        assert ObjectUtil.to_string(None) == ""
        assert ObjectUtil.to_string(123) == "123"
