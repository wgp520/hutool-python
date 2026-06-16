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

# 驼峰转换
MapUtil.to_camel_case_map({"first_name": "John"})
# {"firstName": "John"}

# 转为二维数组
MapUtil.to_object_array({"a": 1, "b": 2})
# [["a", 1], ["b", 2]]

# 连接
MapUtil.join({"a": 1, "b": 2}, "&", "=")  # "a=1&b=2"
MapUtil.sort_join({"b": 2, "a": 1}, "&", "=")  # "a=1&b=2"（按键排序）

# 拼接（忽略 null 值）
MapUtil.join_ignore_null({"a": 1, "b": None, "c": 3})
# "a=1&c=3"
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

# 键操作
MapUtil.rename_key({"old": 1}, "old", "new")  # {"new": 1}

# 过滤/删除
m = {"a": 1, "b": None, "c": 3}
MapUtil.remove_null_value(m)  # m 变为 {"a": 1, "c": 3}
MapUtil.remove_by_value({"a": 1, "b": 2}, 1)  # {"b": 2}
MapUtil.remove_if({"a": 1, "b": 2}, lambda k, v: v > 1)  # {"a": 1}

# 分割/扁平化
MapUtil.partition({"a": 1, "b": 2, "c": 3, "d": 4}, 2)
# [{"a": 1, "b": 2}, {"c": 3, "d": 4}]

MapUtil.flatten({"a": {"b": 1, "c": {"d": 2}}, "e": 3})
# {"a.b": 1, "a.c.d": 2, "e": 3}

# 值映射
MapUtil.edit({"a": 1, "b": 2}, lambda k, v: v * 10)  # {"a": 10, "b": 20}
MapUtil.map_({"a": 1}, key_func=str.upper, value_func=lambda v: v * 2)
# {"A": 2}

# 惰性计算
m = {}
MapUtil.compute_if_absent(m, "key", lambda k: 42)  # m["key"] = 42
```

### 安全取值

```python
data = {"name": "test", "count": "5", "active": "true"}

MapUtil.get_str(data, "name")                   # "test"
MapUtil.get_str(data, "missing", "")            # ""
MapUtil.get_int(data, "count")                  # 5
MapUtil.get_float(data, "count")                # 5.0
MapUtil.get_bool(data, "active")                # True
MapUtil.get_any({"a": 1, "b": 2}, "x", "b")     # 2
MapUtil.get_double({"a": "2.5"}, "a")           # 2.5
MapUtil.get_long({"a": "2"}, "a")               # 2
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
