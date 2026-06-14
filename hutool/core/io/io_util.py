"""IO工具模块"""

from typing import IO, List, Optional, Union


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
