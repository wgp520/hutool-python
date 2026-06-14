# 十六进制工具 - HexUtil

## 由来

十六进制编码在加密、网络通信等场景中广泛使用，`HexUtil` 提供便捷的十六进制编解码方法。

## 方法

```python
from hutool import HexUtil

# 编码
HexUtil.encode_hex_str(b"hello")          # "68656c6c6f"
HexUtil.encode_hex_str(b"hello", True)    # "68656C6C6F"（大写）

# 解码
HexUtil.decode_hex("68656c6c6f")          # b"hello"

# 数字转换
HexUtil.to_hex(255)                       # "ff"
HexUtil.hex_to_int("ff")                  # 255

# 颜色转换
HexUtil.encode_color_str((255, 128, 0))   # "#ff8000"
HexUtil.decode_color("#ff8000")           # (255, 128, 0)
```
