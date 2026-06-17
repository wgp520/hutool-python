import io

from hutool import IoUtil


class TestIoUtil:
    def test_checksum(self):
        stream = io.BytesIO(b"hello")
        result = IoUtil.checksum(stream)
        assert isinstance(result, str)
        assert len(result) == 32  # MD5 hex

    def test_checksum_crc32(self):
        stream = io.BytesIO(b"hello")
        result = IoUtil.checksum_crc32(stream)
        assert isinstance(result, int)

    def test_checksum_value(self):
        stream = io.BytesIO(b"hello")
        result = IoUtil.checksum_value(stream)
        assert isinstance(result, int)

    def test_content_equals_same(self):
        s1 = io.BytesIO(b"hello")
        s2 = io.BytesIO(b"hello")
        assert IoUtil.content_equals(s1, s2) is True

    def test_content_equals_diff(self):
        s1 = io.BytesIO(b"hello")
        s2 = io.BytesIO(b"world")
        assert IoUtil.content_equals(s1, s2) is False

    def test_content_equals_ignore_eol(self):
        s1 = io.BytesIO(b"a\r\nb\nc")
        s2 = io.BytesIO(b"a\nb\nc")
        assert IoUtil.content_equals_ignore_eol(s1, s2) is True

    def test_flush(self):
        buf = io.BytesIO()
        IoUtil.flush(buf)  # should not raise

    def test_line_iter(self):
        stream = io.BytesIO(b"line1\nline2\nline3")
        lines = list(IoUtil.line_iter(stream))
        assert lines == ["line1", "line2", "line3"]

    def test_read_hex(self):
        stream = io.BytesIO(b"\xab\xcd")
        result = IoUtil.read_hex(stream)
        assert "abcd" in result.lower()

    def test_read_utf8(self):
        stream = io.BytesIO("你好".encode())
        result = IoUtil.read_utf8(stream)
        assert result == "你好"

    def test_read_utf8_lines(self):
        stream = io.BytesIO(b"a\nb\nc")
        result = IoUtil.read_utf8_lines(stream)
        assert result == ["a", "b", "c"]

    def test_to_str(self):
        stream = io.BytesIO(b"hello")
        assert IoUtil.to_str(stream) == "hello"

    def test_to_stream(self):
        stream = IoUtil.to_stream("hello")
        assert stream.read() == b"hello"

    def test_to_utf8_stream(self):
        stream = IoUtil.to_utf8_stream("你好")
        assert stream.read() == "你好".encode()

    def test_write_utf8(self):
        buf = io.BytesIO()
        IoUtil.write_utf8(buf, "你好")
        buf.seek(0)
        assert buf.read() == "你好".encode()
