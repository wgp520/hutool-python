"""数据大小工具模块"""

import re
from typing import Dict


class DataSizeUtil:
    """数据大小工具类"""

    _UNITS: Dict[str, int] = {
        "B": 1,
        "KB": 1024,
        "MB": 1024**2,
        "GB": 1024**3,
        "TB": 1024**4,
        "PB": 1024**5,
    }

    # 用于匹配 "数字 + 可选空格 + 单位" 的正则
    _SIZE_PATTERN = re.compile(
        r"^\s*(\d+(?:\.\d+)?)\s*(B|KB|MB|GB|TB|PB)\s*$",
        re.IGNORECASE,
    )

    @staticmethod
    def parse(size_str: str) -> int:
        """解析数据大小字符串为字节数

        支持的单位（不区分大小写）: B, KB, MB, GB, TB, PB

        示例::

            DataSizeUtil.parse("10KB")   -> 10240
            DataSizeUtil.parse("1.5GB")  -> 1610612736
            DataSizeUtil.parse("512 B")  -> 512

        :param size_str: 数据大小字符串，如 "10KB"、"1.5 GB"
        :return: 对应的字节数（int）
        :raises ValueError: 无法解析时抛出
        """
        match = DataSizeUtil._SIZE_PATTERN.match(size_str)
        if not match:
            raise ValueError(f"无法解析数据大小字符串: '{size_str}'")
        number = float(match.group(1))
        unit = match.group(2).upper()
        multiplier = DataSizeUtil._UNITS[unit]
        return int(number * multiplier)

    @staticmethod
    def format_size(size: int) -> str:
        """将字节数格式化为可读字符串

        自动选择最合适的单位，保留两位小数并去除末尾的零。

        示例::

            DataSizeUtil.format_size(10240)       -> "10KB"
            DataSizeUtil.format_size(1073741824)   -> "1GB"
            DataSizeUtil.format_size(512)          -> "512B"

        :param size: 字节数
        :return: 格式化后的字符串
        """
        if size < 0:
            return "-" + DataSizeUtil.format_size(-size)

        if size < DataSizeUtil._UNITS["KB"]:
            return f"{size}B"

        # 从大到小尝试匹配合适的单位
        for unit in ("PB", "TB", "GB", "MB", "KB"):
            unit_size = DataSizeUtil._UNITS[unit]
            if size >= unit_size:
                value = size / unit_size
                # 保留两位小数，去除末尾多余的零和小数点
                formatted = f"{value:.2f}".rstrip("0").rstrip(".")
                return f"{formatted}{unit}"

        return f"{size}B"
