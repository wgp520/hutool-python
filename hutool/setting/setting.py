"""配置文件工具类"""

import os
import re
from typing import Any


class SettingUtil:
    """配置文件工具类

    支持 .properties/.setting 格式，支持 key=value 和 key: value 两种写法。
    """

    @staticmethod
    def load(path: str, charset: str = "utf-8") -> dict:
        """加载配置文件

        支持的格式:
            - key=value
            - key: value
            - # 注释行
            - ! 注释行

        :param path: 配置文件路径
        :param charset: 文件编码，默认为 'utf-8'
        :return: 解析后的配置字典
        """
        path = os.path.abspath(path)
        props: dict = {}
        with open(path, encoding=charset) as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释行
                if not line or line.startswith("#") or line.startswith("!"):
                    continue
                # 匹配 key=value 或 key: value
                match = re.match(r"^([^=:]+)[=:](.*)$", line)
                if match:
                    key = match.group(1).strip()
                    value = match.group(2).strip()
                    # 处理布尔值和数字
                    props[key] = SettingUtil._parse_value(value)
        return props

    @staticmethod
    def get(props: dict, key: str, default: Any = None) -> Any:
        """获取配置值

        :param props: 配置字典
        :param key: 配置键
        :param default: 默认值
        :return: 配置值，不存在时返回默认值
        """
        return props.get(key, default)

    @staticmethod
    def _parse_value(value: str) -> Any:
        """解析配置值的类型

        :param value: 字符串类型的值
        :return: 解析后的值（bool、int、float或原始字符串）
        """
        if not value:
            return ""
        # 布尔值
        if value.lower() in ("true", "yes", "on"):
            return True
        if value.lower() in ("false", "no", "off"):
            return False
        # 整数
        try:
            return int(value)
        except ValueError:
            pass
        # 浮点数
        try:
            return float(value)
        except ValueError:
            pass
        return value
