"""Quartz 风格 Cron 表达式校验工具类。"""

import re
from datetime import datetime
from typing import Optional


class CronValidator:
    """Cron 表达式校验工具类。

    支持 Quartz 风格 6-7 字段 cron 表达式的逐字段校验和整体校验。

    字段格式::

        秒 分 时 日 月 周 [年]

    特殊字符说明：

    - ``*`` : 匹配任意值
    - ``-`` : 范围 (如 ``1-5``)
    - ``/`` : 步长 (如 ``0/5``)
    - ``,`` : 列举多个值 (如 ``1,3,5``)
    - ``?`` : 不指定（日、周字段）
    - ``L`` : 最后（日、周字段）
    - ``W`` : 最近工作日（日字段）
    - ``#`` : 第几个星期几 (如 ``6#3`` 表示第三个星期五)
    """

    # ── 内部辅助 ──────────────────────────────────────────────

    @staticmethod
    def _valid_range(search_str: str, start_range: int, end_range: int) -> bool:
        """校验范围表达式 (如 ``1-5``) 是否在合法区间内。"""
        match = re.match(r"^(\d+)-(\d+)$", search_str)
        if match:
            start, end = int(match.group(1)), int(match.group(2))
            return start_range <= start < end <= end_range
        return False

    @staticmethod
    def _valid_sum(
        search_str: str,
        start_range_a: int,
        start_range_b: int,
        end_range_a: int,
        end_range_b: int,
        sum_range: int,
    ) -> bool:
        """校验步长表达式 (如 ``0/5``) 是否在合法区间内。"""
        match = re.match(r"^(\d+)/(\d+)$", search_str)
        if match:
            start, end = int(match.group(1)), int(match.group(2))
            return (
                start_range_a <= start <= start_range_b
                and end_range_a <= end <= end_range_b
                and start + end <= sum_range
            )
        return False

    # ── 单字段校验 ────────────────────────────────────────────

    @staticmethod
    def validate_second_or_minute(second_or_minute: str) -> bool:
        """校验秒或分钟字段是否合法。

        合法值：``*``、范围 (``0-59``)、步长 (``0/5``)、枚举 (``1,3,5``)。

        :param second_or_minute: 秒或分钟值
        :return: 是否合法
        """
        return bool(
            second_or_minute == "*"
            or ("-" in second_or_minute and CronValidator._valid_range(second_or_minute, 0, 59))
            or ("/" in second_or_minute and CronValidator._valid_sum(second_or_minute, 0, 58, 1, 59, 59))
            or re.match(r"^(?:[0-5]?\d|59)(?:,(?:[0-5]?\d|59))*$", second_or_minute)
        )

    @staticmethod
    def validate_hour(hour: str) -> bool:
        """校验小时字段是否合法。

        合法值：``*``、范围 (``0-23``)、步长 (``0/2``)、枚举 (``1,3,5``)。

        :param hour: 小时值
        :return: 是否合法
        """
        return bool(
            hour == "*"
            or ("-" in hour and CronValidator._valid_range(hour, 0, 23))
            or ("/" in hour and CronValidator._valid_sum(hour, 0, 22, 1, 23, 23))
            or re.match(r"^(?:0|[1-9]|1\d|2[0-3])(?:,(?:0|[1-9]|1\d|2[0-3]))*$", hour)
        )

    @staticmethod
    def validate_day(day: str) -> bool:
        """校验日字段是否合法。

        合法值：``*``、``?``、``L``、``W``、范围、步长、枚举。

        :param day: 日值
        :return: 是否合法
        """
        return bool(
            day in ("*", "?", "L")
            or ("-" in day and CronValidator._valid_range(day, 1, 31))
            or ("/" in day and CronValidator._valid_sum(day, 1, 30, 1, 30, 31))
            or ("W" in day and re.match(r"^(?:[1-9]|1\d|2\d|3[01])W$", day))
            or re.match(r"^(?:0|[1-9]|1\d|2\d|3[01])(?:,(?:0|[1-9]|1\d|2\d|3[01]))*$", day)
        )

    @staticmethod
    def validate_month(month: str) -> bool:
        """校验月字段是否合法。

        合法值：``*``、范围 (``1-12``)、步长、枚举。

        :param month: 月值
        :return: 是否合法
        """
        return bool(
            month == "*"
            or ("-" in month and CronValidator._valid_range(month, 1, 12))
            or ("/" in month and CronValidator._valid_sum(month, 1, 11, 1, 11, 12))
            or re.match(r"^(?:0|[1-9]|1[0-2])(?:,(?:0|[1-9]|1[0-2]))*$", month)
        )

    @staticmethod
    def validate_week(week: str) -> bool:
        """校验周字段是否合法。

        合法值：``*``、``?``、``L``、``#``、范围 (``1-7``)、枚举。

        :param week: 周值
        :return: 是否合法
        """
        return bool(
            week in ("*", "?")
            or ("-" in week and CronValidator._valid_range(week, 1, 7))
            or ("#" in week and re.match(r"^[1-7]#[1-4]$", week))
            or ("L" in week and re.match(r"^[1-7]L$", week))
            or re.match(r"^[1-7](?:(,[1-7]))*$", week)
        )

    @staticmethod
    def validate_year(year: str) -> bool:
        """校验年字段是否合法。

        合法值：``*``、范围、步长、枚举（4 位年份，当前年至 2099）。

        :param year: 年值
        :return: 是否合法
        """
        current_year = int(datetime.now().year)
        future_years = [current_year + i for i in range(9)]
        return bool(
            year == "*"
            or ("-" in year and CronValidator._valid_range(year, current_year, 2099))
            or ("/" in year and CronValidator._valid_sum(year, current_year, 2098, 1, 2099 - current_year, 2099))
            or ("#" in year and re.match(r"^[1-7]#[1-4]$", year))
            or ("L" in year and re.match(r"^[1-7]L$", year))
            or (
                (len(year) == 4 or "," in year)
                and all(int(item) in future_years and current_year <= int(item) <= 2099 for item in year.split(","))
            )
        )

    # ── 整体校验 ──────────────────────────────────────────────

    @staticmethod
    def validate(cron_expression: str) -> bool:
        """校验 Cron 表达式是否合法。

        支持 6 字段 (秒 分 时 日 月 周) 和 7 字段 (秒 分 时 日 月 周 年) 格式。

        :param cron_expression: Cron 表达式
        :return: 是否合法

        示例::

            >>> CronValidator.validate("0 0 12 * * ?")
            True
            >>> CronValidator.validate("0 0/5 14 * * ?")
            True
            >>> CronValidator.validate("invalid")
            False
        """
        values = cron_expression.split()
        if len(values) not in (6, 7):
            return False
        if not CronValidator.validate_second_or_minute(values[0]):
            return False
        if not CronValidator.validate_second_or_minute(values[1]):
            return False
        if not CronValidator.validate_hour(values[2]):
            return False
        if not CronValidator.validate_day(values[3]):
            return False
        if not CronValidator.validate_month(values[4]):
            return False
        if not CronValidator.validate_week(values[5]):
            return False
        if len(values) == 7:
            return CronValidator.validate_year(values[6])
        return True

    # ── 别名 ──────────────────────────────────────────────────

    @staticmethod
    def validate_cron_expression(cron_expression: str) -> bool:
        """校验 Cron 表达式是否合法（``validate`` 的别名）。

        :param cron_expression: Cron 表达式
        :return: 是否合法
        """
        return CronValidator.validate(cron_expression)

    @staticmethod
    def is_valid(cron_expression: Optional[str]) -> bool:
        """判断 Cron 表达式是否合法。

        ``None`` 或空字符串返回 ``False``。

        :param cron_expression: Cron 表达式
        :return: 是否合法
        """
        if not cron_expression:
            return False
        return CronValidator.validate(cron_expression)
