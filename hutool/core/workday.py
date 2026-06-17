"""
工作日计算工具类

提供工作日判断、工作日数计算、加减工作日等功能。
默认使用中国法定节假日配置，支持自定义假日列表。
"""

import datetime
from datetime import date, timedelta
from typing import List, Optional, Tuple


class WorkdayUtil:
    """工作日计算工具类。

    默认使用中国法定节假日配置（不含调休补班日），支持自定义假日列表。

    默认假日包含：元旦、春节、清明、劳动节、端午、中秋、国庆。

    .. note::

        中国法定假日的实际日期每年可能由国务院调整（含调休），
        默认配置仅覆盖固定日期部分。如需精确到具体年份的调休安排，
        请通过 ``set_custom_holidays()`` 传入完整假日列表。
    """

    # 中国法定固定假日（月, 日）
    STATIC_HOLIDAYS: List[Tuple[int, int]] = [
        (1, 1),  # 元旦
        (5, 1),  # 劳动节
        (10, 1),  # 国庆节
        (10, 2),  # 国庆节
        (10, 3),  # 国庆节
    ]

    # 自定义假日缓存 {year: [date, ...]}
    _custom_holidays: Optional[dict] = None

    @classmethod
    def set_custom_holidays(cls, holidays):
        # type: (Optional[List[date]]) -> None
        """
        设置自定义假日列表，覆盖默认的中国法定假日。

        传入 ``None`` 可清除自定义配置，恢复默认。

        :param holidays: 自定义假日日期列表，或 ``None`` 清除

        ::

            >>> from datetime import date
            >>> WorkdayUtil.set_custom_holidays([date(2024, 1, 1), date(2024, 2, 10)])
        """
        if holidays is None:
            cls._custom_holidays = None
        else:
            cls._custom_holidays = {}
            for d in holidays:
                cls._custom_holidays.setdefault(d.year, []).append(d)

    @classmethod
    def holidays(cls, year: int) -> List[date]:
        """
        获取指定年份的所有法定假日。

        如果已设置自定义假日，则返回自定义假日；否则返回中国法定假日。

        :param year: 年份
        :return: 假日日期列表

        ::

            >>> holidays = WorkdayUtil.holidays(2024)
            >>> date(2024, 1, 1) in holidays
            True
        """
        if cls._custom_holidays is not None:
            return list(cls._custom_holidays.get(year, []))

        result: List[date] = []
        for month, day in cls.STATIC_HOLIDAYS:
            try:
                result.append(date(year, month, day))
            except ValueError:
                pass
        # 添加春节、清明、端午、中秋的估算日期
        # 这些节日基于农历，每年日期不同，此处使用 2024 年数据作为默认配置
        # 实际使用时建议通过 set_custom_holidays() 设置精确假日
        if year == 2024:
            result.extend(
                [
                    date(2024, 2, 10),
                    date(2024, 2, 11),
                    date(2024, 2, 12),  # 春节
                    date(2024, 2, 13),
                    date(2024, 2, 14),
                    date(2024, 2, 15),
                    date(2024, 2, 16),
                    date(2024, 2, 17),
                    date(2024, 4, 4),
                    date(2024, 4, 5),
                    date(2024, 4, 6),  # 清明
                    date(2024, 5, 1),
                    date(2024, 5, 2),
                    date(2024, 5, 3),  # 劳动节
                    date(2024, 5, 4),
                    date(2024, 5, 5),
                    date(2024, 6, 8),
                    date(2024, 6, 9),
                    date(2024, 6, 10),  # 端午
                    date(2024, 9, 15),
                    date(2024, 9, 16),
                    date(2024, 9, 17),  # 中秋
                    date(2024, 10, 1),
                    date(2024, 10, 2),
                    date(2024, 10, 3),  # 国庆
                    date(2024, 10, 4),
                    date(2024, 10, 5),
                    date(2024, 10, 6),
                    date(2024, 10, 7),
                ]
            )
        elif year == 2025:
            result.extend(
                [
                    date(2025, 1, 28),
                    date(2025, 1, 29),
                    date(2025, 1, 30),  # 春节
                    date(2025, 1, 31),
                    date(2025, 2, 1),
                    date(2025, 2, 2),
                    date(2025, 2, 3),
                    date(2025, 2, 4),
                    date(2025, 4, 4),
                    date(2025, 4, 5),
                    date(2025, 4, 6),  # 清明
                    date(2025, 5, 2),
                    date(2025, 5, 3),
                    date(2025, 5, 4),  # 劳动节
                    date(2025, 5, 5),
                    date(2025, 5, 31),
                    date(2025, 6, 1),
                    date(2025, 6, 2),  # 端午
                    date(2025, 10, 4),
                    date(2025, 10, 5),  # 国庆+中秋
                    date(2025, 10, 6),
                    date(2025, 10, 7),
                    date(2025, 10, 8),
                ]
            )
        return result

    @classmethod
    def _is_holiday(cls, dt: date) -> bool:
        """判断日期是否为假日。"""
        return dt in cls.holidays(dt.year)

    @classmethod
    def is_workday(cls, dt):
        # type: (Union[date, datetime.datetime]) -> bool
        """
        判断指定日期是否为工作日。

        工作日 = 非周末 且 非法定假日。

        :param dt: 日期对象
        :return: 是否为工作日

        ::

            >>> from datetime import date
            >>> WorkdayUtil.is_workday(date(2024, 1, 2))  # 周二，非假日
            True
            >>> WorkdayUtil.is_workday(date(2024, 1, 1))  # 元旦
            False
        """
        if isinstance(dt, datetime.datetime):
            dt = dt.date()
        if dt.isoweekday() > 5:
            return False
        return not cls._is_holiday(dt)

    @classmethod
    def next_workday(cls, dt):
        # type: (Union[date, datetime.datetime]) -> date
        """
        获取下一个工作日。

        :param dt: 起始日期
        :return: 下一个工作日

        ::

            >>> from datetime import date
            >>> WorkdayUtil.next_workday(date(2024, 1, 5))  # 周五
            date(2024, 1, 8)
        """
        is_datetime = isinstance(dt, datetime.datetime)
        if is_datetime:
            dt = dt.date()
        next_day = dt + timedelta(days=1)
        while not cls.is_workday(next_day):
            next_day += timedelta(days=1)
        return next_day

    @classmethod
    def previous_workday(cls, dt):
        # type: (Union[date, datetime.datetime]) -> date
        """
        获取上一个工作日。

        :param dt: 起始日期
        :return: 上一个工作日

        ::

            >>> from datetime import date
            >>> WorkdayUtil.previous_workday(date(2024, 1, 8))  # 周一
            date(2024, 1, 5)
        """
        is_datetime = isinstance(dt, datetime.datetime)
        if is_datetime:
            dt = dt.date()
        prev_day = dt - timedelta(days=1)
        while not cls.is_workday(prev_day):
            prev_day -= timedelta(days=1)
        return prev_day

    @classmethod
    def workdays(cls, start, end):
        # type: (Union[date, datetime.datetime], Union[date, datetime.datetime]) -> int
        """
        计算两个日期之间的工作日数（含首日和末日）。

        如果 start > end，返回负数。

        :param start: 起始日期
        :param end: 结束日期
        :return: 工作日数

        ::

            >>> from datetime import date
            >>> WorkdayUtil.workdays(date(2024, 1, 1), date(2024, 1, 5))
            3
        """
        if isinstance(start, datetime.datetime):
            start = start.date()
        if isinstance(end, datetime.datetime):
            end = end.date()

        if start > end:
            return -1 * cls._workdays_count(end, start)
        return cls._workdays_count(start, end)

    @classmethod
    def _workdays_count(cls, start: date, end: date) -> int:
        """计算 start 到 end（含两端）之间的工作日数。"""
        count = 0
        current = start
        while current <= end:
            if cls.is_workday(current):
                count += 1
            current += timedelta(days=1)
        return count

    @classmethod
    def add_workdays(cls, dt, count):
        # type: (Union[date, datetime.datetime], int) -> date
        """
        日期加减指定工作日数。

        正数向后加工作日，负数向前减工作日。

        :param dt: 起始日期
        :param count: 工作日数（可为负数）
        :return: 目标日期

        ::

            >>> from datetime import date
            >>> WorkdayUtil.add_workdays(date(2024, 1, 1), 5)
            date(2024, 1, 8)
        """
        is_datetime = isinstance(dt, datetime.datetime)
        if is_datetime:
            dt = dt.date()

        day = dt
        step = 1 if count >= 0 else -1
        remaining = abs(count)
        while remaining > 0:
            day += timedelta(days=step)
            if cls.is_workday(day):
                remaining -= 1
        return day

    @classmethod
    def workday_hours(
        cls,
        start: datetime.datetime,
        end: datetime.datetime,
        workday_hours_per_day: int = 8,
    ) -> float:
        """计算两个 datetime 之间的工作小时数。

        仅计算工作日的工作时间（每天 ``workday_hours_per_day`` 小时，从 09:00 开始）。
        非工作日不计入。

        :param start: 起始时间
        :param end: 结束时间
        :param workday_hours_per_day: 每日工作小时数，默认 8
        :return: 工作小时数
        """
        if start > end:
            start, end = end, start

        total_hours = 0.0
        current = start
        while current.date() <= end.date():
            if cls.is_workday(current.date()):
                if current.date() == start.date() and current.date() == end.date():
                    # 同一天
                    hours = (end - start).total_seconds() / 3600
                    total_hours += min(hours, workday_hours_per_day)
                elif current.date() == start.date():
                    # 起始日：从 start 到当天结束
                    day_end = current.replace(hour=17, minute=0, second=0)
                    if start < day_end:
                        total_hours += (day_end - start).total_seconds() / 3600
                elif current.date() == end.date():
                    # 结束日：从当天 09:00 到 end
                    day_start = current.replace(hour=9, minute=0, second=0)
                    if end > day_start:
                        total_hours += (end - day_start).total_seconds() / 3600
                else:
                    # 中间全天工作日
                    total_hours += workday_hours_per_day
            current += timedelta(days=1)

        return min(total_hours, workday_hours_per_day * cls.workdays(start.date(), end.date()))

    @staticmethod
    def easter(year: int) -> date:
        """计算复活节日期（Meeus/Jones/Butcher 算法，适用于 1900-2099）。

        :param year: 年份
        :return: 复活节 date 对象

        ::

            >>> WorkdayUtil.easter(2024)
            date(2024, 3, 31)
        """
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l_ = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l_) // 451
        month = (h + l_ - 7 * m + 114) // 31
        day = ((h + l_ - 7 * m + 114) % 31) + 1
        return date(year, month, day)

    @staticmethod
    def easter_related_holidays(year: int) -> List[Tuple[date, str]]:
        """获取复活节相关节假日列表。

        包括：圣灰星期三、棕枝主日、耶稳升天节、五旬节、基督圣体节。

        :param year: 年份
        :return: ``(日期, 节日名)`` 列表
        """
        easter_date = WorkdayUtil.easter(year)
        holidays = [
            (easter_date - timedelta(days=46), "圣灰星期三"),
            (easter_date - timedelta(days=7), "棕枝主日"),
            (easter_date, "复活节"),
            (easter_date + timedelta(days=39), "耶稳升天节"),
            (easter_date + timedelta(days=49), "五旬节"),
            (easter_date + timedelta(days=60), "基督圣体节"),
        ]
        return holidays
