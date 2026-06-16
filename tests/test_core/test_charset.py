import os

from hutool import CharsetUtil


class TestCharsetUtil:
    def test_constants(self):
        assert CharsetUtil.UTF_8 == "utf-8"
        assert CharsetUtil.GBK == "gbk"
        assert CharsetUtil.ISO_8859_1 == "iso-8859-1"

    def test_default_charset(self):
        result = CharsetUtil.default_charset()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_convert_bytes(self):
        original = "hello"
        encoded = original.encode("utf-8")
        result = CharsetUtil.convert(encoded, "utf-8", "utf-8")
        assert result == encoded

    def test_convert_str(self):
        result = CharsetUtil.convert_str("hello", "utf-8", "utf-8")
        assert isinstance(result, str)

    def test_clean_bom(self):
        result = CharsetUtil.clean_bom("﻿hello")
        assert not result.startswith("﻿")

    def test_clean_invalid(self):
        # 包含 NUL(0x00) 和 BEL(0x07) 控制字符
        assert CharsetUtil.clean_invalid("hello\x00world") == "helloworld"
        assert CharsetUtil.clean_invalid("a\x07b\x08c") == "abc"
        # 保留 \t \n \r
        assert CharsetUtil.clean_invalid("a\tb\nc\rd") == "a\tb\nc\rd"
        assert CharsetUtil.clean_invalid("") == ""
        assert CharsetUtil.clean_invalid(None) == ""

    def test_parse(self):
        assert CharsetUtil.parse(None) == "utf-8"
        assert CharsetUtil.parse("") == "utf-8"
        assert CharsetUtil.parse("GBK") == "gbk"

    def test_system_charset_name(self):
        result = CharsetUtil.system_charset_name()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_default_charset_name(self):
        result = CharsetUtil.default_charset_name()
        assert isinstance(result, str)

    def test_detect_charset(self):
        # UTF-8 BOM
        data = b"\xef\xbb\xbfhello"
        assert CharsetUtil.detect_charset(data) == "utf-8-sig"
        # 普通 UTF-8
        assert CharsetUtil.detect_charset(b"hello") == "utf-8"

    def test_convert_file(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src.txt")
            dest = os.path.join(tmpdir, "dest.txt")
            with open(src, "wb") as f:
                f.write("你好".encode())
            CharsetUtil.convert_file(src, dest, "utf-8", "utf-8")
            with open(dest, "rb") as f:
                assert f.read() == "你好".encode()
