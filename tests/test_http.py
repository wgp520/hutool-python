import os
import tempfile
from unittest.mock import MagicMock

from hutool import HtmlUtil, HttpRequest, HttpResponse, HttpUtil


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

    def test_head(self):
        req = HttpRequest.head("http://example.com")
        assert req._method == "HEAD"

    def test_put(self):
        req = HttpRequest.put("http://example.com")
        assert req._method == "PUT"

    def test_patch(self):
        req = HttpRequest.patch("http://example.com")
        assert req._method == "PATCH"

    def test_delete(self):
        req = HttpRequest.delete("http://example.com")
        assert req._method == "DELETE"

    def test_options(self):
        req = HttpRequest.options("http://example.com")
        assert req._method == "OPTIONS"

    def test_trace(self):
        req = HttpRequest.trace("http://example.com")
        assert req._method == "TRACE"

    def test_content_type(self):
        req = HttpRequest.get("http://example.com").content_type("application/json")
        assert req._headers["Content-Type"] == "application/json"

    def test_keep_alive(self):
        req = HttpRequest.get("http://example.com").keep_alive(True)
        assert req._headers["Connection"] == "keep-alive"

    def test_basic_auth(self):
        req = HttpRequest.get("http://example.com").basic_auth("user", "pass")
        assert "Authorization" in req._headers
        assert req._headers["Authorization"].startswith("Basic ")

    def test_bearer_auth(self):
        req = HttpRequest.get("http://example.com").bearer_auth("mytoken")
        assert req._headers["Authorization"] == "Bearer mytoken"

    def test_body_bytes(self):
        req = HttpRequest.post("http://example.com").body_bytes(b"raw data")
        assert req._body_bytes == b"raw data"

    def test_params(self):
        req = HttpRequest.get("http://example.com").params({"q": "test"})
        assert req._params == {"q": "test"}


class TestHttpResponse:
    def _make_response(self, headers=None, content=b"data"):
        """Helper to create a mock HttpResponse"""
        import httpx

        h = headers or {}
        resp = httpx.Response(200, headers=h, content=content, request=httpx.Request("GET", "http://test"))
        return HttpResponse(resp)

    def _make_mock_response(self, header_name, header_value):
        """Helper to test headers that trigger httpx auto-decompression"""

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {header_name: header_value}
        mock_resp.content = b"data"
        mock_resp.text = "data"
        mock_resp.url = "http://test"
        mock_resp.cookies = {}
        return HttpResponse(mock_resp)

    def test_content_encoding(self):
        resp = self._make_mock_response("content-encoding", "gzip")
        assert resp.content_encoding == "gzip"

    def test_is_gzip(self):
        resp = self._make_mock_response("content-encoding", "gzip")
        assert resp.is_gzip() is True
        resp2 = self._make_response()
        assert resp2.is_gzip() is False

    def test_is_deflate(self):
        # Test the actual property without triggering httpx decompression
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"content-encoding": "deflate"}
        mock_resp.content = b"data"
        mock_resp.text = "data"
        mock_resp.url = "http://test"
        mock_resp.cookies = {}
        resp2 = HttpResponse(mock_resp)
        assert resp2.is_deflate() is True

    def test_is_chunked(self):
        resp = self._make_response({"transfer-encoding": "chunked"})
        assert resp.is_chunked() is True

    def test_body_bytes_method(self):
        resp = self._make_response(content=b"test")
        assert resp.body_bytes() == b"test"

    def test_get_cookies(self):
        resp = self._make_response()
        cookies = resp.get_cookies()
        assert isinstance(cookies, dict)

    def test_get_filename_from_disposition(self):
        resp = self._make_response({"content-disposition": 'attachment; filename="test.txt"'})
        assert resp.get_filename_from_disposition() == "test.txt"

    def test_get_filename_from_disposition_none(self):
        resp = self._make_response()
        assert resp.get_filename_from_disposition() is None

    def test_write_body(self):
        resp = self._make_response(content=b"hello world")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
            path = f.name
        try:
            count = resp.write_body(path)
            assert count == 11
            with open(path, "rb") as f:
                assert f.read() == b"hello world"
        finally:
            os.unlink(path)


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

    def test_clean_empty_tag(self):
        html = "<p></p><p>text</p><span>  </span>"
        result = HtmlUtil.clean_empty_tag(html)
        assert "<p>text</p>" in result
        assert "<p></p>" not in result

    def test_remove_html_tag_by_name(self):
        html = "<p>Hello</p><script>alert(1)</script><p>World</p>"
        result = HtmlUtil.remove_html_tag_by_name(html, "script")
        assert "alert" not in result
        assert "Hello" in result
        assert "World" in result

    def test_unwrap_html_tag(self):
        html = "<b>bold text</b>"
        result = HtmlUtil.unwrap_html_tag(html, "b")
        assert "bold text" in result
        assert "<b>" not in result

    def test_remove_html_attr(self):
        html = '<p class="test" id="main">text</p>'
        result = HtmlUtil.remove_html_attr(html, "class")
        assert "class" not in result
        assert "id" in result

    def test_remove_all_html_attr(self):
        html = '<p class="test" id="main">text</p>'
        result = HtmlUtil.remove_all_html_attr(html)
        assert "<p>" in result or "<p " not in result
