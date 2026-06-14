# 集合工具 - CollUtil / ListUtil

## 由来

Java 中集合操作繁琐，需要大量样板代码。`CollUtil` 提供了集合判空、转换、分组、过滤等常用操作。Python 版将 Java 的 Stream 操作理念与 Python 的列表推导式结合。

## CollUtil

### 判空

```python
from hutool import CollUtil

CollUtil.is_empty([])        # True
CollUtil.is_not_empty([1])   # True
CollUtil.has_null([1, None]) # True
CollUtil.contains([1, 2, 3], 2)        # True
CollUtil.contains_any([1, 2, 3], 2, 5) # True
```

### 创建

```python
CollUtil.new_array_list(1, 2, 3)       # [1, 2, 3]
CollUtil.new_hash_set(1, 2, 3)         # {1, 2, 3}
CollUtil.new_linked_hash_set(1, 2, 3)  # 有序集合
```

### 转换

```python
# 转为列表/集合
CollUtil.to_list((1, 2, 3))      # [1, 2, 3]
CollUtil.to_set([1, 2, 2, 3])    # {1, 2, 3}

# 分组
items = [{"type": "a", "val": 1}, {"type": "b", "val": 2}, {"type": "a", "val": 3}]
CollUtil.group_by(items, lambda x: x["type"])
# {"a": [{"type": "a", "val": 1}, ...], "b": [...]}

# 分区
CollUtil.partition([1, 2, 3, 4, 5], 2)  # [[1, 2], [3, 4], [5]]

# 转 Map
CollUtil.to_map([("a", 1), ("b", 2)], lambda x: x[0], lambda x: x[1])
# {"a": 1, "b": 2}
```

### 操作

```python
# 过滤与映射
CollUtil.filter([1, 2, 3, 4], lambda x: x > 2)    # [3, 4]
CollUtil.map([1, 2, 3], lambda x: x * 2)           # [2, 4, 6]
CollUtil.flat_map([[1, 2], [3, 4]], lambda x: x)   # [1, 2, 3, 4]

# 去重与排序
CollUtil.distinct([1, 2, 2, 3])         # [1, 2, 3]
CollUtil.sort([3, 1, 2])                # [1, 2, 3]
CollUtil.reverse([1, 2, 3])             # [3, 2, 1]

# 查找
CollUtil.find_first([1, 2, 3], lambda x: x > 1)  # 2
CollUtil.find_last([1, 2, 3], lambda x: x < 3)   # 2
CollUtil.any_match([1, 2, 3], lambda x: x > 2)    # True
CollUtil.all_match([1, 2, 3], lambda x: x > 0)    # True
CollUtil.none_match([1, 2, 3], lambda x: x > 5)   # True

# 连接
CollUtil.join([1, 2, 3], ",")  # "1,2,3"
```

### 工具

```python
CollUtil.get_first([1, 2, 3])   # 1
CollUtil.get_last([1, 2, 3])    # 3
CollUtil.min([3, 1, 4])         # 1
CollUtil.max([3, 1, 4])         # 4
CollUtil.count([1, 2, 3, 4], lambda x: x > 2)  # 2
```

## ListUtil

`ListUtil` 提供列表特有的操作：

```python
from hutool import ListUtil

# 子列表
ListUtil.sub([1, 2, 3, 4, 5], 1, 3)  # [2, 3]

# 分页
ListUtil.page([1, 2, 3, 4, 5], 1, 2)  # [1, 2]（第1页，每页2条）

# 空安全
ListUtil.empty_if_null(None)     # []
ListUtil.default_if_empty([], [0])  # [0]
```
