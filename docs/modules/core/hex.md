# 十六进制工具 - HexUtil

## 由来

十六进制编码在加密、网络通信等场景中广泛使用，`HexUtil` 提供便捷的十六进制编解码方法。

## 方法

```python
from hutool import HexUtil

# 编码（默认小写，与 Java Hutool 一致）
HexUtil.encode_hex_str(b"hello")          # "68656c6c6f"
HexUtil.encode_hex_str(b"hello", False)   # "68656C6C6F"（大写）

# 字符串编码
HexUtil.encode_hex("Hello")               # "48656c6c6f"
HexUtil.decode_hex_str("48656c6c6f")      # "Hello"

# 解码
HexUtil.decode_hex("68656c6c6f")          # b"hello"

# 数字转换
HexUtil.to_hex(255)                       # "ff"
HexUtil.hex_to_int("ff")                  # 255

# 颜色转换
HexUtil.encode_color_str((255, 128, 0))   # "#FF8000"
HexUtil.decode_color("#ff8000")           # (255, 128, 0)

# 判断是否十六进制数
HexUtil.is_hex_number("0xff")    # True
HexUtil.is_hex_number("xyz")     # False

# 字符转 Unicode 十六进制
HexUtil.to_unicode_hex("中")    # "\\u4e2d"
```

### IEEE 754 位重解释

```python
# float ↔ 十六进制
HexUtil.to_hex_float(1.0)                # "3f800000"
HexUtil.hex_to_float("3f800000")         # 1.0

# double ↔ 十六进制
HexUtil.to_hex_double(1.0)               # "3ff0000000000000"
HexUtil.hex_to_double("3ff0000000000000") # 1.0
```

### 进制转换

```python
# long ↔ 十六进制
HexUtil.to_hex_long(255)       # "ff"
HexUtil.hex_to_long("ff")      # 255

# 十六进制转大整数
HexUtil.to_big_integer("100000000")  # 4294967296
```

### 颜色编码

```python
# encodeColor — RGB 颜色编码为 #RRGGBB
HexUtil.encode_color(255, 128, 0)   # "#FF8000"
HexUtil.encode_color(0, 0, 0)       # "#000000"
```

### 格式化十六进制

```python
# formatHex — 格式化十六进制字符串
HexUtil.format_hex("AABBCCDD", "-", 2)   # "AA-BB-CC-DD"
HexUtil.format_hex("AABBCCDD", ":", 2)   # "AA:BB:CC:DD"
HexUtil.format_hex("AABBCCDD", " ", 4)   # "AABB CCDD"
```
