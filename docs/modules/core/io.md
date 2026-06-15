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

## IoUtil

```python
from hutool import IoUtil

# 读取流
content = IoUtil.read(input_stream, charset="utf-8")
data = IoUtil.read_bytes(input_stream)

# 写入流
IoUtil.write(output_stream, "内容", charset="utf-8")

# 拷贝
IoUtil.copy(input_stream, output_stream)

# 关闭
IoUtil.close(closable)
```

## PathUtil

```python
from hutool import PathUtil

PathUtil.normalize("/path/../to/file")  # "/to/file"
PathUtil.get_parent("/path/to/file")    # "/path/to"
PathUtil.get_name("/path/to/file.txt")  # "file.txt"
PathUtil.is_absolute("/path/to/file")   # True
```
