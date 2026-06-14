"""
文件工具类，对应 Java cn.hutool.core.io.FileUtil

基于 pathlib.Path 实现，辅以 os 和 shutil。
"""

import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Optional, Union


class FileUtil:
    """文件工具类，对应 Java cn.hutool.core.io.FileUtil"""

    FILE_SEPARATOR: str = os.sep

    # ------------------------------------------------------------------
    # 判断
    # ------------------------------------------------------------------

    @staticmethod
    def is_windows() -> bool:
        """判断当前操作系统是否为 Windows"""
        return os.name == "nt"

    @staticmethod
    def exist(path: Union[str, Path]) -> bool:
        """判断文件或目录是否存在"""
        return Path(path).exists()

    @staticmethod
    def is_dir(path: Union[str, Path]) -> bool:
        """判断是否为目录"""
        return Path(path).is_dir()

    @staticmethod
    def is_file(path: Union[str, Path]) -> bool:
        """判断是否为文件"""
        return Path(path).is_file()

    @staticmethod
    def is_absolute(path: Union[str, Path]) -> bool:
        """判断路径是否为绝对路径"""
        return Path(path).is_absolute()

    @staticmethod
    def is_empty(path: Union[str, Path]) -> bool:
        """文件或目录是否为空

        - 文件：大小为 0 视为空。
        - 目录：不含任何子项视为空。
        - 路径不存在视为空。
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
        """根据多个名称段构建文件路径

        例如: FileUtil.file("home", "user", "test.txt")
        """
        if not names:
            raise ValueError("至少需要一个路径段")
        result = Path(names[0])
        for name in names[1:]:
            result = result / name
        return result

    @staticmethod
    def touch(path: Union[str, Path]) -> Path:
        """创建文件（包括父目录）

        如果文件已存在则只更新访问/修改时间。
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        return p

    @staticmethod
    def mkdir(path: Union[str, Path]) -> Path:
        """创建目录

        如果目录已存在则直接返回。
        """
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @staticmethod
    def mkdirs(path: Union[str, Path]) -> Path:
        """创建多级目录（与 mkdir 行为一致，支持多级创建）"""
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
        """复制文件

        如果目标目录不存在则自动创建。
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
        """读取文件内容为字节数组"""
        return Path(path).read_bytes()

    @staticmethod
    def read_lines(path: Union[str, Path], charset: str = "utf-8") -> List[str]:
        """读取文件内容为字符串列表（每行一个元素，保留换行符）"""
        with open(path, encoding=charset) as f:
            return f.readlines()

    @staticmethod
    def read_utf8_lines(path: Union[str, Path]) -> List[str]:
        """以 UTF-8 编码读取文件的每一行（去除行尾换行符）"""
        return FileUtil.read_lines_str(path, charset="utf-8")

    @staticmethod
    def read_lines_str(path: Union[str, Path], charset: str = "utf-8") -> List[str]:
        """读取文件的每一行，去除行尾换行符"""
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
        """递归遍历文件并对每个文件执行操作

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
        """获取文件大小（字节）

        对于目录，返回整个目录树的总大小。
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
        """获取文件总行数"""
        count = 0
        with open(path, "rb") as f:
            for _ in f:
                count += 1
        return count

    @staticmethod
    def get_name(path: Union[str, Path]) -> str:
        """获取文件名（含扩展名）

        例如: /home/user/test.txt -> test.txt
        """
        return Path(path).name

    @staticmethod
    def get_suffix(path: Union[str, Path]) -> str:
        """获取文件扩展名（不带点号）

        例如: /home/user/test.txt -> txt

        如果没有扩展名则返回空字符串。
        """
        name = Path(path).name
        dot_index = name.rfind(".")
        if dot_index <= 0:
            return ""
        return name[dot_index + 1 :]

    @staticmethod
    def get_prefix(path: Union[str, Path]) -> str:
        """获取文件名前缀（不含扩展名）

        例如: /home/user/test.txt -> test
        """
        name = Path(path).name
        dot_index = name.rfind(".")
        if dot_index <= 0:
            return name
        return name[:dot_index]

    @staticmethod
    def main_name(path: Union[str, Path]) -> str:
        """获取主文件名（同 get_prefix）"""
        return FileUtil.get_prefix(path)

    @staticmethod
    def normalize(path: Union[str, Path]) -> str:
        """标准化路径，解析 ~ 和相对路径符号

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
        """获取系统临时目录路径（字符串）"""
        return tempfile.gettempdir()

    @staticmethod
    def get_tmp_dir() -> Path:
        """获取系统临时目录（Path 对象）"""
        return Path(tempfile.gettempdir())

    @staticmethod
    def get_user_home_path() -> str:
        """获取用户主目录路径（字符串）"""
        return str(Path.home())

    @staticmethod
    def get_user_home_dir() -> Path:
        """获取用户主目录（Path 对象）"""
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
        """判断是否为符号链接"""
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
