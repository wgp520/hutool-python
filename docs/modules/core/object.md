# 对象工具 - ObjectUtil

## 由来

类似于 Apache Commons Lang 中的 `ObjectUtils`，提供对象判空、默认值、比较等常用操作。

## 方法

### 判空

```python
from hutool import ObjectUtil

ObjectUtil.is_null(None)        # True
ObjectUtil.is_not_null("abc")   # True
ObjectUtil.is_empty("")         # True
ObjectUtil.is_empty([])         # True
ObjectUtil.is_empty(None)       # True
ObjectUtil.is_not_empty("abc")  # True
```

### 默认值

```python
ObjectUtil.default_if_null(None, "default")     # "default"
ObjectUtil.default_if_null("value", "default")  # "value"
ObjectUtil.default_if_empty("", "default")      # "default"
ObjectUtil.default_if_blank("  ", "default")    # "default"
```

### 批量判断

```python
ObjectUtil.has_null("a", None, "b")          # True
ObjectUtil.has_empty("a", "", "b")           # True
ObjectUtil.is_all_empty("", None, [])        # True
ObjectUtil.is_all_not_empty("a", "b", "c")   # True
```

### 比较

```python
ObjectUtil.equals("abc", "abc")   # True
ObjectUtil.not_equal("abc", "def") # True
ObjectUtil.compare(1, 2)           # -1
```

### 工具

```python
ObjectUtil.length("hello")         # 5
ObjectUtil.length([1, 2, 3])       # 3
ObjectUtil.contains([1, 2, 3], 2)  # True
ObjectUtil.to_string(123)          # "123"
```

### 其他

```python
# 克隆（仅 list/dict 深拷贝）
cloned = ObjectUtil.clone_if_possible([1, 2])

# 数字有效性
ObjectUtil.is_valid_if_number(1.5)        # True
ObjectUtil.is_valid_if_number(float("nan"))  # False

# supplier 惰性默认值
ObjectUtil.default_if_null_supplier(None, lambda: "default")     # "default"
ObjectUtil.default_if_empty_supplier("", lambda: "default")      # "default"
ObjectUtil.default_if_blank_supplier("   ", lambda: "default")   # "default"
```

### 安全属性获取

```python
# getAttrSafe — 安全获取对象属性（不存在返回默认值）
class User:
    name = "张三"

ObjectUtil.get_attr_safe(User(), "name")          # "张三"
ObjectUtil.get_attr_safe(User(), "age", 0)        # 0
ObjectUtil.get_attr_safe(None, "name")             # None
```

### 键格式化

```python
# getKeyFmt — 格式化 Map 键
ObjectUtil.get_key_fmt({"name": "test"}, "name", "key_{}")  # "test"
ObjectUtil.get_key_fmt({}, "name", "key_{}")                 # "key_name"
```

### 解包到字典

```python
# unpackToDict — 将对象属性解包为字典
class Config:
    host = "localhost"
    port = 8080

ObjectUtil.unpack_to_dict(Config())
# {"host": "localhost", "port": 8080}
```

### 异常安全

```python
# noneOnException — 捕获异常返回 None
ObjectUtil.none_on_exception(lambda: 1 / 0)  # None
ObjectUtil.none_on_exception(lambda: 100)     # 100
```

### 空值计数

```python
# emptyCount — 统计空值数量（None/""/空集合）
ObjectUtil.empty_count(None, "", [], "abc")   # 3
ObjectUtil.empty_count(1, 2, 3)               # 0
```

### 安全相等比较

```python
# equal — None 安全相等比较
ObjectUtil.equal(None, None)   # True
ObjectUtil.equal("abc", "abc") # True
ObjectUtil.equal(None, "abc")  # False
```
