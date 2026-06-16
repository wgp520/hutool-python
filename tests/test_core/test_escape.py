from hutool import EscapeUtil


class TestEscapeUtil:
    def test_escape_html(self):
        result = EscapeUtil.escape_html("<div>test</div>")
        assert "&lt;" in result
        assert "&gt;" in result

    def test_unescape_html(self):
        result = EscapeUtil.unescape_html("&lt;div&gt;test&lt;/div&gt;")
        assert result == "<div>test</div>"

    def test_escape_xml(self):
        result = EscapeUtil.escape_xml("<root>test</root>")
        assert "&lt;" in result
        assert "&gt;" in result

    def test_unescape_xml(self):
        result = EscapeUtil.unescape_xml("&lt;root&gt;test&lt;/root&gt;")
        assert result == "<root>test</root>"

    def test_escape_sql(self):
        result = EscapeUtil.escape_sql("it's")
        assert result == "it''s"

    def test_roundtrip_html(self):
        original = '<p class="test">Hello & Goodbye</p>'
        escaped = EscapeUtil.escape_html(original)
        unescaped = EscapeUtil.unescape_html(escaped)
        assert unescaped == original

    # ── unescape_html_chars ────────────────────────────────

    def test_unescape_html_chars_basic(self):
        """测试 HTML 实体反转义"""
        result = EscapeUtil.unescape_html_chars("&lt;p&gt;Hello &amp; World&lt;/p&gt;")
        assert result == "<p>Hello & World</p>"

    def test_unescape_html_chars_quote(self):
        """测试引号反转义"""
        result = EscapeUtil.unescape_html_chars("&quot;test&quot;")
        assert result == '"test"'

    def test_unescape_html_chars_apos(self):
        """测试单引号反转义"""
        result = EscapeUtil.unescape_html_chars("it&#39;s")
        assert result == "it's"

    def test_unescape_html_chars_none(self):
        """测试 None/空"""
        assert EscapeUtil.unescape_html_chars("") == ""
        assert EscapeUtil.unescape_html_chars(None) is None

    def test_escape_all(self):
        """测试转义所有非字母数字字符"""
        result = EscapeUtil.escape_all("hello world!")
        assert "hello" in result
        assert "world" in result
        # 空格和感叹号被转义
        assert "\\u0020" in result
        assert "\\u0021" in result

    def test_escape_all_alphanumeric(self):
        """测试字母数字不被转义"""
        result = EscapeUtil.escape_all("abc123")
        assert result == "abc123"

    def test_escape_all_empty(self):
        """测试空字符串"""
        assert EscapeUtil.escape_all("") == ""
        assert EscapeUtil.escape_all(None) == ""

    def test_safe_unescape(self):
        """测试安全反转义"""
        result = EscapeUtil.safe_unescape("\\u0048\\u0065\\u006c\\u006c\\u006f")
        assert result == "Hello"

    def test_safe_unescape_invalid(self):
        """测试无效转义返回原串"""
        original = "\\uGGGG"
        result = EscapeUtil.safe_unescape(original)
        assert result == original

    def test_safe_unescape_empty(self):
        """测试空字符串"""
        assert EscapeUtil.safe_unescape("") == ""
        assert EscapeUtil.safe_unescape(None) == ""

    def test_unescape(self):
        """测试 Unicode 转义序列反转义"""
        result = EscapeUtil.unescape("\\u0041\\u0042\\u0043")
        assert result == "ABC"

    def test_unescape_mixed(self):
        """测试混合内容"""
        result = EscapeUtil.unescape("Hello \\u0057orld")
        assert result == "Hello World"
