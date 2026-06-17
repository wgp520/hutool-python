# 数组工具 - ArrayUtil

## 由来

Java 中数组操作不够方便，`ArrayUtil` 提供了一系列静态方法简化数组操作。Python 中列表（list）是主要的序列类型，此工具针对列表提供增强操作。

## 方法

### 判空

```python
from hutool import ArrayUtil

ArrayUtil.is_empty([])        # True
ArrayUtil.is_not_empty([1])   # True
ArrayUtil.has_null(1, None)   # True

# 默认值
ArrayUtil.default_if_empty([], [1])          # [1]
```

### 操作

```python
# 添加元素
ArrayUtil.append([1, 2], 3, 4)        # [1, 2, 3, 4]
ArrayUtil.insert([1, 3], 1, 2)        # [1, 2, 3]

# 删除
ArrayUtil.remove([1, 2, 3], 1)        # [1, 3]
ArrayUtil.remove_ele([1, 2, 3], 2)    # [1, 3]

# 反转
ArrayUtil.reverse([1, 2, 3])          # [3, 2, 1]

# 洗牌
ArrayUtil.shuffle([1, 2, 3, 4, 5])    # 随机排列

# 替换/调整
ArrayUtil.replace([1, 2, 3], 1, 99)          # 返回旧值 2
ArrayUtil.resize([1, 2], 4, 0)               # [1, 2, 0, 0]
ArrayUtil.add_all([1, 2], 3, 4)              # [1, 2, 3, 4]

# 编辑/过滤
ArrayUtil.edit([1, 2, 3], lambda x: x * 2)  # [2, 4, 6]
ArrayUtil.remove_null([1, None, 2])          # [1, 2]
ArrayUtil.remove_blank(["a", "  ", "b"])     # ["a", "b"]
```

### 查找

```python
ArrayUtil.index_of([1, 2, 3], 2)          # 1
ArrayUtil.contains([1, 2, 3], 2)           # True
ArrayUtil.contains_any([1, 2, 3], 2, 5)   # True
ArrayUtil.contains_all([1, 2, 3], 1, 2)   # True
ArrayUtil.first_match([1, 2, 3], lambda x: x > 1)  # 2
ArrayUtil.match_index([1, 2, 3], lambda x: x > 1)   # 1

# 大小写忽略查找
ArrayUtil.contains_ignore_case(["A", "b"], "a")  # True

# 安全获取
ArrayUtil.get([1, 2, 3], 5)                  # None
ArrayUtil.get_any([1, 2, 3])                 # 1
```

### 子数组

```python
ArrayUtil.sub([1, 2, 3, 4, 5], 1, 3)  # [2, 3]
```

### 转换

```python
ArrayUtil.join([1, 2, 3], ",")        # "1,2,3"
ArrayUtil.zip(["a", "b"], [1, 2])     # {"a": 1, "b": 2}
ArrayUtil.to_list((1, 2, 3))          # [1, 2, 3]
```

### 工具

```python
ArrayUtil.length([1, 2, 3])           # 3
ArrayUtil.min([3, 1, 4])              # 1
ArrayUtil.max([3, 1, 4])              # 4
ArrayUtil.swap([1, 2, 3], 0, 2)      # [3, 2, 1]
ArrayUtil.filter([1, 2, 3, 4], lambda x: x > 2)  # [3, 4]
```

### 子数组查找

```python
# indexOfSub — 子数组首次出现索引
ArrayUtil.index_of_sub([1, 2, 3, 4, 5], [2, 3])  # 1
ArrayUtil.index_of_sub([1, 2, 3, 4, 5], [3, 4])  # 2

# lastIndexOfSub — 子数组最后出现索引
ArrayUtil.last_index_of_sub([1, 2, 3, 2, 3], [2, 3])  # 3
```

### 批量判空

```python
# isAllEmpty — 是否全部为空
ArrayUtil.is_all_empty([], None)       # True
ArrayUtil.is_all_empty([], [1])        # False

# isAllNotEmpty — 是否全部非空
ArrayUtil.is_all_not_empty([1], [2])   # True
ArrayUtil.is_all_not_empty([1], [])    # False

# isAllNotNull — 是否全部非 None
ArrayUtil.is_all_not_null([1], [2])    # True
ArrayUtil.is_all_not_null([1], None)   # False
```

### 排序检查

```python
# isSorted — 是否已排序
ArrayUtil.is_sorted([1, 2, 3], cmp=lambda a, b: (a > b) - (a < b))  # True

# isSortedAsc — 是否升序
ArrayUtil.is_sorted_asc([1, 2, 3])    # True
ArrayUtil.is_sorted_asc([1, 3, 2])    # False

# isSortedDesc — 是否降序
ArrayUtil.is_sorted_desc([3, 2, 1])   # True
```

### 子数组判断

```python
# isSub — 是否为子数组
ArrayUtil.is_sub([2, 3], [1, 2, 3, 4])   # True
ArrayUtil.is_sub([2, 4], [1, 2, 3, 4])   # False
```

### 映射与转换

```python
# mapToSet — 数组映射为集合
ArrayUtil.map_to_set([1, 2, 3], lambda x: x * 2)  # {2, 4, 6}

# toArray — 转为列表
ArrayUtil.to_array((1, 2, 3))    # [1, 2, 3]
ArrayUtil.to_array(range(5))     # [0, 1, 2, 3, 4]
```

### 数组合并

```python
# zipArrays — 数组交错合并
ArrayUtil.zip_arrays([1, 2, 3], ["a", "b", "c"])
# [(1, "a"), (2, "b"), (3, "c")]

# 长度不等时用 None 填充
ArrayUtil.zip_arrays([1, 2], ["a", "b", "c"])
# [(1, "a"), (2, "b"), (None, "c")]
```
