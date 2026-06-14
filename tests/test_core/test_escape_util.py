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
