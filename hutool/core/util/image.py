"""
图片工具类

提供图片格式检测功能（通过文件头魔数），纯标准库实现，无第三方依赖。
"""

from typing import Optional, Union


class ImageUtil:
    """图片工具类，提供图片格式检测。"""

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
