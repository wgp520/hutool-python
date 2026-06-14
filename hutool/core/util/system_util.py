"""系统属性工具类"""

from __future__ import annotations

import os
import platform
import tempfile
from typing import Optional


class SystemUtil:
    """系统属性工具类，提供环境变量和系统信息获取功能。"""

    @staticmethod
    def get(name: str, default: Optional[str] = None) -> Optional[str]:
        """
        获取系统环境变量。

        :param name: 环境变量名
        :param default: 不存在时的默认值，默认 None
        :return: 环境变量值或默认值
        """
        return os.environ.get(name, default)

    @staticmethod
    def get_all() -> dict:
        """
        获取所有系统环境变量。

        :return: 环境变量字典
        """
        return dict(os.environ)

    @staticmethod
    def get_os_name() -> str:
        """
        获取操作系统名称。

        :return: 操作系统名称，如 ``"Windows"``、``"Linux"``、``"Darwin"``
        """
        return platform.system()

    @staticmethod
    def get_os_arch() -> str:
        """
        获取操作系统架构。

        :return: 架构字符串，如 ``"x86_64"``、``"AMD64"``
        """
        return platform.machine()

    @staticmethod
    def get_user_dir() -> str:
        """
        获取用户当前工作目录。

        :return: 当前工作目录的绝对路径
        """
        return os.getcwd()

    @staticmethod
    def get_user_home() -> str:
        """
        获取用户主目录。

        :return: 用户主目录路径
        """
        return os.path.expanduser("~")

    @staticmethod
    def get_tmp_dir() -> str:
        """
        获取系统临时目录。

        :return: 临时目录路径
        """
        return tempfile.gettempdir()

    @staticmethod
    def get_file_separator() -> str:
        """
        获取文件路径分隔符。

        :return: 路径分隔符，Windows 为 ``\\``，Unix 为 ``/``
        """
        return os.sep

    @staticmethod
    def get_line_separator() -> str:
        """
        获取行分隔符。

        :return: 行分隔符，Windows 为 ``\\r\\n``，Unix 为 ``\\n``
        """
        return os.linesep

    @staticmethod
    def is_windows() -> bool:
        """
        判断当前系统是否为 Windows。

        :return: 是否为 Windows 系统
        """
        return platform.system().lower() == "windows"
