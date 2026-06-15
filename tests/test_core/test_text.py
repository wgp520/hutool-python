from hutool import CsvUtil, StrBuilder, UnicodeUtil


class TestUnicodeUtil:
    def test_to_unicode(self):
        result = UnicodeUtil.to_unicode("中")
        assert "\\u" in result

    def test_from_unicode(self):
        result = UnicodeUtil.from_unicode("\\u4e2d")
        assert result == "中"

    def test_roundtrip(self):
        original = "中文测试"
        encoded = UnicodeUtil.to_unicode(original)
        decoded = UnicodeUtil.from_unicode(encoded)
        assert decoded == original

    def test_escape(self):
        result = UnicodeUtil.escape("abc")
        assert isinstance(result, str)

    def test_unescape(self):
        result = UnicodeUtil.unescape("\\u4e2d")
        assert result == "中"


class TestCsvUtil:
    def test_read(self):
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write("a,b,c\n1,2,3\n")
            path = f.name
        try:
            result = CsvUtil.read(path)
            assert len(result) == 2
            assert result[0] == ["a", "b", "c"]
            assert result[1] == ["1", "2", "3"]
        finally:
            os.unlink(path)

    def test_write(self):
        import os
        import tempfile

        path = tempfile.mktemp(suffix=".csv")
        try:
            CsvUtil.write(path, [["a", "b"], ["1", "2"]])
            result = CsvUtil.read(path)
            assert len(result) == 2
        finally:
            if os.path.exists(path):
                os.unlink(path)


class TestStrBuilder:
    def test_append(self):
        sb = StrBuilder()
        sb.append("hello").append(" ").append("world")
        assert sb.to_string() == "hello world"

    def test_length(self):
        sb = StrBuilder()
        sb.append("test")
        assert sb.length() == 4

    def test_is_empty(self):
        sb = StrBuilder()
        assert sb.is_empty() is True
        sb.append("x")
        assert sb.is_empty() is False

    def test_delete(self):
        sb = StrBuilder()
        sb.append("hello world")
        sb.delete(5, 11)
        assert sb.to_string() == "hello"

    def test_replace(self):
        sb = StrBuilder()
        sb.append("hello world")
        sb.replace(6, 11, "python")
        assert sb.to_string() == "hello python"

    def test_reverse(self):
        sb = StrBuilder()
        sb.append("abc")
        sb.reverse()
        assert sb.to_string() == "cba"

    def test_insert(self):
        sb = StrBuilder()
        sb.append("ac")
        sb.insert(1, "b")
        assert sb.to_string() == "abc"

    def test_to_string(self):
        sb = StrBuilder()
        assert sb.to_string() == ""
