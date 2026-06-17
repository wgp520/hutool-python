"""
图片工具类

提供图片格式检测功能（通过文件头魔数）以及图片操作（缩放、颜色替换、水印、人脸检测）。
格式检测为纯标准库实现；图片操作依赖 Pillow，以 try...except ImportError 保护。
"""

from typing import Optional, Union


class ImageUtil:
    """图片工具类，提供图片格式检测和基础操作。"""

    # 格式魔数映射表
    _MAGIC_TABLE = (
        (b"\xff\xd8\xff", "jpg"),
        (b"\x89PNG\r\n\x1a\n", "png"),
        (b"GIF87a", "gif"),
        (b"GIF89a", "gif"),
        (b"BM", "bmp"),
        (b"II\x2a\x00", "tiff"),
        (b"MM\x00\x2a", "tiff"),
        (b"RIFF", "webp"),  # 需进一步校验 WEBP 标记
    )

    @staticmethod
    def detect_image_type(file_or_bytes: Union[str, bytes, bytearray]) -> Optional[str]:
        """
        通过文件头魔数检测图片格式。

        支持 JPEG、PNG、GIF、BMP、TIFF、WebP。

        :param file_or_bytes: 文件路径（str）或原始字节数据
        :return: 图片格式字符串（``"jpg"``/``"png"``/``"gif"``/``"bmp"``/``"tiff"``/``"webp"``），无法识别时返回 ``None``

        ::

            >>> ImageUtil.detect_image_type(b'\\x89PNG\\r\\n\\x1a\\n...')
            'png'
            >>> ImageUtil.detect_image_type(b'random data') is None
            True
        """
        if isinstance(file_or_bytes, (bytes, bytearray)):
            header = bytes(file_or_bytes[:32])
        elif isinstance(file_or_bytes, str):
            with open(file_or_bytes, "rb") as f:
                header = f.read(32)
        else:
            raise TypeError(f"期望 str/bytes/bytearray，实际为 {type(file_or_bytes)}")

        if len(header) < 2:
            return None

        for magic, fmt in ImageUtil._MAGIC_TABLE:
            if header[: len(magic)] == magic:
                # WebP 需要额外校验偏移 8 处为 "WEBP"
                if fmt == "webp":
                    if len(header) >= 12 and header[8:12] == b"WEBP":
                        return "webp"
                    continue
                return fmt
        return None

    # ── 图片操作 ───────────────────────────────

    @staticmethod
    def resize_image(
        file_or_bytes,  # type: Union[str, bytes]
        width,  # type: int
        height,  # type: int
        output_path=None,  # type: Optional[str]
    ):
        # type: (...) -> Union[bytes, str]
        """缩放图片到指定尺寸。

        需要安装 Pillow（``pip install Pillow``）。

        :param file_or_bytes: 图片文件路径或字节数据
        :param width: 目标宽度
        :param height: 目标高度
        :param output_path: 输出文件路径，为 ``None`` 时返回 bytes
        :return: 缩放后的图片字节数据或输出文件路径
        :raises ImportError: 未安装 Pillow 时
        """
        try:
            import io

            from PIL import Image

            if isinstance(file_or_bytes, (bytes, bytearray)):
                img = Image.open(io.BytesIO(file_or_bytes))
            else:
                img = Image.open(file_or_bytes)

            img = img.resize((width, height), Image.LANCZOS)

            if output_path:
                img.save(output_path)
                return output_path
            else:
                buf = io.BytesIO()
                fmt = img.format or "PNG"
                img.save(buf, format=fmt)
                return buf.getvalue()
        except ImportError:
            raise ImportError("resize_image 需要安装 Pillow: pip install Pillow")

    @staticmethod
    def replace_color(
        file_or_bytes,  # type: Union[str, bytes]
        target_color,  # type: tuple
        replacement_color,  # type: tuple
        tolerance=30,  # type: int
        output_path=None,  # type: Optional[str]
    ):
        # type: (...) -> Union[bytes, str]
        """替换图片中的指定颜色。

        需要安装 Pillow（``pip install Pillow``）。

        :param file_or_bytes: 图片文件路径或字节数据
        :param target_color: 目标颜色，RGB 元组如 ``(255, 0, 0)``
        :param replacement_color: 替换颜色，RGB 元组如 ``(0, 255, 0)``
        :param tolerance: 颜色容差，默认 30
        :param output_path: 输出文件路径，为 ``None`` 时返回 bytes
        :return: 替换后的图片字节数据或输出文件路径
        :raises ImportError: 未安装 Pillow 时
        """
        try:
            import io

            from PIL import Image

            if isinstance(file_or_bytes, (bytes, bytearray)):
                img = Image.open(io.BytesIO(file_or_bytes)).convert("RGB")
            else:
                img = Image.open(file_or_bytes).convert("RGB")

            pixels = img.load()
            w, h = img.size
            for y in range(h):
                for x in range(w):
                    r, g, b = pixels[x, y]
                    tr, tg, tb = target_color
                    if abs(r - tr) <= tolerance and abs(g - tg) <= tolerance and abs(b - tb) <= tolerance:
                        pixels[x, y] = replacement_color

            if output_path:
                img.save(output_path)
                return output_path
            else:
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                return buf.getvalue()
        except ImportError:
            raise ImportError("replace_color 需要安装 Pillow: pip install Pillow")

    @staticmethod
    def add_watermark(
        file_or_bytes,  # type: Union[str, bytes]
        text,  # type: str
        position=None,  # type: Optional[tuple]
        color=(255, 255, 255),  # type: tuple
        font_size=36,  # type: int
        output_path=None,  # type: Optional[str]
    ):
        # type: (...) -> Union[bytes, str]
        """为图片添加文字水印。

        需要安装 Pillow（``pip install Pillow``）。

        :param file_or_bytes: 图片文件路径或字节数据
        :param text: 水印文字
        :param position: 水印位置 ``(x, y)``，为 ``None`` 时默认右下角
        :param color: 文字颜色 RGB 元组，默认白色 ``(255, 255, 255)``
        :param font_size: 字体大小，默认 36
        :param output_path: 输出文件路径，为 ``None`` 时返回 bytes
        :return: 添加水印后的图片字节数据或输出文件路径
        :raises ImportError: 未安装 Pillow 时
        """
        try:
            import io

            from PIL import Image, ImageDraw, ImageFont

            if isinstance(file_or_bytes, (bytes, bytearray)):
                img = Image.open(io.BytesIO(file_or_bytes)).convert("RGBA")
            else:
                img = Image.open(file_or_bytes).convert("RGBA")

            overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)

            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except OSError:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]

            if position is None:
                position = (img.width - tw - 10, img.height - th - 10)

            draw.text(position, text, fill=(*color, 180), font=font)
            result = Image.alpha_composite(img, overlay).convert("RGB")

            if output_path:
                result.save(output_path)
                return output_path
            else:
                buf = io.BytesIO()
                result.save(buf, format="PNG")
                return buf.getvalue()
        except ImportError:
            raise ImportError("add_watermark 需要安装 Pillow: pip install Pillow")

    @staticmethod
    def face_detect(file_or_bytes):
        # type: (Union[str, bytes]) -> list
        """检测图片中的人脸位置。

        需要安装 Pillow（``pip install Pillow``）。
        使用 Haar 级联分类器（OpenCV 内置的 ``haarcascade_frontalface_default.xml``）。

        :param file_or_bytes: 图片文件路径或字节数据
        :return: 人脸位置列表，每个元素为 ``(x, y, w, h)`` 元组；无法检测时返回空列表
        :raises ImportError: 未安装 Pillow 或 opencv-python 时
        """
        try:
            import io

            from PIL import Image
        except ImportError:
            raise ImportError("face_detect 需要安装 Pillow: pip install Pillow")
        try:
            import cv2
            import numpy as np
        except ImportError:
            raise ImportError("face_detect 需要安装 opencv-python: pip install opencv-python")

        if isinstance(file_or_bytes, (bytes, bytearray)):
            img = Image.open(io.BytesIO(file_or_bytes))
        else:
            img = Image.open(file_or_bytes)

        img_cv = cv2.cvtColor(np.array(img.convert("RGB")), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(cascade_path)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        return [(int(x), int(y), int(w), int(h)) for x, y, w, h in faces]
