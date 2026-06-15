"""Tests for ImageUtil."""

import pytest

from hutool.core.util.image_util import ImageUtil


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
