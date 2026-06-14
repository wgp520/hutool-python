"""系统属性工具类"""

from __future__ import annotations

import os
import platform
import tempfile
from typing import Optional


class SystemUtil:
    """系统属性工具类，对应 Java SystemPropsUtil"""

    @staticmethod
    def get(name: str, default: Optional[str] = None) -> Optional[str]:
        """获取系统环境变量"""
        return os.environ.get(name, default)

    @staticmethod
    def get_all() -> dict:
        """获取所有环境变量"""
        return dict(os.environ)

    @staticmethod
    def get_os_name() -> str:
        """获取操作系统名称"""
        return platform.system()

    @staticmethod
    def get_os_arch() -> str:
        """获取操作系统架构"""
        return platform.machine()

    @staticmethod
    def get_user_dir() -> str:
        """获取用户当前工作目录"""
        return os.getcwd()

    @staticmethod
    def get_user_home() -> str:
        """获取用户主目录"""
        return os.path.expanduser("~")

    @staticmethod
    def get_tmp_dir() -> str:
        """获取临时目录"""
        return tempfile.gettempdir()

    @staticmethod
    def get_file_separator() -> str:
        """获取文件分隔符"""
        return os.sep

    @staticmethod
    def get_line_separator() -> str:
        """获取行分隔符"""
        return os.linesep

    @staticmethod
    def is_windows() -> bool:
        """是否Windows系统"""
        return platform.system().lower() == "windows"
