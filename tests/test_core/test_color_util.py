"""Tests for ColorUtil."""

import pytest

from hutool.core.util.color_util import ColorUtil


class TestColorUtil:
    def test_hex_to_rgb_standard(self):
        assert ColorUtil.hex_to_rgb("#FF0000") == (255, 0, 0)

    def test_hex_to_rgb_lowercase(self):
        assert ColorUtil.hex_to_rgb("#00ff00") == (0, 255, 0)

    def test_hex_to_rgb_no_hash(self):
        assert ColorUtil.hex_to_rgb("0000FF") == (0, 0, 255)

    def test_hex_to_rgb_shorthand(self):
        assert ColorUtil.hex_to_rgb("#369") == (51, 102, 153)

    def test_hex_to_rgb_shorthand_no_hash(self):
        assert ColorUtil.hex_to_rgb("F00") == (255, 0, 0)

    def test_hex_to_rgb_invalid_raises(self):
        with pytest.raises(ValueError):
            ColorUtil.hex_to_rgb("#GG0000")

    def test_hex_to_rgb_invalid_length_raises(self):
        with pytest.raises(ValueError):
            ColorUtil.hex_to_rgb("#12345")

    def test_rgb_to_hex_red(self):
        assert ColorUtil.rgb_to_hex(255, 0, 0) == "#ff0000"

    def test_rgb_to_hex_green(self):
        assert ColorUtil.rgb_to_hex(0, 255, 0) == "#00ff00"

    def test_rgb_to_hex_blue(self):
        assert ColorUtil.rgb_to_hex(0, 0, 255) == "#0000ff"

    def test_rgb_to_hex_mixed(self):
        assert ColorUtil.rgb_to_hex(51, 102, 153) == "#336699"

    def test_rgb_to_hex_black(self):
        assert ColorUtil.rgb_to_hex(0, 0, 0) == "#000000"

    def test_rgb_to_hex_white(self):
        assert ColorUtil.rgb_to_hex(255, 255, 255) == "#ffffff"

    def test_rgb_to_hex_out_of_range_raises(self):
        with pytest.raises(ValueError):
            ColorUtil.rgb_to_hex(256, 0, 0)

    def test_rgb_to_hex_negative_raises(self):
        with pytest.raises(ValueError):
            ColorUtil.rgb_to_hex(-1, 0, 0)

    def test_roundtrip(self):
        for r, g, b in [(255, 0, 0), (0, 128, 255), (100, 200, 50)]:
            hex_str = ColorUtil.rgb_to_hex(r, g, b)
            assert ColorUtil.hex_to_rgb(hex_str) == (r, g, b)
