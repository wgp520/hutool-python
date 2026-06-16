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
