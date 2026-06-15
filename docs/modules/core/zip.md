# 压缩工具 - ZipUtil

## 由来

文件压缩和解压是常见的文件操作需求。`ZipUtil` 基于 Python 内置的 `zipfile`、`gzip`、`zlib` 模块，提供了统一的压缩解压接口。

## 方法

### Zip 压缩/解压

```python
from hutool import ZipUtil

# 压缩文件/目录
ZipUtil.zip("/path/to/dir", "/path/to/output.zip")

# 解压
ZipUtil.unzip("/path/to/output.zip", "/path/to/dest")
```

### Gzip 压缩/解压

```python
# 压缩
compressed = ZipUtil.gzip(b"hello world")
compressed = ZipUtil.gzip("hello world")  # 字符串自动编码

# 解压
original = ZipUtil.ungzip(compressed)  # b"hello world"
```

### Zlib 压缩/解压

```python
# 压缩
compressed = ZipUtil.zlib(b"hello world")

# 解压
original = ZipUtil.unzlib(compressed)
```
