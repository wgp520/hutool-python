# 数学工具 - MathUtil / BitStatusUtil

## 由来

提供精确的数学运算和位状态管理。

## MathUtil

```python
from hutool import MathUtil

# 精确加法（使用 Decimal）
MathUtil.add(0.1, 0.2)  # Decimal('0.3')

# 角度与弧度转换
MathUtil.point_to_radians((1, 1))      # 弧度值
MathUtil.radians_to_point(3.14159)     # (x, y) 坐标

# 排列数 A(n, m)
MathUtil.arrangement_count(5, 3)   # 60

# 组合数 C(n, m)
MathUtil.combination_count(5, 3)   # 10

# 元/分转换
MathUtil.yuan_to_cent(1.23)        # 123
MathUtil.cent_to_yuan(123)         # 1.23
```

## BitStatusUtil

位状态管理，常用于权限管理等场景：

```python
from hutool import BitStatusUtil

# 添加状态
status = 0
status = BitStatusUtil.add(status, 1, 2)    # 添加状态 1 和 2

# 判断状态
BitStatusUtil.has(status, 1)    # True
BitStatusUtil.has(status, 4)    # False

# 移除状态
status = BitStatusUtil.remove(status, 1)

# 转为二进制字符串
BitStatusUtil.to_binary_string(status)  # "10"
```
