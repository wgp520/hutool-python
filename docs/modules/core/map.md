# Map 工具 - MapUtil / BiMap

## 由来

提供 Map（字典）的增强操作，包括判空、转换、过滤、排序等。`BiMap` 提供双向查找的映射关系。

## MapUtil

### 判空

```python
from hutool import MapUtil

MapUtil.is_empty({})        # True
MapUtil.is_not_empty({"a": 1})  # True
```

### 创建

```python
MapUtil.of("key", "value")                   # {"key": "value"}
MapUtil.of_entries(("a", 1), ("b", 2))       # {"a": 1, "b": 2}
MapUtil.of_array(["a", 1, "b", 2])           # {"a": 1, "b": 2}
```

### 转换

```python
# 列表转 Map
MapUtil.to_list_map([{"type": "a", "val": 1}, {"type": "a", "val": 2}])
# {"a": [{"type": "a", "val": 1}, {"type": "a", "val": 2}]}

# 连接
MapUtil.join({"a": 1, "b": 2}, "&", "=")  # "a=1&b=2"
MapUtil.sort_join({"b": 2, "a": 1}, "&", "=")  # "a=1&b=2"（按键排序）
```

### 操作

```python
# 过滤
MapUtil.filter({"a": 1, "b": 2, "c": 3}, "a", "c")  # {"a": 1, "c": 3}
MapUtil.filter_by_func({"a": 1, "b": 2, "c": 3}, lambda k, v: v > 1)
# {"b": 2, "c": 3}

# 映射值
MapUtil.map_values({"a": 1, "b": 2}, lambda v: v * 10)
# {"a": 10, "b": 20}

# 排序
MapUtil.sort({"b": 2, "a": 1, "c": 3})         # 按键排序
MapUtil.sort_by_value({"a": 3, "b": 1, "c": 2}) # 按值排序

# 反转
MapUtil.inverse({"a": 1, "b": 2})  # {1: "a", 2: "b"}

# 取值最大的前 N 个键
MapUtil.top_n_keys({"a": 3, "b": 1, "c": 5, "d": 2}, 2)  # ["c", "a"]
```

### 安全取值

```python
data = {"name": "test", "count": "5", "active": "true"}

MapUtil.get_str(data, "name")           # "test"
MapUtil.get_str(data, "missing", "")    # ""
MapUtil.get_int(data, "count")          # 5
MapUtil.get_float(data, "count")        # 5.0
MapUtil.get_bool(data, "active")        # True
```

## BiMap

双向 Map，支持通过键查值和通过值查键：

```python
from hutool import BiMap

bi_map = BiMap()
bi_map.put("a", 1)
bi_map.put("b", 2)

bi_map.get("a")          # 1
bi_map.inverse().get(1)  # "a"
```
