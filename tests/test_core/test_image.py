"""Tests for ImageUtil."""

import pytest

from hutool import ImageUtil


class TestImageUtil:
    def test_detect_jpeg(self):
        header = b"\xff\xd8\xff\xe0" + b"\x00" * 28
        assert ImageUtil.detect_image_type(header) == "jpg"

    def test_detect_png(self):
        header = b"\x89PNG\r\n\x1a\n" + b"\x00" * 24
        assert ImageUtil.detect_image_type(header) == "png"

    def test_detect_gif87a(self):
        header = b"GIF87a" + b"\x00" * 26
        assert ImageUtil.detect_image_type(header) == "gif"

    def test_detect_gif89a(self):
        header = b"GIF89a" + b"\x00" * 26
        assert ImageUtil.detect_image_type(header) == "gif"

    def test_detect_bmp(self):
        header = b"BM" + b"\x00" * 30
        assert ImageUtil.detect_image_type(header) == "bmp"

    def test_detect_tiff_little_endian(self):
        header = b"II\x2a\x00" + b"\x00" * 28
        assert ImageUtil.detect_image_type(header) == "tiff"

    def test_detect_tiff_big_endian(self):
        header = b"MM\x00\x2a" + b"\x00" * 28
        assert ImageUtil.detect_image_type(header) == "tiff"

    def test_detect_webp(self):
        header = b"RIFF\x00\x00\x00\x00WEBP" + b"\x00" * 20
        assert ImageUtil.detect_image_type(header) == "webp"

    def test_detect_riff_not_webp(self):
        header = b"RIFF\x00\x00\x00\x00AVI " + b"\x00" * 20
        assert ImageUtil.detect_image_type(header) is None

    def test_detect_unknown(self):
        assert ImageUtil.detect_image_type(b"random data that is not an image") is None

    def test_detect_empty(self):
        assert ImageUtil.detect_image_type(b"") is None

    def test_detect_short(self):
        assert ImageUtil.detect_image_type(b"\x00") is None

    def test_detect_from_file(self, tmp_path):
        png_file = tmp_path / "test.png"
        png_file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        assert ImageUtil.detect_image_type(str(png_file)) == "png"

    def test_detect_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            ImageUtil.detect_image_type("/nonexistent/file.png")

    def test_detect_invalid_type(self):
        with pytest.raises(TypeError):
            ImageUtil.detect_image_type(12345)

    def _make_png_bytes(self, width=10, height=10, color=(255, 0, 0)):
        """创建测试用 PNG 图片字节"""
        try:
            import io

            from PIL import Image

            img = Image.new("RGB", (width, height), color)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue()
        except ImportError:
            pytest.skip("Pillow not installed")

    def test_resize_image(self):
        data = self._make_png_bytes(20, 20)
        result = ImageUtil.resize_image(data, 10, 10)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_replace_color(self):
        data = self._make_png_bytes(5, 5, (255, 0, 0))
        result = ImageUtil.replace_color(data, (255, 0, 0), (0, 255, 0))
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_add_watermark(self):
        data = self._make_png_bytes(100, 100)
        result = ImageUtil.add_watermark(data, "TEST")
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_face_detect_no_face(self):
        data = self._make_png_bytes(100, 100, (0, 0, 0))
        try:
            result = ImageUtil.face_detect(data)
            assert isinstance(result, list)
        except ImportError as e:
            if "opencv-python" in str(e):
                pytest.skip("opencv-python not installed")
            raise
