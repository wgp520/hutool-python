# 字符编码工具 - CharsetUtil

## 由来

字符编码问题是开发中的常见坑，尤其是在中文环境下。`CharsetUtil` 提供编码相关的便捷方法。

## 常量

```python
from hutool import CharsetUtil

CharsetUtil.UTF_8       # "utf-8"
CharsetUtil.GBK         # "gbk"
CharsetUtil.ISO_8859_1  # "iso-8859-1"
```

## 方法

```python
# 编码转换
data = CharsetUtil.convert("你好".encode("utf-8"), "utf-8", "gbk")
text = CharsetUtil.convert(data, "gbk", "utf-8")  # "你好"

# 字符串形式的编码转换
result = CharsetUtil.convert("你好", "utf-8", "gbk")

# 获取默认编码
CharsetUtil.default_charset()  # "utf-8"

# 清理 BOM
clean = CharsetUtil.clean_bom("﻿内容")  # "内容"
```
