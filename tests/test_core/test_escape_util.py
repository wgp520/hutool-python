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
