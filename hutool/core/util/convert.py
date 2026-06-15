"""
类型转换工具类

对应 PyHutool Convert.py 的核心功能。
提供 bytes↔int、通用类型转换等常用类型转换方法。
"""

from typing import Any


class ConvertUtil:
    """类型转换工具类。

    提供 ``bytes_to_int``、``int_to_bytes``、``to_str``、``convert`` 等
    常用类型转换方法。
    """

    @staticmethod
    def bytes_to_int(data: bytes) -> int:
        """
        将 bytes 按大端序转换为 int。

        :param data: 字节数据
        :return: 转换后的整数

        ::

            >>> ConvertUtil.bytes_to_int(b'\\x00\\x00\\x01\\x00')
            256
            >>> ConvertUtil.bytes_to_int(b'\\xff')
            255
        """
        return int.from_bytes(data, byteorder="big", signed=False)

    @staticmethod
    def int_to_bytes(value: int, length: int = 4) -> bytes:
        """
        将 int 按大端序转换为指定长度的 bytes。

        :param value: 整数值（非负）
        :param length: 输出 bytes 的长度（字节数），默认 4
        :return: 字节数据
        :raises ValueError: value 为负数时

        ::

            >>> ConvertUtil.int_to_bytes(256, 2)
            b'\\x01\\x00'
            >>> ConvertUtil.int_to_bytes(0, 1)
            b'\\x00'
        """
        if value < 0:
            raise ValueError("value 必须为非负整数")
        return value.to_bytes(length, byteorder="big", signed=False)

    @staticmethod
    def to_str(value: Any, encoding: str = "utf-8") -> str:
        """
        安全地将值转换为字符串。

        ``bytes``/``bytearray`` 类型使用 *encoding* 解码，其他类型使用 ``str()`` 转换。

        :param value: 待转换的值
        :param encoding: 字节解码编码，默认 ``"utf-8"``
        :return: 字符串

        ::

            >>> ConvertUtil.to_str(b'hello')
            'hello'
            >>> ConvertUtil.to_str(123)
            '123'
            >>> ConvertUtil.to_str(None)
            ''
        """
        if value is None:
            return ""
        if isinstance(value, (bytes, bytearray)):
            return value.decode(encoding)
        return str(value)

    @staticmethod
    def convert(value: Any, target_type: type) -> Any:
        """
        将值转换为指定类型。

        支持常见类型：``int``、``float``、``str``、``bool``、``list``、``tuple``、``set``。
        ``None`` 输入返回 ``target_type()`` 的默认值。

        :param value: 待转换的值
        :param target_type: 目标类型
        :return: 转换后的值
        :raises ValueError: 无法转换时

        ::

            >>> ConvertUtil.convert('123', int)
            123
            >>> ConvertUtil.convert(3.14, str)
            '3.14'
            >>> ConvertUtil.convert(None, str)
            ''
        """
        if value is None:
            if target_type in (int, float):
                return target_type(0)
            return target_type()
        if isinstance(value, target_type):
            return value
        return target_type(value)
