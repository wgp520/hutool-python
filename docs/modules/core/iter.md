# 迭代工具 - IterUtil

## 由来

Python 的 `itertools` 模块功能强大但 API 较底层。`IterUtil` 提供常用的 itertools recipes（迭代器配方），兼容 Python 3.8，无需依赖 3.10+ 的 `itertools.pairwise`。

## 方法

### 取值

```python
from hutool import IterUtil

IterUtil.take(3, range(10))        # [0, 1, 2]
IterUtil.take(5, "Hello")          # ['H', 'e', 'l', 'l', 'o']

IterUtil.tail(3, range(10))        # [7, 8, 9]

IterUtil.nth(range(10), 3)         # 3
IterUtil.nth(range(3), 10)         # None（越界）
IterUtil.nth(range(3), 10, -1)     # -1（自定义默认值）

IterUtil.get([10, 20, 30], 1)         # 20
IterUtil.get_first([10, 20])           # 10
IterUtil.get_first_none_null([None, 1])  # 1
IterUtil.first_match([1, 2, 3], lambda x: x > 2)  # 3
IterUtil.get_element_type([1, 2])      # <class 'int'>
```

### 判断与统计

```python
IterUtil.all_equal([1, 1, 1])                       # True
IterUtil.all_equal([1, 2, 1])                       # False
IterUtil.is_empty([])                               # True
IterUtil.is_not_empty([1])                          # True
IterUtil.has_null([1, None, 3])                     # True
IterUtil.is_all_null([None, None])                  # True

IterUtil.quantify([1, 2, 3, 4], lambda x: x % 2 == 0)       # 2（偶数个数）
IterUtil.count_map(["a", "b", "a"])                         # {"a": 2, "b": 1}
IterUtil.field_value_map([{"n": "a", "v": 1}], "n", "v")    # {"a": 1}
```

### 变换

```python
# 展平一层嵌套
list(IterUtil.flatten([[1, 2], [3, 4], [5]]))  # [1, 2, 3, 4, 5]

# 相邻配对
list(IterUtil.pairwise("ABC"))  # [('A', 'B'), ('B', 'C')]

# 按固定长度分组（不足用 fillvalue 填充）
list(IterUtil.grouper("ABCDEFG", 3, 'x'))
# [('A','B','C'), ('D','E','F'), ('G','x','x')]

# 交替轮询
list(IterUtil.roundrobin("ABC", "D", "EF"))
# ['A', 'D', 'E', 'B', 'F', 'C']

IterUtil.to_map([("a", 1)], lambda x: x[0], lambda x: x[1])  # {"a": 1}
IterUtil.to_list(range(3))  # [0, 1, 2]
```

### 分组与幂集

```python
# 按谓词分为两组
f, t = IterUtil.partition(lambda x: x % 2, range(5))
list(f)  # [0, 2, 4]
list(t)  # [1, 3]

# 幂集（所有子集）
list(IterUtil.powerset([1, 2, 3]))
# [(), (1,), (2,), (3,), (1,2), (1,3), (2,3), (1,2,3)]
```

### 去重

```python
# 保序去重
list(IterUtil.unique_everseen("AAAABBBCCDAABBB"))  # ['A','B','C','D']

# 带键函数的去重
list(IterUtil.unique_everseen("ABBCcAD", str.lower))  # ['A','B','C','D']
```

### 其他

```python
# 拼接
IterUtil.join([1, 2, 3], "-")  # "1-2-3"

# 映射/过滤
IterUtil.edit([1, 2, 3], lambda x: x * 2)  # [2, 4, 6]
IterUtil.filter_([1, 2, 3, 4], lambda x: x > 2)  # [3, 4]
IterUtil.for_each([1, 2], print)

# 工具
IterUtil.size(range(100))            # 100
IterUtil.is_equal_list([1, 2], [1, 2])  # True
IterUtil.to_str([1, 2, 3], "-")       # "1-2-3"
```
