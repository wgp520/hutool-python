# 颜色工具 - ColorUtil

## 由来

前端开发和 UI 设计中经常需要在十六进制颜色和 RGB 之间转换。`ColorUtil` 提供简洁的颜色格式转换方法。

## 方法

### 十六进制转 RGB

```python
from hutool import ColorUtil

ColorUtil.hex_to_rgb('#336699')    # (51, 102, 153)
ColorUtil.hex_to_rgb('336699')     # (51, 102, 153)（不带 # 也可以）
ColorUtil.hex_to_rgb('#f00')       # (255, 0, 0)（支持简写格式）
ColorUtil.hex_to_rgb('#FF6600')    # (255, 102, 0)（不区分大小写）
```

### RGB 转十六进制

```python
ColorUtil.rgb_to_hex(51, 102, 153)   # '#336699'
ColorUtil.rgb_to_hex(255, 0, 0)      # '#ff0000'
ColorUtil.rgb_to_hex(0, 0, 0)        # '#000000'
```

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
