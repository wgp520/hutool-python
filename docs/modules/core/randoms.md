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
RandomUtil.random_string_lower(8)      # "abcdefgh"（小写）
RandomUtil.random_numbers(6)           # "384756"（纯数字）
```

### 随机选择

```python
items = ["apple", "banana", "cherry"]
RandomUtil.random_ele(items)           # 随机选一个
RandomUtil.random_eles(items, 2)       # 随机选两个
```

### 其他

```python
RandomUtil.random_color()              # "#a1b2c3"（随机十六进制颜色）
```

### 加权随机

```python
# 按权重随机选择
RandomUtil.weighted_choice(["a", "b", "c"], [1, 2, 3])
# "c" 出现概率最高（权重 3/6）
```

### 新增方法

```python
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
```
