"""路径工具模块"""

import os
import shutil
from pathlib import Path
from typing import Callable, List, Optional, Union


class PathUtil:
    """路径工具类"""

    @staticmethod
    def get_path_separator() -> str:
        """获取当前操作系统的路径分隔符

        :return: 路径分隔符字符串（Windows 为 '\\'，Linux/macOS 为 '/'）
        """
        return os.sep

    @staticmethod
    def normalize(path: Union[str, Path]) -> str:
        """标准化路径

        解析符号链接、去除冗余分隔符和上级引用（..），返回绝对路径。

        :param path: 原始路径
        :return: 标准化后的路径字符串
        """
        return str(Path(path).resolve())

    @staticmethod
    def get_parent(path: Union[str, Path]) -> str:
        """获取父目录路径

        :param path: 文件或目录路径
        :return: 父目录的路径字符串
        """
        return str(Path(path).parent)

    @staticmethod
    def get_name(path: Union[str, Path]) -> str:
        """获取路径中的文件名或最后一级目录名

        :param path: 文件或目录路径
        :return: 文件名或目录名
        """
        return Path(path).name

    @staticmethod
    def sub_path(path: Union[str, Path], from_index: int, to_index: int) -> str:
        """获取路径的子段

        按路径层级截取子路径。索引从 0 开始。

        :param path: 原始路径
        :param from_index: 起始索引（含）
        :param to_index: 结束索引（不含）
        :return: 子路径字符串
        :raises ValueError: 索引越界时抛出
        """
        p = Path(path)
        parts = p.parts
        if from_index < 0 or to_index > len(parts) or from_index > to_index:
            raise ValueError(f"无效的索引范围: [{from_index}, {to_index})，路径共 {len(parts)} 层")
        sub_parts = parts[from_index:to_index]
        return str(Path(*sub_parts))

    @staticmethod
    def is_absolute(path: Union[str, Path]) -> bool:
        """判断路径是否为绝对路径

        :param path: 文件路径
        :return: 是绝对路径返回 True
        """
        return Path(path).is_absolute()

    @staticmethod
    def exists(path: Union[str, Path]) -> bool:
        """判断路径是否存在

        :param path: 文件或目录路径
        :return: 存在返回 True
        """
        return Path(path).exists()

    @staticmethod
    def mkdir(path: Union[str, Path]) -> Path:
        """创建目录（包括所有必要的父目录）

        如果目录已存在则不做任何操作。

        :param path: 目录路径
        :return: 创建的目录 Path 对象
        """
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @staticmethod
    def mk_parent_dirs(path: Union[str, Path]) -> Path:
        """创建文件的父目录

        :param path: 文件路径
        :return: 父目录的 Path 对象
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p.parent

    @staticmethod
    def loop_files(
        path: Union[str, Path],
        file_filter: Optional[Callable[[Path], bool]] = None,
    ) -> List[Path]:
        """递归遍历目录下的所有文件

        :param path: 目录路径
        :param file_filter: 可选的过滤函数，接受 Path 参数，返回 True 表示保留
        :return: 文件 Path 列表
        :raises FileNotFoundError: 路径不存在时抛出
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"路径不存在: {path}")
        if p.is_file():
            files = [p]
        else:
            files = sorted(p.rglob("*"))
            files = [f for f in files if f.is_file()]
        if file_filter is not None:
            files = [f for f in files if file_filter(f)]
        return files

    @staticmethod
    def copy(
        src: Union[str, Path],
        dest: Union[str, Path],
        is_override: bool = True,
    ) -> Path:
        """复制文件或目录

        :param src: 源路径
        :param dest: 目标路径
        :param is_override: 是否覆盖已存在的目标，默认 True
        :return: 目标路径的 Path 对象
        :raises FileExistsError: 目标已存在且 is_override 为 False 时抛出
        :raises FileNotFoundError: 源路径不存在时抛出
        """
        src_p = Path(src)
        dest_p = Path(dest)
        if not src_p.exists():
            raise FileNotFoundError(f"源路径不存在: {src}")
        if dest_p.exists() and not is_override:
            raise FileExistsError(f"目标路径已存在: {dest}")
        if src_p.is_dir():
            if dest_p.exists() and is_override:
                shutil.rmtree(dest_p)
            shutil.copytree(src_p, dest_p)
        else:
            dest_p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_p, dest_p)
        return dest_p

    @staticmethod
    def move(
        src: Union[str, Path],
        dest: Union[str, Path],
        is_override: bool = True,
    ) -> Path:
        """移动文件或目录

        :param src: 源路径
        :param dest: 目标路径
        :param is_override: 是否覆盖已存在的目标，默认 True
        :return: 目标路径的 Path 对象
        :raises FileExistsError: 目标已存在且 is_override 为 False 时抛出
        :raises FileNotFoundError: 源路径不存在时抛出
        """
        src_p = Path(src)
        dest_p = Path(dest)
        if not src_p.exists():
            raise FileNotFoundError(f"源路径不存在: {src}")
        if dest_p.exists():
            if not is_override:
                raise FileExistsError(f"目标路径已存在: {dest}")
            if dest_p.is_dir():
                shutil.rmtree(dest_p)
            else:
                dest_p.unlink()
        dest_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_p), str(dest_p))
        return dest_p

    @staticmethod
    def del_path(path: Union[str, Path]) -> bool:
        """删除文件或目录

        目录将递归删除。如果路径不存在则返回 False。

        :param path: 文件或目录路径
        :return: 删除成功返回 True，路径不存在返回 False
        """
        p = Path(path)
        if not p.exists():
            return False
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
        return True

    @staticmethod
    def equals(
        path1: Union[str, Path],
        path2: Union[str, Path],
    ) -> bool:
        """比较两个路径是否指向同一位置

        通过解析后的绝对路径进行比较。

        :param path1: 第一个路径
        :param path2: 第二个路径
        :return: 相等返回 True
        """
        return Path(path1).resolve() == Path(path2).resolve()

    @staticmethod
    def starts_with(path: Union[str, Path], prefix: str) -> bool:
        """判断路径是否以指定前缀开头

        :param path: 文件路径
        :param prefix: 路径前缀
        :return: 匹配返回 True
        """
        normalized_path = PathUtil.normalize(path)
        normalized_prefix = PathUtil.normalize(prefix)
        return normalized_path.startswith(normalized_prefix)

    @staticmethod
    def ends_with(path: Union[str, Path], suffix: str) -> bool:
        """判断路径是否以指定后缀结尾

        :param path: 文件路径
        :param suffix: 路径后缀
        :return: 匹配返回 True
        """
        return str(path).replace("\\", "/").endswith(suffix.replace("\\", "/"))
