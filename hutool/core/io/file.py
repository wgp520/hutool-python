"""
文件工具类，对应 Java cn.hutool.core.io.FileUtil

基于 pathlib.Path 实现，辅以 os 和 shutil。
"""

import binascii
import hashlib
import mimetypes
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union


class FileUtil:
    """文件工具类，对应 Java cn.hutool.core.io.FileUtil"""

    FILE_SEPARATOR: str = os.sep

    # ------------------------------------------------------------------
    # 判断
    # ------------------------------------------------------------------

    @staticmethod
    def is_windows() -> bool:
        """
        判断当前操作系统是否为 Windows。

        :return: 是否为 Windows 系统
        """
        return os.name == "nt"

    @staticmethod
    def exist(path: Union[str, Path]) -> bool:
        """
        判断文件或目录是否存在。

        :param path: 文件或目录路径
        :return: 是否存在
        """
        return Path(path).exists()

    @staticmethod
    def is_dir(path: Union[str, Path]) -> bool:
        """
        判断是否为目录。

        :param path: 路径
        :return: 是否为目录
        """
        return Path(path).is_dir()

    @staticmethod
    def is_file(path: Union[str, Path]) -> bool:
        """
        判断是否为文件。

        :param path: 路径
        :return: 是否为文件
        """
        return Path(path).is_file()

    @staticmethod
    def is_absolute(path: Union[str, Path]) -> bool:
        """
        判断路径是否为绝对路径。

        :param path: 路径
        :return: 是否为绝对路径
        """
        return Path(path).is_absolute()

    @staticmethod
    def is_empty(path: Union[str, Path]) -> bool:
        """
        文件或目录是否为空。

        - 文件：大小为 0 视为空。
        - 目录：不含任何子项视为空。
        - 路径不存在视为空。

        :param path: 文件或目录路径
        :return: 是否为空
        """
        p = Path(path)
        if not p.exists():
            return True
        if p.is_file():
            return p.stat().st_size == 0
        if p.is_dir():
            # 如果能列出任何子项则非空
            return not any(p.iterdir())
        return True

    # ------------------------------------------------------------------
    # 创建
    # ------------------------------------------------------------------

    @staticmethod
    def file(*names: str) -> Path:
        """
        根据多个名称段构建文件路径。

        例如: ``FileUtil.file("home", "user", "test.txt")``

        :param names: 路径段
        :return: Path 对象
        :raises ValueError: 未传入任何路径段时
        """
        if not names:
            raise ValueError("至少需要一个路径段")
        result = Path(names[0])
        for name in names[1:]:
            result = result / name
        return result

    @staticmethod
    def touch(path: Union[str, Path]) -> Path:
        """
        创建文件（包括父目录）。

        如果文件已存在则只更新访问/修改时间。

        :param path: 文件路径
        :return: 创建的文件路径
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        return p

    @staticmethod
    def mkdir(path: Union[str, Path]) -> Path:
        """
        创建目录。

        如果目录已存在则直接返回。

        :param path: 目录路径
        :return: 创建的目录路径
        """
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @staticmethod
    def mkdirs(path: Union[str, Path]) -> Path:
        """
        创建多级目录（与 mkdir 行为一致，支持多级创建）。

        :param path: 目录路径
        :return: 创建的目录路径
        """
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @staticmethod
    def create_temp_file(
        prefix: str = "hutool",
        suffix: str = ".tmp",
        parent_dir: Optional[str] = None,
    ) -> Path:
        """创建临时文件

        :param prefix: 文件名前缀
        :param suffix: 文件名后缀（含点号）
        :param parent_dir: 临时文件所在目录，为 None 时使用系统临时目录
        :return: 创建的临时文件路径
        """
        dir_path: Optional[str] = parent_dir
        fd, tmp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir_path)
        os.close(fd)
        return Path(tmp_path)

    # ------------------------------------------------------------------
    # 删除
    # ------------------------------------------------------------------

    @staticmethod
    def del_file(path: Union[str, Path]) -> bool:
        """删除文件或目录

        - 文件：直接删除。
        - 目录：递归删除整个目录树。
        - 路径不存在时返回 True。

        :return: 是否删除成功
        """
        p = Path(path)
        if not p.exists():
            return True
        if p.is_file() or p.is_symlink():
            p.unlink()
            return True
        if p.is_dir():
            shutil.rmtree(p)
            return True
        return False

    @staticmethod
    def clean(path: Union[str, Path]) -> bool:
        """清空目录内容（不删除目录本身）

        :return: 是否清空成功
        """
        p = Path(path)
        if not p.is_dir():
            return False
        for child in p.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
        return True

    # ------------------------------------------------------------------
    # 复制 / 移动
    # ------------------------------------------------------------------

    @staticmethod
    def copy(
        src: Union[str, Path],
        dest: Union[str, Path],
        is_override: bool = True,
    ) -> Path:
        """复制文件或目录

        :param src: 源路径
        :param dest: 目标路径
        :param is_override: 是否覆盖已存在的目标
        :return: 目标路径
        """
        src_path = Path(src)
        dest_path = Path(dest)

        if not src_path.exists():
            raise FileNotFoundError(f"源路径不存在: {src_path}")

        if src_path.is_dir():
            # 复制目录
            if dest_path.exists() and is_override:
                shutil.rmtree(dest_path)
            shutil.copytree(src_path, dest_path)
        else:
            # 复制文件
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            if not is_override and dest_path.exists():
                return dest_path
            shutil.copy2(src_path, dest_path)
        return dest_path

    @staticmethod
    def copy_file(
        src: Union[str, Path],
        dest: Union[str, Path],
    ) -> Path:
        """
        复制文件。

        如果目标目录不存在则自动创建。

        :param src: 源文件路径
        :param dest: 目标文件路径
        :return: 目标文件路径
        :raises FileNotFoundError: 源文件不存在或不是文件时
        """
        src_path = Path(src)
        dest_path = Path(dest)

        if not src_path.is_file():
            raise FileNotFoundError(f"源文件不存在或不是文件: {src_path}")

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest_path)
        return dest_path

    @staticmethod
    def move(
        src: Union[str, Path],
        dest: Union[str, Path],
        is_override: bool = True,
    ) -> Path:
        """移动文件或目录

        :param src: 源路径
        :param dest: 目标路径
        :param is_override: 是否覆盖已存在的目标
        :return: 目标路径
        """
        src_path = Path(src)
        dest_path = Path(dest)

        if not src_path.exists():
            raise FileNotFoundError(f"源路径不存在: {src_path}")

        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if dest_path.exists():
            if not is_override:
                return dest_path
            if dest_path.is_dir():
                shutil.rmtree(dest_path)
            else:
                dest_path.unlink()

        shutil.move(str(src_path), str(dest_path))
        return dest_path

    @staticmethod
    def rename(file: Union[str, Path], new_name: str) -> Path:
        """重命名文件或目录

        :param file: 源文件或目录路径
        :param new_name: 新名称（仅名称部分，不含路径）
        :return: 重命名后的路径
        """
        p = Path(file)
        if not p.exists():
            raise FileNotFoundError(f"路径不存在: {p}")
        new_path = p.parent / new_name
        p.rename(new_path)
        return new_path

    # ------------------------------------------------------------------
    # 读写
    # ------------------------------------------------------------------

    @staticmethod
    def read_string(path: Union[str, Path], charset: str = "utf-8") -> str:
        """读取文件内容为字符串

        :param path: 文件路径
        :param charset: 字符编码
        :return: 文件内容字符串
        """
        return Path(path).read_text(encoding=charset)

    @staticmethod
    def read_bytes(path: Union[str, Path]) -> bytes:
        """
        读取文件内容为字节数组。

        :param path: 文件路径
        :return: 字节数据
        """
        return Path(path).read_bytes()

    @staticmethod
    def read_lines(path: Union[str, Path], charset: str = "utf-8") -> List[str]:
        """
        读取文件内容为字符串列表（每行一个元素，保留换行符）。

        :param path: 文件路径
        :param charset: 字符编码
        :return: 行列表
        """
        with open(path, encoding=charset) as f:
            return f.readlines()

    @staticmethod
    def read_utf8_lines(path: Union[str, Path]) -> List[str]:
        """
        以 UTF-8 编码读取文件的每一行（去除行尾换行符）。

        :param path: 文件路径
        :return: 行列表
        """
        return FileUtil.read_lines_str(path, charset="utf-8")

    @staticmethod
    def read_lines_str(path: Union[str, Path], charset: str = "utf-8") -> List[str]:
        """
        读取文件的每一行，去除行尾换行符。

        :param path: 文件路径
        :param charset: 字符编码
        :return: 行列表
        """
        with open(path, encoding=charset) as f:
            return f.read().splitlines()

    @staticmethod
    def write_string(
        path: Union[str, Path],
        content: str,
        charset: str = "utf-8",
        is_append: bool = False,
    ) -> Path:
        """写入字符串到文件

        :param path: 文件路径
        :param content: 写入内容
        :param charset: 字符编码
        :param is_append: 是否追加模式
        :return: 文件路径
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if is_append else "w"
        with open(p, mode, encoding=charset) as f:
            f.write(content)
        return p

    @staticmethod
    def write_bytes(
        path: Union[str, Path],
        data: bytes,
        is_append: bool = False,
    ) -> Path:
        """写字节数组到文件

        :param path: 文件路径
        :param data: 字节数据
        :param is_append: 是否追加模式
        :return: 文件路径
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        mode = "ab" if is_append else "wb"
        with open(p, mode) as f:
            f.write(data)
        return p

    @staticmethod
    def write_lines(
        path: Union[str, Path],
        lines: list,
        charset: str = "utf-8",
        is_append: bool = False,
    ) -> Path:
        """写入行列表到文件

        每个元素后自动追加换行符。

        :param path: 文件路径
        :param lines: 行列表
        :param charset: 字符编码
        :param is_append: 是否追加模式
        :return: 文件路径
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if is_append else "w"
        with open(p, mode, encoding=charset) as f:
            for line in lines:
                f.write(str(line))
                f.write("\n")
        return p

    @staticmethod
    def append_string(
        path: Union[str, Path],
        content: str,
        charset: str = "utf-8",
    ) -> Path:
        """追加字符串到文件末尾

        :param path: 文件路径
        :param content: 追加内容
        :param charset: 字符编码
        :return: 文件路径
        """
        return FileUtil.write_string(path, content, charset=charset, is_append=True)

    @staticmethod
    def append_lines(
        path: Union[str, Path],
        lines: list,
        charset: str = "utf-8",
    ) -> Path:
        """追加行列表到文件末尾

        :param path: 文件路径
        :param lines: 行列表
        :param charset: 字符编码
        :return: 文件路径
        """
        return FileUtil.write_lines(path, lines, charset=charset, is_append=True)

    # ------------------------------------------------------------------
    # 遍历
    # ------------------------------------------------------------------

    @staticmethod
    def loop_files(
        path: Union[str, Path],
        max_depth: Optional[int] = None,
        file_filter: Optional[Callable[[Path], bool]] = None,
    ) -> List[Path]:
        """递归遍历目录下的所有文件

        :param path: 根目录路径
        :param max_depth: 最大递归深度，None 表示不限制
        :param file_filter: 文件过滤函数，返回 True 保留
        :return: 符合条件的文件路径列表
        """
        root = Path(path)
        if not root.is_dir():
            return []

        result: List[Path] = []
        FileUtil._walk_files(root, 0, max_depth, file_filter, result)
        return result

    @staticmethod
    def _walk_files(
        directory: Path,
        current_depth: int,
        max_depth: Optional[int],
        file_filter: Optional[Callable[[Path], bool]],
        result: List[Path],
    ) -> None:
        """递归遍历的内部实现"""
        if max_depth is not None and current_depth > max_depth:
            return
        try:
            for child in sorted(directory.iterdir()):
                if child.is_file():
                    if file_filter is None or file_filter(child):
                        result.append(child)
                elif child.is_dir():
                    FileUtil._walk_files(child, current_depth + 1, max_depth, file_filter, result)
        except PermissionError:
            pass

    @staticmethod
    def list_file_names(path: Union[str, Path]) -> List[str]:
        """列出目录下的文件名（仅直接子文件，不含子目录内的文件）

        :param path: 目录路径
        :return: 文件名列表（不含路径前缀）
        """
        p = Path(path)
        if not p.is_dir():
            return []
        return [child.name for child in sorted(p.iterdir()) if child.is_file()]

    @staticmethod
    def walk_files(
        path: Union[str, Path],
        consumer: Callable[[Path], None],
    ) -> None:
        """
        递归遍历文件并对每个文件执行操作。

        :param path: 根目录路径
        :param consumer: 对每个文件执行的回调函数
        """
        root = Path(path)
        if not root.exists():
            return
        if root.is_file():
            consumer(root)
            return
        for file_path in FileUtil.loop_files(root):
            consumer(file_path)

    # ------------------------------------------------------------------
    # 信息
    # ------------------------------------------------------------------

    @staticmethod
    def size(path: Union[str, Path]) -> int:
        """
        获取文件大小（字节）。

        对于目录，返回整个目录树的总大小。

        :param path: 文件或目录路径
        :return: 大小（字节）
        :raises FileNotFoundError: 路径不存在时
        """
        p = Path(path)
        if p.is_file():
            return p.stat().st_size
        if p.is_dir():
            total = 0
            for child in p.rglob("*"):
                if child.is_file():
                    total += child.stat().st_size
            return total
        raise FileNotFoundError(f"路径不存在: {p}")

    @staticmethod
    def last_modified_time(path: Union[str, Path]) -> datetime:
        """获取文件最后修改时间

        :return: 最后修改时间的 datetime 对象
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"路径不存在: {p}")
        mtime = p.stat().st_mtime
        return datetime.fromtimestamp(mtime)

    @staticmethod
    def get_total_lines(path: Union[str, Path]) -> int:
        """
        获取文件总行数。

        :param path: 文件路径
        :return: 总行数
        """
        count = 0
        with open(path, "rb") as f:
            for _ in f:
                count += 1
        return count

    @staticmethod
    def get_name(path: Union[str, Path]) -> str:
        """
        获取文件名（含扩展名）。

        例如: ``/home/user/test.txt -> test.txt``

        :param path: 文件路径
        :return: 文件名
        """
        return Path(path).name

    @staticmethod
    def get_suffix(path: Union[str, Path]) -> str:
        """
        获取文件扩展名（不带点号）。

        例如: ``/home/user/test.txt -> txt``

        如果没有扩展名则返回空字符串。

        :param path: 文件路径
        :return: 扩展名，无扩展名时返回空字符串
        """
        name = Path(path).name
        dot_index = name.rfind(".")
        if dot_index <= 0:
            return ""
        return name[dot_index + 1 :]

    @staticmethod
    def get_prefix(path: Union[str, Path]) -> str:
        """
        获取文件名前缀（不含扩展名）。

        例如: ``/home/user/test.txt -> test``

        :param path: 文件路径
        :return: 文件名前缀
        """
        name = Path(path).name
        dot_index = name.rfind(".")
        if dot_index <= 0:
            return name
        return name[:dot_index]

    @staticmethod
    def main_name(path: Union[str, Path]) -> str:
        """
        获取主文件名（同 get_prefix）。

        :param path: 文件路径
        :return: 主文件名
        """
        return FileUtil.get_prefix(path)

    @staticmethod
    def normalize(path: Union[str, Path]) -> str:
        """
        标准化路径，解析 ~ 和相对路径符号。

        :param path: 原始路径
        :return: 标准化后的路径字符串
        """
        p = Path(path).expanduser()
        try:
            return str(p.resolve())
        except OSError:
            return str(p)

    # ------------------------------------------------------------------
    # 系统路径
    # ------------------------------------------------------------------

    @staticmethod
    def get_tmp_dir_path() -> str:
        """
        获取系统临时目录路径（字符串）。

        :return: 临时目录路径
        """
        return tempfile.gettempdir()

    @staticmethod
    def get_tmp_dir() -> Path:
        """
        获取系统临时目录（Path 对象）。

        :return: 临时目录 Path 对象
        """
        return Path(tempfile.gettempdir())

    @staticmethod
    def get_user_home_path() -> str:
        """
        获取用户主目录路径（字符串）。

        :return: 用户主目录路径
        """
        return str(Path.home())

    @staticmethod
    def get_user_home_dir() -> Path:
        """
        获取用户主目录（Path 对象）。

        :return: 用户主目录 Path 对象
        """
        return Path.home()

    # ------------------------------------------------------------------
    # 工具
    # ------------------------------------------------------------------

    @staticmethod
    def newer_than(file: Union[str, Path], reference: Union[str, Path]) -> bool:
        """判断文件是否比参考文件更新

        :param file: 待比较的文件
        :param reference: 参考文件
        :return: 如果 file 的修改时间晚于 reference 则返回 True
        """
        file_path = Path(file)
        ref_path = Path(reference)

        if not file_path.exists():
            return False
        if not ref_path.exists():
            return True

        file_mtime = file_path.stat().st_mtime
        ref_mtime = ref_path.stat().st_mtime
        return file_mtime > ref_mtime

    @staticmethod
    def is_symlink(path: Union[str, Path]) -> bool:
        """
        判断是否为符号链接。

        :param path: 路径
        :return: 是否为符号链接
        """
        return Path(path).is_symlink()

    @staticmethod
    def sub_path(path: Union[str, Path], start: int, end: int) -> str:
        """获取子路径

        :param path: 源路径
        :param start: 起始索引（含）
        :param end: 结束索引（不含）
        :return: 子路径字符串

        例如: sub_path("/home/user/test.txt", 1, 3) -> "user/test.txt"
        """
        p = Path(path)
        parts = p.parts
        if start < 0:
            start = 0
        if end > len(parts):
            end = len(parts)
        if start >= end:
            return ""
        sub_parts = parts[start:end]
        return str(Path(*sub_parts))

    # ================================================================== #
    #  UTF-8 便捷方法
    # ================================================================== #

    @staticmethod
    def write_utf8_string(path: Union[str, Path], content: str) -> Path:
        """
        以 UTF-8 编码写入字符串到文件。

        :param path: 文件路径
        :param content: 写入内容
        :return: 文件路径
        """
        return FileUtil.write_string(path, content, charset="utf-8")

    @staticmethod
    def write_utf8_lines(path: Union[str, Path], lines: list) -> Path:
        """
        以 UTF-8 编码写入多行到文件。

        :param path: 文件路径
        :param lines: 行列表
        :return: 文件路径
        """
        return FileUtil.write_lines(path, lines, charset="utf-8")

    @staticmethod
    def write_utf8_map(
        path: Union[str, Path],
        map_data: Dict[str, Any],
        kv_separator: str = "=",
    ) -> Path:
        """
        以 UTF-8 编码将字典写入文件（每行一个 key=value）。

        :param path: 文件路径
        :param map_data: 字典数据
        :param kv_separator: 键值分隔符，默认 "="
        :return: 文件路径
        """
        lines = [f"{k}{kv_separator}{v}" for k, v in map_data.items()]
        return FileUtil.write_utf8_lines(path, lines)

    @staticmethod
    def write_map(
        path: Union[str, Path],
        map_data: Dict[str, Any],
        kv_separator: str = "=",
        charset: str = "utf-8",
    ) -> Path:
        """
        将字典写入文件（每行一个 key=value）。

        :param path: 文件路径
        :param map_data: 字典数据
        :param kv_separator: 键值分隔符，默认 "="
        :param charset: 字符编码
        :return: 文件路径
        """
        lines = [f"{k}{kv_separator}{v}" for k, v in map_data.items()]
        return FileUtil.write_lines(path, lines, charset=charset)

    @staticmethod
    def append_utf8_string(path: Union[str, Path], content: str) -> Path:
        """
        以 UTF-8 编码追加字符串到文件。

        :param path: 文件路径
        :param content: 追加内容
        :return: 文件路径
        """
        return FileUtil.append_string(path, content, charset="utf-8")

    @staticmethod
    def append_utf8_lines(path: Union[str, Path], lines: list) -> Path:
        """
        以 UTF-8 编码追加多行到文件。

        :param path: 文件路径
        :param lines: 行列表
        :return: 文件路径
        """
        return FileUtil.append_lines(path, lines, charset="utf-8")

    @staticmethod
    def read_utf8_string(path: Union[str, Path]) -> str:
        """
        以 UTF-8 编码读取文件内容为字符串。

        :param path: 文件路径
        :return: 文件内容字符串
        """
        return FileUtil.read_string(path, charset="utf-8")

    @staticmethod
    def read_line(
        path: Union[str, Path],
        line_number: int,
        charset: str = "utf-8",
    ) -> Optional[str]:
        """
        按行号读取文件的指定行（0-based）。

        :param path: 文件路径
        :param line_number: 行号（从 0 开始）
        :param charset: 字符编码
        :return: 指定行的内容，超出范围返回 None
        """
        if line_number < 0:
            return None
        with open(path, encoding=charset) as f:
            for i, line in enumerate(f):
                if i == line_number:
                    return line.rstrip("\n\r")
        return None

    @staticmethod
    def load_file(
        path: Union[str, Path],
        charset: str = "utf-8",
    ) -> List[str]:
        """
        加载文件内容为行列表（去除行尾换行符）。

        :param path: 文件路径
        :param charset: 字符编码
        :return: 行列表
        """
        return FileUtil.read_lines_str(path, charset=charset)

    @staticmethod
    def load_utf8(path: Union[str, Path]) -> List[str]:
        """
        以 UTF-8 编码加载文件内容为行列表。

        :param path: 文件路径
        :return: 行列表
        """
        return FileUtil.read_lines_str(path, charset="utf-8")

    # ================================================================== #
    #  路径操作
    # ================================================================== #

    @staticmethod
    def ls(path: Union[str, Path]) -> List[Path]:
        """
        列出目录内容（仅直接子项）。

        :param path: 目录路径
        :return: 子项路径列表
        :raises FileNotFoundError: 路径不存在时
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"路径不存在: {p}")
        if not p.is_dir():
            raise NotADirectoryError(f"不是目录: {p}")
        return sorted(p.iterdir())

    @staticmethod
    def ext_name(path: Union[str, Path]) -> str:
        """
        获取文件扩展名（不带点号）。

        与 :meth:`get_suffix` 等价。

        :param path: 文件路径
        :return: 扩展名，无扩展名时返回空字符串
        """
        return FileUtil.get_suffix(path)

    @staticmethod
    def get_absolute_path(path: Union[str, Path]) -> str:
        """
        获取路径的绝对路径字符串。

        :param path: 文件路径
        :return: 绝对路径字符串
        """
        return str(Path(path).resolve())

    @staticmethod
    def get_canonical_path(path: Union[str, Path]) -> str:
        """
        获取路径的规范路径字符串（解析符号链接和 ``..``）。

        :param path: 文件路径
        :return: 规范路径字符串
        """
        p = Path(path)
        try:
            return str(p.resolve())
        except OSError:
            return str(p.absolute())

    @staticmethod
    def get_parent(path: Union[str, Path], depth: int = 1) -> str:
        """
        获取父目录路径（支持多级）。

        :param path: 文件路径
        :param depth: 向上层级数，默认 1
        :return: 父目录路径字符串
        """
        p = Path(path)
        for _ in range(depth):
            p = p.parent
        return str(p)

    @staticmethod
    def get_type(path: Union[str, Path]) -> str:
        """
        获取文件类型（通过扩展名推断 MIME 类型）。

        :param path: 文件路径
        :return: MIME 类型字符串，无法推断时返回空字符串
        """
        mime_type, _ = mimetypes.guess_type(str(path))
        return mime_type or ""

    @staticmethod
    def get_mime_type(path: Union[str, Path]) -> str:
        """
        获取文件的 MIME 类型。

        :param path: 文件路径
        :return: MIME 类型字符串
        """
        return FileUtil.get_type(path)

    @staticmethod
    def is_absolute_path(path: Union[str, Path]) -> bool:
        """
        判断路径是否为绝对路径。

        :param path: 路径
        :return: 是否为绝对路径
        """
        return Path(path).is_absolute()

    @staticmethod
    def last_index_of_separator(path: str) -> int:
        """
        获取路径中最后一个分隔符的索引位置。

        :param path: 路径字符串
        :return: 最后分隔符索引，无分隔符时返回 -1
        """
        sep_pos = max(path.rfind("/"), path.rfind("\\"))
        return sep_pos

    @staticmethod
    def path_ends_with(path: Union[str, Path], suffix: str) -> bool:
        """
        判断路径是否以指定后缀结尾。

        :param path: 路径
        :param suffix: 后缀字符串
        :return: 是否以指定后缀结尾
        """
        return str(path).endswith(suffix)

    # ================================================================== #
    #  状态检查
    # ================================================================== #

    @staticmethod
    def is_dir_empty(path: Union[str, Path]) -> bool:
        """
        判断目录是否为空。

        :param path: 目录路径
        :return: 是否为空目录
        """
        p = Path(path)
        if not p.is_dir():
            return True
        return not any(p.iterdir())

    @staticmethod
    def is_directory(path: Union[str, Path]) -> bool:
        """
        判断是否为目录。

        与 :meth:`is_dir` 等价。

        :param path: 路径
        :return: 是否为目录
        """
        return FileUtil.is_dir(path)

    @staticmethod
    def is_modified(path: Union[str, Path], reference_time: float = 0) -> bool:
        """
        判断文件是否在指定时间之后被修改。

        :param path: 文件路径
        :param reference_time: 参考时间戳（Unix 秒），默认 0 表示始终返回 True
        :return: 是否被修改
        """
        p = Path(path)
        if not p.exists():
            return False
        return p.stat().st_mtime > reference_time

    @staticmethod
    def file_not_empty(path: Union[str, Path]) -> bool:
        """
        判断文件是否非空。

        :param path: 文件路径
        :return: 文件是否存在且大小 > 0
        """
        p = Path(path)
        return p.is_file() and p.stat().st_size > 0

    @staticmethod
    def is_sub_path(parent: Union[str, Path], child: Union[str, Path]) -> bool:
        """
        判断 child 是否为 parent 的子路径。

        :param parent: 父路径
        :param child: 子路径
        :return: 是否为子路径
        """
        try:
            parent_resolved = Path(parent).resolve()
            child_resolved = Path(child).resolve()
            return str(child_resolved).startswith(str(parent_resolved) + os.sep) or child_resolved == parent_resolved
        except OSError:
            return False

    @staticmethod
    def path_equals(path1: Union[str, Path], path2: Union[str, Path]) -> bool:
        """
        判断两个路径是否指向同一文件/目录。

        :param path1: 第一个路径
        :param path2: 第二个路径
        :return: 是否相等
        """
        try:
            return Path(path1).resolve() == Path(path2).resolve()
        except OSError:
            return str(path1) == str(path2)

    @staticmethod
    def content_equals(
        file1: Union[str, Path],
        file2: Union[str, Path],
        charset: str = "utf-8",
    ) -> bool:
        """
        判断两个文件的内容是否相等。

        :param file1: 第一个文件路径
        :param file2: 第二个文件路径
        :param charset: 字符编码（用于文本比较）
        :return: 内容是否相等
        """
        p1, p2 = Path(file1), Path(file2)
        if not p1.is_file() or not p2.is_file():
            return False
        if p1.stat().st_size != p2.stat().st_size:
            return False
        return FileUtil.read_string(p1, charset=charset) == FileUtil.read_string(p2, charset=charset)

    # ================================================================== #
    #  创建操作
    # ================================================================== #

    @staticmethod
    def mk_parent_dirs(path: Union[str, Path]) -> Path:
        """
        创建文件的父目录（如果不存在）。

        :param path: 文件路径
        :return: 文件路径
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    @staticmethod
    def mkdirs_safely(path: Union[str, Path]) -> Path:
        """
        安全创建目录（如果不存在则创建）。

        与 :meth:`mkdir` 等价。

        :param path: 目录路径
        :return: 目录路径
        """
        return FileUtil.mkdir(path)

    @staticmethod
    def new_file(path: Union[str, Path]) -> Path:
        """
        创建新文件（包含父目录）。

        与 :meth:`touch` 等价。

        :param path: 文件路径
        :return: 文件路径
        """
        return FileUtil.touch(path)

    @staticmethod
    def readable_file_size(size: int, precision: int = 1) -> str:
        """
        将文件大小转换为可读字符串（如 "1.5 MB"）。

        :param size: 文件大小（字节）
        :param precision: 小数精度
        :return: 可读大小字符串
        """
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        unit_index = 0
        fsize = float(size)
        while fsize >= 1024.0 and unit_index < len(units) - 1:
            fsize /= 1024.0
            unit_index += 1
        if unit_index == 0:
            return f"{int(fsize)} B"
        return "{:.{}f} {}".format(fsize, precision, units[unit_index])

    # ================================================================== #
    #  内容操作
    # ================================================================== #

    @staticmethod
    def copy_content(
        src: Union[str, Path],
        dest: Union[str, Path],
        is_override: bool = True,
    ) -> Path:
        """
        复制文件内容。

        与 :meth:`copy` 等价。

        :param src: 源路径
        :param dest: 目标路径
        :param is_override: 是否覆盖
        :return: 目标路径
        """
        return FileUtil.copy(src, dest, is_override=is_override)

    @staticmethod
    def move_content(src: Union[str, Path], dest: Union[str, Path]) -> Path:
        """
        移动文件内容。

        与 :meth:`move` 等价（默认覆盖）。

        :param src: 源路径
        :param dest: 目标路径
        :return: 目标路径
        """
        return FileUtil.move(src, dest, is_override=True)

    @staticmethod
    def convert_charset(
        path: Union[str, Path],
        src_charset: str,
        dest_charset: str = "utf-8",
    ) -> Path:
        """
        转换文件编码。

        :param path: 文件路径
        :param src_charset: 源编码
        :param dest_charset: 目标编码，默认 "utf-8"
        :return: 文件路径
        """
        p = Path(path)
        content = p.read_text(encoding=src_charset)
        p.write_text(content, encoding=dest_charset)
        return p

    @staticmethod
    def convert_line_separator(
        path: Union[str, Path],
        separator: str = "\n",
    ) -> Path:
        """
        转换文件的换行符。

        :param path: 文件路径
        :param separator: 目标换行符（``"\\n"``、``"\\r\\n"``、``"\\r"``）
        :return: 文件路径
        """
        p = Path(path)
        content = p.read_bytes()
        # 先统一为 \n
        text = content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        # 再转换为目标分隔符
        if separator != "\n":
            text = text.replace(b"\n", separator.encode())
        p.write_bytes(text)
        return p

    @staticmethod
    def copy_files_from_dir(
        src_dir: Union[str, Path],
        dest_dir: Union[str, Path],
        is_override: bool = True,
    ) -> List[Path]:
        """
        从源目录复制所有文件到目标目录（不含子目录结构）。

        :param src_dir: 源目录路径
        :param dest_dir: 目标目录路径
        :param is_override: 是否覆盖已存在的文件
        :return: 复制的文件路径列表
        """
        src = Path(src_dir)
        dest = Path(dest_dir)
        dest.mkdir(parents=True, exist_ok=True)
        result = []
        for child in src.iterdir():
            if child.is_file():
                dest_file = dest / child.name
                if not is_override and dest_file.exists():
                    continue
                shutil.copy2(child, dest_file)
                result.append(dest_file)
        return result

    @staticmethod
    def check_slip(file_path: Union[str, Path]) -> None:
        """
        检查路径是否存在路径穿越（``..`` 攻击）。

        直接分析原始路径字符串中的 ``..`` 段，不做 resolve，
        确保任何包含目录穿越的路径都能被检测到。

        :param file_path: 文件路径
        :raises ValueError: 存在路径穿越时抛出
        """
        p = str(file_path).replace("\\", "/")
        parts = p.split("/")
        depth = 0
        for part in parts:
            if part == "..":
                depth -= 1
                if depth < 0:
                    raise ValueError(f"路径穿越攻击检测: [{file_path}]")
            elif part and part != ".":
                depth += 1

    @staticmethod
    def checksum(
        path: Union[str, Path],
        algorithm: str = "md5",
    ) -> str:
        """
        计算文件的校验和。

        :param path: 文件路径
        :param algorithm: 哈希算法（"md5"、"sha1"、"sha256" 等）
        :return: 校验和的十六进制字符串
        """
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(f"文件不存在: {p}")
        h = hashlib.new(algorithm)
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def checksum_crc32(path: Union[str, Path]) -> int:
        """
        计算文件的 CRC32 校验值。

        :param path: 文件路径
        :return: CRC32 校验值（有符号整数）
        """
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(f"文件不存在: {p}")
        crc = 0
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                crc = binascii.crc32(chunk, crc)
        return crc

    # ================================================================== #
    #  清理操作
    # ================================================================== #

    @staticmethod
    def clean_empty(path: Union[str, Path]) -> int:
        """
        清理目录下的空文件和空目录。

        :param path: 根目录路径
        :return: 清理的项目数
        """
        p = Path(path)
        count = 0
        if not p.is_dir():
            return count
        # 先清理空文件
        for child in p.rglob("*"):
            if child.is_file() and child.stat().st_size == 0:
                child.unlink()
                count += 1
        # 再清理空目录（从深到浅）
        for child in sorted(p.rglob("*"), reverse=True):
            if child.is_dir() and not any(child.iterdir()):
                child.rmdir()
                count += 1
        return count

    @staticmethod
    def clean_invalid(path: Union[str, Path]) -> int:
        """
        清理目录下文件名含无效字符的文件。

        :param path: 根目录路径
        :return: 清理的文件数
        """
        p = Path(path)
        count = 0
        if not p.is_dir():
            return count
        for child in p.rglob("*"):
            if child.is_file() and FileUtil.contains_invalid(child.name):
                child.unlink()
                count += 1
        return count

    @staticmethod
    def contains_invalid(name: str) -> bool:
        """
        判断文件名是否包含无效字符。

        :param name: 文件名
        :return: 是否包含无效字符
        """
        # Windows 不允许的字符
        invalid_chars = set('<>:"/\\|?*\x00-\x1f')
        return any(c in invalid_chars for c in name)

    @staticmethod
    def tail(
        path: Union[str, Path],
        lines: int = 10,
        charset: str = "utf-8",
        handler: Optional[Callable[[str], None]] = None,
    ) -> List[str]:
        """
        读取文件最后 N 行。

        使用反向读取实现，不会将整个文件加载到内存。

        :param path: 文件路径
        :param lines: 返回的行数，默认 10
        :param charset: 字符编码，默认 "utf-8"
        :param handler: 行处理器回调函数（每行调用一次），可选
        :return: 最后 N 行的列表（不含行尾换行符）
        """
        if not Path(path).is_file():
            raise FileNotFoundError(f"文件不存在: {path}")
        result: List[str] = []
        with open(path, "rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            if file_size == 0:
                return []
            buffer = b""
            pos = file_size
            while pos > 0 and len(result) < lines + 1:
                read_size = min(8192, pos)
                pos -= read_size
                f.seek(pos)
                chunk = f.read(read_size)
                buffer = chunk + buffer
                result = buffer.decode(charset, errors="replace").splitlines()
        result = result[-lines:] if len(result) >= lines else result
        if handler is not None:
            for line in result:
                handler(line)
        return result
