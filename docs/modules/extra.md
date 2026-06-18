# 扩展工具 - extra

## 概述

`hutool.extra` 包含一些基于第三方库的扩展工具。

## EmojiUtil

Emoji 表情处理工具。

```python
from hutool import EmojiUtil

# 是否包含 Emoji
EmojiUtil.contains_emoji("hello 😀")       # True
EmojiUtil.contains_emoji("hello world")     # False

# Emoji 与 Unicode 互转
EmojiUtil.emoji_to_unicode("😀")           # "\\U0001F600"
EmojiUtil.unicode_to_emoji("\\U0001F600")  # "😀"

# 移除 Emoji
EmojiUtil.remove_emojis("hello 😀 world")  # "hello  world"

# removeAllEmojis — 移除所有 Emoji（别名）
EmojiUtil.remove_all_emojis("hello 😀👍 world")  # "hello  world"

# toHtmlHex — Emoji 转 HTML 十六进制实体
EmojiUtil.to_html_hex("😀")   # "&#x1F600;"

# toUnicode — Emoji 转 Unicode 表示
EmojiUtil.to_unicode("😀")    # "\\U0001F600"
```

## PinyinUtil

中文拼音转换工具，基于 `pypinyin` 实现。

```python
from hutool import PinyinUtil

# 获取拼音
PinyinUtil.get_pinyin("中国")              # "zhongguo"
PinyinUtil.get_pinyin("中国", separator=" ")  # "zhong guo"

# 获取拼音首字母
PinyinUtil.get_pinyin_first_letter("中国")  # "Z"

# 获取全拼（带声调）
PinyinUtil.get_full_pinyin("中国")          # "zhōng guó"
```

## TemplateUtil

模板引擎工具，基于 Jinja2 实现。

```python
from hutool import TemplateUtil

# 渲染模板
result = TemplateUtil.render("Hello {{ name }}!", {"name": "World"})
# "Hello World!"

result = TemplateUtil.render("{% for i in items %}{{ i }},{% endfor %}",
                             {"items": [1, 2, 3]})
# "1,2,3,"

# 创建模板引擎（带模板目录）
engine = TemplateUtil.create_engine("/path/to/templates")
template = engine.get_template("index.html")
result = template.render({"title": "test"})

# renderTemplate — render_file 的别名
result = TemplateUtil.render_template("/path/to/template.html", {"name": "World"})
```

## QrCodeUtil

二维码生成工具，基于 `qrcode` 库实现。

```python
from hutool import QrCodeUtil

# 生成二维码图片
image = QrCodeUtil.generate("https://example.com")

# 生成为字节
image_bytes = QrCodeUtil.generate_as_bytes("https://example.com",
                                           width=300, height=300,
                                           format="png")

# 生成并保存到文件
QrCodeUtil.generate_to_file("https://example.com", "/path/to/qr.png",
                            width=300, height=300)
```

### ASCII 艺术二维码

```python
# generateAsAsciiArt — 生成 ASCII 艺术二维码
ascii_art = QrCodeUtil.generate_as_ascii_art("https://example.com")
print(ascii_art)
# ██████████████    ██  ██████
# ██          ██  ████    ██
# ██  ██████  ██    ██  ████
# ...

# toAsciiArt — QR 图片转 ASCII 艺术
text = QrCodeUtil.to_ascii_art("/path/to/qr.png")
```

## Epub / EpubFactory

EPUB 生成工具，支持多引擎切换：ebooklib（功能全面）、mkepub（轻量）、pypub3（自动生成封面）。
所有引擎均为可选依赖，按需安装。

```python
from hutool import EpubFactory

# 推荐：通过工厂创建
epub = EpubFactory.create(
    engine="ebooklib",   # 或 "mkepub" / "pypub3"
    epub_name="我的小说",
    author="作者名",
    language="zh",
)

# 添加文本章节
epub.add_page("第一章", ["段落一", "段落二"])

# 添加混合章节（文本 + 图片）
epub.add_page("第二章", ["文字", image_bytes])

# 添加纯图片章节（漫画模式）
epub.add_image_page("番外", [img1, img2])

# 保存
path = epub.save("/path/to/dir")  # 自动以书名命名
path = epub.save("/path/to/book.epub")  # 指定文件名
```

### 引擎选择

| 引擎 | 安装 | 特点 |
|------|------|------|
| ``ebooklib`` | ``pip install ebooklib`` | 功能最全，支持封面、目录、CSS、多语言 |
| ``mkepub`` | ``pip install mkepub`` | 轻量，适合简单文本+图片 EPUB |
| ``pypub3`` | ``pip install pypub3`` | 自动生成封面，支持自定义 CSS |

### 自定义引擎扩展

```python
from hutool.extra.epub import Epub, register_engine

@register_engine("my_engine")
class MyEpub(Epub):
    def _add_item(self, title, content): ...
    def _write_epub(self, path): ...
    def add_image(self, name, img): ...
    @property
    def book(self): ...
```
