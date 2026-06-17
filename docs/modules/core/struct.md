# 结构体工具 - Struct

## 由来

`Struct` 是 `dict` 子类，支持属性访问语法，递归嵌套转换，类似 JavaScript 对象。

## 方法

### 创建 Struct

```python
from hutool import Struct, make_struct

# 直接创建
s = Struct({"name": "test", "age": 20})
s.name       # 'test'
s["age"]     # 20

# 设置属性
s.email = "test@example.com"
s["email"]   # 'test@example.com'

# 删除属性
del s.name
```

### 从字典创建（Struct.from_dict）

```python
# 类方法 — 递归转换
data = {"user": {"name": "Alice", "tags": [{"id": 1}]}}
s = Struct.from_dict(data)
s.user.name       # 'Alice'
s.user.tags[0].id # 1

# 非递归模式
s = Struct.from_dict({"user": {"name": "test"}}, recursive=False)
s.user            # {'name': 'test'}（仍是 dict）
```

### 递归转换

```python
data = {
    "user": {
        "name": "Alice",
        "address": {"city": "Beijing"}
    },
    "tags": [{"id": 1}, {"id": 2}]
}
s = make_struct(data)
s.user.name            # 'Alice'
s.user.address.city    # 'Beijing'
s.tags[0].id           # 1
```

### 非递归模式

```python
s = make_struct({"user": {"name": "test"}}, recursive=False)
s.user            # {'name': 'test'}（仍是 dict）
isinstance(s.user, Struct)  # False
```

---

```{note}
`Struct` 继承自 `dict`，所有 dict 操作（`keys()`、`items()`、`len()`、`in` 等）均正常工作。
注意：保留字属性（如 `items`、`keys`、`values`）会优先返回 dict 方法而非字典值。
```
