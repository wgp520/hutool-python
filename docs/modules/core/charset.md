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

# 清理无效控制字符
CharsetUtil.clean_invalid("hello\x00world")  # "helloworld"
CharsetUtil.clean_invalid("a\x07b\x08c")     # "abc"（清除 BEL/BS）
CharsetUtil.clean_invalid("a\tb\nc")          # "a\tb\nc"（保留 TAB/LF/CR）

# 解析字符集名称
CharsetUtil.parse("GBK")          # "gbk"
CharsetUtil.parse(None)           # "utf-8"

# 系统字符集
CharsetUtil.system_charset_name() # "utf-8"

# 检测字节数据字符集（基于 BOM）
CharsetUtil.detect_charset(b"\xef\xbb\xbfhello")  # "utf-8-sig"

# 转换文件字符集
CharsetUtil.convert_file("src.txt", "dest.txt", "gbk", "utf-8")
```
