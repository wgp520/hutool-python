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
```
