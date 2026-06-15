import random
import secrets
import string
import sys
from datetime import datetime, timedelta
from typing import Any, List, Optional, Sequence, Tuple, TypeVar

T = TypeVar("T")


class RandomUtil:
    """随机工具类，对应 Java cn.hutool.core.util.RandomUtil

    默认使用线程安全的 secrets 模块生成密码学安全随机数，
    部分方法（如 random_color、random_date）使用 random 模块。
    """

    @staticmethod
    def random_int(min_include: int = 0, max_exclude: int = sys.maxsize) -> int:
        """
        生成随机int，范围[min, max)。

        :param min_include: 最小值（含），默认 0
        :param max_exclude: 最大值（不含），默认 sys.maxsize
        :return: 随机整数
        :raises ValueError: min_include 大于等于 max_exclude 时
        """
        if min_include >= max_exclude:
            raise ValueError(f"min_include({min_include}) 必须小于 max_exclude({max_exclude})")
        return secrets.randbelow(max_exclude - min_include) + min_include

    @staticmethod
    def random_long(min_include: int = 0, max_exclude: int = 2**63) -> int:
        """
        生成随机long整数，范围[min, max)。

        :param min_include: 最小值（含），默认 0
        :param max_exclude: 最大值（不含），默认 2^63
        :return: 随机长整数
        :raises ValueError: min_include 大于等于 max_exclude 时
        """
        if min_include >= max_exclude:
            raise ValueError(f"min_include({min_include}) 必须小于 max_exclude({max_exclude})")
        return secrets.randbelow(max_exclude - min_include) + min_include

    @staticmethod
    def random_float(min_include: float = 0.0, max_exclude: float = 1.0) -> float:
        """
        生成随机float，范围[min, max)。

        :param min_include: 最小值（含），默认 0.0
        :param max_exclude: 最大值（不含），默认 1.0
        :return: 随机浮点数
        :raises ValueError: min_include 大于等于 max_exclude 时
        """
        if min_include >= max_exclude:
            raise ValueError(f"min_include({min_include}) 必须小于 max_exclude({max_exclude})")
        # 使用 secrets 生成 [0, 1) 的安全随机数，再映射到目标范围
        ratio = secrets.randbelow(1 << 32) / (1 << 32)
        return min_include + ratio * (max_exclude - min_include)

    @staticmethod
    def random_double(min_include: float = 0.0, max_exclude: float = 1.0) -> float:
        """
        生成随机double（random_float 的别名）。

        :param min_include: 最小值（含），默认 0.0
        :param max_exclude: 最大值（不含），默认 1.0
        :return: 随机浮点数
        """
        return RandomUtil.random_float(min_include, max_exclude)

    @staticmethod
    def random_boolean() -> bool:
        """
        生成随机布尔值。

        :return: 随机 True 或 False
        """
        return bool(secrets.randbelow(2))

    @staticmethod
    def random_bytes(length: int) -> bytes:
        """
        生成指定长度的随机字节数组。

        :param length: 字节长度
        :return: 随机字节串
        :raises ValueError: length 为负数时
        """
        if length < 0:
            raise ValueError(f"length({length}) 不能为负数")
        return secrets.token_bytes(length)

    @staticmethod
    def random_ele(sequence: Sequence[T]) -> T:
        """
        从序列中随机选取一个元素。

        :param sequence: 待选取的序列
        :return: 随机选中的元素
        :raises ValueError: 序列为空时
        """
        if not sequence:
            raise ValueError("序列不能为空")
        return random.choice(sequence)

    @staticmethod
    def random_eles(sequence: Sequence[T], count: int) -> List[T]:
        """
        从序列中随机选取指定个数的元素（不重复）。

        :param sequence: 待选取的序列
        :param count: 选取个数
        :return: 随机选中的元素列表
        :raises ValueError: 序列为空、count 为负数或大于序列长度时
        """
        if not sequence:
            raise ValueError("序列不能为空")
        if count < 0:
            raise ValueError(f"count({count}) 不能为负数")
        if count > len(sequence):
            raise ValueError(f"count({count}) 不能大于序列长度({len(sequence)})")
        return random.sample(list(sequence), count)

    @staticmethod
    def random_string(length: int, base: Optional[str] = None) -> str:
        """
        生成随机字符串，默认包含大小写字母和数字。

        :param length: 字符串长度
        :param base: 字符集，默认为大小写字母 + 数字
        :return: 随机字符串
        :raises ValueError: length 为负数时
        """
        if length < 0:
            raise ValueError(f"length({length}) 不能为负数")
        if base is None:
            base = string.ascii_letters + string.digits
        return "".join(secrets.choice(base) for _ in range(length))

    @staticmethod
    def random_string_upper(length: int) -> str:
        """
        生成随机大写字母字符串。

        :param length: 字符串长度
        :return: 随机大写字符串
        """
        return RandomUtil.random_string(length, string.ascii_uppercase)

    @staticmethod
    def random_string_lower(length: int) -> str:
        """
        生成随机小写字母字符串。

        :param length: 字符串长度
        :return: 随机小写字符串
        """
        return RandomUtil.random_string(length, string.ascii_lowercase)

    @staticmethod
    def random_numbers(length: int) -> str:
        """
        生成随机纯数字字符串。

        :param length: 字符串长度
        :return: 随机数字字符串
        """
        return RandomUtil.random_string(length, string.digits)

    @staticmethod
    def random_color() -> str:
        """
        生成随机十六进制颜色值。

        :return: 颜色字符串，格式如 ``#A1B2C3``
        """
        return f"#{random.randint(0, 0xFFFFFF):06X}"

    @staticmethod
    def random_date(start: datetime, end: datetime) -> datetime:
        """
        在日期范围内生成随机日期时间。

        :param start: 起始日期（含）
        :param end: 结束日期（不含）
        :return: 范围内的随机日期时间
        :raises ValueError: start 大于等于 end 时
        """
        if start >= end:
            raise ValueError("开始日期必须早于结束日期")
        delta = end - start
        random_seconds = random.uniform(0, delta.total_seconds())
        return start + timedelta(seconds=random_seconds)

    @staticmethod
    def weighted_choice(pairs: List[Tuple[int, Any]]) -> Any:
        """
        根据权重随机选择。

        *pairs* 为 ``(weight, value)`` 列表，权重越大被选中的概率越高。

        Examples::

            weighted_choice([(1, "a"), (3, "b"), (6, "c")])
            # "c" 被选中的概率为 60%

        :param pairs: 权重-值对列表，如 ``[(1, "a"), (3, "b")]``
        :return: 随机选中的值
        :raises ValueError: pairs 为空或权重和为 0
        """
        if not pairs:
            raise ValueError("pairs 不能为空")
        total = sum(w for w, _ in pairs)
        if total <= 0:
            raise ValueError("权重总和必须大于 0")
        r = random.randint(1, total)
        for weight, value in pairs:
            r -= weight
            if r <= 0:
                return value
        # 不应到达此处
        return pairs[-1][1]
