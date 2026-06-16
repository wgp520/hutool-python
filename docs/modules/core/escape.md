# Escape 工具 - EscapeUtil

## 由来

在 Web 开发中，HTML/XML 转义是防止 XSS 攻击的基本手段。`EscapeUtil` 提供常用的转义和反转义方法。

## 方法

```python
from hutool import EscapeUtil

# HTML 转义
EscapeUtil.escape_html('<script>alert("xss")</script>')
# '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;'

EscapeUtil.unescape_html('&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;')
# '<script>alert("xss")</script>'

# XML 转义
EscapeUtil.escape_xml('<root>content</root>')
# '&lt;root&gt;content&lt;/root&gt;'

EscapeUtil.unescape_xml('&lt;root&gt;content&lt;/root&gt;')
# '<root>content</root>'

# SQL 转义
EscapeUtil.escape_sql("it's a test")  # "it''s a test"

# HTML 实体反转义
EscapeUtil.unescape_html_chars("&lt;div&gt;hello&lt;/div&gt;")
# '<div>hello</div>'

# Unicode 全转义（非字母数字全部转义为 \uXXXX）
EscapeUtil.escape_all("hello world!")
# 'hello world!'

# 安全反转义（失败返回原串）
EscapeUtil.safe_unescape("\\u0048\\u0065\\u006c\\u006c\\u006f")  # "Hello"
EscapeUtil.safe_unescape("\\uGGGG")  # "\\uGGGG"（原样返回）

# Unicode 转义序列反转义
EscapeUtil.unescape("\\u0041\\u0042\\u0043")  # "ABC"
```
