# 校验码工具 - CheckUtil

## 由来

校验码广泛用于条形码、身份证号、银行卡号等场景，用于检测输入错误。`CheckUtil` 提供了 EAN/UPC 条形码校验位和 Verhoeff 校验位算法，以及常用的格式校验方法。

## 方法

### EAN/UPC 校验位

```python
from hutool import CheckUtil

# 计算校验位
CheckUtil.ean_digit('400599871650')   # '2'
CheckUtil.ean_digit('1234567890123')  # '1'

# 验证条形码
CheckUtil.verify_ean('4005998000007')   # True
CheckUtil.verify_ean('4005998000000')   # False
```

### Verhoeff 校验位

Verhoeff 算法基于二面体群 D₅，可检测所有单字符错误和相邻换位错误，优于传统模 10 校验：

```python
# 计算校验位
CheckUtil.verhoeff_digit('123456654321')  # '9'
CheckUtil.verhoeff_digit('1')             # '5'

# 验证
CheckUtil.verify_verhoeff('1234566543219')  # True
CheckUtil.verify_verhoeff('1234566543210')  # False

# 生成带校验位的 ID
CheckUtil.build_verhoeff_id('Foo', 1)          # 'Foo00011'
CheckUtil.build_verhoeff_id('ORD', 123, length=6)  # 'ORD000123...'
```

### 格式校验

```python
# MAC 地址
CheckUtil.is_mac('00:1A:2B:3C:4D:5E')  # True
CheckUtil.is_mac('00-1A-2B-3C-4D-5E')  # True
CheckUtil.is_mac('invalid')             # False

# 中文字符
CheckUtil.is_chinese('你好世界')    # True
CheckUtil.is_chinese('你好world')   # False

# 英文字母
CheckUtil.is_english('Hello')      # True
CheckUtil.is_english('Hello123')   # False

# 符号
CheckUtil.is_symbol('!@#$%')       # True
CheckUtil.is_symbol('!@#abc')      # False

# URL
CheckUtil.contains_url('visit https://example.com now')  # True
CheckUtil.contains_url('no url here')                     # False

# 空白行
CheckUtil.is_blank_line('   ')  # True
CheckUtil.is_blank_line('hello') # False

# QQ 号
CheckUtil.is_qq('123456789')   # True（5-11 位，不以 0 开头）
CheckUtil.is_qq('01234')       # False

# 日期时间
CheckUtil.is_date_time('2024-01-15 08:30:00')  # True
CheckUtil.is_date_time('2024-13-01 00:00:00')  # False

# 邮编
CheckUtil.is_post_code('100000')  # True
CheckUtil.is_post_code('1234')    # False

# 手机号
CheckUtil.is_phone_number('13812345678')  # True
CheckUtil.is_phone_number('12345678')     # False

# 银行卡号
CheckUtil.is_bank_card('6222021234567890123')  # True

# 日期
CheckUtil.is_date('2024-01-15')     # True
CheckUtil.is_date('2024/01/15')     # True

# IP 地址
CheckUtil.is_ip('192.168.1.1')      # True
CheckUtil.is_ip('::1')              # True

# Unicode 字符
CheckUtil.is_unicode('\\u4e2d')     # True

# DPD 校验位
CheckUtil.dpd_check_digit('12345')  # 校验位
```

### Validator 验证器

`Validator` 提供 `is_*` 判断和 `validate_*` 校验（失败抛 `ValidateException`）两套方法：

```python
from hutool import Validator

# is_* 系列 — 返回 bool
Validator.is_email('test@example.com')           # True
Validator.is_ipv4('192.168.1.1')                 # True
Validator.is_ipv6('::1')                         # True
Validator.is_url('https://example.com')           # True
Validator.is_uuid('550e8400-e29b-41d4-a716-446655440000')  # True
Validator.is_mobile('13812345678')               # True
Validator.is_plate_number('京A12345')             # True
Validator.is_car_vin('LSGJA52U7AH000001')       # True
Validator.is_birthday('1990-01-15')              # True
Validator.is_chinese_name('张三')                 # True
Validator.is_credit_code('91350100M000100Y43')   # True
Validator.is_citizen_id('110101199001011234')    # True
Validator.is_money('123.45')                     # True
Validator.is_general('hello_123')                # True
Validator.is_general_with_chinese('你好abc')      # True
Validator.is_word('Hello')                       # True
Validator.is_hex('FF00FF')                       # True
Validator.is_letter('abc')                       # True
Validator.is_number('123')                       # True
Validator.is_zip_code('100000')                  # True
Validator.is_between(5, 1, 10)                   # True
Validator.is_null(None)                          # True
Validator.is_not_null('abc')                     # True
Validator.is_empty([])                           # True
Validator.is_not_empty([1])                      # True
Validator.has_chinese('你好')                     # True
Validator.has_number('abc123')                   # True
```

### validate_* 系列

```python
# 校验通过返回 None，失败抛 ValidateException
Validator.validate_email('test@example.com')     # None
Validator.validate_mobile('13812345678')          # None
Validator.validate_not_empty('abc')               # None
Validator.validate_not_null('abc')                # None
Validator.validate_between(5, 1, 10)              # None
Validator.validate_upper_case('ABC')              # None
Validator.validate_lower_case('abc')              # None

# 自定义错误信息
Validator.validate_email('invalid', '邮箱格式错误')
# 抛出 ValidateException: 邮箱格式错误
```

### 索引校验

```python
# checkIndexLimit — 索引范围校验
CheckUtil.check_index_limit(5, 10)  # True（5 < 10）
CheckUtil.check_index_limit(10, 10) # False（10 >= 10）
```

### 正则匹配校验

```python
# validateMatchRegex — 正则匹配校验
Validator.validate_match_regex('abc123', r'^[a-z0-9]+$')  # True
```

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
