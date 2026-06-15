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
```

### 查找

```python
ArrayUtil.index_of([1, 2, 3], 2)          # 1
ArrayUtil.contains([1, 2, 3], 2)           # True
ArrayUtil.contains_any([1, 2, 3], 2, 5)   # True
ArrayUtil.contains_all([1, 2, 3], 1, 2)   # True
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
