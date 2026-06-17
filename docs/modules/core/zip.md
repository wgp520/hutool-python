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

### 其他

```python
# 压缩为字节流
data = ZipUtil.zip_to_stream("/path/to/dir")

# 压缩并返回条目列表
entries = ZipUtil.zip_entries("/path/to/dir", "out.zip")

# 向已有 zip 追加文件
ZipUtil.append("out.zip", "new_file.txt")

# 从字节流解压
ZipUtil.unzip_stream(data, "/dest/dir")

# 列出 zip 文件中的文件名
names = ZipUtil.list_file_names("out.zip")

# 读取 zip 中指定条目的内容
content = ZipUtil.read("out.zip", "test.txt")
```

### Zlib 增强

```python
# zlibCompress — Zlib 压缩（别名）
compressed = ZipUtil.zlib_compress(b"hello world")

# zlibDecompress — Zlib 解压（别名）
original = ZipUtil.zlib_decompress(compressed)

# gzipDecompress — Gzip 解压（别名）
original = ZipUtil.gzip_decompress(gzipped_data)
```

### 文件转换

```python
# toZipFile — 路径/文件转为 zip 文件
ZipUtil.to_zip_file("/path/to/dir", "/path/to/output.zip")

# getZipOutputStream — 获取 ZipFile 写入对象
zf = ZipUtil.get_zip_output_stream("/path/to/output.zip")

# getZipStream — 获取 zip 读取对象
zf = ZipUtil.get_zip_stream("/path/to/file.zip")
```
