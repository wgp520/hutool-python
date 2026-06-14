# JSON 工具 - JSONUtil

## 由来

`JSONUtil` 基于 Python 内置 `json` 模块封装增强，提供更便捷的 JSON 操作。

## 方法

### 序列化

```python
from hutool import JSONUtil

# 转 JSON 字符串
JSONUtil.to_json_str({"name": "test", "value": 123})
# '{"name": "test", "value": 123}'

# 格式化输出
JSONUtil.to_json_pretty_str({"name": "test"})
# {
#     "name": "test"
# }
```

### 解析

```python
# 解析 JSON 字符串
obj = JSONUtil.parse_obj('{"name": "test"}')     # {"name": "test"}
arr = JSONUtil.parse_array('[1, 2, 3]')           # [1, 2, 3]
data = JSONUtil.parse('{"key": "value"}')          # 自动判断类型
```

### Bean 转换

```python
class User:
    def __init__(self):
        self.name = ""
        self.age = 0

# JSON 转对象
user = JSONUtil.to_bean('{"name": "张三", "age": 25}', User)
print(user.name)  # "张三"

# JSON 数组转对象列表
users = JSONUtil.to_bean_list('[{"name": "张三"}, {"name": "李四"}]', User)

# 对象转 JSON
JSONUtil.from_bean(user)  # '{"name": "张三", "age": 25}'
```

### 文件操作

```python
# 读取 JSON 文件
data = JSONUtil.read_json("config.json")
obj = JSONUtil.read_json_object("config.json")
arr = JSONUtil.read_json_array("data.json")

# 写入 JSON 文件
JSONUtil.write_json("output.json", {"key": "value"}, indent=2)
```

### 路径操作

```python
data = {"user": {"profile": {"name": "张三", "age": 25}}}

# 按路径获取值
JSONUtil.get_by_path(data, "user.profile.name")  # "张三"

# 按路径设置值
JSONUtil.put_by_path(data, "user.profile.email", "test@example.com")
```

### 判断

```python
JSONUtil.is_json('{"key": "value"}')     # True
JSONUtil.is_json_obj('{"key": "value"}') # True
JSONUtil.is_json_array('[1, 2, 3]')      # True
JSONUtil.is_json("not json")             # False
```

### 格式化

```python
# 格式化 JSON
JSONUtil.format_json('{"a":1,"b":2}')
# {
#   "a": 1,
#   "b": 2
# }

# 压缩 JSON（去除空白）
JSONUtil.compress('{\n  "a": 1,\n  "b": 2\n}')
# '{"a":1,"b":2}'
```
