import random
import secrets
import string
import sys
from datetime import date, datetime, timedelta
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
    def random_eles(sequence: Sequence[T], count: int, allow_duplicate: bool = False) -> List[T]:
        """
        从序列中随机选取指定个数的元素。

        :param sequence: 待选取的序列
        :param count: 选取个数
        :param allow_duplicate: 是否允许重复选取，默认 False（不重复）
        :return: 随机选中的元素列表
        :raises ValueError: 序列为空、count 为负数或（不允许重复时）大于序列长度
        """
        if not sequence:
            raise ValueError("序列不能为空")
        if count < 0:
            raise ValueError(f"count({count}) 不能为负数")
        if allow_duplicate:
            return [random.choice(list(sequence)) for _ in range(count)]
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
        生成随机小写字母+数字字符串

        :param length: 字符串长度
        :return: 随机小写字符串
        """
        return RandomUtil.random_string(length, string.ascii_lowercase + string.digits)

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

    @staticmethod
    def random_chinese(count: int = 1) -> str:
        """
        生成指定个数的随机中文字符（常用汉字范围 0x4E00~0x9FFF）。

        :param count: 字符个数，默认 1
        :return: 随机中文字符串
        """
        return "".join(chr(secrets.randbelow(0x9FFF - 0x4E00 + 1) + 0x4E00) for _ in range(count))

    @staticmethod
    def random_char(char_set: str) -> str:
        """
        从字符集中随机选取一个字符。

        :param char_set: 字符集
        :return: 随机字符
        :raises ValueError: 字符集为空时
        """
        if not char_set:
            raise ValueError("字符集不能为空")
        return secrets.choice(char_set)

    @staticmethod
    def random_day(start: datetime, end: datetime) -> datetime:
        """
        在日期范围内生成随机日期（时分秒归零）。

        :param start: 起始日期（含）
        :param end: 结束日期（不含）
        :return: 范围内的随机日期
        """
        delta = (end - start).days
        if delta <= 0:
            raise ValueError("结束日期必须晚于开始日期")
        random_days = secrets.randbelow(delta)
        return start + timedelta(days=random_days)

    @staticmethod
    def random_ints(count: int, min_include: int = 0, max_exclude: int = 100) -> List[int]:
        """
        生成指定个数的随机整数列表（可重复）。

        :param count: 个数
        :param min_include: 最小值（含）
        :param max_exclude: 最大值（不含）
        :return: 随机整数列表
        """
        return [secrets.randbelow(max_exclude - min_include) + min_include for _ in range(count)]

    @staticmethod
    def random_string_without_str(length: int, exclude_chars: str) -> str:
        """
        生成不包含指定字符的随机字符串（大小写字母 + 数字）。

        :param length: 字符串长度
        :param exclude_chars: 需要排除的字符
        :return: 随机字符串
        """
        base = string.ascii_letters + string.digits
        filtered = "".join(c for c in base if c not in exclude_chars)
        if not filtered:
            raise ValueError("排除后字符集为空")
        return "".join(secrets.choice(filtered) for _ in range(length))

    @staticmethod
    def random_string_lower_without_str(length: int, exclude_chars: str) -> str:
        """
        生成不包含指定字符的随机小写字符串。

        :param length: 字符串长度
        :param exclude_chars: 需要排除的字符
        :return: 随机小写字符串
        """
        base = string.ascii_lowercase + string.digits
        filtered = "".join(c for c in base if c not in exclude_chars)
        if not filtered:
            raise ValueError("排除后字符集为空")
        return "".join(secrets.choice(filtered) for _ in range(length))

    @staticmethod
    def random_element_weighted(pairs: List[Tuple[int, Any]]) -> Any:
        """
        根据权重随机选择（:meth:`weighted_choice` 的别名）。

        :param pairs: 权重-值对列表
        :return: 随机选中的值
        """
        return RandomUtil.weighted_choice(pairs)

    @staticmethod
    def random_ele_with_condition(sequence: Sequence[T], condition, count: int = 1) -> List[T]:
        """
        按条件随机选取元素。

        :param sequence: 待选取的序列
        :param condition: 过滤函数，接受元素返回 bool
        :param count: 选取个数，默认 1
        :return: 满足条件的随机元素列表
        """
        filtered = [item for item in sequence if condition(item)]
        if not filtered:
            return []
        actual_count = min(count, len(filtered))
        return random.sample(filtered, actual_count)

    # ------------------------------------------------------------------
    # SecureRandom 工厂方法
    # ------------------------------------------------------------------

    @staticmethod
    def create_secure_random(seed: Optional[bytes] = None) -> "random.Random":
        """
        创建随机数生成器实例。

        :param seed: 随机种子，None 表示使用系统熵
        :return: random.Random 实例
        """
        rng = random.Random()
        if seed is not None:
            rng.seed(seed)
        return rng

    @staticmethod
    def get_secure_random() -> "random.Random":
        """
        获取默认随机数生成器。

        :return: random.Random 实例
        """
        return random.Random()

    @staticmethod
    def get_secure_random_strong() -> "random.Random":
        """
        获取强随机数生成器（使用系统熵）。

        :return: random.Random 实例
        """
        return random.Random(secrets.token_bytes(32))

    # ------------------------------------------------------------------
    # 扩展随机数生成
    # ------------------------------------------------------------------

    @staticmethod
    def random_int_with_bound(
        min_include: int = 0,
        max_exclude: int = 100,
        include_min: bool = True,
        include_max: bool = False,
    ) -> int:
        """
        带边界控制的随机整数。

        :param min_include: 最小值
        :param max_exclude: 最大值
        :param include_min: 是否包含最小值，默认 True
        :param include_max: 是否包含最大值，默认 False
        :return: 随机整数
        """
        low = min_include if include_min else min_include + 1
        high = max_exclude if not include_max else max_exclude + 1
        if low >= high:
            raise ValueError(f"无效范围: [{low}, {high})")
        return secrets.randbelow(high - low) + low

    @staticmethod
    def random_ints_permutation(count: int) -> List[int]:
        """
        生成 [0, count) 的随机排列。

        :param count: 数量
        :return: 随机排列列表
        """
        lst = list(range(count))
        random.shuffle(lst)
        return lst

    @staticmethod
    def random_number_char() -> str:
        """
        生成随机数字字符（'0'-'9'）。

        :return: 随机数字字符
        """
        return str(secrets.randbelow(10))

    @staticmethod
    def random_char_no_arg() -> str:
        """
        从大小写字母+数字中随机取一个字符（无参版本）。

        :return: 随机字符
        """
        base = string.ascii_letters + string.digits
        return secrets.choice(base)

    @staticmethod
    def random_ele_list(sequence: Sequence[T], count: int) -> List[T]:
        """
        从序列中随机选取不重复的元素列表。

        :param sequence: 待选取的序列
        :param count: 选取个数
        :return: 不重复的随机元素列表
        """
        return RandomUtil.random_eles(sequence, count, allow_duplicate=False)

    @staticmethod
    def random_ele_set(sequence: Sequence[T], count: int) -> set:
        """
        从序列中随机选取不重复的元素集合。

        :param sequence: 待选取的序列
        :param count: 选取个数
        :return: 不重复的随机元素集合
        """
        return set(RandomUtil.random_eles(sequence, count, allow_duplicate=False))

    @staticmethod
    def random_ele_from_first_n(sequence: Sequence[T], limit: int) -> T:
        """
        从前 limit 个元素中随机选取一个。

        :param sequence: 待选取的序列
        :param limit: 限制范围
        :return: 随机元素
        :raises ValueError: 序列为空或 limit <= 0
        """
        if not sequence:
            raise ValueError("序列不能为空")
        if limit <= 0:
            raise ValueError("limit 必须大于 0")
        actual_limit = min(limit, len(sequence))
        return random.choice(list(sequence)[:actual_limit])

    @staticmethod
    def weight_random(pairs: List[Tuple[int, Any]]) -> Any:
        """
        创建加权随机生成器（weighted_choice 的别名）。

        :param pairs: 权重-值对列表
        :return: 随机选中的值
        """
        return RandomUtil.weighted_choice(pairs)

    @staticmethod
    def random_datetime(
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> datetime:
        """生成指定范围内的随机 datetime。

        :param start: 起始时间，默认 2000-01-01
        :param end: 结束时间，默认当前时间
        :return: 随机 datetime 对象
        """
        if start is None:
            start = datetime(2000, 1, 1)
        if end is None:
            end = datetime.now()
        delta = end - start
        random_seconds = random.uniform(0, delta.total_seconds())
        return start + timedelta(seconds=random_seconds)

    @staticmethod
    def random_date_obj(
        start: Optional[date] = None,
        end: Optional[date] = None,
    ) -> date:
        """生成指定范围内的随机 date。

        :param start: 起始日期，默认 2000-01-01
        :param end: 结束日期，默认今日
        :return: 随机 date 对象
        """
        if start is None:
            start = date(2000, 1, 1)
        if end is None:
            end = date.today()
        delta = (end - start).days
        if delta < 0:
            raise ValueError("start 必须早于 end")
        random_days = random.randint(0, delta)
        return start + timedelta(days=random_days)

    @staticmethod
    def random_digits(length: int) -> str:
        """生成指定长度的随机数字字符串。

        :param length: 字符串长度
        :return: 仅包含数字的随机字符串
        :raises ValueError: 长度小于 0
        """
        if length < 0:
            raise ValueError("length 必须大于等于 0")
        return "".join(random.choices("0123456789", k=length))

    @staticmethod
    def random_alphanumeric(length: int) -> str:
        """生成指定长度的随机字母数字字符串。

        :param length: 字符串长度
        :return: 仅包含字母和数字的随机字符串
        :raises ValueError: 长度小于 0
        """
        if length < 0:
            raise ValueError("length 必须大于等于 0")
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return "".join(random.choices(chars, k=length))

    @staticmethod
    def random_upper_ascii(length: int) -> str:
        """生成指定长度的随机大写字母字符串。

        :param length: 字符串长度
        :return: 仅包含大写字母的随机字符串
        :raises ValueError: 长度小于 0
        """
        if length < 0:
            raise ValueError("length 必须大于等于 0")
        return "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=length))


class WeightedRand:
    """加权随机类，支持按概率选取。

    构造时传入权重-值对列表，之后每次调用 ``pick()`` 按权重随机选取一个值。

    ::

        >>> from hutool.core.util.randoms import WeightedRand
        >>> wr = WeightedRand([(1, "a"), (3, "b"), (6, "c")])
        >>> wr.pick()  # "a" 概率 10%, "b" 概率 30%, "c" 概率 60%
    """

    def __init__(self, pairs: List[Tuple[int, Any]]) -> None:
        """初始化加权随机生成器。

        :param pairs: 权重-值对列表 ``[(weight, value), ...]``
        """
        self._values = []  # type: list
        self._weights = []  # type: list
        for weight, value in pairs:
            if weight < 0:
                raise ValueError("权重不能为负数")
            self._values.append(value)
            self._weights.append(weight)
        if not self._values:
            raise ValueError("pairs 不能为空")
        self._total = sum(self._weights)

    def pick(self) -> Any:
        """按权重随机选取一个值。

        :return: 选中的值
        """
        r = random.uniform(0, self._total)
        cumulative = 0
        for weight, value in zip(self._weights, self._values):
            cumulative += weight
            if r <= cumulative:
                return value
        return self._values[-1]

    def picks(self, n: int) -> list:
        """按权重随机选取 N 个值（可重复）。

        :param n: 选取次数
        :return: 选中的值列表
        """
        return [self.pick() for _ in range(n)]
