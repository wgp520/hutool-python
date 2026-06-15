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
