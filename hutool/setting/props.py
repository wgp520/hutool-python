"""Properties文件工具类"""

import os
import re
from typing import Any


class PropsUtil:
    """Properties文件工具类

    加载和解析标准 .properties 格式的配置文件。
    """

    @staticmethod
    def load(path: str, charset: str = "utf-8") -> dict:
        """加载.properties文件

        支持的格式:
            - key=value
            - key: value
            - key value
            - # 注释行
            - ! 注释行
            - 续行符（行尾 \\）

        :param path: .properties文件路径
        :param charset: 文件编码，默认为 'utf-8'
        :return: 解析后的属性字典
        """
        path = os.path.abspath(path)
        props: dict = {}
        with open(path, encoding=charset) as f:
            lines = f.readlines()

        continued_line = ""
        for line in lines:
            line = line.strip()
            # 跳过空行和注释
            if not line or line.startswith("#") or line.startswith("!"):
                continue

            # 处理续行
            if continued_line:
                line = continued_line + line
                continued_line = ""

            if line.endswith("\\"):
                continued_line = line[:-1]
                continue

            # 解析 key=value 或 key: value 或 key value
            match = re.match(r"^([^=: \t]+)[ \t]*[=: \t](.*)$", line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                props[key] = PropsUtil._unescape(value)

        return props

    @staticmethod
    def get(props: dict, key: str, default: Any = None) -> Any:
        """获取属性值

        :param props: 属性字典
        :param key: 属性键
        :param default: 默认值
        :return: 属性值，不存在时返回默认值
        """
        return props.get(key, default)

    @staticmethod
    def _unescape(value: str) -> str:
        """反转义properties值中的特殊字符

        :param value: 原始值
        :return: 反转义后的值
        """
        result = value.replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\")
        return result

    @staticmethod
    def create() -> dict:
        """创建空属性字典

        :return: 空字典
        """
        return {}

    @staticmethod
    def store(props: dict, path: str, charset: str = "utf-8", comment: str = "") -> None:
        """将属性字典持久化到.properties文件

        :param props: 属性字典
        :param path: 文件路径
        :param charset: 文件编码
        :param comment: 文件头部注释
        """
        path = os.path.abspath(path)
        with open(path, "w", encoding=charset) as f:
            if comment:
                f.write(f"# {comment}\n")
            for key, value in props.items():
                # 转义特殊字符
                escaped_value = str(value).replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")
                f.write(f"{key}={escaped_value}\n")

    @staticmethod
    def to_dict(props: dict) -> dict:
        """转为普通字典

        :param props: 属性字典
        :return: 字典副本
        """
        return dict(props)
