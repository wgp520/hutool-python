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
