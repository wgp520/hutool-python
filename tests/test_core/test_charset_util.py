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
