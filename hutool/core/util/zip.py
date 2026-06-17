import gzip
import io
import os
import zipfile
import zlib
from typing import List, Optional


class ZipUtil:
    """压缩工具类"""

    @staticmethod
    def zip(src_path: str, dest_path: Optional[str] = None, charset: str = "utf-8") -> str:
        """压缩文件或目录为zip

        :param src_path: 源文件或目录路径
        :param dest_path: 目标zip文件路径，默认为源路径加.zip后缀
        :param charset: 文件名编码字符集，默认utf-8
        :return: 生成的zip文件路径
        """
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"源路径不存在: {src_path}")

        if dest_path is None:
            dest_path = src_path + ".zip"

        dest_path = os.path.abspath(dest_path)
        src_path = os.path.abspath(src_path)

        with zipfile.ZipFile(dest_path, "w", zipfile.ZIP_DEFLATED) as zf:
            if os.path.isfile(src_path):
                zf.write(src_path, os.path.basename(src_path))
            elif os.path.isdir(src_path):
                base_dir = os.path.basename(src_path)
                for root, dirs, files in os.walk(src_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.join(base_dir, os.path.relpath(file_path, src_path))
                        zf.write(file_path, arcname)
            else:
                raise ValueError(f"不支持的路径类型: {src_path}")

        return dest_path

    @staticmethod
    def unzip(zip_file: str, dest_path: str, charset: str = "utf-8") -> str:
        """解压zip文件

        :param zip_file: zip文件路径
        :param dest_path: 解压目标目录
        :param charset: 文件名编码字符集，默认utf-8
        :return: 解压目标目录路径
        """
        if not os.path.exists(zip_file):
            raise FileNotFoundError(f"zip文件不存在: {zip_file}")

        dest_path = os.path.abspath(dest_path)
        os.makedirs(dest_path, exist_ok=True)

        with zipfile.ZipFile(zip_file, "r") as zf:
            for info in zf.infolist():
                # 尝试用指定编码解码文件名
                try:
                    filename = info.filename.encode("cp437").decode(charset)
                except (UnicodeDecodeError, UnicodeEncodeError):
                    filename = info.filename
                info.filename = filename
                zf.extract(info, dest_path)

        return dest_path

    @staticmethod
    def gzip(data: bytes) -> bytes:
        """Gzip压缩

        :param data: 待压缩的字节数据
        :return: 压缩后的字节数据
        """
        return gzip.compress(data)

    @staticmethod
    def gzip_str(data: str, charset: str = "utf-8") -> bytes:
        """字符串Gzip压缩

        :param data: 待压缩的字符串
        :param charset: 字符编码，默认utf-8
        :return: 压缩后的字节数据
        """
        return gzip.compress(data.encode(charset))

    @staticmethod
    def ungzip(data: bytes) -> bytes:
        """Gzip解压

        :param data: 待解压的字节数据
        :return: 解压后的字节数据
        """
        return gzip.decompress(data)

    @staticmethod
    def ungzip_str(data: bytes, charset: str = "utf-8") -> str:
        """Gzip解压为字符串

        :param data: 待解压的字节数据
        :param charset: 字符编码，默认utf-8
        :return: 解压后的字符串
        """
        return gzip.decompress(data).decode(charset)

    @staticmethod
    def zlib_compress(data: bytes, level: int = -1) -> bytes:
        """Zlib压缩

        :param data: 待压缩的字节数据
        :param level: 压缩级别，-1为默认，0为不压缩，1-9为压缩级别（1最快，9最小）
        :return: 压缩后的字节数据
        """
        return zlib.compress(data, level)

    @staticmethod
    def zlib_uncompress(data: bytes) -> bytes:
        """Zlib解压

        :param data: 待解压的字节数据
        :return: 解压后的字节数据
        """
        return zlib.decompress(data)

    @staticmethod
    def zip_to_stream(src_path: str) -> bytes:
        """将文件或目录压缩为 zip 格式的字节流。

        :param src_path: 源文件或目录路径
        :return: zip 格式字节数据
        """
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            if os.path.isfile(src_path):
                zf.write(src_path, os.path.basename(src_path))
            elif os.path.isdir(src_path):
                base_dir = os.path.basename(src_path)
                for root, dirs, files in os.walk(src_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.join(base_dir, os.path.relpath(file_path, src_path))
                        zf.write(file_path, arcname)
            else:
                raise ValueError(f"不支持的路径类型: {src_path}")
        return buf.getvalue()

    @staticmethod
    def zip_entries(src_path: str, dest_path: str) -> List[str]:
        """将文件或目录压缩为 zip 并返回压缩的文件名列表。

        :param src_path: 源文件或目录路径
        :param dest_path: 目标 zip 文件路径
        :return: 压缩的文件名列表
        """
        entries: List[str] = []
        dest_path = os.path.abspath(dest_path)
        src_path = os.path.abspath(src_path)
        with zipfile.ZipFile(dest_path, "w", zipfile.ZIP_DEFLATED) as zf:
            if os.path.isfile(src_path):
                name = os.path.basename(src_path)
                zf.write(src_path, name)
                entries.append(name)
            elif os.path.isdir(src_path):
                base_dir = os.path.basename(src_path)
                for root, dirs, files in os.walk(src_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.join(base_dir, os.path.relpath(file_path, src_path))
                        zf.write(file_path, arcname)
                        entries.append(arcname)
        return entries

    @staticmethod
    def append(zip_file: str, file_path: str, arcname: Optional[str] = None) -> str:
        """向已有 zip 文件追加文件。

        :param zip_file: 已有 zip 文件路径
        :param file_path: 要追加的文件路径
        :param arcname: zip 内的文件名，默认使用原文件名
        :return: zip 文件路径
        """
        if arcname is None:
            arcname = os.path.basename(file_path)
        with zipfile.ZipFile(zip_file, "a", zipfile.ZIP_DEFLATED) as zf:
            zf.write(file_path, arcname)
        return zip_file

    @staticmethod
    def unzip_stream(zip_data: bytes, dest_path: str) -> str:
        """将 zip 字节流解压到指定目录。

        :param zip_data: zip 格式的字节数据
        :param dest_path: 解压目标目录
        :return: 解压目录路径
        """
        dest_path = os.path.abspath(dest_path)
        os.makedirs(dest_path, exist_ok=True)
        buf = io.BytesIO(zip_data)
        with zipfile.ZipFile(buf, "r") as zf:
            zf.extractall(dest_path)
        return dest_path

    @staticmethod
    def get(zip_file: str, entry_name: str) -> Optional[zipfile.ZipInfo]:
        """从 zip 文件中获取指定条目的信息。

        :param zip_file: zip 文件路径
        :param entry_name: 条目名称
        :return: ZipInfo 对象，未找到返回 None
        """
        with zipfile.ZipFile(zip_file, "r") as zf:
            for info in zf.infolist():
                if info.filename == entry_name:
                    return info
        return None

    @staticmethod
    def read(zip_file: str, entry_name: str) -> bytes:
        """从 zip 文件中读取指定条目的内容。

        :param zip_file: zip 文件路径
        :param entry_name: 条目名称
        :return: 条目内容字节数据
        :raises KeyError: 条目不存在时
        """
        with zipfile.ZipFile(zip_file, "r") as zf:
            return zf.read(entry_name)

    @staticmethod
    def unzip_file_bytes(zip_file: str, entry_name: str) -> bytes:
        """从 zip 文件中读取指定条目的字节数据（同 read）。

        :param zip_file: zip 文件路径
        :param entry_name: 条目名称
        :return: 条目内容字节数据
        """
        return ZipUtil.read(zip_file, entry_name)

    @staticmethod
    def list_file_names(zip_file: str) -> List[str]:
        """列出 zip 文件中的所有文件名。

        :param zip_file: zip 文件路径
        :return: 文件名列表
        """
        with zipfile.ZipFile(zip_file, "r") as zf:
            return zf.namelist()

    @staticmethod
    def to_zip_file(src_path: str, dest_path: Optional[str] = None) -> str:
        """将文件或目录转换为 zip 文件。

        与 ``zip`` 方法类似，但默认目标路径为源路径加 ``.zip`` 后缀。

        :param src_path: 源文件或目录路径
        :param dest_path: 目标 zip 文件路径，默认为源路径加 .zip 后缀
        :return: 生成的 zip 文件路径
        :rtype: str
        """
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"源路径不存在: {src_path}")

        if dest_path is None:
            dest_path = src_path + ".zip"

        dest_path = os.path.abspath(dest_path)
        src_path = os.path.abspath(src_path)

        with zipfile.ZipFile(dest_path, "w", zipfile.ZIP_DEFLATED) as zf:
            if os.path.isfile(src_path):
                zf.write(src_path, os.path.basename(src_path))
            elif os.path.isdir(src_path):
                for root, dirs, files in os.walk(src_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, src_path)
                        zf.write(file_path, arcname)
            else:
                raise ValueError(f"不支持的路径类型: {src_path}")

        return dest_path

    @staticmethod
    def get_zip_output_stream(file_path: str) -> zipfile.ZipFile:
        """获取 zip 写入流

        返回一个可写入的 ``ZipFile`` 对象，调用者负责关闭。

        :param file_path: zip 文件路径
        :return: 可写入的 ZipFile 对象
        :rtype: zipfile.ZipFile
        """
        return zipfile.ZipFile(file_path, "w", zipfile.ZIP_DEFLATED)

    @staticmethod
    def get_zip_stream(file_path: str) -> zipfile.ZipFile:
        """获取 zip 读取流

        返回一个可读取的 ``ZipFile`` 对象，调用者负责关闭。

        :param file_path: zip 文件路径
        :return: 可读取的 ZipFile 对象
        :rtype: zipfile.ZipFile
        """
        return zipfile.ZipFile(file_path, "r")
