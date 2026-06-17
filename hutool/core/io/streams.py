"""IO工具模块"""

import binascii
import hashlib
import io
import zlib
from typing import IO, Iterator, List, Optional, Union


class IoUtil:
    """IO工具类"""

    @staticmethod
    def read(stream: IO, charset: str = "utf-8") -> str:
        """从流中读取字符串

        :param stream: 输入流（需支持 read 方法）
        :param charset: 字符编码，默认 utf-8
        :return: 读取到的字符串内容
        """
        raw = stream.read()
        if isinstance(raw, bytes):
            return raw.decode(charset)
        return raw

    @staticmethod
    def read_bytes(stream: IO) -> bytes:
        """从流中读取字节数组

        :param stream: 输入流（需支持 read 方法）
        :return: 读取到的字节数组
        """
        data = stream.read()
        if isinstance(data, str):
            return data.encode("utf-8")
        return data

    @staticmethod
    def read_lines(stream: IO, charset: str = "utf-8") -> List[str]:
        """从流中读取行列表

        :param stream: 输入流（需支持 read 或 readlines 方法）
        :param charset: 字符编码，默认 utf-8
        :return: 行列表
        """
        raw = stream.read()
        if isinstance(raw, bytes):
            raw = raw.decode(charset)
        return raw.splitlines(keepends=False)

    @staticmethod
    def write(stream: IO, data: Union[str, bytes], charset: str = "utf-8") -> int:
        """写入数据到流

        :param stream: 输出流（需支持 write 方法）
        :param data: 要写入的数据（str 或 bytes）
        :param charset: 当 data 为 str 时使用的编码，默认 utf-8
        :return: 写入的字节数
        """
        if isinstance(data, str):
            encoded = data.encode(charset)
        elif isinstance(data, (bytes, bytearray)):
            encoded = bytes(data)
        else:
            encoded = str(data).encode(charset)
        return stream.write(encoded)

    @staticmethod
    def write_bytes(stream: IO, data: bytes) -> int:
        """写入字节数组到流

        :param stream: 输出流（需支持 write 方法）
        :param data: 要写入的字节数组
        :return: 写入的字节数
        """
        if isinstance(data, bytearray):
            data = bytes(data)
        return stream.write(data)

    @staticmethod
    def copy(
        input_stream: IO,
        output_stream: IO,
        buffer_size: int = 8192,
    ) -> int:
        """拷贝流数据

        :param input_stream: 输入流
        :param output_stream: 输出流
        :param buffer_size: 缓冲区大小，默认 8192 字节
        :return: 拷贝的总字节数
        """
        total = 0
        while True:
            chunk = input_stream.read(buffer_size)
            if not chunk:
                break
            if isinstance(chunk, str):
                chunk = chunk.encode("utf-8")
            output_stream.write(chunk)
            total += len(chunk)
        return total

    @staticmethod
    def close(closable: Optional[IO]) -> None:
        """安全关闭可关闭对象

        如果对象为 None 或已关闭，则不做任何操作。

        :param closable: 可关闭对象（如文件流），可以为 None
        """
        if closable is None:
            return
        try:
            closable.close()
        except Exception:
            pass

    @staticmethod
    def to_bytes(obj: Union[str, bytes, bytearray, memoryview]) -> bytes:
        """将对象转为 bytes

        支持 str / bytes / bytearray / memoryview 类型。

        :param obj: 待转换的对象
        :return: 字节数组
        :raises TypeError: 不支持的对象类型
        """
        if isinstance(obj, bytes):
            return obj
        if isinstance(obj, str):
            return obj.encode("utf-8")
        if isinstance(obj, bytearray):
            return bytes(obj)
        if isinstance(obj, memoryview):
            return obj.tobytes()
        raise TypeError(f"不支持的对象类型: {type(obj).__name__}")

    # ------------------------------------------------------------------
    # 校验 / 比较
    # ------------------------------------------------------------------

    @staticmethod
    def checksum(stream: IO, algorithm: str = "md5") -> str:
        """计算流内容的校验和（十六进制字符串）

        :param stream: 输入流（需支持 read 方法）
        :param algorithm: 哈希算法名称，默认 md5；支持 sha1、sha256 等
        :return: 校验和的十六进制字符串
        """
        h = hashlib.new(algorithm)
        data = stream.read()
        if isinstance(data, str):
            data = data.encode("utf-8")
        h.update(data)
        return h.hexdigest()

    @staticmethod
    def checksum_crc32(stream: IO) -> int:
        """计算流内容的 CRC32 校验和

        :param stream: 输入流（需支持 read 方法）
        :return: CRC32 校验和（无符号 32 位整数）
        """
        data = stream.read()
        if isinstance(data, str):
            data = data.encode("utf-8")
        return zlib.crc32(data) & 0xFFFFFFFF

    @staticmethod
    def checksum_value(stream: IO, algorithm: str = "md5") -> int:
        """计算流内容的校验和（整数形式）

        :param stream: 输入流（需支持 read 方法）
        :param algorithm: 哈希算法名称，默认 md5
        :return: 校验和对应的整数值
        """
        h = hashlib.new(algorithm)
        data = stream.read()
        if isinstance(data, str):
            data = data.encode("utf-8")
        h.update(data)
        return int(h.hexdigest(), 16)

    @staticmethod
    def content_equals(stream1: IO, stream2: IO) -> bool:
        """比较两个流的内容是否完全相同

        :param stream1: 第一个输入流
        :param stream2: 第二个输入流
        :return: 内容相同返回 True，否则返回 False
        """
        buf_size = 8192
        while True:
            b1 = stream1.read(buf_size)
            b2 = stream2.read(buf_size)
            if isinstance(b1, str):
                b1 = b1.encode("utf-8")
            if isinstance(b2, str):
                b2 = b2.encode("utf-8")
            if b1 != b2:
                return False
            if not b1:
                return True

    @staticmethod
    def content_equals_ignore_eol(stream1: IO, stream2: IO) -> bool:
        """比较两个流的内容是否相同（忽略行结束符差异）

        将 \\r\\n 和 \\r 统一转为 \\n 后再进行比较。

        :param stream1: 第一个输入流
        :param stream2: 第二个输入流
        :return: 忽略行结束符后内容相同返回 True，否则返回 False
        """

        def _normalized_lines(s: IO) -> List[str]:
            data = s.read()
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            data = data.replace("\r\n", "\n").replace("\r", "\n")
            return data.split("\n")

        return _normalized_lines(stream1) == _normalized_lines(stream2)

    # ------------------------------------------------------------------
    # 流操作
    # ------------------------------------------------------------------

    @staticmethod
    def flush(output_stream: IO) -> None:
        """刷新输出流

        如果流对象没有 flush 方法则不做任何操作。

        :param output_stream: 输出流
        """
        fn = getattr(output_stream, "flush", None)
        if callable(fn):
            fn()

    @staticmethod
    def line_iter(stream: IO, charset: str = "utf-8") -> Iterator[str]:
        """逐行迭代流内容

        :param stream: 输入流（需支持 read 方法）
        :param charset: 字符编码，默认 utf-8
        :return: 行内容的迭代器（不含换行符）
        """
        data = stream.read()
        if isinstance(data, bytes):
            data = data.decode(charset)
        yield from data.splitlines()

    # ------------------------------------------------------------------
    # 读取
    # ------------------------------------------------------------------

    @staticmethod
    def read_hex(stream: IO, separator: str = "") -> str:
        """以十六进制字符串形式读取流内容

        :param stream: 输入流（需支持 read 方法）
        :param separator: 每个字节之间的分隔符，默认为空
        :return: 十六进制字符串
        """
        data = stream.read()
        if isinstance(data, str):
            data = data.encode("utf-8")
        hex_str = binascii.hexlify(data).decode("ascii")
        if separator:
            hex_str = separator.join(hex_str[i : i + 2] for i in range(0, len(hex_str), 2))
        return hex_str

    @staticmethod
    def read_utf8(stream: IO) -> str:
        """以 UTF-8 编码读取流内容

        :param stream: 输入流（需支持 read 方法）
        :return: UTF-8 解码后的字符串
        """
        return IoUtil.read(stream, charset="utf-8")

    @staticmethod
    def read_utf8_lines(stream: IO) -> List[str]:
        """以 UTF-8 编码读取流的行列表

        :param stream: 输入流（需支持 read 方法）
        :return: 行列表
        """
        return IoUtil.read_lines(stream, charset="utf-8")

    # ------------------------------------------------------------------
    # 转换
    # ------------------------------------------------------------------

    @staticmethod
    def to_str(stream: IO, charset: str = "utf-8") -> str:
        """将流内容转为字符串

        :param stream: 输入流（需支持 read 方法）
        :param charset: 字符编码，默认 utf-8
        :return: 解码后的字符串
        """
        return IoUtil.read(stream, charset=charset)

    @staticmethod
    def to_stream(s: str, charset: str = "utf-8") -> IO:
        """将字符串转为 BytesIO 流

        :param s: 待转换的字符串
        :param charset: 编码方式，默认 utf-8
        :return: 包含编码后数据的 BytesIO 对象
        """
        return io.BytesIO(s.encode(charset))

    @staticmethod
    def to_utf8_stream(s: str) -> IO:
        """将字符串转为 UTF-8 编码的 BytesIO 流

        :param s: 待转换的字符串
        :return: 包含 UTF-8 编码数据的 BytesIO 对象
        """
        return IoUtil.to_stream(s, charset="utf-8")

    # ------------------------------------------------------------------
    # 写入
    # ------------------------------------------------------------------

    @staticmethod
    def write_utf8(output_stream: IO, data: str) -> int:
        """以 UTF-8 编码写入字符串到流

        :param output_stream: 输出流（需支持 write 方法）
        :param data: 要写入的字符串
        :return: 写入的字节数
        """
        encoded = data.encode("utf-8")
        return output_stream.write(encoded)
