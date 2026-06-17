"""
Python port of Java Hutool's NumberUtil.

提供精确的加减乘除运算、四舍五入、数字格式化、数字判断等常用数字工具方法。
"""

import decimal
import math
import random
import re
from decimal import Decimal, InvalidOperation
from typing import Any, Final, Iterable, List, Literal, Optional, Union

from .._base import DefaultParam
from .strings import StrUtil

__all__ = [
    "NumberUtil",
]

# 数字工具类默认参数
DEFAULT_NUMBER_PARAM = DefaultParam()


class NumberUtil:
    """
    数字工具类
    """

    # 默认除法运算精度
    DEFAULT_DIV_SCALE: Final[int] = 10
    # 零
    ZERO: Final[Decimal] = Decimal("0")
    # Base62 编码常量
    _BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    _BASE62_REVERSE = {c: i for i, c in enumerate(_BASE62_ALPHABET)}

    @staticmethod
    def add(*values: Union[int, float, str, None, Decimal]) -> Decimal:
        """
        提供精确的加法运算
        如果传入多个值为None或者空，则返回0
        :param values: 多个被加值
        :return: 和
        """
        if not values:
            return NumberUtil.ZERO
        result = NumberUtil.ZERO
        for value in values:
            result += NumberUtil.to_decimal(value)
        return result

    @staticmethod
    def sub(*values: Union[int, float, str, None, Decimal]) -> Decimal:
        """
        提供精确的减法运算
        如果传入多个值为None或者空，则返回0
        :param values: 多个被减值
        :return: 差
        """
        if not values:
            return NumberUtil.ZERO
        result = NumberUtil.to_decimal(values[0])
        for i in range(1, len(values)):
            result -= NumberUtil.to_decimal(values[i])
        return result

    @staticmethod
    def mul(*values: Union[int, float, str, None, Decimal]) -> Decimal:
        """
        提供精确的乘法运算

        如果传入多个值为None或者空，则返回0

        :param values: 多个被乘值
        :return: 积
        """
        if not values or any(v is None for v in values):
            return NumberUtil.ZERO
        result = NumberUtil.to_decimal(values[0])
        for i in range(1, len(values)):
            result *= NumberUtil.to_decimal(values[i])
        return result

    @staticmethod
    def div(
        v1: Union[int, float, str, None, Decimal],
        v2: Union[int, float, str, Decimal],
        scale: Union[int, Decimal] = DEFAULT_DIV_SCALE,
        rounding: str = decimal.ROUND_HALF_UP,
    ) -> Decimal:
        """
        提供(相对)精确的除法运算,当发生除不尽的情况时,由scale指定精确度
        :param v1: 被除数
        :param v2: 除数
        :param scale: 精确度，如果为负值，取绝对值, 如果为Decimal, 需要为Decimal('0.00')格式
        :param rounding: 保留小数的模式
        :return: 两个参数的商
        """
        assert v2 is not None, "Divisor must be not none!"
        if v1 is None:
            return NumberUtil.ZERO

        v1 = NumberUtil.to_decimal(v1)
        v2 = NumberUtil.to_decimal(v2)
        return NumberUtil.round(v1 / v2, scale, rounding=rounding)

    @staticmethod
    def ceil_div(v1: int, v2: int) -> int:
        """
        除法, 向上取整
        :param v1: 被除数
        :param v2: 除数
        :return: 两个参数的商
        """
        return math.ceil(v1 / v2)

    @staticmethod
    def round(
        number: Union[int, float, str, None, Decimal],
        scale: Union[int, Decimal],
        rounding: str = decimal.ROUND_HALF_UP,
    ) -> Decimal:
        """
        保留固定位数小数
        :param number: 数字值
        :param scale: 精确度，如果为负值，取绝对值, 如果为Decimal, 需要为Decimal('0.00')格式
        :param rounding: 保留小数的模式
        :return: 新值
        """
        number = NumberUtil.to_decimal(number)

        if isinstance(scale, int):
            if scale < 0:
                scale = -scale
            scale_num = scale
            scale = Decimal("0." + "0" * scale)
        else:
            scale_num = len(str(scale)) - 2

        if decimal.getcontext().prec < scale_num:
            decimal.getcontext().prec = scale_num

        return number.quantize(scale, rounding=rounding)

    @staticmethod
    def round_str(
        number: Union[int, float, str, None, Decimal],
        scale: Union[int, Decimal],
        rounding: str = decimal.ROUND_HALF_UP,
    ) -> str:
        """
        保留固定位数小数
        :param number: 数字值
        :param scale: 精确度，如果为负值，取绝对值, 如果为Decimal, 需要为Decimal('0.00')格式
        :param rounding: 保留小数的模式
        :return: 新值
        """
        return f"{NumberUtil.round(number, scale, rounding=rounding).normalize():f}"

    @staticmethod
    def round_half_even(
        number: Union[int, float, str, None, Decimal],
        scale: Union[int, Decimal],
    ) -> Decimal:
        """
        四舍六入五成双计算法
        四舍六入五成双是一种比较精确比较科学的计数保留法，是一种数字修约规则。
        算法规则:
        四舍六入五考虑，
        五后非零就进一，
        五后皆零看奇偶，
        五前为偶应舍去，
        五前为奇要进一。
        :param number: 需要科学计算的数据
        :param scale: 精确度，如果为负值，取绝对值, 如果为Decimal, 需要为Decimal('0.00')格式
        :return: 结果
        """
        return NumberUtil.round(number, scale, rounding=decimal.ROUND_HALF_EVEN)

    @staticmethod
    def round_down(
        number: Union[int, float, str, None, Decimal],
        scale: Union[int, Decimal],
    ) -> Decimal:
        """
        保留固定小数位数，舍去多余位数
        :param number: 需要科学计算的数据
        :param scale: 保留的小数位
        :return: 结果
        """
        return NumberUtil.round(number, scale, rounding=decimal.ROUND_DOWN)

    @staticmethod
    def decimal_format(pattern: str, value: Union[int, float, str, None, Decimal]) -> str:
        """格式化

        :param pattern: 格式，例如:

            - ``'{:.2f}'`` 保留两位小数
            - ``'{:.0f}'`` 取所有整数部分
            - ``'{:.2%}'`` 以百分比方式计数，并取两位小数
            - ``'{:.5e}'`` 显示为科学计数法，并取五位小数
            - ``'{:,}'`` 每三位以逗号进行分隔

        :param value: 值
        :return: 格式化后的值
        """
        assert NumberUtil.is_valid(value), "value is NaN or Infinite!"
        return pattern.format(NumberUtil.to_decimal(value))

    @staticmethod
    def decimal_format_money(value: float) -> str:
        """
        格式化金额输出，每三位用逗号分隔
        :param value: 金额
        :return: 格式化后的值
        """
        return NumberUtil.decimal_format("{:,.2f}", value)

    @staticmethod
    def format_percent(number: float, scale: int) -> str:
        """
        格式化百分比，小数采用四舍五入方式
        :param number: 值
        :param scale: 保留小数位数
        :return: 百分比
        """
        return NumberUtil.decimal_format("{:." + str(scale) + "%}", NumberUtil.round(number, scale + 2))

    @staticmethod
    def is_number(string: str) -> bool:
        """
        是否为数字，支持包括：
        1、10进制
        2、16进制数字（0x开头, 0x1aF）
        3、科学计数法形式（1234E3）
        4、正负数标识形式（+123、-234）
        :param string: 字符串值
        :return: 是否为数字
        """
        if StrUtil.is_blank(string):
            return False
        pattern = r"^[+-]?((0[xX][0-9a-fA-F]+)|((\d+\.?\d*|\.\d+)([eE][+-]?\d+)?))$"
        return re.match(pattern, string) is not None

    @staticmethod
    def is_int(string: Union[str, None]) -> bool:
        """
        判断string是否是整数
        :param string: 字符串值
        :return: 是否为整数
        """
        if StrUtil.is_blank(string):
            return False
        try:
            int(string)
        except ValueError:
            return False
        return True

    @staticmethod
    def is_float(string: str) -> bool:
        """
        判断字符串是否是浮点数
        :param string: 字符串值
        :return: 是否是浮点数
        """
        if StrUtil.is_blank(string):
            return False
        try:
            float(string)
        except ValueError:
            return False
        return "." in string

    @staticmethod
    def is_primes(n: int) -> bool:
        """
        是否是质数（素数）
        质数表的质数又称素数。指整数在一个大于1的自然数中,除了1和此整数自身外,没法被其他自然数整除的数。
        :param n: 数字
        :return: 是否是质数
        """
        assert n > 1, "The number must be > 1"
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def generate_random_number(begin: int, end: int, size: int, seed: Optional[int] = None) -> List[int]:
        """
        生成不重复随机数 根据给定的最小数字和最大数字，以及随机数的个数，产生指定的不重复的列表
        :param begin: 最小数字（包含该数）
        :param end: 最大数字（不包含该数）
        :param size: 指定产生随机数的个数
        :param seed: 随机种子
        :return: 随机int列表
        """
        return random.Random(seed).sample(list(range(begin, end)), size)

    @staticmethod
    def factorial(start: int, end: int = 0) -> int:
        """
        计算阶乘
        factorial(start, end) = start * (start - 1) * ... * (end + 1)
        :param start: 阶乘起始（包含）
        :param end: 阶乘结束，必须小于起始（不包括）
        :return: 结果
        """
        assert start is not None, "Factorial start must be not null!"
        assert end is not None, "Factorial end must be not null!"
        if start < 0 or end < 0:
            raise ValueError(f"Factorial start and end both must be > 0, but got start={start}, end={end}")

        if start == 0 or start == end:
            return 1
        if start < end:
            return 0
        if end < 1:
            end = 1

        result = start
        end += 1
        while start > end:
            start -= 1
            result *= start
        return result

    @staticmethod
    def divisor(m: int, n: int) -> int:
        """
        最大公约数
        :param m: 第一个值
        :param n: 第二个值
        :return: 最大公约数
        """
        while m % n != 0:
            temp = m % n
            m = n
            n = temp
        return n

    @staticmethod
    def multiple(m: int, n: int) -> int:
        """
        最小公倍数
        :param m: 第一个值
        :param n: 第二个值
        :return: 最小公倍数
        """
        return m * n // NumberUtil.divisor(m, n)

    @staticmethod
    def get_binary_str(number: int) -> str:
        """
        获得数字对应的二进制字符串
        :param number: 数字
        :return: 二进制字符串
        """
        return bin(number)

    @staticmethod
    def binary_to_int(binary_str: str) -> int:
        """
        二进制转int
        :param binary_str: 二进制字符串
        :return: int
        """
        return int(binary_str, 2)

    @staticmethod
    def compare(num1: Union[int, float, str, Decimal], num2: Union[int, float, str, Decimal]) -> int:
        """
        比较两个值的大小
        :param num1: 第一个值
        :param num2: 第二个值
        :return: x==y返回0，x<y返回小于0的数，x>y返回大于0的数
        """
        assert num1 is not None, "first value must not be none!"
        assert num2 is not None, "second value must not be none!"
        return int(NumberUtil.to_decimal(num1).compare(NumberUtil.to_decimal(num2)))

    @staticmethod
    def is_greater(num1: Union[int, float, str, Decimal], num2: Union[int, float, str, Decimal]) -> bool:
        """
        比较大小，参数1 > 参数2 返回True
        :param num1: 数字1
        :param num2: 数字2
        :return: 是否大于
        """
        return NumberUtil.compare(num1, num2) > 0

    @staticmethod
    def is_greater_or_equal(num1: Union[int, float, str, Decimal], num2: Union[int, float, str, Decimal]) -> bool:
        """
        比较大小，参数1 >= 参数2 返回True
        :param num1: 数字1
        :param num2: 数字2
        :return: 是否大于等于
        """
        return NumberUtil.compare(num1, num2) >= 0

    @staticmethod
    def is_less(num1: Union[int, float, str, Decimal], num2: Union[int, float, str, Decimal]) -> bool:
        """
        比较大小，参数1 < 参数2 返回True
        :param num1: 数字1
        :param num2: 数字2
        :return: 是否小于
        """
        return NumberUtil.compare(num1, num2) < 0

    @staticmethod
    def is_less_or_equal(num1: Union[int, float, str, Decimal], num2: Union[int, float, str, Decimal]) -> bool:
        """
        比较大小，参数1 <= 参数2 返回True
        :param num1: 数字1
        :param num2: 数字2
        :return: 是否小于等于
        """
        return NumberUtil.compare(num1, num2) <= 0

    @staticmethod
    def is_in(
        value: Union[int, float, str, Decimal],
        min_include: Union[int, float, str, Decimal],
        max_include: Union[int, float, str, Decimal],
    ) -> bool:
        """
        检查值是否在指定范围内
        :param value: 值
        :param min_include: 最小值（包含）
        :param max_include: 最大值（包含）
        :return: 经过检查后的值
        """
        assert value is not None, "value must be not none!"
        assert min_include is not None, "min_include must be not none!"
        assert max_include is not None, "max_include must be not none!"
        return NumberUtil.is_greater_or_equal(value, min_include) and NumberUtil.is_less_or_equal(value, max_include)

    @staticmethod
    def equals(num1: Union[int, float, str, Decimal], num2: Union[int, float, str, Decimal]) -> bool:
        """
        比较大小，值相等 返回True
        :param num1: 数字1
        :param num2: 数字2
        :return: 是否相等
        """
        return NumberUtil.compare(num1, num2) == 0

    @staticmethod
    def min(*numbers: Union[int, float, str, Decimal]) -> Decimal:
        """
        取最小值
        :param numbers: 数字数组
        :return: 最小值
        """
        assert bool(numbers), "Number array must not empty!"
        nums = [NumberUtil.to_decimal(num) for num in numbers]
        return min(*nums)

    @staticmethod
    def max(*numbers: Union[int, float, str, Decimal]) -> Decimal:
        """
        取最大值
        :param numbers: 数字数组
        :return: 最大值
        """
        assert bool(numbers), "Number array must not empty!"
        nums = [NumberUtil.to_decimal(num) for num in numbers]
        return max(*nums)

    @staticmethod
    def to_str(
        number: Union[int, float, Decimal],
        normalize: bool = True,
        default_value: Optional[str] = None,
    ) -> str:
        """
        数字转字符串
        :param number: 数字
        :param normalize: 是否去除末尾多余0，例如5.0返回5
        :param default_value: 如果number参数为None，返回此默认值
        :return: 字符串
        """
        if number is None:
            if default_value is None:
                raise ValueError("Number is None!")
            else:
                return default_value

        assert NumberUtil.is_valid(number), "Number is non-finite!"
        if normalize:
            return f"{NumberUtil.to_decimal(number).normalize():f}"
        return str(number)

    @staticmethod
    def to_decimal(number: Union[int, float, str, None, Decimal]) -> Decimal:
        """
        转成Decimal
        float有精度问题，转换为字符串后再转换
        None或""或空白符转换为0
        :param number: 数字
        :return: Decimal
        """
        if number is None:
            return NumberUtil.ZERO

        if isinstance(number, int):
            return Decimal(number)
        elif isinstance(number, Decimal):
            return number

        number = str(number)
        if StrUtil.is_blank(number):
            return NumberUtil.ZERO

        try:
            return Decimal(number)
        except InvalidOperation:
            # 忽略解析错误
            pass

        return NumberUtil.to_decimal(str(NumberUtil.parse_float(number)))

    @staticmethod
    def count(total: int, part: int) -> int:
        """
        计算等份个数
        :param total: 总数
        :param part: 每份的个数
        :return: 分成了几份
        """
        return (total // part) if total % part == 0 else (total // part + 1)

    @staticmethod
    def none_to_zero(number: Union[int, float, str, Decimal]) -> Union[int, float, str, Decimal]:
        """
        空转0
        :param number: 参数
        :return: 参数为空时返回0的值
        """
        if number is not None:
            return number

        if isinstance(number, int):
            return 0
        elif isinstance(number, float):
            return 0.0
        elif isinstance(number, str):
            return "0"
        elif isinstance(number, Decimal):
            return NumberUtil.ZERO
        return 0

    @staticmethod
    def zero2one(value: int) -> int:
        """
        如果给定值为0，返回1，否则返回原值
        :param value: 值
        :return: 1或非0值
        """
        return 1 if value == 0 else value

    @staticmethod
    def is_beside(number1: Union[int, float, str, Decimal], number2: Union[int, float, str, Decimal]) -> bool:
        """
        判断两个数字是否相邻，例如1和2相邻，1和3不相邻
        判断方法为做差取绝对值判断是否为1
        :param number1: 数字1
        :param number2: 数字2
        :return: 是否相邻
        """
        return math.fabs(NumberUtil.to_decimal(number1) - NumberUtil.to_decimal(number2)) == 1

    @staticmethod
    def part_value(total: int, part_count: int, is_plus_one_when_has_rem: bool = True) -> int:
        """
        把给定的总数平均分成N份，返回每份的个数
        如果is_plus_one_when_has_rem为True，则当除以分数有余数时每份+1，否则丢弃余数部分
        :param total: 总数
        :param part_count: 份数
        :param is_plus_one_when_has_rem: 在有余数时是否每份+1
        :return: 每份的个数
        """
        pv = total // part_count
        if is_plus_one_when_has_rem and total % part_count > 0:
            pv += 1
        return pv

    @staticmethod
    def pow(number: Union[int, float, str, Decimal], n: int) -> Decimal:
        """
        提供精确的幂运算
        :param number: 底数
        :param n: 指数
        :return: 幂的积
        """
        return NumberUtil.to_decimal(number) ** n

    @staticmethod
    def is_power_of_two(n: int) -> bool:
        """
        判断一个整数是否是2的幂
        :param n: 待验证的整数
        :return: 如果n是2的幂返回True, 反之返回False
        """
        return n > 0 and n & (n - 1) == 0

    @staticmethod
    def parse_int(number_str: str, default_value: Union[int, DefaultParam, None] = DEFAULT_NUMBER_PARAM) -> int:
        """
        解析转换数字字符串为int型数字，规则如下：
        1、0x开头的视为16进制数字
        2、0开头的忽略开头的0
        3、其它情况按照10进制转换
        4、空串返回默认值
        5、.123形式返回0（按照小于0的小数对待）
        6、123.56截取小数点之前的数字，忽略小数部分
        7、返回默认值
        :param number_str: 数字，支持0x开头、0开头和普通十进制
        :param default_value: 返回默认值
        :return: int
        """
        is_default = isinstance(default_value, DefaultParam)
        if StrUtil.is_blank(number_str):
            return 0 if is_default else default_value

        try:
            if StrUtil.start_with_ignore_case(number_str, "0x"):
                return int(number_str, 16)
            if StrUtil.contains(number_str, "."):
                number_str = float(number_str)
            return int(number_str)
        except ValueError as ve:
            if is_default:
                raise ve
            else:
                return default_value

    @staticmethod
    def parse_float(number_str: str, default_value: Union[int, DefaultParam, None] = DEFAULT_NUMBER_PARAM) -> float:
        """
        解析转换数字字符串为float型数字，规则如下：
        1、0开头的忽略开头的0
        2、空串返回默认值
        3、其它情况按照10进制转换
        :param number_str: 数字，支持0x开头、0开头和普通十进制
        :param default_value: 返回默认值
        :return: float
        """
        is_default = isinstance(default_value, DefaultParam)
        if StrUtil.is_blank(number_str):
            return 0 if is_default else default_value
        try:
            if StrUtil.start_with_ignore_case(number_str, "0x"):
                return float.fromhex(number_str)
            return float(number_str)
        except ValueError as ve:
            if is_default:
                raise ve
            else:
                return default_value

    @staticmethod
    def to_bytes(
        value: int,
        length: Optional[int] = None,
        byteorder: Literal["little", "big"] = "big",
        signed: bool = True,
    ) -> bytes:
        """
        int值转bytes
        :param value: 值
        :param length: bytes长度
        :param byteorder: 默认大端字节序（高位字节在前，低位字节在后）
        :param signed: 是否带符号
        :return: bytes
        """
        if length is None:
            length = (value.bit_length() + 7) // 8
        return value.to_bytes(length, byteorder, signed=signed)

    @staticmethod
    def to_int(value: bytes, byteorder: Literal["little", "big"] = "big", signed: bool = True) -> int:
        """
        bytes转int
        :param value: bytes
        :param byteorder: 默认大端字节序（高位字节在前，低位字节在后）
        :param signed: 是否带符号
        :return: int
        """
        return int.from_bytes(value, byteorder, signed=signed)

    @staticmethod
    def is_valid(number: Union[int, float, Decimal]) -> bool:
        """
        检查是否为有效的数字
        检查是否为无限大，或者Not a Number
        :param number: 被检查的数字
        :return: 检查结果，非数字类型和None将返回False
        """
        return not (number is None or math.isinf(number) or math.isnan(number))

    @staticmethod
    def is_odd(num: int) -> bool:
        """
        检查是否为奇数
        :param num: 被判断的数值
        :return: 是否是奇数
        """
        return (num & 1) == 1

    @staticmethod
    def is_even(num: int) -> bool:
        """
        检查是否为偶数
        :param num: 被判断的数值
        :return: 是否是偶数
        """
        return not NumberUtil.is_odd(num)

    @staticmethod
    def int_or_default(data: Any, default: int = 0) -> int:
        """
        安全地将数据转换为整数，失败时返回默认值。

        支持 int、float、str、list/tuple（取第一个元素）等类型。
        ``None``、空容器直接返回默认值。

        :param data: 待转换的数据
        :param default: 转换失败时的默认值，默认 0
        :return: 整数值
        """
        if data is None:
            return default
        if isinstance(data, (list, tuple)):
            if not data:
                return default
            return NumberUtil.int_or_default(data[0], default)
        try:
            return int(float(data))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def float_or_default(data: Any, default: float = 0.0) -> float:
        """
        安全地将数据转换为浮点数，失败时返回默认值。

        ``None``、空容器直接返回默认值。

        :param data: 待转换的数据
        :param default: 转换失败时的默认值，默认 0.0
        :return: 浮点数值
        """
        if data is None:
            return default
        if isinstance(data, (list, tuple)):
            if not data:
                return default
            return NumberUtil.float_or_default(data[0], default)
        try:
            return float(data)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def int_or_0(data: Any) -> int:
        """
        安全转 int，失败返回 ``0``。

        等价于 ``int_or_default(data, 0)``，提供与 huTools 兼容的命名。

        :param data: 待转换的值
        :return: int 值，转换失败返回 ``0``
        """
        return NumberUtil.int_or_default(data, 0)

    @staticmethod
    def float_or_0(data: Any) -> float:
        """
        安全转 float，失败返回 ``0.0``。

        等价于 ``float_or_default(data, 0.0)``，提供与 huTools 兼容的命名。

        :param data: 待转换的值
        :return: float 值，转换失败返回 ``0.0``
        """
        return NumberUtil.float_or_default(data, 0.0)

    @staticmethod
    def avg(data: Iterable) -> float:
        """
        计算数值列表的平均值。

        空列表返回 ``0.0``。

        :param data: 数值可迭代对象
        :return: 平均值
        """
        items = list(data)
        if not items:
            return 0.0
        return sum(items) / float(len(items))

    @staticmethod
    def median(data: Iterable) -> float:
        """
        计算数值列表的中位数。

        空列表返回 ``0.0``。

        :param data: 数值可迭代对象
        :return: 中位数
        """
        items = sorted(data)
        n = len(items)
        if n == 0:
            return 0.0
        if n % 2 == 1:
            return float(items[n // 2])
        return (items[n // 2 - 1] + items[n // 2]) / 2.0

    @staticmethod
    def robust_min(data: Iterable) -> Optional[float]:
        """
        安全取最小值，空列表返回 ``None``。

        与 ``CollUtil.safe_min`` 不同，本方法对空输入返回 ``None`` 而非抛出异常。

        :param data: 数值可迭代对象
        :return: 最小值，空列表返回 ``None``
        """
        items = list(data)
        if not items:
            return None
        return float(min(items))

    @staticmethod
    def robust_max(data: Iterable) -> Optional[float]:
        """
        安全取最大值，空列表返回 ``None``。

        与 ``CollUtil.safe_max`` 不同，本方法对空输入返回 ``None`` 而非抛出异常。

        :param data: 数值可迭代对象
        :return: 最大值，空列表返回 ``None``
        """
        items = list(data)
        if not items:
            return None
        return float(max(items))

    @staticmethod
    def robust_div(a: float, b: float, default: float = 0.0) -> float:
        """
        安全除法，除数为 0 时返回默认值（默认 ``0.0``）。

        :param a: 被除数
        :param b: 除数
        :param default: 除数为 0 时的返回值，默认 ``0.0``
        :return: 除法结果或默认值
        """
        if b == 0:
            return default
        return a / b

    @staticmethod
    def percent(part: float, total: float, default: float = 0.0) -> float:
        """
        百分比计算，``total`` 为 0 时返回默认值。

        计算公式：``(part / total) * 100``。

        :param part: 部分值
        :param total: 总值
        :param default: ``total`` 为 0 时的返回值，默认 ``0.0``
        :return: 百分比值（如 25.0 表示 25%）
        """
        return NumberUtil.robust_div(part, total, default) * 100

    @staticmethod
    def num_encode(n: int) -> str:
        """
        将整数编码为 base62 字符串（字符集：``0-9A-Za-z``）。

        负数会以 ``$`` 前缀表示。

        :param n: 待编码的整数
        :return: base62 编码字符串
        """
        if n < 0:
            return "$" + NumberUtil.num_encode(-n)
        alphabet = NumberUtil._BASE62_ALPHABET
        base = len(alphabet)
        if n == 0:
            return alphabet[0]
        s = []
        while n > 0:
            n, r = divmod(n, base)
            s.append(alphabet[r])
        return "".join(reversed(s))

    @staticmethod
    def bytes_to_int(data: bytes) -> int:
        """
        将 bytes 按大端序转换为 int。

        :param data: 字节数据
        :return: 转换后的整数

        ::

            >>> NumberUtil.bytes_to_int(b'\\x00\\x00\\x01\\x00')
            256
            >>> NumberUtil.bytes_to_int(b'\\xff')
            255
        """
        return int.from_bytes(data, byteorder="big", signed=False)

    @staticmethod
    def int_to_bytes(value: int, length: int = 4) -> bytes:
        """
        将 int 按大端序转换为指定长度的 bytes。

        :param value: 整数值
        :param length: 输出 bytes 的长度（字节数），默认 4
        :return: 字节数据

        ::

            >>> NumberUtil.int_to_bytes(256, 2)
            b'\\x01\\x00'
            >>> NumberUtil.int_to_bytes(0, 1)
            b'\\x00'
        """
        if value < 0:
            raise ValueError("value 必须为非负整数")
        return value.to_bytes(length, byteorder="big", signed=False)

    @staticmethod
    def num_decode(s: str) -> int:
        """
        将 base62 字符串解码为整数。

        :param s: base62 编码字符串
        :return: 解码后的整数
        :raises ValueError: 字符串包含非法字符时
        """
        if s.startswith("$"):
            return -NumberUtil.num_decode(s[1:])
        reverse = NumberUtil._BASE62_REVERSE
        base = len(NumberUtil._BASE62_ALPHABET)
        n = 0
        for c in s:
            if c not in reverse:
                raise ValueError(f"非法 base62 字符: {c!r}")
            n = n * base + reverse[c]
        return n

    @staticmethod
    def range_(start: int, end: int, step: int = 1) -> List[int]:
        """
        生成数字范围列表（含 start，不含 end）。

        :param start: 起始值（含）
        :param end: 结束值（不含）
        :param step: 步长，默认 1
        :return: 数字列表
        """
        return list(range(start, end, step))

    @staticmethod
    def append_range(collection: List[int], start: int, end: int, step: int = 1) -> List[int]:
        """
        追加数字范围到列表。

        :param collection: 目标列表
        :param start: 起始值（含）
        :param end: 结束值（不含）
        :param step: 步长，默认 1
        :return: 追加后的列表
        """
        collection.extend(range(start, end, step))
        return collection

    @staticmethod
    def generate_by_set(count: int, min_val: int, max_val: int) -> List[int]:
        """
        生成 count 个 [min_val, max_val] 范围内的不重复随机数。

        :param count: 个数
        :param min_val: 最小值（含）
        :param max_val: 最大值（含）
        :return: 不重复随机数列表
        :raises ValueError: 范围不足时
        """
        population = max_val - min_val + 1
        if count > population:
            raise ValueError(f"范围 [{min_val}, {max_val}] 不足以生成 {count} 个不重复随机数")
        return random.sample(range(min_val, max_val + 1), count)

    @staticmethod
    def calculate(expression: str) -> float:
        """
        计算数学表达式（仅支持安全的数字和运算符）。

        支持: ``+``, ``-``, ``*``, ``/``, ``//``, ``%``, ``**``, 括号。

        :param expression: 数学表达式字符串
        :return: 计算结果
        :raises ValueError: 表达式不安全时
        """
        # 仅允许数字、运算符、括号、空格和小数点
        safe_pattern = r"^[\d\s\+\-\*\/\%\.\(\)\*\*]+$"
        if not re.match(safe_pattern, expression):
            raise ValueError(f"不安全的表达式: {expression}")
        try:
            result = eval(expression)
        except Exception as e:
            raise ValueError(f"表达式计算失败: {expression}") from e
        return float(result)

    @staticmethod
    def sqrt(x: Union[int, float, str, Decimal], scale: int = 10) -> Decimal:
        """
        精确平方根。

        :param x: 待开方的数值
        :param scale: 小数位数
        :return: 平方根
        """
        x_dec = NumberUtil.to_decimal(x)
        if x_dec < 0:
            raise ValueError(f"无法对负数开平方: {x}")
        ctx = decimal.Context(prec=scale + 10)
        result = x_dec.sqrt(ctx)
        return NumberUtil.round(result, scale)

    @staticmethod
    def is_integer(s: Union[str, None]) -> bool:
        """
        判断字符串是否为整数（与 is_int 相同）。

        :param s: 字符串
        :return: 是否为整数
        """
        return NumberUtil.is_int(s)

    @staticmethod
    def is_double(s: str) -> bool:
        """
        判断字符串是否为浮点数（与 is_float 相同）。

        :param s: 字符串
        :return: 是否为浮点数
        """
        return NumberUtil.is_float(s)

    @staticmethod
    def parse_number(s: str) -> Union[int, float]:
        """
        解析字符串为数字，整数返回 int，小数返回 float。

        :param s: 数字字符串
        :return: int 或 float
        :raises ValueError: 解析失败时
        """
        if StrUtil.is_blank(s):
            raise ValueError("空字符串无法解析为数字")
        if "." in s or "e" in s.lower():
            return float(s)
        return int(s)

    @staticmethod
    def parse_long(number_str: str, default_value: int = 0) -> int:
        """
        解析字符串为长整数（Python int）。

        :param number_str: 数字字符串
        :param default_value: 解析失败时的默认值
        :return: 长整数
        """
        try:
            return int(number_str)
        except (ValueError, TypeError):
            return default_value

    # ------------------------------------------------------------------
    # 进制转换
    # ------------------------------------------------------------------

    @staticmethod
    def binary_to_long(binary_str: str) -> int:
        """
        二进制字符串转整数。

        :param binary_str: 二进制字符串，如 ``"1010"``
        :return: 对应的整数
        :raises ValueError: 非法二进制字符串时
        """
        return int(binary_str, 2)

    @staticmethod
    def to_big_integer(n: Union[int, str], radix: int = 10) -> int:
        """
        将数字或字符串转为大整数（Python int）。

        :param n: 数字或字符串
        :param radix: 进制，默认 10
        :return: 大整数
        """
        if isinstance(n, int):
            return n
        return int(str(n), radix)

    @staticmethod
    def new_big_integer(s: str, radix: int = 10) -> int:
        """
        按指定进制解析字符串为大整数。

        :param s: 数字字符串
        :param radix: 进制（2、8、10、16 等）
        :return: 大整数
        """
        return int(s, radix)

    @staticmethod
    def to_unsigned_byte_array(n: int) -> bytes:
        """
        将非负整数转为无符号字节数组（大端序）。

        :param n: 非负整数
        :return: 字节串
        :raises ValueError: n 为负数时
        """
        if n < 0:
            raise ValueError("n 不能为负数")
        if n == 0:
            return b"\x00"
        result = bytearray()
        while n > 0:
            result.append(n & 0xFF)
            n >>= 8
        return bytes(reversed(result))

    @staticmethod
    def from_unsigned_byte_array(data: bytes) -> int:
        """
        无符号字节数组（大端序）转整数。

        :param data: 字节串
        :return: 整数
        """
        return int.from_bytes(data, byteorder="big", signed=False)

    # ------------------------------------------------------------------
    # 整数运算
    # ------------------------------------------------------------------

    @staticmethod
    def integer_sqrt(x: int) -> int:
        """
        整数平方根（向下取整）。

        使用牛顿迭代法，避免浮点精度问题。

        :param x: 非负整数
        :return: 平方根的整数部分
        :raises ValueError: x 为负数时
        """
        if x < 0:
            raise ValueError("不能对负数求平方根")
        if x < 2:
            return x
        # 牛顿迭代
        guess = x
        while guess * guess > x:
            guess = (guess + x // guess) // 2
        return guess

    @staticmethod
    def process_multiple(n: int, m: int) -> int:
        """
        计算组合数 C(n, m)。

        :param n: 总数
        :param m: 选取数
        :return: 组合数
        :raises ValueError: 参数非法时
        """
        if n < 0 or m < 0 or m > n:
            raise ValueError(f"参数非法：n={n}, m={m}")
        if m == 0 or m == n:
            return 1
        # 利用对称性减少计算
        if m > n - m:
            m = n - m
        result = 1
        for i in range(m):
            result = result * (n - i) // (i + 1)
        return result

    # ------------------------------------------------------------------
    # 解析扩展
    # ------------------------------------------------------------------

    @staticmethod
    def parse_double(s: str, default_value: float = 0.0) -> float:
        """
        解析字符串为 float，失败返回默认值。

        :param s: 数字字符串
        :param default_value: 默认值
        :return: float 值
        """
        try:
            return float(s)
        except (ValueError, TypeError):
            return default_value

    # ------------------------------------------------------------------
    # 范围与生成
    # ------------------------------------------------------------------

    @staticmethod
    def range(start: int, end: int, step: int = 1) -> List[int]:
        """
        生成数字范围列表（含 start，不含 end）。

        :param start: 起始值（含）
        :param end: 结束值（不含）
        :param step: 步长，默认 1
        :return: 数字列表
        """
        return list(range(start, end, step))

    @staticmethod
    def generate(count: int, min_val: int = 0, max_val: int = 100) -> List[int]:
        """
        生成指定个数的随机整数列表。

        :param count: 个数
        :param min_val: 最小值（含）
        :param max_val: 最大值（不含）
        :return: 随机整数列表
        """
        import secrets

        if count <= 0:
            return []
        return [secrets.randbelow(max_val - min_val) + min_val for _ in range(count)]

    # ------------------------------------------------------------------
    # 空值处理
    # ------------------------------------------------------------------

    @staticmethod
    def null_to_zero(n: Optional[Union[int, float]]) -> Union[int, float]:
        """
        None 转为 0。

        :param n: 数值
        :return: n 为 None 时返回 0，否则返回原值
        """
        return 0 if n is None else n

    @staticmethod
    def is_long(value: Any) -> bool:
        """判断值是否为长整数类型（Python int 类型）。

        :param value: 待检查的值
        :return: 是否为 int 类型（排除 bool）
        """
        return isinstance(value, int) and not isinstance(value, bool)

    @staticmethod
    def is_valid_number(value: Any) -> bool:
        """判断值是否为有效数字（支持科学计数法）。

        None、非数字类型返回 False。NaN 和 Inf 返回 False。

        :param value: 待检查的值
        :return: 是否为有效数字
        """
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return not (isinstance(value, float) and (math.isnan(value) or math.isinf(value)))
        if isinstance(value, Decimal):
            return value.is_finite()
        if isinstance(value, str):
            try:
                float(value)
                return True
            except (ValueError, TypeError):
                return False
        return False

    @staticmethod
    def to_float_safe(value: Any, default: float = 0.0) -> float:
        """安全地将值转为 float，失败返回默认值。

        :param value: 待转换的值
        :param default: 转换失败时的默认值，默认 0.0
        :return: float 值
        """
        if value is None:
            return default
        if isinstance(value, bool):
            return float(value)
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def operator_exec(left: Any, operator: str, right: Any) -> bool:
        """执行运算符比较操作。

        支持 ``==``、``!=``、``>``、``>=``、``<``、``<=`` 六种比较运算符。
        用于需要动态指定比较运算符的场景。

        :param left: 左操作数
        :param operator: 运算符字符串（``"=="``、``"!="``、``">"``、``">="``、``"<"``、``"<="``）
        :param right: 右操作数
        :return: 比较结果
        :raises ValueError: 不支持的运算符时
        """
        _ops = {
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            ">": lambda a, b: a > b,
            ">=": lambda a, b: a >= b,
            "<": lambda a, b: a < b,
            "<=": lambda a, b: a <= b,
        }
        op_func = _ops.get(operator)
        if op_func is None:
            raise ValueError(f"不支持的运算符: {operator}，支持: {', '.join(_ops.keys())}")
        return op_func(left, right)
