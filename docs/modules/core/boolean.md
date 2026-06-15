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

### 新增方法

```python
# toBoolean — 万能布尔转换
BooleanUtil.to_boolean("true")  # True
BooleanUtil.to_boolean("yes")   # True
BooleanUtil.to_boolean(1)       # True
BooleanUtil.to_boolean("no")    # False

# isBoolean — 判断是否为布尔字符串
BooleanUtil.is_boolean("true")   # True
BooleanUtil.is_boolean("abc")    # False

# 格式化输出
BooleanUtil.to_string_true_false(True)  # "true"
BooleanUtil.to_string_yes_no(True)      # "yes"
BooleanUtil.to_string_on_off(True)      # "on"

# xorOfWrap — 两值异或
BooleanUtil.xor_of_wrap(True, False)  # True

# exactlyOneTrue — 恰好一个为 True
BooleanUtil.exactly_one_true(True, False, False)  # True
BooleanUtil.exactly_one_true(True, True, False)   # False

# ifTrue — 三元表达式
BooleanUtil.if_true(True, "yes", "no")   # "yes"
BooleanUtil.if_true(False, "yes", "no")  # "no"
```
