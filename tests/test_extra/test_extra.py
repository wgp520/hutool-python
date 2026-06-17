import base64

import jinja2
import pytest

from hutool import EmojiUtil, PinyinUtil, QrCodeUtil, TemplateUtil


class TestEmojiUtil:
    def test_contains_emoji(self):
        assert EmojiUtil.contains_emoji("hello 😀") is True
        assert EmojiUtil.contains_emoji("hello world") is False

    def test_remove_emojis(self):
        result = EmojiUtil.remove_emojis("hello 😀 world 🌍")
        assert "😀" not in result
        assert "🌍" not in result
        assert "hello" in result

    def test_emoji_to_unicode(self):
        result = EmojiUtil.emoji_to_unicode("😀")
        assert "\\U" in result or "\\u" in result

    def test_unicode_to_emoji(self):
        result = EmojiUtil.unicode_to_emoji("\\U0001F600")
        assert isinstance(result, str)

    def test_is_emoji(self):
        assert EmojiUtil.is_emoji("😀") is True
        assert EmojiUtil.is_emoji("a") is False

    def test_extract_emojis(self):
        result = EmojiUtil.extract_emojis("hello 😀 world 🎉")
        assert "😀" in result
        assert "🎉" in result

    def test_extract_emojis_none(self):
        result = EmojiUtil.extract_emojis("no emojis")
        assert result == []

    def test_to_html(self):
        result = EmojiUtil.to_html("A")
        assert "A" in result or "&#x" in result

    def test_remove_all_emojis(self):
        assert EmojiUtil.remove_all_emojis("hello 😀 world 🌍") == "hello  world "

    def test_to_html_hex(self):
        result = EmojiUtil.to_html_hex("😀")
        assert result.startswith("&#x")
        assert result.endswith(";")

    def test_to_unicode(self):
        result = EmojiUtil.to_unicode("A")
        assert result == "U+0041"


class TestPinyinUtil:
    def test_get_pinyin(self):
        result = PinyinUtil.get_pinyin("中文")
        assert isinstance(result, str)
        assert len(result) > 0
        # Should be lowercase letters
        assert result.replace(" ", "").isalpha()

    def test_get_pinyin_with_separator(self):
        result = PinyinUtil.get_pinyin("中", separator="-")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_pinyin_first_letter(self):
        result = PinyinUtil.get_pinyin_first_letter("中文")
        assert len(result) >= 1
        assert result[0].isalpha()

    def test_get_full_pinyin(self):
        result = PinyinUtil.get_full_pinyin("中文测试")
        assert isinstance(result, str)

    def test_get_pinyin_char(self):
        result = PinyinUtil.get_pinyin_char("你")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_first_letter(self):
        result = PinyinUtil.get_first_letter("北京")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_is_chinese(self):
        assert PinyinUtil.is_chinese("你") is True
        assert PinyinUtil.is_chinese("a") is False
        assert PinyinUtil.is_chinese("1") is False

    def test_get_pinyin_with_tone(self):
        result = PinyinUtil.get_pinyin_with_tone("北京")
        assert isinstance(result, str)
        assert len(result) > 0


class TestTemplateUtil:
    def test_render(self):
        result = TemplateUtil.render("Hello, {{ name }}!", {"name": "World"})
        assert result == "Hello, World!"

    def test_render_with_loop(self):
        template = "{% for item in items %}{{ item }} {% endfor %}"
        result = TemplateUtil.render(template, {"items": [1, 2, 3]})
        assert "1" in result
        assert "2" in result
        assert "3" in result

    def test_render_missing_key(self):
        with pytest.raises(jinja2.exceptions.UndefinedError):
            TemplateUtil.render("{{ missing }}", {})

    def test_render_template_alias(self):
        assert callable(TemplateUtil.render_template)


class TestQrCodeUtil:
    def test_generate_as_base64(self):
        result = QrCodeUtil.generate_as_base64("test content")
        assert isinstance(result, str)
        # Verify it's valid base64
        decoded = base64.b64decode(result)
        assert len(decoded) > 0

    def test_generate_as_svg(self):
        result = QrCodeUtil.generate_as_svg("test content")
        assert isinstance(result, str)
        assert "svg" in result.lower() or "SVG" in result
