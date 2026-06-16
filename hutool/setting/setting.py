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

    @staticmethod
    def store(props: dict, path: str, charset: str = "utf-8", comment: str = "") -> None:
        """将配置字典持久化到文件

        :param props: 配置字典
        :param path: 文件路径
        :param charset: 文件编码
        :param comment: 文件头部注释
        """
        path = os.path.abspath(path)
        with open(path, "w", encoding=charset) as f:
            if comment:
                f.write(f"# {comment}\n")
            for key, value in props.items():
                f.write(f"{key}={value}\n")

    @staticmethod
    def to_dict(props: dict) -> dict:
        """将配置字典转为普通字典（别名，直接返回副本）

        :param props: 配置字典
        :return: 字典副本
        """
        return dict(props)

    @staticmethod
    def create() -> dict:
        """创建空配置字典

        :return: 空字典
        """
        return {}

    @staticmethod
    def set_value(props: dict, key: str, value) -> None:
        """设置配置值

        :param props: 配置字典
        :param key: 键名
        :param value: 值
        """
        props[key] = value

    @staticmethod
    def get_group(props: dict, prefix: str) -> dict:
        """获取指定前缀的配置组

        :param props: 配置字典
        :param prefix: 组前缀
        :return: 过滤后的字典
        """
        result = {}
        dot_prefix = prefix if prefix.endswith(".") else prefix + "."
        for key, value in props.items():
            if key.startswith(dot_prefix):
                # 去掉前缀，保留剩余部分作为新键名
                new_key = key[len(dot_prefix) :]
                result[new_key] = value
            elif key == prefix:
                result[key] = value
        return result
