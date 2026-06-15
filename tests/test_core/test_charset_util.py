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
