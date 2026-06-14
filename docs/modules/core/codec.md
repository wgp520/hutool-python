# 编解码工具 - Base64 / Base32

## 由来

Base64 和 Base32 是最常用的编码方案，广泛用于数据传输、URL 安全编码等场景。基于 Python 内置 `base64` 模块封装。

## Base64

```python
from hutool import Base64

# 编码
Base64.encode(b"hello")                    # "aGVsbG8="
Base64.encode("你好", charset="utf-8")     # "5L2g5aW9"

# 解码
Base64.decode("aGVsbG8=")                  # b"hello"
Base64.decode_str("aGVsbG8=")              # "hello"

# URL 安全编码
Base64.encode_url_safe(b"hello")           # "aGVsbG8"
Base64.decode_url_safe("aGVsbG8")          # b"hello"
```

## Base32

```python
from hutool import Base32

# 编码
Base32.encode(b"hello")                    # "NBSWY3DP"

# 解码
Base32.decode("NBSWY3DP")                  # b"hello"
```
