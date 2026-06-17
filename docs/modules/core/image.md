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

### 图片操作

以下方法需要安装 Pillow（`pip install Pillow`），`face_detect` 还需要 `opencv-python`。

#### 缩放图片

```python
from hutool import ImageUtil

# 缩放为 200x200，返回 bytes
data = ImageUtil.resize_image("/path/to/photo.jpg", 200, 200)

# 缩放并保存到文件
ImageUtil.resize_image(b"\x89PNG...", 100, 100, output_path="/tmp/small.png")
```

#### 颜色替换

```python
# 将红色替换为绿色（容差 30）
data = ImageUtil.replace_color(
    b"\x89PNG...",
    target_color=(255, 0, 0),
    replacement_color=(0, 255, 0),
    tolerance=30
)
```

#### 添加水印

```python
# 在右下角添加白色半透明水印
data = ImageUtil.add_watermark("/path/to/photo.jpg", "CONFIDENTIAL")

# 自定义位置和颜色
data = ImageUtil.add_watermark(
    photo_bytes, "DRAFT",
    position=(10, 10),
    color=(255, 0, 0),
    font_size=48
)
```

#### 人脸检测

```python
# 返回人脸位置列表 [(x, y, w, h), ...]
faces = ImageUtil.face_detect("/path/to/photo.jpg")
for x, y, w, h in faces:
    print(f"Face at ({x}, {y}), size {w}x{h}")
```
