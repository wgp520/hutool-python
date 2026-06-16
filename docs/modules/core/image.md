# 图片工具 - ImageUtil

## 由来

在文件上传、图片处理等场景中，需要根据文件内容（而非扩展名）判断图片格式。`ImageUtil` 通过读取文件头魔数（magic bytes）进行格式检测，纯标准库实现，无第三方依赖。

## 方法

### 检测图片格式

支持 JPEG、PNG、GIF、BMP、TIFF、WebP 六种格式：

```python
from hutool import ImageUtil

# 从文件路径检测
fmt = ImageUtil.detect_image_type("/path/to/image.png")  # 'png'

# 从字节数据检测
with open("photo.jpg", "rb") as f:
    data = f.read()
fmt = ImageUtil.detect_image_type(data)  # 'jpg'

# 无法识别时返回 None
ImageUtil.detect_image_type(b'random data')  # None
```

### 支持的格式

| 格式 | 返回值 | 魔数 |
| --- | --- | --- |
| JPEG | `"jpg"` | `FF D8 FF` |
| PNG | `"png"` | `89 50 4E 47 0D 0A 1A 0A` |
| GIF | `"gif"` | `47 49 46 38 37/39 61` |
| BMP | `"bmp"` | `42 4D` |
| TIFF | `"tiff"` | `49 49 2A 00` 或 `4D 4D 00 2A` |
| WebP | `"webp"` | `52 49 46 46 ... 57 45 42 50` |

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
