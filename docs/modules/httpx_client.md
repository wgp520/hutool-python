# HTTP 客户端 - HttpUtil / HttpRequest / HttpResponse

## 由来

在 Java 的世界中，HTTP 客户端之前一直是 Apache HttpClient 占据主导，但其较为庞大且 API 复杂。Hutool-http 针对 `HttpURLConnection` 做了封装。Python 版基于 `httpx` 实现，提供了同样简洁的 API。

## HttpUtil 快速使用

```python
from hutool import HttpUtil

# GET 请求
content = HttpUtil.get("https://httpbin.org/get")

# POST 请求
result = HttpUtil.post("https://httpbin.org/post",
                       json_data={"city": "北京"})

# 下载文件
HttpUtil.download_file("https://example.com/file.zip", "/path/to/save.zip")

# 下载为字符串
html = HttpUtil.download_string("https://example.com")
```

## HttpRequest 链式调用

对于更复杂的请求场景，使用 `HttpRequest` 的链式 API：

```python
from hutool import HttpRequest

response = (HttpRequest.get("https://httpbin.org/get")
    .header("Accept", "application/json")
    .header("User-Agent", "Hutool-Python")
    .cookie("session=abc123")
    .timeout(5000)
    .charset("utf-8")
    .follow_redirects(True)
    .execute())

print(response.status)     # 200
print(response.body)       # 响应内容
print(response.is_ok())    # True
```

### POST 请求

```python
# 表单提交
response = (HttpRequest.post("https://httpbin.org/post")
    .form("username", "admin")
    .form("password", "123456")
    .execute())

# JSON 提交
response = (HttpRequest.post("https://httpbin.org/post")
    .json({"key": "value"})
    .execute())

# 原始 Body
response = (HttpRequest.post("https://httpbin.org/post")
    .body("raw content")
    .header("Content-Type", "text/plain")
    .execute())
```

## HttpResponse

```python
response = HttpRequest.get("https://httpbin.org/get").execute()

response.status          # 状态码
response.headers         # 响应头
response.body            # 响应体（字符串）
response.is_ok()         # 状态码是否为 2xx
response.to_bytes()      # 响应体（字节）
response.to_json()       # 解析为 JSON
```

## HtmlUtil

HTML 相关工具：

```python
from hutool import HtmlUtil

# HTML 转义
HtmlUtil.escape('<script>alert("xss")</script>')

# 移除 HTML 标签
HtmlUtil.remove_html_tag("<p>Hello <b>World</b></p>")  # "Hello World"
HtmlUtil.clean_html_tag("<p>content</p>")               # "content"
```

## 与 Java Hutool 的差异

- 基于 `httpx` 而非 `HttpURLConnection`，支持 HTTP/2
- 不支持 Java 特有的 `multipart/form-data` 文件上传语法，但通过 `form()` 方法支持
- Cookie 管理由 httpx 自动处理
