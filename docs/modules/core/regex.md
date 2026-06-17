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

### 查找与位置

```python
# 查找所有匹配
ReUtil.find_all(r"\d+", "a1b2c3")            # ["1", "2", "3"]
ReUtil.find_all_group0(r"\d+", "a1b2c3")     # ["1", "2", "3"]（等价于 find_all）
ReUtil.find_all_group1(r"(\d)(\d)", "12 34") # ["2", "4"]（捕获组1）

# 查找第一个数字
ReUtil.find_first_number("abc123def")  # "123"

# 匹配位置
ReUtil.index_of(r"\d+", "abc123")       # 3（第一个匹配的起始位置）
ReUtil.last_index_of(r"\d+", "a1b2c3")  # 4（最后一个匹配的起始位置）
```

### 删除匹配

```python
# 删除第一个/最后一个匹配
ReUtil.del_first(r"\d+", "a1b2c3")  # "ab2c3"
ReUtil.del_last(r"\d+", "a1b2c3")   # "a1b2c"

# 删除匹配之前的内容
ReUtil.del_pre(r"\d+", "abc123def")  # "123def"

# 提取并删除
ReUtil.extract_multi_and_del_pre(r"\d+", "abc123def456", 0)
# ("123", "def456")
```

### 其他

```python
# 获取命名捕获组
ReUtil.get_all_group_names(r"(?P<year>\d{4})-(?P<month>\d{2})")
# {"year": 1, "month": 2}

# 正则替换 + 回调函数
ReUtil.replace_by_func("hello123", r"\d+", lambda m: "[NUM]")
# "hello[NUM]"
```

### 模式匹配

```python
# findFirstPattern — 按优先级查找第一个匹配的模式
ReUtil.find_first_pattern("abc123", [r"\d+", r"[a-z]+"])  # r"\d+"
ReUtil.find_first_pattern("!!!", [r"\d+", r"[a-z]+"])      # None

# findAllPatterns — 查找所有匹配的模式
ReUtil.find_all_patterns("Hello123", [r"\d+", r"[a-z]+", r"[A-Z]+"])
# [r"\d+", r"[a-z]+", r"[A-Z]+"]
```
