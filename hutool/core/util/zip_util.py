import gzip
import os
import zipfile
import zlib
from typing import Optional


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
