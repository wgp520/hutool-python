# 正则工具 - ReUtil

## 由来

Python 内置的 `re` 模块功能强大，但使用起来较为繁琐。`ReUtil` 封装了常用的正则操作，提供更简洁的 API。

## 方法

### 匹配

```python
from hutool import ReUtil

# 判断是否匹配
ReUtil.is_match(r"\d+", "123")       # True
ReUtil.contains(r"\d+", "abc123")    # True

# 提取匹配内容
ReUtil.get(r"\d+", "abc123def")      # "123"
ReUtil.get(r"(\d+)", "abc123def", 1) # "123"（指定分组）

# 获取所有匹配
ReUtil.get_all(r"\d+", "a1b2c3")     # ["1", "2", "3"]
```

### 替换

```python
# 替换所有匹配
ReUtil.replace_all("a1b2c3", r"\d+", "x")    # "axbxcx"

# 替换第一个匹配
ReUtil.replace_first("a1b2c3", r"\d+", "x")  # "axb2c3"

# 删除所有匹配
ReUtil.del_all(r"\d+", "a1b2c3")              # "abc"
```

### 提取与分割

```python
# 提取（使用模板）
ReUtil.extract(r"(\d+)-(\d+)", "2024-01", "$1年$2月")  # "2024年01月"

# 分割
ReUtil.split("a,b,,c", r",")       # ["a", "b", "", "c"]

# 统计匹配次数
ReUtil.count(r"\d+", "a1b2c3")     # 3
```

### 转义

```python
# 转义正则特殊字符
ReUtil.escape("[hello]")  # "\\[hello\\]"
```
