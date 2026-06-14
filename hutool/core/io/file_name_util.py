"""文件名工具模块"""

import os
import re
from typing import List


class FileNameUtil:
    """文件名工具类"""

    # 文件名中不允许出现的字符（Windows + 通用）
    _INVALID_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')

    @staticmethod
    def get_name(path: str) -> str:
        """获取文件名（含扩展名）

        :param path: 文件路径
        :return: 文件名，如 "document.txt"
        """
        return os.path.basename(path)

    @staticmethod
    def get_prefix(path: str) -> str:
        """获取文件名前缀（不含扩展名）

        :param path: 文件路径
        :return: 文件名前缀，如 "document"
        """
        name = os.path.basename(path)
        dot_index = name.rfind(".")
        if dot_index <= 0:
            return name
        return name[:dot_index]

    @staticmethod
    def get_suffix(path: str) -> str:
        """获取扩展名（不含点）

        :param path: 文件路径
        :return: 扩展名，如 "txt"；无扩展名时返回空字符串
        """
        name = os.path.basename(path)
        dot_index = name.rfind(".")
        if dot_index < 0 or dot_index == len(name) - 1:
            return ""
        return name[dot_index + 1 :]

    @staticmethod
    def main_name(path: str) -> str:
        """获取主文件名（等同于 get_prefix）

        :param path: 文件路径
        :return: 主文件名
        """
        return FileNameUtil.get_prefix(path)

    @staticmethod
    def ext_name(path: str) -> str:
        """获取扩展名（同 get_suffix）

        :param path: 文件路径
        :return: 扩展名
        """
        return FileNameUtil.get_suffix(path)

    @staticmethod
    def normalize(path: str) -> str:
        """标准化文件名路径

        将路径中的反斜杠统一替换为正斜杠，并去除多余分隔符。

        :param path: 文件路径
        :return: 标准化后的路径
        """
        normalized = path.replace("\\", "/")
        # 去除连续的斜杠（保留开头的 ./ 或协议部分）
        parts = normalized.split("/")
        result_parts: List[str] = []
        for part in parts:
            if part == "" and result_parts:
                continue
            result_parts.append(part)
        return "/".join(result_parts)

    @staticmethod
    def clean_invalid(name: str) -> str:
        """清理文件名中的非法字符

        移除 Windows 及通用文件系统中不允许出现的字符。

        :param name: 原始文件名
        :return: 清理后的合法文件名
        """
        cleaned = FileNameUtil._INVALID_CHARS.sub("", name)
        # 去除首尾空格和点（Windows 不允许）
        cleaned = cleaned.strip(" .")
        return cleaned if cleaned else "unnamed"

    @staticmethod
    def is_type(path: str, ext: str) -> bool:
        """检查文件扩展名是否匹配

        比较时忽略大小写。

        :param path: 文件路径
        :param ext: 期望的扩展名（不含点，如 "txt"）
        :return: 匹配返回 True，否则 False
        """
        actual = FileNameUtil.get_suffix(path)
        return actual.lower() == ext.lower().lstrip(".")
