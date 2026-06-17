# IO 工具 - FileUtil / IoUtil / PathUtil

## 由来

文件操作是日常开发中最频繁的操作之一。`FileUtil` 封装了常用的文件读写、复制、删除等操作，`IoUtil` 处理 IO 流操作，`PathUtil` 提供路径操作。

## FileUtil

### 判断

```python
from hutool import FileUtil

FileUtil.exist("/path/to/file")     # True
FileUtil.is_file("/path/to/file")   # True
FileUtil.is_dir("/path/to/dir")     # True
FileUtil.is_empty("/path/to/file")  # True（文件为空或目录为空）
FileUtil.is_absolute("/path")       # True
```

### 创建

```python
# 创建文件
FileUtil.touch("/path/to/newfile.txt")

# 创建目录
FileUtil.mkdir("/path/to/newdir")
FileUtil.mkdirs("/path/to/new/deep/dir")

# 创建临时文件
tmp = FileUtil.create_temp_file("prefix", ".txt")
```

### 读写

```python
# 读取
content = FileUtil.read_string("/path/to/file.txt", charset="utf-8")
data = FileUtil.read_bytes("/path/to/file.bin")
lines = FileUtil.read_lines("/path/to/file.txt")
lines = FileUtil.read_utf8_lines("/path/to/file.txt")

# 写入
FileUtil.write_string("/path/to/file.txt", "内容")
FileUtil.write_bytes("/path/to/file.bin", b"data")
FileUtil.write_lines("/path/to/file.txt", ["line1", "line2"])

# 追加
FileUtil.append_string("/path/to/file.txt", "追加内容")
FileUtil.append_lines("/path/to/file.txt", ["追加行"])

# 读取末尾 N 行
FileUtil.tail("/path/to/file.log", 10)      # 最后 10 行
FileUtil.tail("/path/to/file.log")           # 最后 10 行（默认）
```

### 复制与移动

```python
FileUtil.copy("/src/file.txt", "/dest/file.txt")
FileUtil.copy_file("/src/file.txt", "/dest/file.txt")
FileUtil.move("/src/file.txt", "/dest/file.txt")
FileUtil.rename("/path/old.txt", "new.txt")
```

### 删除

```python
FileUtil.del("/path/to/file.txt")    # 删除文件
FileUtil.clean("/path/to/dir")       # 清空目录
```

### 遍历

```python
# 遍历目录下所有文件
files = FileUtil.loop_files("/path/to/dir")

# 带过滤器
files = FileUtil.loop_files("/path/to/dir", file_filter=lambda f: f.endswith(".py"))

# 列出文件名
names = FileUtil.list_file_names("/path/to/dir")
```

### 信息

```python
FileUtil.size("/path/to/file")                    # 文件大小（字节）
FileUtil.last_modified_time("/path/to/file")      # 最后修改时间
FileUtil.get_total_lines("/path/to/file")         # 总行数
FileUtil.get_name("/path/to/file.txt")            # "file.txt"
FileUtil.get_suffix("/path/to/file.txt")          # ".txt"
FileUtil.get_prefix("/path/to/file.txt")          # "file"
FileUtil.main_name("/path/to/file.txt")           # "file"
```

### 系统路径

```python
FileUtil.get_tmp_dir_path()     # "/tmp" 或系统临时目录
FileUtil.get_user_home_path()   # 用户主目录
```

### 其他

```python
# UTF-8 读写
FileUtil.write_utf8_string("/path/to/file.txt", "内容")
FileUtil.read_utf8_string("/path/to/file.txt")   # "内容"

# UTF-8 追加
FileUtil.append_utf8_string("/path/to/file.txt", "追加内容")
FileUtil.append_utf8_lines("/path/to/file.txt", ["行1", "行2"])

# UTF-8 写入多行
FileUtil.write_utf8_lines("/path/to/file.txt", ["行1", "行2"])

# Map 写入（key=value 格式）
FileUtil.write_utf8_map("/path/to/config.ini", {"host": "localhost", "port": "8080"})

# 读取行
FileUtil.read_line("/path/to/file.txt", 3)  # 第 3 行
FileUtil.load_utf8("/path/to/file.txt")     # 按行加载为列表

# 路径操作
FileUtil.get_absolute_path("relative/path")     # 绝对路径
FileUtil.get_canonical_path("/path/../to/file")  # 规范路径
FileUtil.get_parent("/a/b/c", depth=2)          # "/a"
FileUtil.is_absolute_path("/path/to/file")       # True

# 状态检查
FileUtil.is_dir_empty("/path/to/dir")           # True（空目录）
FileUtil.is_sub_path("/parent", "/parent/child") # True
FileUtil.content_equals("/path/a.txt", "/path/b.txt")  # True
FileUtil.check_slip("/path/to/file")            # 路径穿越检查

# 文件类型检测
FileUtil.get_type("/path/to/image.png")          # "png"
FileUtil.get_mime_type("/path/to/file.txt")       # "text/plain"

# 校验和
FileUtil.checksum("/path/to/file", "sha256")     # SHA-256 校验和
FileUtil.checksum_crc32("/path/to/file")         # CRC32 校验

# 编码转换
FileUtil.convert_charset("/path/to/file", "gbk", "utf-8")

# 换行符转换
FileUtil.convert_line_separator("/path/to/file", "\n")

# 安全创建
FileUtil.mk_parent_dirs("/path/to/deep/file.txt")  # 创建父目录
```

## IoUtil

```python
from hutool import IoUtil
from io import BytesIO

# 读取流
content = IoUtil.read(input_stream, charset="utf-8")
data = IoUtil.read_bytes(input_stream)

# 写入流
IoUtil.write(output_stream, "内容", charset="utf-8")

# 拷贝
IoUtil.copy(input_stream, output_stream)

# 关闭
IoUtil.close(closable)

# UTF-8 读写
stream = BytesIO(b"hello")
IoUtil.read_utf8(stream)            # "hello"
IoUtil.read_utf8_lines(stream)      # ["hello"]

# 流转字符串
IoUtil.to_str(stream, charset="utf-8")

# 字符串转流
s = IoUtil.to_stream("hello")       # BytesIO
s = IoUtil.to_utf8_stream("hello")  # UTF-8 BytesIO

# 行迭代器
for line in IoUtil.line_iter(stream):
    print(line)

# 十六进制读取
IoUtil.read_hex(BytesIO(b"\x00\xff"))  # "00ff"

# 校验和
IoUtil.checksum(stream, "md5")
IoUtil.checksum_crc32(stream)
IoUtil.checksum_value(stream, "sha256")  # 返回 int

# 流比较
IoUtil.content_equals(BytesIO(b"abc"), BytesIO(b"abc"))  # True

# 刷新
IoUtil.flush(output_stream)

# UTF-8 写入
output = BytesIO()
IoUtil.write_utf8(output, "hello")
```

## PathUtil

```python
from hutool import PathUtil

PathUtil.normalize("/path/../to/file")  # "/to/file"
PathUtil.get_parent("/path/to/file")    # "/path/to"
PathUtil.get_name("/path/to/file.txt")  # "file.txt"
PathUtil.is_absolute("/path/to/file")   # True

# 复制/移动
PathUtil.copy_content("/src/file", "/dest/file")
PathUtil.copy_file("/src/file.txt", "/dest/file.txt")
PathUtil.move_content("/src/file", "/dest/file")

# 临时文件
PathUtil.create_temp_file(prefix="tmp", suffix=".txt")

# 删除
PathUtil.del_path("/path/to/file")

# 路径元素
PathUtil.get_last_path_ele("/path/to/file")   # "file"
PathUtil.get_path_ele("/a/b/c", 1)            # "b"
PathUtil.get_path_ele("/a/b/c", -1)           # "c"

# 判断
PathUtil.is_dir_empty("/path/to/dir")
PathUtil.is_exists_and_not_directory("/path/to/file")
PathUtil.is_sub("/parent", "/parent/child")
PathUtil.is_symlink("/path/to/link")

# MIME 类型
PathUtil.get_mime_type("/path/to/file.txt")  # "text/plain"

# 重命名
PathUtil.rename_path("/path/to/old.txt", "new.txt")

# 绝对规范路径
PathUtil.to_abs_normal("/path/../to/file")  # "/to/file"

# 文件遍历
for f in PathUtil.walk_files("/path/to/dir"):
    print(f)
```
