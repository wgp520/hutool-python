# 数字工具 - NumberUtil

## 由来

Java 中的数字运算存在精度问题（如 `0.1 + 0.2 != 0.3`），`NumberUtil` 使用 `Decimal` 进行精确计算。Python 中同样存在浮点精度问题，因此这个工具同样有价值。

## 方法

### 精确运算

```python
from hutool import NumberUtil

# 加减乘除
NumberUtil.add(0.1, 0.2)          # Decimal('0.3')
NumberUtil.sub(1.0, 0.9)          # Decimal('0.1')
NumberUtil.mul(0.1, 0.2)          # Decimal('0.02')
NumberUtil.div(10, 3, 2)          # Decimal('3.33')（保留2位小数）
NumberUtil.div(10, 0)             # Decimal('0')（除零不抛异常）

# 四舍五入
NumberUtil.round(3.14159, 2)      # Decimal('3.14')
NumberUtil.round_str(3.14159, 2)  # "3.14"
```

### 类型判断

```python
NumberUtil.is_number("123.45")  # True
NumberUtil.is_number("abc")     # False
NumberUtil.is_int("123")        # True
NumberUtil.is_float("123.45")   # True
NumberUtil.is_odd(3)            # True
NumberUtil.is_even(4)           # True
```

### 生成与解析

```python
# 生成随机数
NumberUtil.generate_random_number(6)  # "384756"（6位随机数）

# 解析
NumberUtil.parse_int("123")      # 123
NumberUtil.parse_float("3.14")   # 3.14
```

### 格式化

```python
NumberUtil.decimal_format("#,##0.00", 1234567.89)  # "1,234,567.89"
NumberUtil.decimal_format("0.00%", 0.856)          # "85.60%"
```

### 比较与范围

```python
NumberUtil.compare(3, 5)       # -1
NumberUtil.is_greater(5, 3)    # True
NumberUtil.min([3, 1, 4, 1, 5])  # 1
NumberUtil.max([3, 1, 4, 1, 5])  # 5
NumberUtil.is_in(3, [1, 2, 3])   # True
```

### 数学运算

```python
NumberUtil.factorial(5)       # 120（阶乘）
NumberUtil.pow(2, 10)         # 1024
NumberUtil.is_power_of_two(8) # True
NumberUtil.divisor(12, 8)     # 4（最大公约数）
NumberUtil.multiple(3, 4)     # 12（最小公倍数）
```

### 安全转换

```python
# 安全转整数（失败时返回默认值）
NumberUtil.int_or_default("123")       # 123
NumberUtil.int_or_default("abc")       # 0
NumberUtil.int_or_default("abc", -1)   # -1
NumberUtil.int_or_default(None)        # 0

# 安全转浮点数
NumberUtil.float_or_default("3.14")    # 3.14
NumberUtil.float_or_default("abc")     # 0.0
```

### 统计

```python
NumberUtil.avg([1, 2, 3, 4, 5])        # 3.0
NumberUtil.avg([1.5, 2.5, 3.5])        # 2.5

NumberUtil.median([3, 1, 2])           # 2（奇数个取中间）
NumberUtil.median([1, 2, 3, 4])        # 2.5（偶数个取中间均值）
```

### 编解码

```python
# Base62 编解码（0-9, A-Z, a-z）
NumberUtil.num_encode(0)    # "0"
NumberUtil.num_encode(35)   # "Z"
NumberUtil.num_encode(61)   # "z"
NumberUtil.num_encode(100)  # "1C"

NumberUtil.num_decode("1C")  # 100
```

### 字节转换

```python
# bytes → int（大端序）
NumberUtil.bytes_to_int(b'\x00\x00\x01\x00')  # 256

# int → bytes（大端序）
NumberUtil.int_to_bytes(256, 2)    # b'\x01\x00'
NumberUtil.int_to_bytes(1, 4)      # b'\x00\x00\x00\x01'
```

### 数字范围与生成

```python
# 数字范围列表
NumberUtil.range_(0, 5)          # [0, 1, 2, 3, 4]
NumberUtil.range_(0, 10, 3)      # [0, 3, 6, 9]

# 不重复随机数
NumberUtil.generate_by_set(3, 1, 10)  # 3个[1,10]范围内的不重复随机数
```

### 表达式计算与开方

```python
# 安全的数学表达式计算
NumberUtil.calculate("1 + 2 * 3")       # 7.0
NumberUtil.calculate("(1 + 2) * 3")     # 9.0

# 精确平方根
NumberUtil.sqrt(2, 5)     # Decimal('1.41421')
NumberUtil.sqrt(9)         # Decimal('3.0000000000')
```

### 解析

```python
# parseNumber — 智能解析数字
NumberUtil.parse_number("123")   # 123（int）
NumberUtil.parse_number("3.14")  # 3.14（float）

# parseLong
NumberUtil.parse_long("123456789")  # 123456789
```
