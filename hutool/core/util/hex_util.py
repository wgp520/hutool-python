"""十六进制工具类"""


class HexUtil:
    """十六进制工具类，对应 Java cn.hutool.core.util.HexUtil"""

    # 十六进制字符表（大写和小写）
    _DIGITS_UPPER = "0123456789ABCDEF"
    _DIGITS_LOWER = "0123456789abcdef"

    @staticmethod
    def encode_hex_str(data: bytes, lower_case: bool = False) -> str:
        """字节数组转十六进制字符串

        :param data: 字节数组
        :param lower_case: 是否使用小写，默认大写
        :return: 十六进制字符串
        """
        if data is None:
            return ""
        digits = HexUtil._DIGITS_LOWER if lower_case else HexUtil._DIGITS_UPPER
        result = []
        for b in data:
            result.append(digits[(b >> 4) & 0x0F])
            result.append(digits[b & 0x0F])
        return "".join(result)

    @staticmethod
    def decode_hex(hex_str: str) -> bytes:
        """十六进制字符串转字节数组

        :param hex_str: 十六进制字符串（允许含空格等分隔符，自动去除）
        :return: 字节数组
        :raises ValueError: 当输入包含非法十六进制字符时抛出
        """
        if hex_str is None or len(hex_str) == 0:
            return b""
        # 去除常见分隔符（空格、冒号、短横线）
        hex_str = hex_str.replace(" ", "").replace(":", "").replace("-", "")
        length = len(hex_str)
        if length % 2 != 0:
            raise ValueError(f"十六进制字符串长度必须为偶数，当前长度为 {length}")
        result = bytearray(length // 2)
        for i in range(0, length, 2):
            high = int(hex_str[i], 16)
            low = int(hex_str[i + 1], 16)
            result[i // 2] = (high << 4) | low
        return bytes(result)

    @staticmethod
    def to_hex(number: int) -> str:
        """数字转十六进制字符串（不带0x前缀）

        :param number: 整数
        :return: 十六进制字符串（大写）
        """
        if number == 0:
            return "0"
        # 处理负数：取其二进制补码表示
        if number < 0:
            # 转为无符号表示，取足够位数
            number = number & 0xFFFFFFFFFFFFFFFF
        result = []
        while number > 0:
            digit = number & 0x0F
            result.append(HexUtil._DIGITS_UPPER[digit])
            number >>= 4
        result.reverse()
        return "".join(result)

    @staticmethod
    def hex_to_int(hex_str: str) -> int:
        """十六进制字符串转int

        :param hex_str: 十六进制字符串（可选0x/0X前缀）
        :return: 对应的整数值
        """
        if hex_str is None or len(hex_str) == 0:
            raise ValueError("十六进制字符串不能为空")
        hex_str = hex_str.strip()
        if hex_str.startswith("0x") or hex_str.startswith("0X"):
            hex_str = hex_str[2:]
        return int(hex_str, 16)

    @staticmethod
    def encode_color_str(color: tuple) -> str:
        """RGB元组转十六进制颜色字符串

        :param color: RGB元组，如 (255, 128, 0)
        :return: 十六进制颜色字符串，如 '#FF8000'
        """
        if color is None or len(color) < 3:
            raise ValueError("颜色元组必须包含至少3个元素（R, G, B）")
        r, g, b = color[0], color[1], color[2]
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError("RGB值必须在0-255范围内")
        return f"#{r:02X}{g:02X}{b:02X}"

    @staticmethod
    def decode_color(color_str: str) -> tuple:
        """十六进制颜色字符串转RGB元组

        :param color_str: 十六进制颜色字符串，如 '#FF8000' 或 'FF8000'
        :return: RGB元组，如 (255, 128, 0)
        """
        if color_str is None or len(color_str) == 0:
            raise ValueError("颜色字符串不能为空")
        color_str = color_str.strip().lstrip("#")
        if len(color_str) == 6:
            r = int(color_str[0:2], 16)
            g = int(color_str[2:4], 16)
            b = int(color_str[4:6], 16)
            return (r, g, b)
        elif len(color_str) == 3:
            # 短格式如 #F80 -> #FF8800
            r = int(color_str[0] * 2, 16)
            g = int(color_str[1] * 2, 16)
            b = int(color_str[2] * 2, 16)
            return (r, g, b)
        else:
            raise ValueError(f"非法的颜色字符串长度：{len(color_str)}，期望6位或3位")

    @staticmethod
    def format_hex(hex_str: str, delimiter: str = " ", group_size: int = 2) -> str:
        """格式化十六进制字符串，添加分隔符

        :param hex_str: 十六进制字符串
        :param delimiter: 分隔符，默认为空格
        :param group_size: 每组字符数，默认为2
        :return: 格式化后的十六进制字符串，如 '4A:3F:2B'
        """
        if hex_str is None or len(hex_str) == 0:
            return ""
        hex_str = hex_str.replace(" ", "").replace(":", "").replace("-", "")
        if group_size <= 0:
            raise ValueError("group_size 必须大于 0")
        groups = []
        for i in range(0, len(hex_str), group_size):
            groups.append(hex_str[i : i + group_size].upper())
        return delimiter.join(groups)
