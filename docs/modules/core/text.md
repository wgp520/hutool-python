# 文本操作工具

## UnicodeUtil

Unicode 编码转换工具，常用于处理中文编码问题。

```python
from hutool import UnicodeUtil

# 中文转 Unicode
UnicodeUtil.to_unicode("中文")        # "\\u4e2d\\u6587"

# Unicode 转中文
UnicodeUtil.from_unicode("\\u4e2d\\u6587")  # "中文"

# 转义/反转义
UnicodeUtil.escape("中文")     # "\\u4e2d\\u6587"
UnicodeUtil.unescape("\\u4e2d\\u6587")  # "中文"
```

## CsvUtil

CSV 文件读写工具，基于 Python 内置 `csv` 模块封装。

```python
from hutool import CsvUtil

# 读取 CSV
rows = CsvUtil.read("data.csv")
# [["name", "age"], ["张三", "25"], ["李四", "30"]]

# 写入 CSV
CsvUtil.write("output.csv", [["name", "age"], ["张三", "25"]])

# 使用 Reader/Writer 对象
reader = CsvUtil.get_reader("data.csv")
writer = CsvUtil.get_writer("output.csv")
```

## StrBuilder

可变字符串构建器，类似 Java 的 `StringBuilder`：

```python
from hutool import StrBuilder

builder = StrBuilder()
builder.append("Hello")
builder.append(" ")
builder.append("World")
builder.to_string()  # "Hello World"

builder.insert(5, ",")
builder.to_string()  # "Hello, World"

builder.delete(5, 6)
builder.to_string()  # "Hello World"

builder.reverse()
builder.to_string()  # "dlroW olleH"

len(builder)         # 11
builder.is_empty()   # False
```
