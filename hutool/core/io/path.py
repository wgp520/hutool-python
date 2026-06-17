"""路径工具模块"""

import mimetypes
import os
import shutil
import tempfile
from pathlib import Path
from typing import Callable, Generator, List, Optional, Union


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

    @staticmethod
    def copy_content(
        src_path: Union[str, Path],
        dest_path: Union[str, Path],
        is_override: bool = True,
    ) -> Path:
        """复制路径内容

        本方法是 :meth:`copy` 的别名。

        :param src_path: 源路径
        :param dest_path: 目标路径
        :param is_override: 是否覆盖已存在的目标，默认 True
        :return: 目标路径的 Path 对象
        :raises FileExistsError: 目标已存在且 is_override 为 False 时抛出
        :raises FileNotFoundError: 源路径不存在时抛出
        """
        return PathUtil.copy(src_path, dest_path, is_override)

    @staticmethod
    def copy_file(src_path: Union[str, Path], dest_path: Union[str, Path]) -> Path:
        """复制文件

        仅用于复制文件，若源路径为目录则抛出异常。

        :param src_path: 源文件路径
        :param dest_path: 目标文件路径
        :return: 目标路径的 Path 对象
        :raises FileNotFoundError: 源文件不存在时抛出
        :raises IsADirectoryError: 源路径为目录时抛出
        """
        src_p = Path(src_path)
        dest_p = Path(dest_path)
        if not src_p.exists():
            raise FileNotFoundError(f"源路径不存在: {src_path}")
        if src_p.is_dir():
            raise IsADirectoryError(f"源路径是目录而非文件: {src_path}")
        dest_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_p, dest_p)
        return dest_p

    @staticmethod
    def create_temp_file(
        prefix: str = "hutool",
        suffix: str = ".tmp",
        dir_path: Optional[Union[str, Path]] = None,
    ) -> Path:
        """创建临时文件

        :param prefix: 文件名前缀，默认 'hutool'
        :param suffix: 文件名后缀，默认 '.tmp'
        :param dir_path: 临时文件所在目录，None 表示使用系统临时目录
        :return: 创建的临时文件 Path 对象
        """
        dir_str = str(dir_path) if dir_path is not None else None
        fd, tmp_path = tempfile.mkstemp(prefix=prefix, suffix=suffix, dir=dir_str)
        os.close(fd)
        return Path(tmp_path)

    @staticmethod
    def get_last_path_ele(path: Union[str, Path]) -> str:
        """获取路径的最后一个元素

        本方法是 :meth:`get_name` 的别名。

        :param path: 文件或目录路径
        :return: 路径最后一级的名称
        """
        return PathUtil.get_name(path)

    @staticmethod
    def get_path_ele(path: Union[str, Path], index: int) -> str:
        """按索引获取路径元素

        索引从 0 开始，支持负数索引（-1 表示最后一个元素）。

        :param path: 文件或目录路径
        :param index: 元素索引，支持负数
        :return: 指定索引处的路径元素
        :raises IndexError: 索引越界时抛出
        """
        parts = Path(path).parts
        try:
            return parts[index]
        except IndexError:
            raise IndexError(f"路径索引 {index} 越界，路径共 {len(parts)} 层: {path}")

    @staticmethod
    def get_mime_type(path: Union[str, Path]) -> Optional[str]:
        """获取文件的 MIME 类型

        根据文件扩展名猜测 MIME 类型。

        :param path: 文件路径
        :return: MIME 类型字符串，无法识别时返回 None
        """
        mime_type, _ = mimetypes.guess_type(str(path))
        return mime_type

    @staticmethod
    def is_dir_empty(dir_path: Union[str, Path]) -> bool:
        """判断目录是否为空

        :param dir_path: 目录路径
        :return: 目录为空或不存在返回 True
        """
        p = Path(dir_path)
        if not p.is_dir():
            return True
        return not any(p.iterdir())

    @staticmethod
    def is_directory(path: Union[str, Path]) -> bool:
        """判断路径是否为目录

        本方法是 ``Path.is_dir()`` 的别名。

        :param path: 文件或目录路径
        :return: 是目录返回 True
        """
        return Path(path).is_dir()

    @staticmethod
    def is_exists_and_not_directory(path: Union[str, Path]) -> bool:
        """判断路径是否存在且不是目录

        :param path: 文件路径
        :return: 路径存在且不是目录返回 True
        """
        p = Path(path)
        return p.exists() and not p.is_dir()

    @staticmethod
    def is_file(path: Union[str, Path]) -> bool:
        """判断路径是否为文件

        本方法是 ``Path.is_file()`` 的别名。

        :param path: 文件路径
        :return: 是文件返回 True
        """
        return Path(path).is_file()

    @staticmethod
    def is_sub(parent: Union[str, Path], child: Union[str, Path]) -> bool:
        """判断 child 是否为 parent 的子路径

        :param parent: 父路径
        :param child: 子路径
        :return: child 是 parent 的子路径返回 True
        """
        parent_p = Path(parent).resolve()
        child_p = Path(child).resolve()
        try:
            child_p.relative_to(parent_p)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_symlink(path: Union[str, Path]) -> bool:
        """判断路径是否为符号链接

        :param path: 文件或目录路径
        :return: 是符号链接返回 True
        """
        return Path(path).is_symlink()

    @staticmethod
    def move_content(src_path: Union[str, Path], dest_path: Union[str, Path]) -> Path:
        """移动路径内容

        本方法是 :meth:`move` 的别名，使用默认参数（覆盖已存在的目标）。

        :param src_path: 源路径
        :param dest_path: 目标路径
        :return: 目标路径的 Path 对象
        :raises FileNotFoundError: 源路径不存在时抛出
        """
        return PathUtil.move(src_path, dest_path, is_override=True)

    @staticmethod
    def rename_path(path: Union[str, Path], new_name: str) -> Path:
        """重命名路径的最后一级名称

        :param path: 原始路径
        :param new_name: 新名称（仅最后一级）
        :return: 重命名后的 Path 对象
        :raises FileNotFoundError: 路径不存在时抛出
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"路径不存在: {path}")
        new_path = p.parent / new_name
        p.rename(new_path)
        return new_path

    @staticmethod
    def to_abs_normal(path: Union[str, Path]) -> str:
        """将路径转换为绝对路径并标准化

        先转为绝对路径，再去除冗余分隔符和上级引用。

        :param path: 原始路径
        :return: 绝对标准化路径字符串
        """
        return str(Path(path).resolve())

    @staticmethod
    def walk_files(
        dir_path: Union[str, Path],
        func: Optional[Callable[[Path], None]] = None,
    ) -> Generator[Path, None, None]:
        """遍历目录下的所有文件

        返回一个生成器，逐个产出目录中的文件。若提供回调函数，则对每个文件执行回调。

        :param dir_path: 目录路径
        :param func: 可选的回调函数，接受 Path 参数
        :return: 文件 Path 生成器
        :raises FileNotFoundError: 路径不存在时抛出
        """
        p = Path(dir_path)
        if not p.exists():
            raise FileNotFoundError(f"路径不存在: {dir_path}")
        if p.is_file():
            if func is not None:
                func(p)
            yield p
        else:
            for f in sorted(p.rglob("*")):
                if f.is_file():
                    if func is not None:
                        func(f)
                    yield f
