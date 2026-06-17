# 随机工具 - RandomUtil

## 由来

Java 中 `Random` 类使用不够便捷，`RandomUtil` 封装了常用的随机操作。Python 版基于 `random` 和 `secrets` 模块实现。

## 方法

### 基础随机

```python
from hutool import RandomUtil

RandomUtil.random_int(1, 100)          # 1~99 的随机整数
RandomUtil.random_int()                # 0~MAX 的随机整数
RandomUtil.random_float(0.0, 1.0)     # 随机浮点数
RandomUtil.random_boolean()            # 随机布尔值
RandomUtil.random_bytes(16)            # 16 字节随机数据
```

### 随机字符串

```python
RandomUtil.random_string(10)           # "aB3dE5fG7h"（10位随机字符串）
RandomUtil.random_string_upper(8)      # "ABCDEFGH"（大写）
RandomUtil.random_string_lower(8)      # "ab3cd5ef"（小写+数字）
RandomUtil.random_numbers(6)           # "384756"（纯数字）
```

### 随机选择

```python
items = ["apple", "banana", "cherry"]
RandomUtil.random_ele(items)           # 随机选一个
RandomUtil.random_eles(items, 2)       # 随机选两个
```

### 加权随机

```python
# 按权重随机选择
RandomUtil.weighted_choice(["a", "b", "c"], [1, 2, 3])
# "c" 出现概率最高（权重 3/6）
```

### 其他

```python
# 随机颜色
RandomUtil.random_color()              # "#a1b2c3"（随机十六进制颜色）

# 随机中文字符
RandomUtil.random_chinese(5)  # 5个随机汉字

# 从字符集随机取一个字符
RandomUtil.random_char("abc")  # "a" 或 "b" 或 "c"

# 随机日期（仅日期，无时分秒）
from datetime import datetime
RandomUtil.random_day(datetime(2024, 1, 1), datetime(2024, 12, 31))

# 随机整数列表（可重复）
RandomUtil.random_ints(5, 1, 10)  # 5个[1,10)范围的随机整数

# 排除指定字符的随机字符串
RandomUtil.random_string_without_str(20, "aeiou")   # 不含元音字母的随机字符串
RandomUtil.random_string_lower_without_str(10, "xz") # 小写，不含 x 和 z

# 按条件随机选取
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
RandomUtil.random_ele_with_condition(data, lambda x: x > 5, 3)  # 3个>5的随机数

# 随机生成器工厂
rng = RandomUtil.create_secure_random()           # 创建随机数生成器
rng = RandomUtil.create_secure_random(b"seed")     # 带种子（可复现）
rng = RandomUtil.get_secure_random()               # 默认随机数生成器
rng = RandomUtil.get_secure_random_strong()        # 强随机数生成器

# 带边界控制的随机整数
RandomUtil.random_int_with_bound(1, 10, include_min=True, include_max=True)  # [1,10]
RandomUtil.random_int_with_bound(1, 10, include_min=False, include_max=False)  # (1,10)

# 随机长整数
RandomUtil.random_long()           # 0~2^63 的随机长整数
RandomUtil.random_long(10, 100)    # [10, 100)

# 随机排列
RandomUtil.random_ints_permutation(5)  # [0, 5) 的随机排列，如 [3, 0, 4, 1, 2]

# 随机字符
RandomUtil.random_number_char()    # 随机数字字符 '0'-'9'
RandomUtil.random_char_no_arg()    # 大小写字母+数字中随机取一个

# 不重复随机元素
RandomUtil.random_ele_list(items, 3)   # 不重复列表
RandomUtil.random_ele_set(items, 3)    # 不重复集合

# 从前 N 个元素中随机取
RandomUtil.random_ele_from_first_n(items, 3)  # 从前3个中随机取1个

# weight_random 别名
RandomUtil.weight_random([(1, "a"), (9, "b")])  # "b" 概率更高

# 允许重复选取
RandomUtil.random_eles(items, 5, allow_duplicate=True)  # 可重复
```

### 日期时间随机

```python
from datetime import datetime

# 随机日期时间
RandomUtil.random_datetime(datetime(2024, 1, 1), datetime(2024, 12, 31))

# 随机日期（仅日期部分）
RandomUtil.random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
```

### 高级随机字符串

```python
# 纯数字随机字符串
RandomUtil.random_digits(8)  # "38475612"（8位纯数字）

# 字母+数字随机字符串
RandomUtil.random_alphanumeric(10)  # "aB3dE5fG7h"

# 大写字母随机字符串
RandomUtil.random_upper_ascii(6)  # "ABCDEF"
```

### 加权随机类

```python
from hutool import WeightedRand

# 创建加权随机选择器
wr = WeightedRand([("a", 1), ("b", 2), ("c", 3)])
wr.next()   # 按权重随机返回 "a"/"b"/"c"
wr.next()
```
