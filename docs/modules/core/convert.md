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

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
