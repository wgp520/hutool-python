"""数学工具类，提供精确运算、坐标转换、位运算状态管理等功能"""

import math
from decimal import Decimal
from typing import Union

__all__ = ("BitStatusUtil", "MathUtil")


class MathUtil:
    """数学工具类，提供精确数学运算和坐标转换功能"""

    @staticmethod
    def add(value1: Union[int, float, str, Decimal], value2: Union[int, float, str, Decimal]) -> Decimal:
        """
        精确加法，使用Decimal避免浮点精度问题

        :param value1: 加数1
        :param value2: 加数2
        :return: 精确的加法结果
        """
        d1 = Decimal(str(value1))
        d2 = Decimal(str(value2))
        return d1 + d2

    @staticmethod
    def point_to_radians(point: tuple) -> float:
        """
        坐标点转弧度，根据(x, y)坐标计算对应的弧度值

        :param point: 坐标点(x, y)
        :return: 弧度值
        """
        if point is None or len(point) < 2:
            raise ValueError("坐标点必须包含x和y两个分量")
        x, y = float(point[0]), float(point[1])
        return math.atan2(y, x)

    @staticmethod
    def radians_to_point(radians: float) -> tuple:
        """
        弧度转坐标点，根据弧度计算单位圆上的(x, y)坐标

        :param radians: 弧度值
        :return: 坐标点(x, y)
        """
        x = math.cos(radians)
        y = math.sin(radians)
        return (x, y)


class BitStatusUtil:
    """位运算状态工具类，使用位运算管理多状态组合"""

    @staticmethod
    def add(status: int, *values: int) -> int:
        """
        添加状态位，将一个或多个状态值添加到当前状态中

        :param status: 当前状态值
        :param values: 要添加的一个或多个状态值
        :return: 添加后的状态值
        """
        for value in values:
            status |= value
        return status

    @staticmethod
    def has(status: int, value: int) -> bool:
        """
        是否包含指定状态

        :param status: 当前状态值
        :param value: 要检测的状态值
        :return: 是否包含该状态
        """
        return (status & value) == value

    @staticmethod
    def remove(status: int, *values: int) -> int:
        """
        移除状态位，从当前状态中移除一个或多个状态值

        :param status: 当前状态值
        :param values: 要移除的一个或多个状态值
        :return: 移除后的状态值
        """
        for value in values:
            status &= ~value
        return status

    @staticmethod
    def to_binary_string(status: int) -> str:
        """
        转二进制字符串

        :param status: 状态值
        :return: 二进制字符串表示
        """
        if status == 0:
            return "0"
        if status > 0:
            return bin(status)[2:]
        # 负数使用补码表示
        return bin(status & 0xFFFFFFFF)[2:]
