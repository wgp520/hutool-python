"""资源工具模块"""

import fnmatch
import os
from pathlib import Path
from typing import IO, List


class ResourceUtil:
    """资源工具类"""

    # 默认资源搜索路径列表，可通过 add_resource_path 扩展
    _resource_paths: List[str] = []

    @classmethod
    def add_resource_path(cls, path: str) -> None:
        """添加资源搜索路径

        :param path: 资源目录的绝对或相对路径
        """
        abs_path = os.path.abspath(path)
        if abs_path not in cls._resource_paths:
            cls._resource_paths.append(abs_path)

    @staticmethod
    def get_resource(path: str) -> str:
        """获取资源的绝对路径

        按以下顺序查找资源:
        1. 绝对路径直接返回
        2. 当前工作目录
        3. 已注册的资源搜索路径

        :param path: 资源的相对或绝对路径
        :return: 资源的绝对路径
        :raises FileNotFoundError: 资源不存在时抛出
        """
        # 如果是绝对路径且存在，直接返回
        if os.path.isabs(path) and os.path.exists(path):
            return os.path.abspath(path)

        # 在当前工作目录查找
        cwd_path = os.path.join(os.getcwd(), path)
        if os.path.exists(cwd_path):
            return os.path.abspath(cwd_path)

        # 在已注册的资源路径中查找
        for res_dir in ResourceUtil._resource_paths:
            candidate = os.path.join(res_dir, path)
            if os.path.exists(candidate):
                return os.path.abspath(candidate)

        raise FileNotFoundError(f"资源不存在: {path}")

    @staticmethod
    def get_resource_bytes(path: str) -> bytes:
        """读取资源为字节数组

        :param path: 资源的相对或绝对路径
        :return: 资源内容的字节数组
        :raises FileNotFoundError: 资源不存在时抛出
        """
        abs_path = ResourceUtil.get_resource(path)
        with open(abs_path, "rb") as f:
            return f.read()

    @staticmethod
    def get_resource_str(path: str, charset: str = "utf-8") -> str:
        """读取资源为字符串

        :param path: 资源的相对或绝对路径
        :param charset: 字符编码，默认 utf-8
        :return: 资源内容的字符串
        :raises FileNotFoundError: 资源不存在时抛出
        """
        abs_path = ResourceUtil.get_resource(path)
        with open(abs_path, encoding=charset) as f:
            return f.read()

    @staticmethod
    def get_resource_stream(path: str) -> IO:
        """获取资源的文件流

        调用方负责关闭返回的文件流。

        :param path: 资源的相对或绝对路径
        :return: 可读的文件对象
        :raises FileNotFoundError: 资源不存在时抛出
        """
        abs_path = ResourceUtil.get_resource(path)
        return open(abs_path, "rb")

    @staticmethod
    def get_resources(pattern: str) -> List[str]:
        """根据模式匹配获取资源列表

        支持通配符模式（如 "*.txt"、"data/*.csv"）。
        在当前工作目录和已注册的资源搜索路径中搜索。

        :param pattern: 文件名匹配模式（支持 * 和 ? 通配符）
        :return: 匹配的资源绝对路径列表
        """
        results: List[str] = []

        # 在当前工作目录中搜索
        cwd = os.getcwd()
        ResourceUtil._search_in_dir(cwd, pattern, results)

        # 在已注册的资源路径中搜索
        for res_dir in ResourceUtil._resource_paths:
            ResourceUtil._search_in_dir(res_dir, pattern, results)

        # 去重并排序
        return sorted(set(results))

    @staticmethod
    def _search_in_dir(base_dir: str, pattern: str, results: List[str]) -> None:
        """在指定目录中递归搜索匹配的文件

        :param base_dir: 基础搜索目录
        :pattern: 文件名匹配模式
        :param results: 结果列表（原地修改）
        """
        base = Path(base_dir)
        if not base.is_dir():
            return

        # 如果 pattern 包含路径分隔符，按路径层级匹配
        if os.sep in pattern or "/" in pattern:
            for match in base.glob(pattern):
                if match.is_file():
                    results.append(str(match.resolve()))
        else:
            # 只按文件名匹配，递归搜索所有子目录
            for file_path in base.rglob("*"):
                if file_path.is_file() and fnmatch.fnmatch(file_path.name, pattern):
                    results.append(str(file_path.resolve()))
