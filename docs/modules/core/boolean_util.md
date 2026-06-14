# 布尔工具 - BooleanUtil

## 由来

提供布尔值的解析、转换和逻辑运算。支持从字符串解析布尔值，以及批量逻辑运算。

## 方法

```python
from hutool import BooleanUtil

# 判断
BooleanUtil.is_true(True)    # True
BooleanUtil.is_false(False)  # True

# 转换
BooleanUtil.to_int(True)             # 1
BooleanUtil.int_to_boolean(0)        # False
BooleanUtil.to_str(True, "是", "否") # "是"

# 解析字符串
BooleanUtil.parse("true")   # True
BooleanUtil.parse("yes")    # True
BooleanUtil.parse("1")      # True
BooleanUtil.parse("on")     # True
BooleanUtil.parse("false")  # False

# 逻辑运算（批量）
BooleanUtil.and_(True, True, False)  # False
BooleanUtil.or_(False, False, True)  # True
BooleanUtil.xor(True, True)          # False
BooleanUtil.negate(True)             # False
```
