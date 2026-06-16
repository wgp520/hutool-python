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

    # ---- 工厂方法 ----

    @classmethod
    def of(cls, dt: Union[datetime, str, PendulumDateTime, DateTime, None] = None) -> DateTime:
        """工厂方法，等同于构造函数。

        :param dt: 日期时间
        :return: DateTime 对象
        """
        return cls(dt)

    @classmethod
    def of_date(cls, y: int, m: int, d: int) -> DateTime:
        """根据年月日创建 DateTime。

        :param y: 年
        :param m: 月
        :param d: 日
        :return: DateTime 对象
        """
        return cls(pendulum.datetime(y, m, d))

    @classmethod
    def of_datetime(cls, y: int, m: int, d: int, h: int = 0, mi: int = 0, s: int = 0) -> DateTime:
        """根据年月日时分秒创建 DateTime。

        :param y: 年
        :param m: 月
        :param d: 日
        :param h: 时
        :param mi: 分
        :param s: 秒
        :return: DateTime 对象
        """
        return cls(pendulum.datetime(y, m, d, h, mi, s))

    @classmethod
    def of_pattern(cls, date_str: str, fmt: str) -> DateTime:
        """根据格式字符串解析创建 DateTime。

        :param date_str: 日期字符串
        :param fmt: 格式模式，如 "yyyy-MM-dd HH:mm:ss"
        :return: DateTime 对象
        """
        # 将 Java 格式转为 Python strftime 格式
        py_fmt = (
            fmt.replace("yyyy", "%Y")
            .replace("yy", "%y")
            .replace("MM", "%m")
            .replace("dd", "%d")
            .replace("HH", "%H")
            .replace("mm", "%M")
            .replace("ss", "%S")
        )
        dt = datetime.strptime(date_str, py_fmt)
        return cls(dt)

    @classmethod
    def now_utc(cls) -> DateTime:
        """获取 UTC 当前时间的 DateTime。

        :return: DateTime 对象
        """
        return cls(pendulum.now("UTC"))

    @classmethod
    def of_epoch(cls, epoch: Union[int, float], is_millis: bool = True) -> DateTime:
        """根据时间戳创建 DateTime。

        :param epoch: 时间戳
        :param is_millis: 是否为毫秒时间戳
        :return: DateTime 对象
        """
        if is_millis:
            epoch = epoch / 1000
        return cls(datetime.fromtimestamp(epoch))

    # ---- 查询方法 ----

    def is_weekend(self) -> bool:
        """是否为周末。

        :return: 周六或周日返回 True
        """
        return self._dt.isoweekday() in (6, 7)

    def is_am(self) -> bool:
        """是否为上午。

        :return: 上午返回 True
        """
        return self._dt.hour < 12

    def is_pm(self) -> bool:
        """是否为下午。

        :return: 下午返回 True
        """
        return self._dt.hour >= 12

    def is_past(self) -> bool:
        """是否为过去时间。

        :return: 过去时间返回 True
        """
        return self._dt < pendulum.now()

    def is_future(self) -> bool:
        """是否为未来时间。

        :return: 未来时间返回 True
        """
        return self._dt > pendulum.now()

    def is_before(self, other: Union[DateTime, datetime]) -> bool:
        """判断是否在指定时间之前。

        :param other: 比较对象
        :return: 是否在前
        """
        if isinstance(other, DateTime):
            return self._dt < other._dt
        return self._dt < pendulum.instance(other)

    def is_after(self, other: Union[DateTime, datetime]) -> bool:
        """判断是否在指定时间之后。

        :param other: 比较对象
        :return: 是否在后
        """
        if isinstance(other, DateTime):
            return self._dt > other._dt
        return self._dt > pendulum.instance(other)

    def is_between(
        self,
        start: Union[DateTime, datetime],
        end: Union[DateTime, datetime],
    ) -> bool:
        """判断是否在指定时间范围内（含边界）。

        :param start: 起始时间
        :param end: 结束时间
        :return: 是否在范围内
        """
        s = start._dt if isinstance(start, DateTime) else pendulum.instance(start)
        e = end._dt if isinstance(end, DateTime) else pendulum.instance(end)
        return s <= self._dt <= e

    def is_leap_year(self) -> bool:
        """是否为闰年。

        :return: 闰年返回 True
        """
        year = self._dt.year
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def is_last_day_of_month(self) -> bool:
        """是否为当月最后一天。

        :return: 最后一天返回 True
        """
        import calendar

        _, last_day = calendar.monthrange(self._dt.year, self._dt.month)
        return self._dt.day == last_day

    def length_of_month(self) -> int:
        """获取当月天数。

        :return: 天数
        """
        import calendar

        _, last_day = calendar.monthrange(self._dt.year, self._dt.month)
        return last_day

    def length_of_year(self) -> int:
        """获取当年天数。

        :return: 天数
        """
        return 366 if self.is_leap_year() else 365

    # ---- 偏移方法 ----

    def offset_day(self, days: int) -> DateTime:
        """按天偏移。

        :param days: 偏移天数
        :return: 新的 DateTime
        """
        return DateTime(self._dt.add(days=days))

    def offset_week(self, weeks: int) -> DateTime:
        """按周偏移。

        :param weeks: 偏移周数
        :return: 新的 DateTime
        """
        return DateTime(self._dt.add(weeks=weeks))

    def offset_month(self, months: int) -> DateTime:
        """按月偏移。

        :param months: 偏移月数
        :return: 新的 DateTime
        """
        return DateTime(self._dt.add(months=months))

    def offset_year(self, years: int) -> DateTime:
        """按年偏移。

        :param years: 偏移年数
        :return: 新的 DateTime
        """
        return DateTime(self._dt.add(years=years))

    # ---- 开始/结束（扩展） ----

    def begin_of_second(self) -> DateTime:
        """获取秒的开始（毫秒归零）。

        :return: DateTime
        """
        return DateTime(self._dt.replace(microsecond=0))

    def end_of_second(self) -> DateTime:
        """获取秒的结束。

        :return: DateTime
        """
        return DateTime(self._dt.replace(microsecond=999999))

    def begin_of_hour(self) -> DateTime:
        """获取小时的开始。

        :return: DateTime
        """
        return DateTime(self._dt.replace(minute=0, second=0, microsecond=0))

    def end_of_hour(self) -> DateTime:
        """获取小时的结束。

        :return: DateTime
        """
        return DateTime(self._dt.replace(minute=59, second=59, microsecond=999999))

    def begin_of_minute(self) -> DateTime:
        """获取分钟的开始。

        :return: DateTime
        """
        return DateTime(self._dt.replace(second=0, microsecond=0))

    def end_of_minute(self) -> DateTime:
        """获取分钟的结束。

        :return: DateTime
        """
        return DateTime(self._dt.replace(second=59, microsecond=999999))

    # ---- 格式化 ----

    def format(self, fmt: str = "YYYY-MM-DD HH:mm:ss") -> str:
        """格式化为字符串。

        :param fmt: pendulum 格式模式
        :return: 格式化字符串
        """
        return self._dt.format(fmt)

    def to_local_datetime_str(self) -> str:
        """转换为本地日期时间字符串 "YYYY-MM-DD HH:mm:ss"。

        :return: 日期时间字符串
        """
        return self._dt.naive().strftime("%Y-%m-%d %H:%M:%S")

    # ---- 时区 ----

    def with_timezone(self, tz: str) -> DateTime:
        """转换时区。

        :param tz: 时区名称，如 "UTC", "Asia/Shanghai"
        :return: 新的 DateTime
        """
        return DateTime(self._dt.in_timezone(tz))

    def timezone_name(self) -> Optional[str]:
        """获取时区名称。

        :return: 时区名称字符串
        """
        tz = self._dt.timezone
        if tz:
            return str(tz.name)
        return None


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

    @staticmethod
    def is_last_day_of_month(dt: Union[DateTime, datetime, date]) -> bool:
        """判断是否为当月最后一天。

        :param dt: 日期
        :return: 是否月末最后一天
        """
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        if isinstance(dt, date) and not isinstance(dt, datetime):
            dt = datetime(dt.year, dt.month, dt.day)
        import calendar

        last_day = calendar.monthrange(dt.year, dt.month)[1]
        return dt.day == last_day

    @staticmethod
    def is_expired(
        check_date: Union[DateTime, datetime, date],
        begin: Union[DateTime, datetime, date],
        end: Union[DateTime, datetime, date],
    ) -> bool:
        """判断日期是否在有效期外（早于 begin 或晚于 end）。

        :param check_date: 待检查的日期
        :param begin: 有效期开始（含）
        :param end: 有效期结束（含）
        :return: 是否过期
        """
        c = DateUtil._to_pendulum(check_date)
        b = DateUtil._to_pendulum(begin)
        e = DateUtil._to_pendulum(end)
        return c < b or c > e

    @staticmethod
    def is_overlap(
        begin1: Union[DateTime, datetime, date],
        end1: Union[DateTime, datetime, date],
        begin2: Union[DateTime, datetime, date],
        end2: Union[DateTime, datetime, date],
    ) -> bool:
        """判断两个时间段是否重叠。

        :param begin1: 第一段开始
        :param end1: 第一段结束
        :param begin2: 第二段开始
        :param end2: 第二段结束
        :return: 是否重叠
        """
        b1 = DateUtil._to_pendulum(begin1)
        e1 = DateUtil._to_pendulum(end1)
        b2 = DateUtil._to_pendulum(begin2)
        e2 = DateUtil._to_pendulum(end2)
        return b1 <= e2 and b2 <= e1

    @staticmethod
    def is_between(
        dt: Union[DateTime, datetime, date],
        begin: Union[DateTime, datetime, date],
        end: Union[DateTime, datetime, date],
    ) -> bool:
        """判断日期是否在范围内（含边界）。

        :param dt: 待检查的日期
        :param begin: 开始（含）
        :param end: 结束（含）
        :return: 是否在范围内
        """
        d = DateUtil._to_pendulum(dt)
        b = DateUtil._to_pendulum(begin)
        e = DateUtil._to_pendulum(end)
        return b <= d <= e

    @staticmethod
    def day_of_year(dt: Union[DateTime, datetime, date]) -> int:
        """获取年内第几天（1~366）。

        :param dt: 日期
        :return: 年内第几天
        """
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        if isinstance(dt, datetime):
            return dt.timetuple().tm_yday
        return dt.timetuple().tm_yday

    @staticmethod
    def length_of_month(dt: Union[DateTime, datetime, date]) -> int:
        """获取当月天数。

        :param dt: 日期
        :return: 当月天数
        """
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        import calendar

        return calendar.monthrange(dt.year, dt.month)[1]

    @staticmethod
    def length_of_year(year: int) -> int:
        """获取当年天数。

        :param year: 年份
        :return: 当年天数（365 或 366）
        """
        return 366 if DateUtil.is_leap_year(year) else 365

    @staticmethod
    def millisecond(dt: Union[DateTime, datetime]) -> int:
        """获取毫秒部分。

        :param dt: 日期时间
        :return: 毫秒数
        """
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        return dt.microsecond // 1000

    @staticmethod
    def get_zodiac(month: int, day: int) -> str:
        """获取星座。

        :param month: 月份（1-12）
        :param day: 日期（1-31）
        :return: 星座名称
        """
        zodiac_dates = [
            (1, 20, "水瓶座"),
            (2, 19, "双鱼座"),
            (3, 21, "白羊座"),
            (4, 20, "金牛座"),
            (5, 21, "双子座"),
            (6, 22, "巨蟹座"),
            (7, 23, "狮子座"),
            (8, 23, "处女座"),
            (9, 23, "天秤座"),
            (10, 24, "天蝎座"),
            (11, 23, "射手座"),
            (12, 22, "摩羯座"),
        ]
        if day >= zodiac_dates[month - 1][1]:
            return zodiac_dates[month - 1][2]
        # 当月之前
        return zodiac_dates[(month - 2) % 12][2]

    @staticmethod
    def get_chinese_zodiac(year: int) -> str:
        """获取生肖。

        :param year: 年份
        :return: 生肖名称
        """
        animals = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
        return animals[(year - 4) % 12]

    @staticmethod
    def compare(
        d1: Union[DateTime, datetime, date, None],
        d2: Union[DateTime, datetime, date, None],
    ) -> int:
        """null-safe 的日期比较。

        :param d1: 日期1
        :param d2: 日期2
        :return: 负数/0/正数
        """
        if d1 is None and d2 is None:
            return 0
        if d1 is None:
            return -1
        if d2 is None:
            return 1
        p1 = DateUtil._to_pendulum(d1)
        p2 = DateUtil._to_pendulum(d2)
        if p1 < p2:
            return -1
        if p1 > p2:
            return 1
        return 0

    @staticmethod
    def convert_timezone(dt: Union[DateTime, datetime], from_tz: str, to_tz: str) -> datetime:
        """时区转换。

        :param dt: 日期时间
        :param from_tz: 源时区，如 "Asia/Shanghai"
        :param to_tz: 目标时区，如 "US/Eastern"
        :return: 转换后的 datetime
        """
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        import pytz

        src_tz = pytz.timezone(from_tz)
        dst_tz = pytz.timezone(to_tz)
        if dt.tzinfo is None:
            dt = src_tz.localize(dt)
        return dt.astimezone(dst_tz)

    @staticmethod
    def format_chinese_date(dt: Union[DateTime, datetime, date]) -> str:
        """中文日期格式，如 "2024年1月15日"。

        :param dt: 日期
        :return: 中文日期字符串
        """
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        return f"{dt.year}年{dt.month}月{dt.day}日"

    @staticmethod
    def _to_pendulum(dt: Union[DateTime, datetime, date]):
        """内部辅助：转为 pendulum 对象。"""
        if isinstance(dt, DateTime):
            return dt._dt
        if isinstance(dt, date) and not isinstance(dt, datetime):
            return pendulum.instance(datetime(dt.year, dt.month, dt.day))
        return pendulum.instance(dt)

    # ── 当前时间快捷方法 ──────────────────────────────────────

    @staticmethod
    def this_year() -> int:
        """获取当前年份。

        :return: 当前年份
        """
        return pendulum.now().year

    @staticmethod
    def this_month() -> int:
        """获取当前月份（1~12）。

        :return: 当前月份
        """
        return pendulum.now().month

    @staticmethod
    def this_week_of_year() -> int:
        """获取当前是本年第几周。

        :return: 周数
        """
        return pendulum.now().week_of_year

    @staticmethod
    def this_week_of_month() -> int:
        """获取当前是本月第几周。

        :return: 周数
        """
        now = pendulum.now()
        return (now.day - 1) // 7 + 1

    @staticmethod
    def this_day_of_month() -> int:
        """获取当前是本月第几天。

        :return: 天数
        """
        return pendulum.now().day

    @staticmethod
    def this_day_of_week() -> int:
        """获取当前是本周第几天（1=周一，7=周日）。

        :return: 天数
        """
        return pendulum.now().isoweekday()

    @staticmethod
    def this_hour() -> int:
        """获取当前小时（0~23）。

        :return: 小时
        """
        return pendulum.now().hour

    @staticmethod
    def this_minute() -> int:
        """获取当前分钟（0~59）。

        :return: 分钟
        """
        return pendulum.now().minute

    @staticmethod
    def this_second() -> int:
        """获取当前秒（0~59）。

        :return: 秒
        """
        return pendulum.now().second

    @staticmethod
    def this_millisecond() -> int:
        """获取当前毫秒（0~999）。

        :return: 毫秒
        """
        return pendulum.now().microsecond // 1000

    # ── 时间转换 ──────────────────────────────────────────────

    @staticmethod
    def time_to_second(time_str: str) -> int:
        """将 HH:mm:ss 格式的时间字符串转为秒数。

        :param time_str: 时间字符串，如 "01:30:00"
        :return: 总秒数
        """
        parts = time_str.split(":")
        if len(parts) == 3:
            h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
        elif len(parts) == 2:
            h, m, s = int(parts[0]), int(parts[1]), 0
        else:
            raise ValueError(f"无效的时间格式: {time_str}")
        return h * 3600 + m * 60 + s

    @staticmethod
    def second_to_time(seconds: int) -> str:
        """将秒数转为 HH:mm:ss 格式。

        :param seconds: 总秒数
        :return: HH:mm:ss 格式字符串
        """
        if seconds < 0:
            raise ValueError("秒数不能为负")
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    # ── 年龄计算 ──────────────────────────────────────────────

    @staticmethod
    def age_of_now(birth: Union[DateTime, datetime, date, str]) -> int:
        """计算到当前时间的年龄。

        :param birth: 出生日期
        :return: 年龄
        """
        if isinstance(birth, str):
            birth = DateUtil.parse(birth)
        return DateUtil.age(birth, pendulum.now())

    @staticmethod
    def age(
        birth: Union[DateTime, datetime, date],
        now: Union[DateTime, datetime, date],
    ) -> int:
        """计算两个日期之间的年龄。

        :param birth: 出生日期
        :param now: 当前日期
        :return: 年龄
        """
        if isinstance(birth, DateTime):
            birth = birth.to_date()
        if isinstance(now, DateTime):
            now = now.to_date()
        if isinstance(birth, datetime):
            birth = birth.date()
        if isinstance(now, datetime):
            now = now.date()
        age = now.year - birth.year
        if (now.month, now.day) < (birth.month, birth.day):
            age -= 1
        return age

    # ── 截断/舍入 ─────────────────────────────────────────────

    @staticmethod
    def truncate(dt: Union[DateTime, datetime], field: str = "day") -> datetime:
        """截断日期时间到指定字段。

        :param dt: 日期时间
        :param field: 截断字段，支持 "year", "month", "day", "hour", "minute", "second"
        :return: 截断后的 datetime
        """
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        if field == "year":
            return dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        elif field == "month":
            return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif field == "day":
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif field == "hour":
            return dt.replace(minute=0, second=0, microsecond=0)
        elif field == "minute":
            return dt.replace(second=0, microsecond=0)
        elif field == "second":
            return dt.replace(microsecond=0)
        raise ValueError(f"不支持的截断字段: {field}")

    # ── 范围操作 ──────────────────────────────────────────────

    @staticmethod
    def range_contains(
        start: Union[DateTime, datetime],
        end: Union[DateTime, datetime],
        dt: Union[DateTime, datetime],
    ) -> bool:
        """判断日期是否在范围内（含边界）。

        :param start: 起始日期
        :param end: 结束日期
        :param dt: 待判断日期
        :return: 是否在范围内
        """
        if isinstance(start, DateTime):
            start = start.to_datetime()
        if isinstance(end, DateTime):
            end = end.to_datetime()
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        return start <= dt <= end

    @staticmethod
    def year_and_quarter(dt: Union[DateTime, datetime, date]) -> str:
        """返回年份和季度，如 "20241" 表示 2024 年第 1 季度。

        :param dt: 日期
        :return: 年份+季度字符串
        """
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        q = (dt.month - 1) // 3 + 1
        return f"{dt.year}{q}"

    # ── StopWatch ─────────────────────────────────────────────

    @staticmethod
    def create_stop_watch(name: str = "") -> "StopWatch":  # noqa: F821,UP037
        """创建秒表计时器。

        :param name: 秒表名称
        :return: StopWatch 实例
        """
        from hutool.core.text import StopWatch

        return StopWatch(name)

    # ── 纳秒转换 ──────────────────────────────────────────────

    @staticmethod
    def nanos_to_millis(nanos: int) -> float:
        """纳秒转毫秒。

        :param nanos: 纳秒
        :return: 毫秒
        """
        return nanos / 1_000_000

    @staticmethod
    def nanos_to_seconds(nanos: int) -> float:
        """纳秒转秒。

        :param nanos: 纳秒
        :return: 秒
        """
        return nanos / 1_000_000_000

    # ── 格式化间隔 ────────────────────────────────────────────

    @staticmethod
    def format_between_ms(between_ms: int, level: str = "millisecond") -> str:
        """格式化时间间隔（毫秒）。

        :param between_ms: 毫秒间隔
        :param level: 精度级别，"day", "hour", "minute", "second", "millisecond"
        :return: 格式化后的间隔字符串
        """
        if between_ms < 0:
            between_ms = -between_ms
        days = between_ms // 86400000
        hours = (between_ms % 86400000) // 3600000
        minutes = (between_ms % 3600000) // 60000
        seconds = (between_ms % 60000) // 1000
        millis = between_ms % 1000

        level_order = ["day", "hour", "minute", "second", "millisecond"]
        try:
            level_idx = level_order.index(level)
        except ValueError:
            raise ValueError(f"不支持的精度级别: {level}")

        time_parts = [
            (days, "天"),
            (hours, "小时"),
            (minutes, "分"),
            (seconds, "秒"),
            (millis, "毫秒"),
        ]
        parts = []
        for i, (val, unit) in enumerate(time_parts):
            if i > level_idx:
                break
            if val > 0 or i == level_idx:
                parts.append(f"{val}{unit}")
                if i == level_idx:
                    break
        return "".join(parts) if parts else "0毫秒"

    # ── 格式化/解析扩展 ──────────────────────────────────────

    @staticmethod
    def format_local_datetime(
        dt: Union[DateTime, datetime, PendulumDateTime, None] = None,
    ) -> str:
        """格式化为本地日期时间字符串 "YYYY-MM-DD HH:mm:ss"。

        :param dt: 日期时间，默认当前时间
        :return: 格式化字符串
        """
        if dt is None:
            dt = pendulum.now()
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        if isinstance(dt, PendulumDateTime):
            dt = dt.naive()
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def parse_local_datetime(s: str) -> datetime:
        """解析本地日期时间字符串 "YYYY-MM-DD HH:mm:ss"。

        :param s: 日期时间字符串
        :return: datetime 对象
        """
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def parse_utc(s: str) -> datetime:
        """解析 UTC 日期时间字符串。

        :param s: UTC 日期时间字符串，如 "2024-01-15T10:30:00Z"
        :return: datetime 对象
        """
        return pendulum.parse(s, tz="UTC").naive()

    @staticmethod
    def parse_cst(s: str) -> datetime:
        """解析 CST（中国标准时间 UTC+8）日期时间字符串。

        :param s: CST 日期时间字符串
        :return: datetime 对象（已转换为本地时间）
        """
        return pendulum.parse(s, tz="Asia/Shanghai").naive()

    @staticmethod
    def parse_rfc2822(s: str) -> datetime:
        """解析 RFC 2822 日期字符串，如 'Mon, 15 Jan 2024 10:30:00 +0800'。

        :param s: RFC 2822 日期字符串
        :return: datetime 对象
        """
        from email.utils import parsedate_to_datetime

        return parsedate_to_datetime(s).replace(tzinfo=None)

    # ── 舍入/天花板 ──────────────────────────────────────────

    @staticmethod
    def round(dt: Union[DateTime, datetime], field: str = "day") -> datetime:
        """四舍五入日期时间到指定字段。

        超过字段中间值时向上舍入，否则截断。
        例如 round(dt, "hour") 在分钟 >= 30 时进位。

        :param dt: 日期时间
        :param field: 舍入字段，支持 "year", "month", "day", "hour", "minute"
        :return: 舍入后的 datetime
        """
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        truncated = DateUtil.truncate(dt, field)
        if field == "year":
            mid = truncated.replace(month=7, day=1)
        elif field == "month":
            import calendar

            _, last_day = calendar.monthrange(dt.year, dt.month)
            mid = truncated.replace(day=last_day // 2 + 1)
        elif field == "day":
            mid = truncated.replace(hour=12)
        elif field == "hour":
            mid = truncated.replace(minute=30)
        elif field == "minute":
            mid = truncated.replace(second=30)
        else:
            raise ValueError(f"不支持的舍入字段: {field}")
        if dt >= mid:
            import calendar

            if field == "year":
                return truncated.replace(year=truncated.year + 1)
            elif field == "month":
                if truncated.month == 12:
                    return truncated.replace(year=truncated.year + 1, month=1)
                return truncated.replace(month=truncated.month + 1)
            elif field == "day":
                return truncated + timedelta(days=1)
            elif field == "hour":
                return truncated + timedelta(hours=1)
            elif field == "minute":
                return truncated + timedelta(minutes=1)
        return truncated

    @staticmethod
    def ceiling(dt: Union[DateTime, datetime], field: str = "day") -> datetime:
        """天花板舍入（向上取整）日期时间到指定字段。

        如果已经是截断值则不变，否则向上进位。

        :param dt: 日期时间
        :param field: 字段，支持 "year", "month", "day", "hour", "minute", "second"
        :return: 天花板后的 datetime
        """
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        truncated = DateUtil.truncate(dt, field)
        if truncated == dt:
            return truncated
        if field == "year":
            return truncated.replace(year=truncated.year + 1)
        elif field == "month":
            if truncated.month == 12:
                return truncated.replace(year=truncated.year + 1, month=1)
            return truncated.replace(month=truncated.month + 1)
        elif field == "day":
            return truncated + timedelta(days=1)
        elif field == "hour":
            return truncated + timedelta(hours=1)
        elif field == "minute":
            return truncated + timedelta(minutes=1)
        elif field == "second":
            return truncated + timedelta(seconds=1)
        raise ValueError(f"不支持的字段: {field}")

    # ── 时间开始/结束（秒/时/分） ────────────────────────────

    @staticmethod
    def begin_of_second(
        dt: Union[DateTime, datetime, PendulumDateTime, None] = None,
    ) -> datetime:
        """获取秒的开始（毫秒归零）。

        :param dt: 日期时间
        :return: 秒开始的 datetime
        """
        if dt is None:
            dt = pendulum.now()
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        if isinstance(dt, PendulumDateTime):
            dt = dt.naive()
        return dt.replace(microsecond=0)

    @staticmethod
    def end_of_second(
        dt: Union[DateTime, datetime, PendulumDateTime, None] = None,
    ) -> datetime:
        """获取秒的结束（毫秒设为最大值）。

        :param dt: 日期时间
        :return: 秒结束的 datetime
        """
        if dt is None:
            dt = pendulum.now()
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        if isinstance(dt, PendulumDateTime):
            dt = dt.naive()
        return dt.replace(microsecond=999999)

    @staticmethod
    def begin_of_hour(
        dt: Union[DateTime, datetime, PendulumDateTime, None] = None,
    ) -> datetime:
        """获取小时的开始。

        :param dt: 日期时间
        :return: 小时开始的 datetime
        """
        if dt is None:
            dt = pendulum.now()
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        if isinstance(dt, PendulumDateTime):
            dt = dt.naive()
        return dt.replace(minute=0, second=0, microsecond=0)

    @staticmethod
    def end_of_hour(
        dt: Union[DateTime, datetime, PendulumDateTime, None] = None,
    ) -> datetime:
        """获取小时的结束。

        :param dt: 日期时间
        :return: 小时结束的 datetime
        """
        if dt is None:
            dt = pendulum.now()
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        if isinstance(dt, PendulumDateTime):
            dt = dt.naive()
        return dt.replace(minute=59, second=59, microsecond=999999)

    @staticmethod
    def begin_of_minute(
        dt: Union[DateTime, datetime, PendulumDateTime, None] = None,
    ) -> datetime:
        """获取分钟的开始。

        :param dt: 日期时间
        :return: 分钟开始的 datetime
        """
        if dt is None:
            dt = pendulum.now()
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        if isinstance(dt, PendulumDateTime):
            dt = dt.naive()
        return dt.replace(second=0, microsecond=0)

    @staticmethod
    def end_of_minute(
        dt: Union[DateTime, datetime, PendulumDateTime, None] = None,
    ) -> datetime:
        """获取分钟的结束。

        :param dt: 日期时间
        :return: 分钟结束的 datetime
        """
        if dt is None:
            dt = pendulum.now()
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        if isinstance(dt, PendulumDateTime):
            dt = dt.naive()
        return dt.replace(second=59, microsecond=999999)

    # ── 通用偏移 ─────────────────────────────────────────────

    @staticmethod
    def offset(dt: Union[DateTime, datetime], field: str, amount: int) -> datetime:
        """通用日期偏移。

        :param dt: 日期时间
        :param field: 偏移字段，支持 "year", "month", "week", "day", "hour", "minute", "second"
        :param amount: 偏移量（正数向未来，负数向过去）
        :return: 偏移后的 datetime
        """
        if isinstance(dt, DateTime):
            dt = dt.to_datetime()
        if field == "year":
            try:
                return dt.replace(year=dt.year + amount)
            except ValueError:
                import calendar

                _, last_day = calendar.monthrange(dt.year + amount, dt.month)
                return dt.replace(year=dt.year + amount, day=min(dt.day, last_day))
        elif field == "month":
            month = dt.month - 1 + amount
            year = dt.year + month // 12
            month = month % 12 + 1
            import calendar

            _, last_day = calendar.monthrange(year, month)
            return dt.replace(year=year, month=month, day=min(dt.day, last_day))
        elif field == "week":
            return dt + timedelta(weeks=amount)
        elif field == "day":
            return dt + timedelta(days=amount)
        elif field == "hour":
            return dt + timedelta(hours=amount)
        elif field == "minute":
            return dt + timedelta(minutes=amount)
        elif field == "second":
            return dt + timedelta(seconds=amount)
        raise ValueError(f"不支持的偏移字段: {field}")

    # ── 日期范围 ─────────────────────────────────────────────

    @staticmethod
    def range(
        start: Union[DateTime, datetime, date],
        end: Union[DateTime, datetime, date],
        unit: str = "day",
    ) -> List[datetime]:
        """生成日期范围列表。

        :param start: 起始日期
        :param end: 结束日期（不含）
        :param unit: 步进单位，"day", "week", "month"
        :return: 日期列表
        """
        if isinstance(start, DateTime):
            start = start.to_datetime()
        if isinstance(end, DateTime):
            end = end.to_datetime()
        if isinstance(start, date) and not isinstance(start, datetime):
            start = datetime(start.year, start.month, start.day)
        if isinstance(end, date) and not isinstance(end, datetime):
            end = datetime(end.year, end.month, end.day)
        result = []
        current = start
        while current < end:
            result.append(current)
            if unit == "day":
                current += timedelta(days=1)
            elif unit == "week":
                current += timedelta(weeks=1)
            elif unit == "month":
                month = current.month - 1 + 1
                year = current.year + month // 12
                month = month % 12 + 1
                import calendar

                _, last_day = calendar.monthrange(year, month)
                current = current.replace(year=year, month=month, day=min(current.day, last_day))
            else:
                raise ValueError(f"不支持的步进单位: {unit}")
        return result

    @staticmethod
    def range_to_list(
        start: Union[DateTime, datetime, date],
        end: Union[DateTime, datetime, date],
        unit: str = "day",
    ) -> List[datetime]:
        """生成日期范围列表（含结束日期）。

        :param start: 起始日期
        :param end: 结束日期（含）
        :param unit: 步进单位，"day", "week", "month"
        :return: 日期列表
        """
        if isinstance(end, DateTime):
            end = end.to_datetime()
        if isinstance(end, date) and not isinstance(end, datetime):
            end = datetime(end.year, end.month, end.day)
        result = DateUtil.range(start, end, unit)
        if result and result[-1] != end:
            result.append(end)
        return result
