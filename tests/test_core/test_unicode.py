from hutool import UnicodeUtil


class TestUnicodeUtil:
    """UnicodeUtil 测试"""

    def test_to_string(self):
        result = UnicodeUtil.to_string("\\u4f60\\u597d")
        assert result == "你好"

    def test_to_string_mixed(self):
        result = UnicodeUtil.to_string("hello\\u4f60\\u597dworld")
        assert result == "hello你好world"

    def test_to_unicode_string(self):
        result = UnicodeUtil.to_unicode_string("你好")
        assert "\\u" in result
        assert "4f60" in result
        assert "597d" in result

    def test_roundtrip(self):
        original = "你好世界"
        unicode_str = UnicodeUtil.to_unicode_string(original)
        restored = UnicodeUtil.to_string(unicode_str)
        assert restored == original

    def test_to_string_no_unicode(self):
        result = UnicodeUtil.to_string("hello world")
        assert result == "hello world"

    def test_to_unicode_string_ascii(self):
        result = UnicodeUtil.to_unicode_string("abc")
        assert result == "abc"
