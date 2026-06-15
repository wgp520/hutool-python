"""
日期时间工具模块，对应 Java Hutool 的 cn.hutool.core.date.DateUtil 和 cn.hutool.core.date.DateTime。

使用 pendulum 作为底层日期时间库，提供丰富的日期操作方法。
"""

from __future__ import annotations

import time as _time
from datetime import date, datetime, timedelta
from typing import List, Optional, Union

import pendulum
from pendulum import DateTime as PendulumDateTime


class DateTime:
    """日期时间封装类，包装 pendulum.DateTime。

    与 Java Hutool 的 cn.hutool.core.date.DateTime 对应，
    对 pendulum 的 DateTime 进行封装，提供链式调用和便捷方法。
    """

    def __init__(self, dt: Union[datetime, str, PendulumDateTime, DateTime, None] = None):
        """构造 DateTime 对象。

        :param dt: 可以是 None（当前时间）、字符串（自动解析）、
            datetime 对象、pendulum.DateTime 或另一个 DateTime。
        """
        if dt is None:
            self._dt: PendulumDateTime = pendulum.now()
        elif isinstance(dt, DateTime):
            self._dt = dt._dt
        elif isinstance(dt, str):
            self._dt = pendulum.parse(dt)
        elif isinstance(dt, datetime):
            self._dt = pendulum.instance(dt)
        elif isinstance(dt, PendulumDateTime):
            self._dt = dt
        else:
            raise TypeError(f"不支持的类型: {type(dt)}")

    @property
    def dt(self) -> PendulumDateTime:
        """获取内部 pendulum.DateTime 对象。"""
        return self._dt

    # ---- 日期部分获取 ----

    def year(self) -> int:
        """
        获取年份。

        :return: 年份
        """
        return self._dt.year

    def month(self) -> int:
        """
        获取月份（1-12）。

        :return: 月份
        """
        return self._dt.month

    def day_of_month(self) -> int:
        """
        获取日（1-31）。

        :return: 日
        """
        return self._dt.day

    def hour(self) -> int:
        """
        获取小时（0-23）。

        :return: 小时
        """
        return self._dt.hour

    def minute(self) -> int:
        """
        获取分钟（0-59）。

        :return: 分钟
        """
        return self._dt.minute

    def second(self) -> int:
        """
        获取秒（0-59）。

        :return: 秒
        """
        return self._dt.second

    def day_of_week(self) -> int:
        """
        获取星期几（ISO 标准：1=周一, 7=周日）。

        :return: 星期几（1-7）
        """
        return self._dt.isoweekday()

    def quarter(self) -> int:
        """
        获取季度（1-4）。

        :return: 季度
        """
        return (self._dt.month - 1) // 3 + 1

    def week_of_year(self) -> int:
        """
        获取一年中的第几周（ISO 标准）。

        :return: 周数
        """
        return self._dt.week_of_year

    # ---- 格式化与转换 ----

    def to_str(self, fmt: str = "YYYY-MM-DD HH:mm:ss") -> str:
        """格式化为字符串。

        :param fmt: 格式化模式，使用 pendulum 的格式化占位符。
        :return: 格式化后的字符串。
        """
        return self._dt.format(fmt)

    def to_date(self) -> date:
        """
        转换为 date 对象。

        :return: date 对象
        """
        return self._dt.date()

    def to_datetime(self) -> datetime:
        """
        转换为标准 datetime 对象。

        :return: datetime 对象
        """
        return self._dt

    # ---- 日期偏移 ----

    def offset(self, **kwargs) -> DateTime:
        """偏移日期时间。

        :param kwargs: 偏移参数，支持 years, months, weeks, days, hours, minutes, seconds。
        :return: 偏移后的新 DateTime 对象。

        示例:
            DateTime().offset(days=1)       # 明天此时
            DateTime().offset(months=-1)    # 上月此时
        """
        return DateTime(self._dt.add(**kwargs))

    def begin_of_day(self) -> DateTime:
        """
        获取当天开始时间（00:00:00）。

        :return: 当天开始的 DateTime 对象
        """
        return DateTime(self._dt.start_of("day"))

    def end_of_day(self) -> DateTime:
        """
        获取当天结束时间（23:59:59.999999）。

        :return: 当天结束的 DateTime 对象
        """
        return DateTime(self._dt.end_of("day"))

    def begin_of_month(self) -> DateTime:
        """
        获取当月开始时间。

        :return: 当月开始的 DateTime 对象
        """
        return DateTime(self._dt.start_of("month"))

    def end_of_month(self) -> DateTime:
        """
        获取当月结束时间。

        :return: 当月结束的 DateTime 对象
        """
        return DateTime(self._dt.end_of("month"))

    def begin_of_year(self) -> DateTime:
        """
        获取当年开始时间。

        :return: 当年开始的 DateTime 对象
        """
        return DateTime(self._dt.start_of("year"))

    def end_of_year(self) -> DateTime:
        """
        获取当年结束时间。

        :return: 当年结束的 DateTime 对象
        """
        return DateTime(self._dt.end_of("year"))

    def begin_of_week(self) -> DateTime:
        """
        获取本周开始时间（周一）。

        :return: 本周开始的 DateTime 对象
        """
        return DateTime(self._dt.start_of("week"))

    def end_of_week(self) -> DateTime:
        """
        获取本周结束时间（周日）。

        :return: 本周结束的 DateTime 对象
        """
        return DateTime(self._dt.end_of("week"))

    def begin_of_quarter(self) -> DateTime:
        """
        获取本季度开始时间。

        :return: 本季度开始的 DateTime 对象
        """
        return DateTime(self._dt.start_of("quarter"))

    def end_of_quarter(self) -> DateTime:
        """
        获取本季度结束时间。

        :return: 本季度结束的 DateTime 对象
        """
        return DateTime(self._dt.end_of("quarter"))

    # ---- 魔术方法 ----

    def __repr__(self) -> str:
        return f"DateTime('{self._dt.to_datetime_string()}')"

    def __str__(self) -> str:
        return self._dt.to_datetime_string()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DateTime):
            return self._dt == other._dt
        if isinstance(other, datetime):
            return self._dt == pendulum.instance(other)
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, DateTime):
            return self._dt < other._dt
        if isinstance(other, datetime):
            return self._dt < pendulum.instance(other)
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, DateTime):
            return self._dt > other._dt
        if isinstance(other, datetime):
            return self._dt > pendulum.instance(other)
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, DateTime):
            return self._dt <= other._dt
        if isinstance(other, datetime):
            return self._dt <= pendulum.instance(other)
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, DateTime):
            return self._dt >= other._dt
        if isinstance(other, datetime):
            return self._dt >= pendulum.instance(other)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._dt)

    def __sub__(self, other: object) -> timedelta:
        if isinstance(other, DateTime):
            return self._dt - other._dt
        if isinstance(other, datetime):
            return self._dt - pendulum.instance(other)
        return NotImplemented

    def __add__(self, other: object) -> DateTime:
        if isinstance(other, timedelta):
            return DateTime(self._dt + other)
        return NotImplemented


def _to_pendulum(dt: Union[DateTime, datetime, PendulumDateTime]) -> PendulumDateTime:
    """将各种日期类型统一转换为 pendulum.DateTime。

    :param dt: DateTime、datetime 或 pendulum.DateTime 对象。
    :return: pendulum.DateTime 对象。
    """
    if isinstance(dt, DateTime):
        return dt.dt
    if isinstance(dt, PendulumDateTime):
        return dt
    if isinstance(dt, datetime):
        return pendulum.instance(dt)
    if isinstance(dt, date):
        return pendulum.instance(datetime(dt.year, dt.month, dt.day))
    raise TypeError(f"不支持的日期类型: {type(dt)}")


class DateUtil:
    """日期工具类，对应 Java cn.hutool.core.date.DateUtil。

    提供静态方法，用于日期的创建、格式化、解析、偏移、比较、时间差计算等操作。
    """

    # ---- 格式常量 ----

    NORM_DATETIME_PATTERN: str = "YYYY-MM-DD HH:mm:ss"
    """标准日期时间格式：yyyy-MM-dd HH:mm:ss"""

    NORM_DATE_PATTERN: str = "YYYY-MM-DD"
    """标准日期格式：yyyy-MM-dd"""

    NORM_TIME_PATTERN: str = "HH:mm:ss"
    """标准时间格式：HH:mm:ss"""

    ISO8601_PATTERN: str = "YYYY-MM-DDTHH:mm:ssZ"
    """ISO 8601 格式"""

    # ================================================================
    # 基础方法
    # ================================================================

    @staticmethod
    def date() -> DateTime:
        """获取当前日期时间。

        :return: 当前时间的 DateTime 对象。
        """
        return DateTime()

    @staticmethod
    def now() -> str:
        """获取当前时间的标准格式字符串（yyyy-MM-dd HH:mm:ss）。

        :return: 当前时间字符串。
        """
        return pendulum.now().format(DateUtil.NORM_DATETIME_PATTERN)

    @staticmethod
    def today() -> str:
        """获取今天日期的标准格式字符串（yyyy-MM-dd）。

        :return: 今天日期字符串。
        """
        return pendulum.now().format(DateUtil.NORM_DATE_PATTERN)

    @staticmethod
    def current(is_millis: bool = True) -> int:
        """获取当前时间戳。

        :param is_millis: True 返回毫秒时间戳，False 返回秒级时间戳。
        :return: 当前时间戳。
        """
        if is_millis:
            return int(_time.time() * 1000)
        return int(_time.time())

    @staticmethod
    def current_seconds() -> int:
        """获取当前秒级时间戳。

        :return: 秒级时间戳。
        """
        return int(_time.time())

    # ================================================================
    # 格式化方法
    # ================================================================

    @staticmethod
    def format(dt: Union[DateTime, datetime, date], fmt: str = "YYYY-MM-DD HH:mm:ss") -> str:
        """格式化日期时间。

        :param dt: 日期时间对象。
        :param fmt: 格式化模式（使用 pendulum 占位符）。
        :return: 格式化后的字符串。
        """
        if isinstance(dt, date) and not isinstance(dt, datetime):
            return pendulum.instance(datetime(dt.year, dt.month, dt.day)).format(fmt)
        pd = _to_pendulum(dt)
        return pd.format(fmt)

    @staticmethod
    def format_date_time(dt: Union[DateTime, datetime]) -> str:
        """格式化为标准日期时间字符串（yyyy-MM-dd HH:mm:ss）。

        :param dt: 日期时间对象。
        :return: 格式化后的字符串。
        """
        return DateUtil.format(dt, DateUtil.NORM_DATETIME_PATTERN)

    @staticmethod
    def format_date(dt: Union[DateTime, datetime, date]) -> str:
        """格式化为标准日期字符串（yyyy-MM-dd）。

        :param dt: 日期时间对象。
        :return: 格式化后的字符串。
        """
        return DateUtil.format(dt, DateUtil.NORM_DATE_PATTERN)

    @staticmethod
    def format_time(dt: Union[DateTime, datetime]) -> str:
        """格式化为标准时间字符串（HH:mm:ss）。

        :param dt: 日期时间对象。
        :return: 格式化后的字符串。
        """
        return DateUtil.format(dt, DateUtil.NORM_TIME_PATTERN)

    # ================================================================
    # 解析方法
    # ================================================================

    @staticmethod
    def parse(date_str: str, fmt: Optional[str] = None) -> DateTime:
        """解析日期时间字符串。

        :param date_str: 日期时间字符串。
        :param fmt: 格式化模式，为 None 时自动识别。
        :return: DateTime 对象。
        """
        if fmt is not None:
            dt = pendulum.from_format(date_str, fmt)
            return DateTime(dt)
        return DateTime(pendulum.parse(date_str))

    @staticmethod
    def parse_date_time(date_str: str) -> DateTime:
        """解析标准日期时间字符串（yyyy-MM-dd HH:mm:ss）。

        :param date_str: 日期时间字符串，如 "2023-10-01 12:30:00"。
        :return: DateTime 对象。
        """
        return DateUtil.parse(date_str, DateUtil.NORM_DATETIME_PATTERN)

    @staticmethod
    def parse_date(date_str: str) -> DateTime:
        """解析标准日期字符串（yyyy-MM-dd）。

        :param date_str: 日期字符串，如 "2023-10-01"。
        :return: DateTime 对象。
        """
        return DateUtil.parse(date_str, DateUtil.NORM_DATE_PATTERN)

    @staticmethod
    def parse_time(time_str: str) -> DateTime:
        """解析标准时间字符串（HH:mm:ss），日期部分取今天。

        :param time_str: 时间字符串，如 "12:30:00"。
        :return: DateTime 对象。
        """
        today = pendulum.today()
        parts = time_str.split(":")
        h = int(parts[0]) if len(parts) > 0 else 0
        m = int(parts[1]) if len(parts) > 1 else 0
        s = int(parts[2]) if len(parts) > 2 else 0
        return DateTime(today.set(hour=h, minute=m, second=s))

    @staticmethod
    def parse_iso8601(iso_str: str) -> DateTime:
        """解析 ISO 8601 格式字符串。

        :param iso_str: ISO 8601 格式字符串，如 "2023-10-01T12:30:00+08:00"。
        :return: DateTime 对象。
        """
        return DateTime(pendulum.parse(iso_str))

    # ================================================================
    # 日期部分提取（静态方法版本）
    # ================================================================

    @staticmethod
    def year(dt: Union[DateTime, datetime]) -> int:
        """获取年份。

        :param dt: 日期时间对象。
        :return: 年份。
        """
        return _to_pendulum(dt).year

    @staticmethod
    def month(dt: Union[DateTime, datetime]) -> int:
        """获取月份（1-12）。

        :param dt: 日期时间对象。
        :return: 月份。
        """
        return _to_pendulum(dt).month

    @staticmethod
    def day_of_month(dt: Union[DateTime, datetime]) -> int:
        """获取日（1-31）。

        :param dt: 日期时间对象。
        :return: 日。
        """
        return _to_pendulum(dt).day

    @staticmethod
    def hour(dt: Union[DateTime, datetime]) -> int:
        """获取小时（0-23）。

        :param dt: 日期时间对象。
        :return: 小时。
        """
        return _to_pendulum(dt).hour

    @staticmethod
    def minute(dt: Union[DateTime, datetime]) -> int:
        """获取分钟（0-59）。

        :param dt: 日期时间对象。
        :return: 分钟。
        """
        return _to_pendulum(dt).minute

    @staticmethod
    def second(dt: Union[DateTime, datetime]) -> int:
        """获取秒（0-59）。

        :param dt: 日期时间对象。
        :return: 秒。
        """
        return _to_pendulum(dt).second

    @staticmethod
    def day_of_week(dt: Union[DateTime, datetime]) -> int:
        """获取星期几（ISO 标准：1=周一, 7=周日）。

        :param dt: 日期时间对象。
        :return: 星期几（1-7）。
        """
        return _to_pendulum(dt).isoweekday()

    @staticmethod
    def quarter(dt: Union[DateTime, datetime]) -> int:
        """获取季度（1-4）。

        :param dt: 日期时间对象。
        :return: 季度。
        """
        return (_to_pendulum(dt).month - 1) // 3 + 1

    @staticmethod
    def week_of_year(dt: Union[DateTime, datetime]) -> int:
        """获取一年中的第几周（ISO 标准）。

        :param dt: 日期时间对象。
        :return: 周数。
        """
        return _to_pendulum(dt).week_of_year

    @staticmethod
    def is_weekend(dt: Union[DateTime, datetime]) -> bool:
        """判断是否为周末（周六或周日）。

        :param dt: 日期时间对象。
        :return: 是否为周末。
        """
        return _to_pendulum(dt).isoweekday() >= 6

    @staticmethod
    def is_am(dt: Union[DateTime, datetime]) -> bool:
        """判断是否为上午。

        :param dt: 日期时间对象。
        :return: 是否为上午。
        """
        return _to_pendulum(dt).hour < 12

    @staticmethod
    def is_pm(dt: Union[DateTime, datetime]) -> bool:
        """判断是否为下午。

        :param dt: 日期时间对象。
        :return: 是否为下午。
        """
        return _to_pendulum(dt).hour >= 12

    # ================================================================
    # 偏移方法
    # ================================================================

    @staticmethod
    def offset_day(dt: Union[DateTime, datetime], n: int) -> DateTime:
        """偏移天数。

        :param dt: 日期时间对象。
        :param n: 偏移天数，正数向后，负数向前。
        :return: 偏移后的 DateTime 对象。
        """
        return DateTime(_to_pendulum(dt).add(days=n))

    @staticmethod
    def offset_week(dt: Union[DateTime, datetime], n: int) -> DateTime:
        """偏移周数。

        :param dt: 日期时间对象。
        :param n: 偏移周数。
        :return: 偏移后的 DateTime 对象。
        """
        return DateTime(_to_pendulum(dt).add(weeks=n))

    @staticmethod
    def offset_month(dt: Union[DateTime, datetime], n: int) -> DateTime:
        """偏移月数。

        :param dt: 日期时间对象。
        :param n: 偏移月数。
        :return: 偏移后的 DateTime 对象。
        """
        return DateTime(_to_pendulum(dt).add(months=n))

    @staticmethod
    def offset_year(dt: Union[DateTime, datetime], n: int) -> DateTime:
        """偏移年数。

        :param dt: 日期时间对象。
        :param n: 偏移年数。
        :return: 偏移后的 DateTime 对象。
        """
        return DateTime(_to_pendulum(dt).add(years=n))

    @staticmethod
    def offset_hour(dt: Union[DateTime, datetime], n: int) -> DateTime:
        """偏移小时数。

        :param dt: 日期时间对象。
        :param n: 偏移小时数。
        :return: 偏移后的 DateTime 对象。
        """
        return DateTime(_to_pendulum(dt).add(hours=n))

    @staticmethod
    def offset_minute(dt: Union[DateTime, datetime], n: int) -> DateTime:
        """偏移分钟数。

        :param dt: 日期时间对象。
        :param n: 偏移分钟数。
        :return: 偏移后的 DateTime 对象。
        """
        return DateTime(_to_pendulum(dt).add(minutes=n))

    @staticmethod
    def offset_second(dt: Union[DateTime, datetime], n: int) -> DateTime:
        """偏移秒数。

        :param dt: 日期时间对象。
        :param n: 偏移秒数。
        :return: 偏移后的 DateTime 对象。
        """
        return DateTime(_to_pendulum(dt).add(seconds=n))

    @staticmethod
    def yesterday() -> DateTime:
        """获取昨天的日期。

        :return: 昨天的 DateTime 对象。
        """
        return DateTime(pendulum.yesterday())

    @staticmethod
    def tomorrow() -> DateTime:
        """获取明天的日期。

        :return: 明天的 DateTime 对象。
        """
        return DateTime(pendulum.tomorrow())

    @staticmethod
    def last_week() -> DateTime:
        """获取上周的今天。

        :return: 上周今天的 DateTime 对象。
        """
        return DateTime(pendulum.now().subtract(weeks=1))

    @staticmethod
    def next_week() -> DateTime:
        """获取下周的今天。

        :return: 下周今天的 DateTime 对象。
        """
        return DateTime(pendulum.now().add(weeks=1))

    @staticmethod
    def last_month() -> DateTime:
        """获取上月的今天。

        :return: 上月今天的 DateTime 对象。
        """
        return DateTime(pendulum.now().subtract(months=1))

    @staticmethod
    def next_month() -> DateTime:
        """获取下月的今天。

        :return: 下月今天的 DateTime 对象。
        """
        return DateTime(pendulum.now().add(months=1))

    # ================================================================
    # 开始 / 结束方法
    # ================================================================

    @staticmethod
    def begin_of_day(dt: Union[DateTime, datetime, None] = None) -> DateTime:
        """获取一天的开始时间（00:00:00）。

        :param dt: 日期时间对象，为 None 时取当前时间。
        :return: 当天开始的 DateTime 对象。
        """
        pd = _to_pendulum(dt) if dt is not None else pendulum.now()
        return DateTime(pd.start_of("day"))

    @staticmethod
    def end_of_day(dt: Union[DateTime, datetime, None] = None) -> DateTime:
        """获取一天的结束时间（23:59:59.999999）。

        :param dt: 日期时间对象，为 None 时取当前时间。
        :return: 当天结束的 DateTime 对象。
        """
        pd = _to_pendulum(dt) if dt is not None else pendulum.now()
        return DateTime(pd.end_of("day"))

    @staticmethod
    def begin_of_week(dt: Union[DateTime, datetime, None] = None) -> DateTime:
        """获取一周的开始时间（周一 00:00:00）。

        :param dt: 日期时间对象，为 None 时取当前时间。
        :return: 本周开始的 DateTime 对象。
        """
        pd = _to_pendulum(dt) if dt is not None else pendulum.now()
        return DateTime(pd.start_of("week"))

    @staticmethod
    def end_of_week(dt: Union[DateTime, datetime, None] = None) -> DateTime:
        """获取一周的结束时间（周日 23:59:59.999999）。

        :param dt: 日期时间对象，为 None 时取当前时间。
        :return: 本周结束的 DateTime 对象。
        """
        pd = _to_pendulum(dt) if dt is not None else pendulum.now()
        return DateTime(pd.end_of("week"))

    @staticmethod
    def begin_of_month(dt: Union[DateTime, datetime, None] = None) -> DateTime:
        """获取一月的开始时间（1号 00:00:00）。

        :param dt: 日期时间对象，为 None 时取当前时间。
        :return: 本月开始的 DateTime 对象。
        """
        pd = _to_pendulum(dt) if dt is not None else pendulum.now()
        return DateTime(pd.start_of("month"))

    @staticmethod
    def end_of_month(dt: Union[DateTime, datetime, None] = None) -> DateTime:
        """获取一月的结束时间（月末 23:59:59.999999）。

        :param dt: 日期时间对象，为 None 时取当前时间。
        :return: 本月结束的 DateTime 对象。
        """
        pd = _to_pendulum(dt) if dt is not None else pendulum.now()
        return DateTime(pd.end_of("month"))

    @staticmethod
    def begin_of_quarter(dt: Union[DateTime, datetime, None] = None) -> DateTime:
        """获取一季度的开始时间。

        :param dt: 日期时间对象，为 None 时取当前时间。
        :return: 本季度开始的 DateTime 对象。
        """
        pd = _to_pendulum(dt) if dt is not None else pendulum.now()
        return DateTime(pd.start_of("quarter"))

    @staticmethod
    def end_of_quarter(dt: Union[DateTime, datetime, None] = None) -> DateTime:
        """获取一季度的结束时间。

        :param dt: 日期时间对象，为 None 时取当前时间。
        :return: 本季度结束的 DateTime 对象。
        """
        pd = _to_pendulum(dt) if dt is not None else pendulum.now()
        return DateTime(pd.end_of("quarter"))

    @staticmethod
    def begin_of_year(dt: Union[DateTime, datetime, None] = None) -> DateTime:
        """获取一年的开始时间（1月1日 00:00:00）。

        :param dt: 日期时间对象，为 None 时取当前时间。
        :return: 本年开始的 DateTime 对象。
        """
        pd = _to_pendulum(dt) if dt is not None else pendulum.now()
        return DateTime(pd.start_of("year"))

    @staticmethod
    def end_of_year(dt: Union[DateTime, datetime, None] = None) -> DateTime:
        """获取一年的结束时间（12月31日 23:59:59.999999）。

        :param dt: 日期时间对象，为 None 时取当前时间。
        :return: 本年结束的 DateTime 对象。
        """
        pd = _to_pendulum(dt) if dt is not None else pendulum.now()
        return DateTime(pd.end_of("year"))

    # ================================================================
    # 时间差计算
    # ================================================================

    @staticmethod
    def between(
        start: Union[DateTime, datetime],
        end: Union[DateTime, datetime],
        unit: str = "ms",
    ) -> int:
        """计算两个时间之间的差值。

        :param start: 起始时间。
        :param end: 结束时间。
        :param unit: 单位，可选值：ms(毫秒)、s(秒)、min(分钟)、hour(小时)、
            day(天)、week(周)、month(月)、year(年)。
        :return: 时间差（整数）。
        """
        pd_start = _to_pendulum(start)
        pd_end = _to_pendulum(end)
        diff = pd_start.diff(pd_end)

        unit_lower = unit.lower()
        if unit_lower in ("ms", "millis", "millisecond", "milliseconds"):
            return diff.in_seconds() * 1000 + diff.microseconds // 1000
        elif unit_lower in ("s", "sec", "second", "seconds"):
            return diff.in_seconds()
        elif unit_lower in ("min", "minute", "minutes"):
            return diff.in_minutes()
        elif unit_lower in ("h", "hour", "hours"):
            return diff.in_hours()
        elif unit_lower in ("d", "day", "days"):
            return diff.in_days()
        elif unit_lower in ("w", "week", "weeks"):
            return diff.in_weeks()
        elif unit_lower in ("mon", "month", "months"):
            return diff.in_months()
        elif unit_lower in ("y", "year", "years"):
            return diff.in_years()
        else:
            raise ValueError(f"不支持的时间单位: {unit}")

    @staticmethod
    def between_ms(
        start: Union[DateTime, datetime],
        end: Union[DateTime, datetime],
    ) -> int:
        """计算两个时间之间的毫秒差。

        :param start: 起始时间。
        :param end: 结束时间。
        :return: 毫秒差。
        """
        return DateUtil.between(start, end, "ms")

    @staticmethod
    def between_day(
        start: Union[DateTime, datetime],
        end: Union[DateTime, datetime],
        is_reset: bool = False,
    ) -> int:
        """计算两个时间之间的天数差。

        :param start: 起始时间。
        :param end: 结束时间。
        :param is_reset: 是否重置时间为当天开始（忽略时分秒）。
        :return: 天数差。
        """
        pd_start = _to_pendulum(start)
        pd_end = _to_pendulum(end)
        if is_reset:
            pd_start = pd_start.start_of("day")
            pd_end = pd_end.start_of("day")
        return pd_start.diff(pd_end).in_days()

    @staticmethod
    def between_week(
        start: Union[DateTime, datetime],
        end: Union[DateTime, datetime],
        is_reset: bool = False,
    ) -> int:
        """计算两个时间之间的周数差。

        :param start: 起始时间。
        :param end: 结束时间。
        :param is_reset: 是否重置时间为当天开始。
        :return: 周数差。
        """
        pd_start = _to_pendulum(start)
        pd_end = _to_pendulum(end)
        if is_reset:
            pd_start = pd_start.start_of("day")
            pd_end = pd_end.start_of("day")
        return pd_start.diff(pd_end).in_weeks()

    @staticmethod
    def between_month(
        start: Union[DateTime, datetime],
        end: Union[DateTime, datetime],
        is_reset: bool = False,
    ) -> int:
        """计算两个时间之间的月数差。

        :param start: 起始时间。
        :param end: 结束时间。
        :param is_reset: 是否重置时间为当月开始。
        :return: 月数差。
        """
        pd_start = _to_pendulum(start)
        pd_end = _to_pendulum(end)
        if is_reset:
            pd_start = pd_start.start_of("month")
            pd_end = pd_end.start_of("month")
        return pd_start.diff(pd_end).in_months()

    @staticmethod
    def between_year(
        start: Union[DateTime, datetime],
        end: Union[DateTime, datetime],
        is_reset: bool = False,
    ) -> int:
        """计算两个时间之间的年数差。

        :param start: 起始时间。
        :param end: 结束时间。
        :param is_reset: 是否重置时间为当年开始。
        :return: 年数差。
        """
        pd_start = _to_pendulum(start)
        pd_end = _to_pendulum(end)
        if is_reset:
            pd_start = pd_start.start_of("year")
            pd_end = pd_end.start_of("year")
        return pd_start.diff(pd_end).in_years()

    @staticmethod
    def format_between(
        start: Union[DateTime, datetime],
        end: Union[DateTime, datetime],
        level: str = "ms",
    ) -> str:
        """格式化时间差为中文可读字符串。

        根据 level 参数决定精度：
        - "ms":   毫秒级，如 "3天2小时5分10秒123毫秒"
        - "s":    秒级，   如 "3天2小时5分10秒"
        - "min":  分钟级， 如 "3天2小时5分"
        - "hour": 小时级， 如 "3天2小时"
        - "day":  天级，   如 "3天"

        :param start: 起始时间。
        :param end: 结束时间。
        :param level: 精度级别。
        :return: 中文格式的时间差字符串。
        """
        pd_start = _to_pendulum(start)
        pd_end = _to_pendulum(end)

        # 总毫秒数（绝对值）
        total_ms = int(abs((pd_end - pd_start).total_seconds()) * 1000)

        if total_ms == 0:
            return "0毫秒" if level == "ms" else "0秒"

        # 逐步分解
        ms = total_ms
        days = ms // (24 * 3600 * 1000)
        ms %= 24 * 3600 * 1000
        hours = ms // (3600 * 1000)
        ms %= 3600 * 1000
        minutes = ms // (60 * 1000)
        ms %= 60 * 1000
        seconds = ms // 1000
        millis = ms % 1000

        parts: List[str] = []
        if days > 0:
            parts.append(f"{days}天")
        if hours > 0:
            parts.append(f"{hours}小时")
        if minutes > 0:
            parts.append(f"{minutes}分")

        level_lower = level.lower()
        if level_lower in ("ms", "millis", "millisecond", "milliseconds"):
            if seconds > 0:
                parts.append(f"{seconds}秒")
            if millis > 0:
                parts.append(f"{millis}毫秒")
        elif level_lower in ("s", "sec", "second", "seconds"):
            if seconds > 0:
                parts.append(f"{seconds}秒")
        elif level_lower in ("min", "minute", "minutes"):
            pass  # 已经处理到分钟级
        elif level_lower in ("h", "hour", "hours"):
            pass  # 已经处理到小时级
        elif level_lower in ("d", "day", "days"):
            pass  # 已经处理到天级
        else:
            # 默认秒级
            if seconds > 0:
                parts.append(f"{seconds}秒")

        return "".join(parts) if parts else "0秒"

    # ================================================================
    # 比较方法
    # ================================================================

    @staticmethod
    def is_same_day(
        dt1: Union[DateTime, datetime],
        dt2: Union[DateTime, datetime],
    ) -> bool:
        """判断两个时间是否为同一天。

        :param dt1: 第一个时间。
        :param dt2: 第二个时间。
        :return: 是否为同一天。
        """
        pd1 = _to_pendulum(dt1)
        pd2 = _to_pendulum(dt2)
        return pd1.year == pd2.year and pd1.month == pd2.month and pd1.day == pd2.day

    @staticmethod
    def is_same_time(
        dt1: Union[DateTime, datetime],
        dt2: Union[DateTime, datetime],
    ) -> bool:
        """判断两个时间是否为同一时刻。

        :param dt1: 第一个时间。
        :param dt2: 第二个时间。
        :return: 是否为同一时刻。
        """
        return _to_pendulum(dt1) == _to_pendulum(dt2)

    @staticmethod
    def is_in(
        dt: Union[DateTime, datetime],
        start: Union[DateTime, datetime],
        end: Union[DateTime, datetime],
    ) -> bool:
        """判断时间是否在指定范围内 [start, end]（含边界）。

        :param dt: 待判断的时间。
        :param start: 范围起始时间。
        :param end: 范围结束时间。
        :return: 是否在范围内。
        """
        pd = _to_pendulum(dt)
        pd_start = _to_pendulum(start)
        pd_end = _to_pendulum(end)
        return pd_start <= pd <= pd_end

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """判断是否为闰年。

        :param year: 年份。
        :return: 是否为闰年。
        """
        return pendulum.instance(datetime(year, 1, 1)).is_leap_year()

    # ================================================================
    # 计时工具
    # ================================================================

    @staticmethod
    def timer() -> int:
        """返回当前毫秒时间戳（用于计时）。

        :return: 当前毫秒时间戳。
        """
        return int(_time.time() * 1000)

    @staticmethod
    def spend_ms(pre_time: int) -> int:
        """计算从 pre_time 到当前的毫秒差。

        :param pre_time: 之前记录的毫秒时间戳（通过 timer() 获取）。
        :return: 经过的毫秒数。
        """
        return int(_time.time() * 1000) - pre_time

    @staticmethod
    def date_trunc(trunc_type: str, dt: Union[datetime, date]) -> Union[datetime, date]:
        """
        截断日期到指定精度。

        受 PostgreSQL 的 ``date_trunc`` 函数启发。
        支持的截断类型：``year``、``quarter``、``month``、``week``、``day``、``hour``、``minute``、``second``。

        :param trunc_type: 截断类型
        :param dt: 日期或日期时间对象
        :return: 截断后的日期/日期时间对象（类型与输入一致）
        :raises ValueError: 不支持的截断类型时
        """
        is_date_only = isinstance(dt, date) and not isinstance(dt, datetime)
        tmp = dt.timetuple()

        if trunc_type == "year":
            ret = datetime(tmp.tm_year, 1, 1)
        elif trunc_type == "quarter":
            q = (tmp.tm_mon - 1) // 3
            ret = datetime(tmp.tm_year, q * 3 + 1, 1)
        elif trunc_type == "month":
            ret = datetime(tmp.tm_year, tmp.tm_mon, 1)
        elif trunc_type == "week":
            firstday = dt - timedelta(days=tmp.tm_wday)
            ret = datetime(firstday.year, firstday.month, firstday.day)
        elif trunc_type == "day":
            ret = datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday)
        elif trunc_type == "hour":
            ret = datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday, tmp.tm_hour)
        elif trunc_type == "minute":
            ret = datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday, tmp.tm_hour, tmp.tm_min)
        elif trunc_type == "second":
            ret = datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday, tmp.tm_hour, tmp.tm_min, tmp.tm_sec)
        else:
            raise ValueError(f"不支持的截断类型: {trunc_type}")

        return ret.date() if is_date_only else ret

    @staticmethod
    def get_week(dt: Union[datetime, date]):
        """
        获取日期所在年周号。

        返回 ``(week_number, year)`` 元组，其中 ``week_number`` 为周号，
        ``year`` 为该周所属的年份（跨年时可能与 ``dt.year`` 不同）。

        :param dt: 日期或日期时间对象
        :return: ``(week_number, year)`` 元组
        """
        # 截断到周
        week_start = DateUtil.date_trunc("week", dt)
        year_start_week = DateUtil.date_trunc("week", DateUtil.date_trunc("year", dt))
        # 如果年份第一个周一在下一年（如 1 月 1 日是周二~周日），则调整
        if year_start_week.year < dt.year:
            year_start_week = year_start_week + timedelta(weeks=1)
        # 如果 week_start 与 year_start_week 在同一年但跨年了
        if week_start.year > dt.year:
            return 1, week_start.year
        if week_start.year < dt.year:
            diff = DateUtil.date_trunc("day", week_start) - DateUtil.date_trunc(
                "day", DateUtil.date_trunc("week", DateUtil.date_trunc("year", week_start))
            )
            return 1 + diff.days // 7, week_start.year
        diff = DateUtil.date_trunc("day", week_start) - DateUtil.date_trunc("day", year_start_week)
        week = 1 + diff.days // 7
        return week, dt.year

    @staticmethod
    def get_monthspan(dt: Union[datetime, date]):
        """
        获取日期所在月的首日和末日。

        :param dt: 日期或日期时间对象
        :return: ``(首日, 末日)`` 元组，类型与输入一致
        """
        import calendar as _cal

        is_date_only = isinstance(dt, date) and not isinstance(dt, datetime)
        first = datetime(dt.year, dt.month, 1)
        _, last_day = _cal.monthrange(dt.year, dt.month)
        last = datetime(dt.year, dt.month, last_day)
        if is_date_only:
            return first.date(), last.date()
        return first, last

    @staticmethod
    def get_weekspan(dt: Union[datetime, date]):
        """
        获取日期所在周的周一和周日。

        :param dt: 日期或日期时间对象
        :return: ``(周一, 周日)`` 元组，类型与输入一致
        """
        is_date_only = isinstance(dt, date) and not isinstance(dt, datetime)
        monday = dt - timedelta(days=dt.weekday())
        sunday = monday + timedelta(days=6)
        first = datetime(monday.year, monday.month, monday.day)
        last = datetime(sunday.year, sunday.month, sunday.day)
        if is_date_only:
            return first.date(), last.date()
        return first, last

    @staticmethod
    def get_quarterspan(dt: Union[datetime, date]):
        """
        获取日期所在季度的首日和末日。

        :param dt: 日期或日期时间对象
        :return: ``(首日, 末日)`` 元组，类型与输入一致
        """
        is_date_only = isinstance(dt, date) and not isinstance(dt, datetime)
        q = (dt.month - 1) // 3
        start = datetime(dt.year, q * 3 + 1, 1)
        # 季度末日 = 下季度首日 - 1 天
        if q == 3:
            end = datetime(dt.year, 12, 31)
        else:
            end = datetime(dt.year, (q + 1) * 3 + 1, 1) - timedelta(days=1)
        if is_date_only:
            return start.date(), end.date()
        return start, end

    @staticmethod
    def get_yearspan(dt: Union[datetime, date]):
        """
        获取日期所在年的首日和末日。

        :param dt: 日期或日期时间对象
        :return: ``(首日, 末日)`` 元组，类型与输入一致
        """
        is_date_only = isinstance(dt, date) and not isinstance(dt, datetime)
        start = datetime(dt.year, 1, 1)
        end = datetime(dt.year, 12, 31)
        if is_date_only:
            return start.date(), end.date()
        return start, end

    @staticmethod
    def month_add(dt: Union[datetime, date], months: int) -> Union[datetime, date]:
        """
        日期加减指定月数。

        自动处理月末溢出（如 1月31日 + 1月 = 2月28日）。

        :param dt: 日期或日期时间对象
        :param months: 加减月数（正数为加，负数为减）
        :return: 新的日期/日期时间对象
        """
        is_date_only = isinstance(dt, date) and not isinstance(dt, datetime)
        year, month = divmod(dt.year * 12 + dt.month + months - 1, 12)
        month += 1
        import calendar as _cal

        max_day = _cal.monthrange(year, month)[1]
        day = min(dt.day, max_day)
        if is_date_only:
            return date(year, month, day)
        return datetime(year, month, day, dt.hour, dt.minute, dt.second, dt.microsecond)

    @staticmethod
    def rfc3339_date(dt: Optional[datetime] = None) -> str:
        """
        格式化为 RFC 3339 日期字符串。

        例如 ``"2024-01-15T08:30:00Z"``。

        :param dt: 日期时间对象，为 None 时使用当前时间
        :return: RFC 3339 格式字符串
        """
        dt = dt or datetime.now()
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def rfc3339_date_parse(date_str: str) -> datetime:
        """
        解析 RFC 3339 日期字符串为 datetime 对象。

        :param date_str: RFC 3339 格式字符串，如 ``"2024-01-15T08:30:00Z"``
        :return: datetime 对象
        :raises ValueError: 格式不合法时
        """
        date_str = date_str.rstrip("Z")
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def rfc2616_date(dt: Optional[datetime] = None) -> str:
        """
        格式化为 RFC 2616 (HTTP) 日期字符串。

        例如 ``"Mon, 15 Jan 2024 08:30:00 GMT"``。

        :param dt: 日期时间对象，为 None 时使用当前时间
        :return: RFC 2616 格式字符串
        """
        import calendar as _cal
        import email.utils as _eu

        dt = dt or datetime.now()
        timestamp = _cal.timegm(dt.timetuple())
        return _eu.formatdate(timeval=timestamp, usegmt=True)

    @staticmethod
    def rfc2616_date_parse(date_str: str) -> datetime:
        """
        解析 RFC 2616 (HTTP) 日期字符串为 datetime 对象。

        :param date_str: RFC 2616 格式字符串
        :return: datetime 对象
        :raises ValueError: 格式不合法时
        """
        import email.utils as _eu

        timestamp = _eu.mktime_tz(_eu.parsedate_tz(date_str))
        return datetime.fromtimestamp(timestamp)

    @staticmethod
    def age_by_birthday(birthday: Union[str, date, datetime]) -> int:
        """
        根据生日计算年龄。

        :param birthday: 生日，支持 str（``YYYY-MM-DD`` 或 ``YYYYMMDD``）、date、datetime
        :return: 年龄（周岁）
        :raises ValueError: 无法解析生日时
        """
        if isinstance(birthday, str):
            birthday = DateUtil.convert_to_date(birthday)
        if isinstance(birthday, datetime):
            bd = birthday.date()
        elif isinstance(birthday, date):
            bd = birthday
        else:
            raise TypeError(f"不支持的类型: {type(birthday)}")
        today = date.today()
        age = today.year - bd.year
        if (today.month, today.day) < (bd.month, bd.day):
            age -= 1
        return age

    @staticmethod
    def is_same_month(dt1: Union[DateTime, datetime, date], dt2: Union[DateTime, datetime, date]) -> bool:
        """
        判断两个日期是否在同一月（同年同月）。

        :param dt1: 第一个日期
        :param dt2: 第二个日期
        :return: 是否在同一月
        """
        d1 = dt1.date() if isinstance(dt1, datetime) and not isinstance(dt1, date) else dt1
        d2 = dt2.date() if isinstance(dt2, datetime) and not isinstance(dt2, date) else dt2
        if isinstance(d1, DateTime):
            d1 = d1.to_date()
        if isinstance(d2, DateTime):
            d2 = d2.to_date()
        return d1.year == d2.year and d1.month == d2.month

    @staticmethod
    def is_same_week(dt1: Union[DateTime, datetime, date], dt2: Union[DateTime, datetime, date]) -> bool:
        """
        判断两个日期是否在同一周（ISO 周，周一为一周起始）。

        :param dt1: 第一个日期
        :param dt2: 第二个日期
        :return: 是否在同一周
        """
        d1 = dt1.date() if isinstance(dt1, datetime) and not isinstance(dt1, date) else dt1
        d2 = dt2.date() if isinstance(dt2, datetime) and not isinstance(dt2, date) else dt2
        if isinstance(d1, DateTime):
            d1 = d1.to_date()
        if isinstance(d2, DateTime):
            d2 = d2.to_date()
        return d1.isocalendar()[:2] == d2.isocalendar()[:2]

    @staticmethod
    def time_ago(timestamp: Union[int, float]) -> str:
        """
        将时间戳转换为人类可读的相对时间描述。

        例如 ``"3天前"``、``"2小时前"``。

        :param timestamp: Unix 时间戳（秒级）
        :return: 中文相对时间描述

        ::

            >>> DateUtil.time_ago(time.time())     # 刚刚
            '刚刚'
        """
        now = _time.time()
        diff = now - timestamp
        if diff < 0:
            return "刚刚"
        seconds = int(diff)
        if seconds < 60:
            return "刚刚"
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes}分钟前"
        hours = minutes // 60
        if hours < 24:
            return f"{hours}小时前"
        days = hours // 24
        if days < 30:
            return f"{days}天前"
        months = days // 30
        if months < 12:
            return f"{months}个月前"
        years = days // 365
        return f"{years}年前"

    @staticmethod
    def iso_timestamp() -> str:
        """
        获取当前 ISO 8601 格式的时间戳字符串。

        格式为 ``YYYY-MM-DDTHH:MM:SS.mmmZ``。

        :return: ISO 8601 时间戳字符串

        ::

            >>> DateUtil.iso_timestamp()  # doctest: +SKIP
            '2024-01-01T12:00:00.000Z'
        """
        from datetime import datetime as _dt
        from datetime import timezone as _tz

        now = _dt.now(_tz.utc)
        return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"

    @staticmethod
    def convert_to_date(value) -> Optional[date]:
        """
        将各种日期格式统一转换为 ``date`` 对象。

        支持：``datetime``、``date``、``str``（ISO 格式或 ``YYYYMMDD``）。

        :param value: 待转换的值
        :return: date 对象，输入为 None/空时返回 None
        :raises ValueError: 无法识别的格式时
        """
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return None
            # 尝试 YYYY-MM-DD
            if len(value) >= 10:
                try:
                    return datetime.strptime(value[:10], "%Y-%m-%d").date()
                except ValueError:
                    pass
            # 尝试 YYYYMMDD
            if len(value) >= 8:
                try:
                    return datetime.strptime(value[:8], "%Y%m%d").date()
                except ValueError:
                    pass
        raise ValueError(f"无法识别的日期格式: {value!r}")

    @staticmethod
    def convert_to_datetime(value) -> Optional[datetime]:
        """
        将各种日期格式统一转换为 ``datetime`` 对象。

        支持：``datetime``、``date``、``str``（多种 ISO 格式）。

        :param value: 待转换的值
        :return: datetime 对象，输入为 None/空时返回 None
        :raises ValueError: 无法识别的格式时
        """
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime(value.year, value.month, value.day)
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return None
            # 移除 Z 后缀
            if value.endswith("Z"):
                value = value[:-1]
            # 移除时区后缀（如 +0000）
            if " +" in value:
                value = value.split(" +")[0]
            # 各种格式尝试
            for fmt in (
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S.%f",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
                "%Y%m%dT%H%M%S",
                "%Y%m%d",
            ):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
        raise ValueError(f"无法识别的日期时间格式: {value!r}")
