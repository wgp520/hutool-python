from hutool import HtmlUtil, HttpRequest, HttpUtil


class TestHttpRequest:
    def test_get(self):
        req = HttpRequest.get("http://example.com")
        assert req is not None

    def test_post(self):
        req = HttpRequest.post("http://example.com")
        assert req is not None

    def test_header(self):
        req = HttpRequest.get("http://example.com").header("X-Test", "value")
        assert req is not None

    def test_headers(self):
        req = HttpRequest.get("http://example.com").headers({"X-Test": "value"})
        assert req is not None

    def test_timeout(self):
        req = HttpRequest.get("http://example.com").timeout(5)
        assert req is not None

    def test_json(self):
        req = HttpRequest.post("http://example.com").json({"key": "value"})
        assert req is not None

    def test_form(self):
        req = HttpRequest.post("http://example.com").form("key", "value")
        assert req is not None

    def test_body(self):
        req = HttpRequest.post("http://example.com").body("test body")
        assert req is not None

    def test_cookie(self):
        req = HttpRequest.get("http://example.com").cookie("session=abc")
        assert req is not None

    def test_method(self):
        req = HttpRequest.get("http://example.com").method("POST")
        assert req is not None


class TestHttpUtil:
    def test_is_http(self):
        assert HttpUtil.is_http("http://example.com") is True
        assert HttpUtil.is_https("http://example.com") is False

    def test_is_https(self):
        assert HttpUtil.is_https("https://example.com") is True

    def test_encode_url(self):
        result = HttpUtil.encode_url("http://example.com/path?q=hello world")
        assert "hello" in result

    def test_decode_url(self):
        result = HttpUtil.decode_url("http://example.com/path?q=hello%20world")
        assert "hello world" in result

    def test_to_params(self):
        result = HttpUtil.to_params({"key": "value", "a": "b"})
        assert "key=value" in result
        assert "a=b" in result

    def test_decode_param_map(self):
        result = HttpUtil.decode_param_map("key=value&a=b")
        assert result["key"] == "value"
        assert result["a"] == "b"

    def test_get_charset(self):
        result = HttpUtil.get_charset("text/html; charset=utf-8")
        assert result == "utf-8" or result == "UTF-8"


class TestHtmlUtil:
    def test_escape(self):
        result = HtmlUtil.escape("<div>test</div>")
        assert "&lt;" in result

    def test_unescape(self):
        result = HtmlUtil.unescape("&lt;div&gt;test&lt;/div&gt;")
        assert result == "<div>test</div>"

    def test_remove_html_tag(self):
        result = HtmlUtil.remove_html_tag("<p>hello <b>world</b></p>")
        assert result == "hello world"

    def test_clean_html_tag(self):
        result = HtmlUtil.clean_html_tag("<p>test</p>")
        assert "<" not in result
        assert ">" not in result
