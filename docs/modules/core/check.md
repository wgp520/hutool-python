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
```

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
