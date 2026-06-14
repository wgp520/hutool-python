import jinja2
import pytest

from hutool import EmojiUtil
from hutool import PinyinUtil
from hutool import TemplateUtil


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
