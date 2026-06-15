"""
颜色工具类

提供十六进制颜色与 RGB 元组之间的转换。
"""

from typing import Tuple


class ColorUtil:
    """颜色工具类，提供颜色格式转换。"""

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, ...]:
        """
        将十六进制颜色字符串转换为 RGB 元组。

        支持 ``#RGB``、``#RRGGBB``、``RGB``、``RRGGBB`` 格式。

        :param hex_color: 十六进制颜色字符串
        :return: RGB 元组 ``(r, g, b)``
        :raises ValueError: 格式不合法时

        ::

            >>> ColorUtil.hex_to_rgb('#FF0000')
            (255, 0, 0)
            >>> ColorUtil.hex_to_rgb('#00ff00')
            (0, 255, 0)
            >>> ColorUtil.hex_to_rgb('369')
            (51, 102, 153)
        """
        h = hex_color.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) != 6:
            raise ValueError(f"无效的十六进制颜色: {hex_color!r}")
        try:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        except ValueError:
            raise ValueError(f"无效的十六进制颜色: {hex_color!r}")

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """
        将 RGB 值转换为十六进制颜色字符串。

        :param r: 红色分量（0-255）
        :param g: 绿色分量（0-255）
        :param b: 蓝色分量（0-255）
        :return: 十六进制颜色字符串（``#RRGGBB`` 格式，小写）
        :raises ValueError: RGB 值超出范围时

        ::

            >>> ColorUtil.rgb_to_hex(255, 0, 0)
            '#ff0000'
            >>> ColorUtil.rgb_to_hex(0, 255, 0)
            '#00ff00'
            >>> ColorUtil.rgb_to_hex(51, 102, 153)
            '#336699'
        """
        for name, val in [("r", r), ("g", g), ("b", b)]:
            if not (0 <= val <= 255):
                raise ValueError(f"{name} 值必须在 0-255 之间，实际为 {val}")
        return f"#{r:02x}{g:02x}{b:02x}"
