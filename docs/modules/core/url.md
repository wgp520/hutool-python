# URL 工具 - URLUtil

## 由来

URL 编解码和参数处理是网络编程中的常见需求。`URLUtil` 提供 URL 相关的便捷操作。

## 方法

```python
from hutool import URLUtil

# 编解码
URLUtil.encode("https://example.com/你好")  # "https://example.com/%E4%BD%A0%E5%A5%BD"
URLUtil.decode("https://example.com/%E4%BD%A0%E5%A5%BD")  # "https://example.com/你好"

# URL 信息提取
URLUtil.get_path("https://example.com/path?query=1")     # "/path"
URLUtil.get_host("https://example.com:8080/path")         # "example.com"
URLUtil.get_port("https://example.com:8080/path")         # 8080
URLUtil.get_query("https://example.com/path?key=value")   # "key=value"

# 构建 URL
URLUtil.build_url("https://example.com", {"key": "value"})
# "https://example.com?key=value"

# 参数处理
URLUtil.to_params({"city": "北京", "type": "test"})
# "city=%E5%8C%97%E4%BA%AC&type=test"

URLUtil.decode_param_map("city=%E5%8C%97%E4%BA%AC&type=test")
# {"city": "北京", "type": "test"}

# 标准化
URLUtil.normalize("https://example.com//path/../file")
# "https://example.com/file"

# 构建查询字符串
URLUtil.build_query({"city": "北京", "type": "test"})
# "city=%E5%8C%97%E4%BA%AC&type=test"
URLUtil.build_query({"key": "val"}, is_encode=False)
# "key=val"

# 编码 URL 中的空白
URLUtil.encode_blank("https://example.com/hello world")
# "https://example.com/hello%20world"

# 补全相对 URL
URLUtil.complete_url("https://example.com/a/b", "../c")
# "https://example.com/c"

# 解析 URL 参数
URLUtil.get_params("https://example.com?a=1&b=2")
# {"a": "1", "b": "2"}

# Data URI
URLUtil.get_data_uri_base64("image/png", "iVBORw0KGgo=")
# "data:image/png;base64,iVBORw0KGgo="

URLUtil.get_data_uri("text/plain", "base64", "SGVsbG8=")
# "data:text/plain;base64,SGVsbG8="

# normalize 改进（自动处理反斜杠、合并连续斜杠）
URLUtil.normalize("http://example.com\\\\path\\\\to")
# "http://example.com/path/to"
```
