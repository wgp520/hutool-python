# 类型转换工具 - ConvertUtil

## 由来

类型转换是日常开发中最常见的操作之一。`ConvertUtil` 提供 `bytes↔int`、通用类型转换、安全字符串转换等常用方法。

## 方法

### 字节转换

```python
from hutool import ConvertUtil

# bytes → int（大端序）
ConvertUtil.bytes_to_int(b'\x00\x00\x01\x00')  # 256
ConvertUtil.bytes_to_int(b'\xff')                # 255

# int → bytes（大端序）
ConvertUtil.int_to_bytes(256, 2)    # b'\x01\x00'
ConvertUtil.int_to_bytes(1, 4)      # b'\x00\x00\x00\x01'
ConvertUtil.int_to_bytes(0, 1)      # b'\x00'
```

### 安全字符串转换

```python
# bytes/bytearray 自动解码
ConvertUtil.to_str(b'hello')       # 'hello'

# 其他类型使用 str()
ConvertUtil.to_str(123)            # '123'
ConvertUtil.to_str(None)           # ''

# 自定义编码
ConvertUtil.to_str(b'\xc4\xe3\xba\xc3', 'gb2312')  # '你好'
```

### 通用类型转换

```python
ConvertUtil.convert('123', int)     # 123
ConvertUtil.convert(3.14, str)      # '3.14'
ConvertUtil.convert('true', bool)   # True
ConvertUtil.convert(None, int)      # 0
ConvertUtil.convert(None, str)      # ''
```

### 中文数字转换

```python
# 数字转中文
ConvertUtil.number_to_chinese(123)   # "一百二十三"
ConvertUtil.number_to_chinese(10001) # "一万零一"

# 数字转中文大写
ConvertUtil.digit_to_chinese(123)    # "壹佰贰拾叁"
ConvertUtil.digit_to_chinese(10000)  # "壹万"

# 中文转数字
ConvertUtil.chinese_to_number("一百二十三")  # 123
ConvertUtil.chinese_to_number("一万零一")    # 10001
```

### 英文数字

```python
# 数字转英文
ConvertUtil.number_to_word(123)   # "one hundred and twenty-three"
ConvertUtil.number_to_word(0)     # "zero"
```

### 中文金额

```python
# 中文金额转数字
ConvertUtil.chinese_money_to_number("壹佰贰拾叁元整")  # 123.0
ConvertUtil.chinese_money_to_number("叁万零伍拾")      # 30050.0
```

### 数字简写

```python
# 数字简写（千/万/亿）
ConvertUtil.number_to_simple(1234)      # "1.2K"
ConvertUtil.number_to_simple(1234567)   # "1.2M"
ConvertUtil.number_to_simple(12345678)  # "1234.6万"
```

### 全角/半角转换

```python
# 全角转半角
ConvertUtil.to_dbc("Ｈｅｌｌｏ")  # "Hello"
ConvertUtil.to_dbc("１２３")       # "123"

# 半角转全角
ConvertUtil.to_sbc("Hello")       # "Ｈｅｌｌｏ"
ConvertUtil.to_sbc("123")         # "１２３"
```

### 表格格式化

```python
# 字典转表格字符串
data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
ConvertUtil.dict_to_tabular(data)
# name    age
# Alice   30
# Bob     25

# 列表转表格字符串
ConvertUtil.list_to_tabular([[1, 2], [3, 4]], headers=["A", "B"])
# A  B
# 1  2
# 3  4
```

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
