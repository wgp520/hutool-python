import time as _time
from datetime import date, datetime, timedelta

from hutool import DateTime, DateUtil


class TestDateUtil:
    def test_now(self):
        result = DateUtil.now()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_today(self):
        result = DateUtil.today()
        assert isinstance(result, str)
        assert len(result) == 10

    def test_format_date(self):
        dt = DateUtil.parse("2024-01-15")
        result = DateUtil.format_date(dt)
        assert "2024" in result

    def test_parse(self):
        dt = DateUtil.parse("2024-01-15")
        assert dt is not None

    def test_parse_with_format(self):
        dt = DateUtil.parse("2024/01/15", "YYYY/MM/DD")
        assert dt is not None

    def test_year_month_day(self):
        dt = DateUtil.parse("2024-01-15")
        assert DateUtil.year(dt) == 2024
        assert DateUtil.month(dt) == 1
        assert DateUtil.day_of_month(dt) == 15

    def test_day_of_week(self):
        dt = DateUtil.parse("2024-01-15")  # Monday
        result = DateUtil.day_of_week(dt)
        assert 1 <= result <= 7

    def test_quarter(self):
        dt = DateUtil.parse("2024-03-15")
        assert DateUtil.quarter(dt) == 1
        dt2 = DateUtil.parse("2024-07-15")
        assert DateUtil.quarter(dt2) == 3

    def test_is_weekend(self):
        dt = DateUtil.parse("2024-01-13")  # Saturday
        assert DateUtil.is_weekend(dt) is True

    def test_offset_day(self):
        dt = DateUtil.parse("2024-01-15")
        result = DateUtil.offset_day(dt, 1)
        assert DateUtil.day_of_month(result) == 16

    def test_offset_month(self):
        dt = DateUtil.parse("2024-01-15")
        result = DateUtil.offset_month(dt, 1)
        assert DateUtil.month(result) == 2

    def test_begin_of_day(self):
        dt = DateUtil.parse("2024-01-15")
        result = DateUtil.begin_of_day(dt)
        assert result is not None

    def test_end_of_day(self):
        dt = DateUtil.parse("2024-01-15")
        result = DateUtil.end_of_day(dt)
        assert result is not None

    def test_begin_of_month(self):
        dt = DateUtil.parse("2024-03-15")
        result = DateUtil.begin_of_month(dt)
        assert DateUtil.day_of_month(result) == 1

    def test_end_of_month(self):
        dt = DateUtil.parse("2024-03-15")
        result = DateUtil.end_of_month(dt)
        assert DateUtil.day_of_month(result) == 31

    def test_between_day(self):
        start = DateUtil.parse("2024-01-01")
        end = DateUtil.parse("2024-01-10")
        result = DateUtil.between_day(start, end)
        assert result == 9

    def test_between_ms(self):
        start = DateUtil.parse("2024-01-01")
        end = DateUtil.parse("2024-01-02")
        result = DateUtil.between_ms(start, end)
        assert result > 0

    def test_is_same_day(self):
        dt1 = DateUtil.parse("2024-01-15")
        dt2 = DateUtil.parse("2024-01-15")
        assert DateUtil.is_same_day(dt1, dt2) is True

    def test_is_leap_year(self):
        assert DateUtil.is_leap_year(2024) is True
        assert DateUtil.is_leap_year(2023) is False
        assert DateUtil.is_leap_year(1900) is False
        assert DateUtil.is_leap_year(2000) is True

    def test_format_between(self):
        start = DateUtil.parse("2024-01-01")
        end = DateUtil.parse("2024-01-02")
        result = DateUtil.format_between(start, end)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_yesterday(self):
        result = DateUtil.yesterday()
        assert result is not None

    def test_tomorrow(self):
        result = DateUtil.tomorrow()
        assert result is not None

    def test_current(self):
        result = DateUtil.current()
        assert isinstance(result, int)
        assert result > 0

    def test_format(self):
        dt = DateUtil.parse("2024-01-15")
        result = DateUtil.format(dt, "YYYY-MM-DD")
        assert "2024-01-15" in result

    def test_is_in(self):
        start = DateUtil.parse("2024-01-01")
        end = DateUtil.parse("2024-12-31")
        middle = DateUtil.parse("2024-06-15")
        assert DateUtil.is_in(middle, start, end) is True

    # ── date_trunc ──────────────────────────────────────────

    def test_date_trunc_day(self):
        """测试截断到天"""
        dt = datetime(2024, 3, 15, 14, 30, 45)
        result = DateUtil.date_trunc("day", dt)
        # datetime 输入截断到 day 仍返回 datetime
        assert result.year == 2024
        assert result.month == 3
        assert result.day == 15
        assert result.hour == 0
        assert result.minute == 0

    def test_date_trunc_day_with_date(self):
        """测试 date 类型截断到天"""
        d = date(2024, 3, 15)
        result = DateUtil.date_trunc("day", d)
        assert result == date(2024, 3, 15)

    def test_date_trunc_month(self):
        """测试截断到月"""
        dt = datetime(2024, 3, 15, 14, 30)
        result = DateUtil.date_trunc("month", dt)
        assert result.year == 2024
        assert result.month == 3
        assert result.day == 1

    def test_date_trunc_year(self):
        """测试截断到年"""
        dt = date(2024, 6, 15)
        result = DateUtil.date_trunc("year", dt)
        assert result == date(2024, 1, 1)

    def test_date_trunc_quarter(self):
        """测试截断到季度"""
        assert DateUtil.date_trunc("quarter", date(2024, 5, 15)) == date(2024, 4, 1)
        assert DateUtil.date_trunc("quarter", date(2024, 2, 15)) == date(2024, 1, 1)
        assert DateUtil.date_trunc("quarter", date(2024, 11, 15)) == date(2024, 10, 1)

    def test_date_trunc_week(self):
        """测试截断到周（周一）"""
        # 2024-03-15 是周五，周一是 2024-03-11
        result = DateUtil.date_trunc("week", date(2024, 3, 15))
        assert result == date(2024, 3, 11)

    def test_date_trunc_hour(self):
        """测试截断到小时"""
        dt = datetime(2024, 3, 15, 14, 30, 45)
        result = DateUtil.date_trunc("hour", dt)
        assert result.hour == 14
        assert result.minute == 0

    def test_date_trunc_invalid(self):
        """测试无效截断类型"""
        import pytest

        with pytest.raises(ValueError):
            DateUtil.date_trunc("invalid", date(2024, 1, 1))

    # ── get_week ────────────────────────────────────────────

    def test_get_week_basic(self):
        """测试基本周号"""
        week_num, year = DateUtil.get_week(date(2024, 1, 1))
        assert isinstance(week_num, int)
        assert isinstance(year, int)

    def test_get_week_iso(self):
        """测试 ISO 周号"""
        # 2024-01-01 是周一，ISO 周号 1
        week_num, _year = DateUtil.get_week(date(2024, 1, 1))
        assert week_num >= 1

    # ── get_monthspan ───────────────────────────────────────

    def test_get_monthspan_basic(self):
        """测试获取月首末日"""
        first, last = DateUtil.get_monthspan(date(2024, 3, 15))
        assert first == date(2024, 3, 1)
        assert last == date(2024, 3, 31)

    def test_get_monthspan_february_leap(self):
        """测试闰年二月"""
        first, last = DateUtil.get_monthspan(date(2024, 2, 15))
        assert first == date(2024, 2, 1)
        assert last == date(2024, 2, 29)

    def test_get_monthspan_february_non_leap(self):
        """测试非闰年二月"""
        first, last = DateUtil.get_monthspan(date(2023, 2, 15))
        assert first == date(2023, 2, 1)
        assert last == date(2023, 2, 28)

    # ── get_weekspan ────────────────────────────────────────

    def test_get_weekspan_basic(self):
        """测试获取周首末日"""
        monday, sunday = DateUtil.get_weekspan(date(2024, 3, 15))
        assert monday == date(2024, 3, 11)
        assert sunday == date(2024, 3, 17)

    def test_get_weekspan_monday(self):
        """测试周一输入"""
        monday, sunday = DateUtil.get_weekspan(date(2024, 3, 11))
        assert monday == date(2024, 3, 11)
        assert sunday == date(2024, 3, 17)

    # ── get_quarterspan ─────────────────────────────────────

    def test_get_quarterspan_q1(self):
        """测试 Q1"""
        first, last = DateUtil.get_quarterspan(date(2024, 2, 15))
        assert first == date(2024, 1, 1)
        assert last == date(2024, 3, 31)

    def test_get_quarterspan_q2(self):
        """测试 Q2"""
        first, last = DateUtil.get_quarterspan(date(2024, 5, 15))
        assert first == date(2024, 4, 1)
        assert last == date(2024, 6, 30)

    def test_get_quarterspan_q4(self):
        """测试 Q4"""
        first, last = DateUtil.get_quarterspan(date(2024, 12, 25))
        assert first == date(2024, 10, 1)
        assert last == date(2024, 12, 31)

    # ── get_yearspan ────────────────────────────────────────

    def test_get_yearspan_basic(self):
        """测试获取年首末日"""
        first, last = DateUtil.get_yearspan(date(2024, 6, 15))
        assert first == date(2024, 1, 1)
        assert last == date(2024, 12, 31)

    # ── month_add ───────────────────────────────────────────

    def test_month_add_basic(self):
        """测试加月份"""
        result = DateUtil.month_add(date(2024, 1, 15), 1)
        assert result == date(2024, 2, 15)

    def test_month_add_overflow(self):
        """测试月末溢出（1月31 + 1月 = 2月29）"""
        result = DateUtil.month_add(date(2024, 1, 31), 1)
        assert result.day == 29  # 2024 是闰年

    def test_month_add_negative(self):
        """测试减月份"""
        result = DateUtil.month_add(date(2024, 3, 15), -2)
        assert result == date(2024, 1, 15)

    def test_month_add_cross_year(self):
        """测试跨年"""
        result = DateUtil.month_add(date(2024, 11, 15), 3)
        assert result == date(2025, 2, 15)

    # ── rfc3339_date / rfc3339_date_parse ───────────────────

    def test_rfc3339_date_format(self):
        """测试 RFC 3339 格式化"""
        dt = datetime(2024, 3, 15, 14, 30, 0)
        result = DateUtil.rfc3339_date(dt)
        assert "2024-03-15" in result
        assert "T" in result

    def test_rfc3339_date_parse(self):
        """测试 RFC 3339 解析（无时区偏移）"""
        dt = DateUtil.rfc3339_date_parse("2024-03-15T14:30:00")
        assert dt.year == 2024
        assert dt.month == 3
        assert dt.day == 15
        assert dt.hour == 14

    def test_rfc3339_roundtrip(self):
        """测试 RFC 3339 往返一致性"""
        original = datetime(2024, 6, 15, 10, 0, 0)
        formatted = DateUtil.rfc3339_date(original)
        parsed = DateUtil.rfc3339_date_parse(formatted)
        assert parsed.year == original.year
        assert parsed.month == original.month
        assert parsed.day == original.day

    # ── rfc2616_date / rfc2616_date_parse ───────────────────

    def test_rfc2616_date_format(self):
        """测试 RFC 2616 格式化"""
        dt = datetime(2024, 3, 15, 14, 30, 0)
        result = DateUtil.rfc2616_date(dt)
        assert "2024" in result
        assert "GMT" in result

    def test_rfc2616_date_parse(self):
        """测试 RFC 2616 解析"""
        dt = DateUtil.rfc2616_date_parse("Fri, 15 Mar 2024 14:30:00 GMT")
        assert dt.year == 2024
        assert dt.month == 3
        assert dt.day == 15

    # ── convert_to_date / convert_to_datetime ───────────────

    def test_convert_to_date_from_string(self):
        """测试字符串转 date"""
        result = DateUtil.convert_to_date("2024-03-15")
        assert result == date(2024, 3, 15)

    def test_convert_to_date_from_datetime(self):
        """测试 datetime 转 date"""
        dt = datetime(2024, 3, 15, 14, 30)
        result = DateUtil.convert_to_date(dt)
        assert result == date(2024, 3, 15)

    def test_convert_to_date_from_date(self):
        """测试 date 保持不变"""
        d = date(2024, 3, 15)
        result = DateUtil.convert_to_date(d)
        assert result == d

    def test_convert_to_date_none(self):
        """测试 None 返回 None"""
        assert DateUtil.convert_to_date(None) is None

    def test_convert_to_datetime_from_string(self):
        """测试字符串转 datetime"""
        result = DateUtil.convert_to_datetime("2024-03-15 14:30:00")
        assert result.year == 2024
        assert result.month == 3
        assert result.hour == 14

    def test_convert_to_datetime_from_date(self):
        """测试 date 转 datetime"""
        d = date(2024, 3, 15)
        result = DateUtil.convert_to_datetime(d)
        assert result.year == 2024
        assert result.month == 3
        assert result.day == 15

    def test_convert_to_datetime_none(self):
        """测试 None 返回 None"""
        assert DateUtil.convert_to_datetime(None) is None

    def test_convert_to_datetime_formats(self):
        """测试多种日期格式"""
        formats = [
            "2024-03-15T14:30:00.123456",
            "2024-03-15T14:30:00",
            "2024-03-15 14:30:00",
            "2024-03-15",
            "20240315",
        ]
        for fmt in formats:
            result = DateUtil.convert_to_datetime(fmt)
            assert result is not None, f"Failed to parse: {fmt}"
            assert result.year == 2024

    def test_week_of_month(self):
        from datetime import date

        # 2024-06-01 是周六，属于第 1 周
        assert DateUtil.week_of_month(date(2024, 6, 1)) >= 1
        # 2024-06-10 是周一，属于第 2 周
        assert DateUtil.week_of_month(date(2024, 6, 10)) >= 2

    def test_week_of_month_with_datetime(self):
        dt = datetime(2024, 6, 15, 12, 0, 0)
        result = DateUtil.week_of_month(dt)
        assert 1 <= result <= 6

    def test_get_last_day_of_month(self):
        assert DateUtil.get_last_day_of_month(datetime(2024, 2, 1)) == 29  # 闰年
        assert DateUtil.get_last_day_of_month(datetime(2023, 2, 1)) == 28  # 非闰年
        assert DateUtil.get_last_day_of_month(datetime(2024, 1, 15)) == 31
        assert DateUtil.get_last_day_of_month(datetime(2024, 4, 10)) == 30

    def test_get_last_day_of_month_with_date(self):
        assert DateUtil.get_last_day_of_month(date(2024, 12, 25)) == 31

    def test_new_simple_format(self):
        fmt_func = DateUtil.new_simple_format("yyyy-MM-dd")
        dt = datetime(2024, 6, 15)
        result = fmt_func(dt)
        assert result == "2024-06-15"

    def test_new_simple_format_with_time(self):
        fmt_func = DateUtil.new_simple_format("yyyy/MM/dd HH:mm:ss")
        dt = datetime(2024, 6, 15, 14, 30, 45)
        result = fmt_func(dt)
        assert result == "2024/06/15 14:30:45"

    def test_offset_millisecond(self):
        dt = datetime(2024, 6, 15, 12, 0, 0, 0)
        result = DateUtil.offset_millisecond(dt, 500)
        assert result.to_datetime().microsecond == 500000

    def test_offset_millisecond_negative(self):
        dt = datetime(2024, 6, 15, 12, 0, 0, 500000)
        result = DateUtil.offset_millisecond(dt, -500)
        assert result.to_datetime().microsecond == 0

    def test_parse_time_today(self):
        result = DateUtil.parse_time_today("12:30:00")
        assert result.hour() == 12
        assert result.minute() == 30
        assert result.second() == 0
        today = datetime.now()
        assert result.to_datetime().date() == today.date()

    def test_parse_time_today_custom_format(self):
        result = DateUtil.parse_time_today("14:30", fmt="%H:%M")
        assert result.hour() == 14
        assert result.minute() == 30

    def test_range_func(self):
        start = datetime(2024, 6, 1)
        end = datetime(2024, 6, 4)
        result = list(DateUtil.range_func(start, end))
        assert len(result) == 3
        assert result[0].day == 1
        assert result[2].day == 3

    def test_range_func_week(self):
        start = datetime(2024, 6, 1)
        end = datetime(2024, 6, 22)
        result = list(DateUtil.range_func(start, end, "week"))
        assert len(result) == 3

    def test_range_consume(self):
        consumed = []
        start = datetime(2024, 6, 1)
        end = datetime(2024, 6, 4)
        result = DateUtil.range_consume(start, end, consumer=lambda d: consumed.append(d.day))
        assert len(result) == 3
        assert consumed == [1, 2, 3]

    def test_range_consume_no_consumer(self):
        start = datetime(2024, 6, 1)
        end = datetime(2024, 6, 3)
        result = DateUtil.range_consume(start, end)
        assert len(result) == 2

    def test_range_not_contains_overlap(self):
        r1 = (datetime(2024, 6, 1), datetime(2024, 6, 10))
        r2 = (datetime(2024, 6, 5), datetime(2024, 6, 15))
        assert DateUtil.range_not_contains(r1, r2) is False

    def test_range_not_contains_no_overlap(self):
        r1 = (datetime(2024, 6, 1), datetime(2024, 6, 5))
        r2 = (datetime(2024, 6, 10), datetime(2024, 6, 15))
        assert DateUtil.range_not_contains(r1, r2) is True

    def test_range_not_contains_adjacent(self):
        r1 = (datetime(2024, 6, 1), datetime(2024, 6, 5))
        r2 = (datetime(2024, 6, 5), datetime(2024, 6, 10))
        # 相邻但不重叠（e1 <= s2）
        assert DateUtil.range_not_contains(r1, r2) is True

    def test_spend_nt(self):
        start = _time.perf_counter_ns()
        # 做一些耗时操作
        sum(range(10000))
        elapsed = DateUtil.spend_nt(start)
        assert elapsed >= 0
        assert isinstance(elapsed, int)

    def test_to_int_second(self):
        dt = datetime(2024, 6, 15, 12, 0, 0)
        result = DateUtil.to_int_second(dt)
        assert isinstance(result, int)
        assert result > 0

    def test_to_int_second_with_date(self):
        d = date(2024, 6, 15)
        result = DateUtil.to_int_second(d)
        assert isinstance(result, int)

    def test_format_http_date(self):
        dt = datetime(2024, 6, 15, 12, 0, 0)
        result = DateUtil.format_http_date(dt)
        assert isinstance(result, str)
        assert "GMT" in result or "UTC" in result
        assert "2024" in result

    def test_format_http_date_default(self):
        result = DateUtil.format_http_date()
        assert isinstance(result, str)

    def test_format_between_enhanced_second(self):
        begin = datetime(2024, 6, 15, 12, 0, 0)
        end = datetime(2024, 6, 15, 12, 0, 5)
        result = DateUtil.format_between_enhanced(begin, end, "second")
        assert "5秒" in result

    def test_format_between_enhanced_millisecond(self):
        begin = datetime(2024, 6, 15, 12, 0, 0, 0)
        end = datetime(2024, 6, 15, 12, 0, 0, 500000)
        result = DateUtil.format_between_enhanced(begin, end, "millisecond")
        assert "500毫秒" in result

    def test_convert_timezone_enhanced(self):
        dt = datetime(2024, 6, 15, 12, 0, 0)
        result = DateUtil.convert_timezone_enhanced(dt, "Asia/Shanghai", "UTC")
        assert result.hour == 4  # 上海 12:00 = UTC 04:00

    def test_convert_timezone_enhanced_with_pendulum(self):
        # 用原生 datetime（naive），假设为上海时间 12:00
        dt = datetime(2024, 6, 15, 12, 0, 0)
        result = DateUtil.convert_timezone_enhanced(dt, "Asia/Shanghai", "UTC")
        assert result.hour == 4

    def test_today_date(self):
        from datetime import date as _date

        result = DateUtil.today_date()
        assert isinstance(result, _date)
        assert result == _date.today()

    def test_yesterday_date(self):
        from datetime import date as _date

        result = DateUtil.yesterday_date()
        assert isinstance(result, _date)
        assert result == _date.today() - timedelta(days=1)

    def test_tomorrow_date(self):
        from datetime import date as _date

        result = DateUtil.tomorrow_date()
        assert isinstance(result, _date)
        assert result == _date.today() + timedelta(days=1)

    def test_week_start_default(self):
        result = DateUtil.week_start()
        assert result.weekday() == 0  # Monday

    def test_week_start_with_date(self):
        d = date(2024, 6, 19)  # Wednesday
        result = DateUtil.week_start(d)
        assert result == date(2024, 6, 17)  # Monday

    def test_week_end_default(self):
        result = DateUtil.week_end()
        assert result.weekday() == 6  # Sunday

    def test_week_end_with_date(self):
        d = date(2024, 6, 19)  # Wednesday
        result = DateUtil.week_end(d)
        assert result == date(2024, 6, 23)  # Sunday

    def test_day_start_default(self):
        result = DateUtil.day_start()
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0

    def test_day_start_with_datetime(self):
        dt = datetime(2024, 6, 15, 14, 30, 45)
        result = DateUtil.day_start(dt)
        assert result == datetime(2024, 6, 15, 0, 0, 0)

    def test_day_end_default(self):
        result = DateUtil.day_end()
        assert result.hour == 23
        assert result.minute == 59

    def test_day_end_with_date(self):
        d = date(2024, 6, 15)
        result = DateUtil.day_end(d)
        assert result.hour == 23
        assert result.microsecond == 999999

    def test_month_start_default(self):
        result = DateUtil.month_start()
        assert result.day == 1

    def test_month_start_with_date(self):
        d = date(2024, 6, 15)
        assert DateUtil.month_start(d) == date(2024, 6, 1)

    def test_month_end_june(self):
        d = date(2024, 6, 15)
        assert DateUtil.month_end(d) == date(2024, 6, 30)

    def test_month_end_feb_leap(self):
        d = date(2024, 2, 1)
        assert DateUtil.month_end(d) == date(2024, 2, 29)

    def test_month_end_feb_non_leap(self):
        d = date(2023, 2, 1)
        assert DateUtil.month_end(d) == date(2023, 2, 28)

    def test_is_between_dates_true(self):
        d = date(2024, 6, 15)
        assert DateUtil.is_between_dates(d, date(2024, 6, 1), date(2024, 6, 30)) is True

    def test_is_between_dates_boundary(self):
        d = date(2024, 6, 1)
        assert DateUtil.is_between_dates(d, date(2024, 6, 1), date(2024, 6, 30)) is True

    def test_is_between_dates_false(self):
        d = date(2024, 7, 1)
        assert DateUtil.is_between_dates(d, date(2024, 6, 1), date(2024, 6, 30)) is False

    def test_get_weekday_name_zh(self):
        d = date(2024, 6, 17)  # Monday
        assert DateUtil.get_weekday_name(d) == "星期一"

    def test_get_weekday_name_en(self):
        d = date(2024, 6, 17)  # Monday
        assert DateUtil.get_weekday_name(d, locale="en") == "Monday"

    def test_get_month_name_zh(self):
        d = date(2024, 6, 1)
        assert DateUtil.get_month_name(d) == "六月"

    def test_get_month_name_en(self):
        d = date(2024, 6, 1)
        assert DateUtil.get_month_name(d, locale="en") == "June"

    def test_get_tertial(self):
        assert DateUtil.get_tertial(date(2024, 1, 1)) == 1
        assert DateUtil.get_tertial(date(2024, 4, 30)) == 1
        assert DateUtil.get_tertial(date(2024, 5, 1)) == 2
        assert DateUtil.get_tertial(date(2024, 8, 31)) == 2
        assert DateUtil.get_tertial(date(2024, 9, 1)) == 3
        assert DateUtil.get_tertial(date(2024, 12, 31)) == 3

    def test_tertial_add(self):
        d = date(2024, 1, 15)
        result = DateUtil.tertial_add(d, 1)
        assert result == date(2024, 5, 15)

    def test_tertial_add_negative(self):
        d = date(2024, 6, 15)
        result = DateUtil.tertial_add(d, -1)
        assert result == date(2024, 2, 15)

    def test_get_tertial_span_q1(self):
        d = date(2024, 3, 15)
        start, end = DateUtil.get_tertial_span(d)
        assert start == date(2024, 1, 1)
        assert end == date(2024, 4, 30)

    def test_get_tertial_span_q2(self):
        d = date(2024, 6, 15)
        start, end = DateUtil.get_tertial_span(d)
        assert start == date(2024, 5, 1)
        assert end == date(2024, 8, 31)

    def test_group_by_day(self):
        data = [
            (datetime(2024, 6, 15, 10, 0), "a"),
            (datetime(2024, 6, 15, 14, 0), "b"),
            (datetime(2024, 6, 16, 9, 0), "c"),
        ]
        result = DateUtil.group_by_day(data)
        assert len(result) == 2
        assert len(result[date(2024, 6, 15)]) == 2
        assert len(result[date(2024, 6, 16)]) == 1

    def test_group_by_week(self):
        data = [
            (datetime(2024, 6, 17, 10, 0), "a"),  # Mon
            (datetime(2024, 6, 18, 10, 0), "b"),  # Tue
            (datetime(2024, 6, 24, 10, 0), "c"),  # next Mon
        ]
        result = DateUtil.group_by_week(data)
        assert len(result) == 2

    def test_group_by_month(self):
        data = [
            (datetime(2024, 6, 15), "a"),
            (datetime(2024, 6, 20), "b"),
            (datetime(2024, 7, 1), "c"),
        ]
        result = DateUtil.group_by_month(data)
        assert len(result) == 2
        assert len(result[(2024, 6)]) == 2

    def test_group_by_quarter(self):
        data = [
            (datetime(2024, 2, 1), "a"),
            (datetime(2024, 4, 1), "b"),
            (datetime(2024, 10, 1), "c"),
        ]
        result = DateUtil.group_by_quarter(data)
        assert len(result) == 3
        assert (2024, 1) in result
        assert (2024, 2) in result
        assert (2024, 4) in result

    def test_group_by_year(self):
        data = [
            (datetime(2023, 6, 1), "a"),
            (datetime(2024, 1, 1), "b"),
            (datetime(2024, 12, 31), "c"),
        ]
        result = DateUtil.group_by_year(data)
        assert len(result) == 2
        assert len(result[2024]) == 2

    # ── parse_natural ────────────────────────────────────────────

    def test_parse_natural_standard_format(self):
        """标准日期时间格式。"""
        result = DateUtil.parse_natural("2024-01-15 12:30:00")
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 12
        assert result.minute == 30
        assert result.second == 0

    def test_parse_natural_now(self):
        """now 关键字。"""
        before = datetime.now()
        result = DateUtil.parse_natural("now")
        after = datetime.now()
        assert before <= result <= after

    def test_parse_natural_now_case_insensitive(self):
        """now 关键字大小写不敏感。"""
        result = DateUtil.parse_natural("NOW")
        assert isinstance(result, datetime)

    def test_parse_natural_plus_days(self):
        """+Nd 正向天偏移。"""
        before = datetime.now()
        result = DateUtil.parse_natural("+1d")
        expected_min = before + timedelta(days=1) - timedelta(seconds=2)
        expected_max = before + timedelta(days=1) + timedelta(seconds=2)
        assert expected_min <= result <= expected_max

    def test_parse_natural_minus_hours(self):
        """-Nh 负向小时偏移。"""
        before = datetime.now()
        result = DateUtil.parse_natural("-2h")
        expected_min = before - timedelta(hours=2) - timedelta(seconds=2)
        expected_max = before - timedelta(hours=2) + timedelta(seconds=2)
        assert expected_min <= result <= expected_max

    def test_parse_natural_combined(self):
        """组合偏移 +1d-2h+30m。"""
        before = datetime.now()
        result = DateUtil.parse_natural("+1d-2h+30m")
        expected_min = before + timedelta(days=1, hours=-2, minutes=30) - timedelta(seconds=2)
        expected_max = before + timedelta(days=1, hours=-2, minutes=30) + timedelta(seconds=2)
        assert expected_min <= result <= expected_max

    def test_parse_natural_years(self):
        """年偏移（按 365.24 天折算）。"""
        before = datetime.now()
        result = DateUtil.parse_natural("+1y")
        expected_days = int(365.24 * 1)
        expected_min = before + timedelta(days=expected_days) - timedelta(seconds=2)
        expected_max = before + timedelta(days=expected_days) + timedelta(seconds=2)
        assert expected_min <= result <= expected_max

    def test_parse_natural_months(self):
        """月偏移（按 30.42 天折算）。"""
        before = datetime.now()
        result = DateUtil.parse_natural("+2M")
        expected_days = int(30.42 * 2)
        expected_min = before + timedelta(days=expected_days) - timedelta(seconds=2)
        expected_max = before + timedelta(days=expected_days) + timedelta(seconds=2)
        assert expected_min <= result <= expected_max

    def test_parse_natural_weeks(self):
        """周偏移。"""
        before = datetime.now()
        result = DateUtil.parse_natural("+1w")
        expected_min = before + timedelta(weeks=1) - timedelta(seconds=2)
        expected_max = before + timedelta(weeks=1) + timedelta(seconds=2)
        assert expected_min <= result <= expected_max

    def test_parse_natural_seconds(self):
        """秒偏移。"""
        before = datetime.now()
        result = DateUtil.parse_natural("+60s")
        expected_min = before + timedelta(seconds=60) - timedelta(seconds=2)
        expected_max = before + timedelta(seconds=60) + timedelta(seconds=2)
        assert expected_min <= result <= expected_max

    def test_parse_natural_complex_expression(self):
        """复杂组合表达式 +1y-3M+5d-2h+30m-10s。"""
        before = datetime.now()
        result = DateUtil.parse_natural("+1y-3M+5d-2h+30m-10s")
        expected_days = int(365.24 * 1) - int(30.42 * 3) + 5
        expected_delta = timedelta(days=expected_days, hours=-2, minutes=30, seconds=-10)
        expected_min = before + expected_delta - timedelta(seconds=2)
        expected_max = before + expected_delta + timedelta(seconds=2)
        assert expected_min <= result <= expected_max

    def test_parse_natural_invalid(self):
        """无效字符串应抛出 ValueError。"""
        import pytest

        with pytest.raises(ValueError, match="无法解析"):
            DateUtil.parse_natural("invalid_string")


class TestDateTime:
    def test_create(self):
        dt = DateTime("2024-01-15")
        assert dt.year() == 2024
        assert dt.month() == 1
        assert dt.day_of_month() == 15

    def test_comparison(self):
        dt1 = DateTime("2024-01-01")
        dt2 = DateTime("2024-01-02")
        assert dt1 < dt2
        assert dt2 > dt1

    def test_offset(self):
        dt = DateTime("2024-01-15")
        result = dt.offset(days=5)
        assert result.day_of_month() == 20

    def test_begin_of_day(self):
        dt = DateTime("2024-01-15T14:30:00")
        result = dt.begin_of_day()
        assert result.hour() == 0

    def test_end_of_day(self):
        dt = DateTime("2024-01-15")
        result = dt.end_of_day()
        assert result.hour() == 23

    def test_to_string(self):
        dt = DateTime("2024-01-15")
        result = str(dt)
        assert "2024" in result

    # ── age_by_birthday ─────────────────────────────────────────────

    def test_age_by_birthday_str(self):
        """测试从字符串计算年龄"""
        from datetime import date

        today = date.today()
        # 使用一个已过去的生日
        birthday = f"{today.year - 25}-01-01"
        if today.month < 1 or (today.month == 1 and today.day < 1):
            birthday = f"{today.year - 26}-01-01"
        age = DateUtil.age_by_birthday(birthday)
        assert age in (25, 24, 26)  # 允许日期边界差异

    def test_age_by_birthday_date(self):
        """测试从 date 对象计算年龄"""
        from datetime import date

        bd = date(1990, 6, 15)
        age = DateUtil.age_by_birthday(bd)
        assert 30 < age < 40

    def test_age_by_birthday_not_yet(self):
        """测试今年生日还没到"""
        from datetime import date

        today = date.today()
        # 用一个未来日期作为生日
        future_birthday = date(today.year - 20, 12, 31)
        if today.month == 12 and today.day == 31:
            future_birthday = date(today.year - 21, 12, 31)
        age = DateUtil.age_by_birthday(future_birthday)
        assert age in (19, 20)

    # ── is_same_month ───────────────────────────────────────────────

    def test_is_same_month_true(self):
        """测试同月"""
        from datetime import date

        assert DateUtil.is_same_month(date(2024, 3, 1), date(2024, 3, 31)) is True

    def test_is_same_month_false(self):
        """测试不同月"""
        from datetime import date

        assert DateUtil.is_same_month(date(2024, 3, 1), date(2024, 4, 1)) is False

    def test_is_same_month_different_year(self):
        """测试不同年同月"""
        from datetime import date

        assert DateUtil.is_same_month(date(2023, 3, 1), date(2024, 3, 1)) is False

    # ── is_same_week ────────────────────────────────────────────────

    def test_is_same_week_true(self):
        """测试同周"""
        from datetime import date

        # 2024-01-15 (周一) 和 2024-01-17 (周三) 在同一周
        assert DateUtil.is_same_week(date(2024, 1, 15), date(2024, 1, 17)) is True

    def test_is_same_week_false(self):
        """测试不同周"""
        from datetime import date

        assert DateUtil.is_same_week(date(2024, 1, 14), date(2024, 1, 15)) is False

    def test_is_same_week_weekend(self):
        """测试跨周末"""
        from datetime import date

        # 2024-01-13 (周六) 和 2024-01-14 (周日) 在同一周
        assert DateUtil.is_same_week(date(2024, 1, 13), date(2024, 1, 14)) is True

    # ── time_ago ────────────────────────────────────────────────────

    def test_time_ago_just_now(self):
        """测试刚刚"""
        import time

        assert DateUtil.time_ago(time.time()) == "刚刚"

    def test_time_ago_minutes(self):
        """测试分钟前"""
        import time

        ts = time.time() - 300  # 5 分钟前
        assert DateUtil.time_ago(ts) == "5分钟前"

    def test_time_ago_hours(self):
        """测试小时前"""
        import time

        ts = time.time() - 7200  # 2 小时前
        assert DateUtil.time_ago(ts) == "2小时前"

    def test_time_ago_days(self):
        """测试天前"""
        import time

        ts = time.time() - 86400 * 3  # 3 天前
        assert DateUtil.time_ago(ts) == "3天前"

    def test_time_ago_future(self):
        """测试未来时间"""
        import time

        assert DateUtil.time_ago(time.time() + 100) == "刚刚"

    # ── iso_timestamp ───────────────────────────────────────────────

    def test_iso_timestamp_format(self):
        """测试 ISO 时间戳格式"""
        result = DateUtil.iso_timestamp()
        assert result.endswith("Z")
        assert "T" in result
        assert len(result) == 24  # 2024-01-01T12:00:00.000Z

    def test_is_last_day_of_month_true(self):
        from datetime import date

        assert DateUtil.is_last_day_of_month(date(2024, 2, 29)) is True
        assert DateUtil.is_last_day_of_month(date(2024, 1, 31)) is True

    def test_is_last_day_of_month_false(self):
        from datetime import date

        assert DateUtil.is_last_day_of_month(date(2024, 2, 28)) is False

    def test_is_expired(self):
        from datetime import date

        assert DateUtil.is_expired(date(2020, 1, 1), date(2023, 1, 1), date(2025, 1, 1)) is True
        assert DateUtil.is_expired(date(2024, 6, 15), date(2023, 1, 1), date(2025, 1, 1)) is False

    def test_is_overlap_true(self):
        from datetime import date

        assert DateUtil.is_overlap(date(2024, 1, 1), date(2024, 6, 30), date(2024, 6, 1), date(2024, 12, 31)) is True

    def test_is_overlap_false(self):
        from datetime import date

        assert DateUtil.is_overlap(date(2024, 1, 1), date(2024, 3, 31), date(2024, 4, 1), date(2024, 6, 30)) is False

    def test_is_between(self):
        from datetime import date

        assert DateUtil.is_between(date(2024, 6, 15), date(2024, 1, 1), date(2024, 12, 31)) is True
        assert DateUtil.is_between(date(2025, 1, 1), date(2024, 1, 1), date(2024, 12, 31)) is False

    def test_day_of_year(self):
        from datetime import date

        assert DateUtil.day_of_year(date(2024, 1, 1)) == 1
        assert DateUtil.day_of_year(date(2024, 12, 31)) == 366

    def test_length_of_month(self):
        from datetime import date

        assert DateUtil.length_of_month(date(2024, 2, 1)) == 29
        assert DateUtil.length_of_month(date(2024, 1, 1)) == 31

    def test_length_of_year(self):
        assert DateUtil.length_of_year(2024) == 366
        assert DateUtil.length_of_year(2023) == 365

    def test_millisecond(self):
        from datetime import datetime

        dt = datetime(2024, 1, 1, 12, 0, 0, 500000)
        assert DateUtil.millisecond(dt) == 500

    def test_get_zodiac(self):
        assert DateUtil.get_zodiac(3, 21) == "白羊座"
        assert DateUtil.get_zodiac(12, 25) == "摩羯座"

    def test_get_chinese_zodiac(self):
        assert DateUtil.get_chinese_zodiac(2024) == "龙"
        assert DateUtil.get_chinese_zodiac(2023) == "兔"

    def test_compare(self):
        from datetime import date

        assert DateUtil.compare(date(2024, 1, 1), date(2024, 1, 2)) < 0
        assert DateUtil.compare(date(2024, 1, 1), date(2024, 1, 1)) == 0
        assert DateUtil.compare(None, date(2024, 1, 1)) < 0
        assert DateUtil.compare(date(2024, 1, 1), None) > 0

    def test_format_chinese_date(self):
        from datetime import date

        assert DateUtil.format_chinese_date(date(2024, 3, 15)) == "2024年3月15日"

    def test_this_year(self):
        from datetime import datetime

        assert DateUtil.this_year() == datetime.now().year

    def test_this_month(self):
        from datetime import datetime

        assert DateUtil.this_month() == datetime.now().month

    def test_this_week_of_year(self):
        result = DateUtil.this_week_of_year()
        assert 1 <= result <= 53

    def test_this_week_of_month(self):
        result = DateUtil.this_week_of_month()
        assert 1 <= result <= 5

    def test_this_day_of_month(self):
        from datetime import datetime

        assert DateUtil.this_day_of_month() == datetime.now().day

    def test_this_day_of_week(self):
        result = DateUtil.this_day_of_week()
        assert 1 <= result <= 7

    def test_this_hour(self):
        from datetime import datetime

        assert DateUtil.this_hour() == datetime.now().hour

    def test_this_minute(self):

        assert 0 <= DateUtil.this_minute() <= 59

    def test_this_second(self):

        assert 0 <= DateUtil.this_second() <= 59

    def test_this_millisecond(self):

        assert 0 <= DateUtil.this_millisecond() <= 999

    def test_time_to_second(self):
        assert DateUtil.time_to_second("01:00:00") == 3600
        assert DateUtil.time_to_second("00:01:30") == 90
        assert DateUtil.time_to_second("00:00:00") == 0

    def test_second_to_time(self):
        assert DateUtil.second_to_time(3600) == "01:00:00"
        assert DateUtil.second_to_time(90) == "00:01:30"
        assert DateUtil.second_to_time(0) == "00:00:00"

    def test_second_to_time_negative(self):
        import pytest

        with pytest.raises(ValueError):
            DateUtil.second_to_time(-1)

    def test_age_of_now(self):
        age = DateUtil.age_of_now("1990-01-01")
        assert 30 < age < 50

    def test_age(self):
        from datetime import date

        assert DateUtil.age(date(1990, 6, 15), date(2024, 6, 14)) == 33
        assert DateUtil.age(date(1990, 6, 15), date(2024, 6, 15)) == 34
        assert DateUtil.age(date(1990, 6, 15), date(2024, 6, 16)) == 34

    def test_truncate_day(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 30, 45)
        result = DateUtil.truncate(dt, "day")
        assert result == datetime(2024, 6, 15, 0, 0, 0)

    def test_truncate_hour(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 30, 45)
        result = DateUtil.truncate(dt, "hour")
        assert result == datetime(2024, 6, 15, 14, 0, 0)

    def test_truncate_year(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 30, 45)
        result = DateUtil.truncate(dt, "year")
        assert result == datetime(2024, 1, 1, 0, 0, 0)

    def test_truncate_month(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 30, 45)
        result = DateUtil.truncate(dt, "month")
        assert result == datetime(2024, 6, 1, 0, 0, 0)

    def test_range_contains(self):
        from datetime import datetime

        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        assert DateUtil.range_contains(start, end, datetime(2024, 6, 15)) is True
        assert DateUtil.range_contains(start, end, datetime(2025, 1, 1)) is False
        assert DateUtil.range_contains(start, end, start) is True
        assert DateUtil.range_contains(start, end, end) is True

    def test_year_and_quarter(self):
        from datetime import datetime

        assert DateUtil.year_and_quarter(datetime(2024, 3, 15)) == "20241"
        assert DateUtil.year_and_quarter(datetime(2024, 6, 15)) == "20242"
        assert DateUtil.year_and_quarter(datetime(2024, 9, 15)) == "20243"
        assert DateUtil.year_and_quarter(datetime(2024, 12, 15)) == "20244"

    def test_create_stop_watch(self):
        sw = DateUtil.create_stop_watch("test")
        assert sw is not None

    def test_nanos_to_millis(self):
        assert DateUtil.nanos_to_millis(1_000_000) == 1.0
        assert DateUtil.nanos_to_millis(1_500_000) == 1.5

    def test_nanos_to_seconds(self):
        assert DateUtil.nanos_to_seconds(1_000_000_000) == 1.0
        assert DateUtil.nanos_to_seconds(2_500_000_000) == 2.5

    def test_format_between_ms(self):
        result = DateUtil.format_between_ms(3661001)
        assert "1小时" in result
        assert "1分" in result
        assert "1秒" in result
        assert "1毫秒" in result

    def test_format_between_ms_level_day(self):
        result = DateUtil.format_between_ms(90000000, level="day")
        assert result == "1天"

    def test_format_between_ms_level_hour(self):
        result = DateUtil.format_between_ms(7200000, level="hour")
        assert result == "2小时"

    def test_format_between_ms_level_second(self):
        result = DateUtil.format_between_ms(5000, level="second")
        assert result == "5秒"

    def test_format_between_ms_zero(self):
        result = DateUtil.format_between_ms(0)
        assert result == "0毫秒"

    def test_format_between_ms_negative(self):
        result = DateUtil.format_between_ms(-5000)
        assert "5秒" in result

    def test_format_local_datetime(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 30, 45)
        result = DateUtil.format_local_datetime(dt)
        assert result == "2024-06-15 14:30:45"

    def test_parse_local_datetime(self):
        result = DateUtil.parse_local_datetime("2024-06-15 14:30:45")
        assert result.year == 2024
        assert result.month == 6
        assert result.hour == 14

    def test_round_day(self):
        from datetime import datetime

        # 12:00:00 is the midpoint
        dt_before = datetime(2024, 6, 15, 11, 59, 59)
        dt_after = datetime(2024, 6, 15, 12, 0, 0)
        assert DateUtil.round(dt_before, "day") == datetime(2024, 6, 15, 0, 0, 0)
        assert DateUtil.round(dt_after, "day") == datetime(2024, 6, 16, 0, 0, 0)

    def test_round_hour(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 29, 59)
        assert DateUtil.round(dt, "hour") == datetime(2024, 6, 15, 14, 0, 0)
        dt2 = datetime(2024, 6, 15, 14, 30, 0)
        assert DateUtil.round(dt2, "hour") == datetime(2024, 6, 15, 15, 0, 0)

    def test_ceiling(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 30, 45)
        assert DateUtil.ceiling(dt, "day") == datetime(2024, 6, 16, 0, 0, 0)
        assert DateUtil.ceiling(dt, "hour") == datetime(2024, 6, 15, 15, 0, 0)

    def test_ceiling_already_truncated(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 0, 0, 0)
        assert DateUtil.ceiling(dt, "day") == datetime(2024, 6, 15, 0, 0, 0)

    def test_begin_of_hour(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 30, 45, 123456)
        assert DateUtil.begin_of_hour(dt) == datetime(2024, 6, 15, 14, 0, 0)

    def test_end_of_hour(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 30, 45)
        result = DateUtil.end_of_hour(dt)
        assert result.hour == 14
        assert result.minute == 59

    def test_begin_of_minute(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 30, 45, 123456)
        assert DateUtil.begin_of_minute(dt) == datetime(2024, 6, 15, 14, 30, 0)

    def test_end_of_minute(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 30, 45)
        result = DateUtil.end_of_minute(dt)
        assert result.second == 59

    def test_begin_of_second(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 30, 45, 123456)
        assert DateUtil.begin_of_second(dt) == datetime(2024, 6, 15, 14, 30, 45)

    def test_end_of_second(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15, 14, 30, 45)
        result = DateUtil.end_of_second(dt)
        assert result.microsecond == 999999

    def test_offset_generic_day(self):
        from datetime import datetime

        dt = datetime(2024, 1, 15)
        result = DateUtil.offset(dt, "day", 5)
        assert result.day == 20

    def test_offset_generic_month(self):
        from datetime import datetime

        dt = datetime(2024, 1, 31)
        result = DateUtil.offset(dt, "month", 1)
        assert result.month == 2
        assert result.day == 29  # 2024 is leap year

    def test_offset_generic_year(self):
        from datetime import datetime

        dt = datetime(2024, 6, 15)
        result = DateUtil.offset(dt, "year", -1)
        assert result.year == 2023

    def test_range(self):
        from datetime import datetime

        result = DateUtil.range(datetime(2024, 1, 1), datetime(2024, 1, 4))
        assert len(result) == 3
        assert result[0] == datetime(2024, 1, 1)
        assert result[-1] == datetime(2024, 1, 3)

    def test_range_to_list(self):
        from datetime import datetime

        result = DateUtil.range_to_list(datetime(2024, 1, 1), datetime(2024, 1, 3))
        assert len(result) == 3
        assert result[-1] == datetime(2024, 1, 3)

    def test_parse_utc(self):
        dt = DateUtil.parse_utc("2024-01-15T10:30:00Z")
        assert dt.year == 2024
        assert dt.hour == 10

    def test_parse_rfc2822(self):
        dt = DateUtil.parse_rfc2822("Mon, 15 Jan 2024 10:30:00 +0000")
        assert dt.year == 2024
        assert dt.month == 1
        assert dt.day == 15

    def test_of_date(self):
        dt = DateTime.of_date(2024, 6, 15)
        assert dt.year() == 2024
        assert dt.month() == 6
        assert dt.day_of_month() == 15

    def test_of_datetime(self):
        dt = DateTime.of_datetime(2024, 6, 15, 14, 30, 45)
        assert dt.hour() == 14
        assert dt.minute() == 30
        assert dt.second() == 45

    def test_of_pattern(self):
        dt = DateTime.of_pattern("2024-06-15 14:30:45", "yyyy-MM-dd HH:mm:ss")
        assert dt.year() == 2024
        assert dt.hour() == 14

    def test_now_utc(self):
        dt = DateTime.now_utc()
        assert dt is not None

    def test_of_epoch_millis(self):
        ts = 1700000000000  # 2023-11-14 ~22:13:20 UTC
        dt = DateTime.of_epoch(ts, is_millis=True)
        assert dt.year() == 2023

    def test_of_epoch_seconds(self):
        ts = 1700000000
        dt = DateTime.of_epoch(ts, is_millis=False)
        assert dt.year() == 2023

    def test_is_weekend(self):
        # 2024-01-13 is Saturday
        dt = DateTime.of_date(2024, 1, 13)
        assert dt.is_weekend() is True
        dt2 = DateTime.of_date(2024, 1, 15)  # Monday
        assert dt2.is_weekend() is False

    def test_is_am_pm(self):
        dt = DateTime.of_datetime(2024, 1, 1, 10, 0, 0)
        assert dt.is_am() is True
        assert dt.is_pm() is False
        dt2 = DateTime.of_datetime(2024, 1, 1, 14, 0, 0)
        assert dt2.is_am() is False
        assert dt2.is_pm() is True

    def test_is_past(self):
        dt = DateTime.of_date(2000, 1, 1)
        assert dt.is_past() is True

    def test_is_future(self):
        dt = DateTime.of_date(2099, 1, 1)
        assert dt.is_future() is True

    def test_is_before_after(self):
        dt1 = DateTime.of_date(2024, 1, 1)
        dt2 = DateTime.of_date(2024, 6, 1)
        assert dt1.is_before(dt2) is True
        assert dt2.is_after(dt1) is True

    def test_is_between_v2(self):
        dt = DateTime.of_date(2024, 6, 15)
        start = DateTime.of_date(2024, 1, 1)
        end = DateTime.of_date(2024, 12, 31)
        assert dt.is_between(start, end) is True

    def test_is_leap_year(self):
        dt = DateTime.of_date(2024, 1, 1)
        assert dt.is_leap_year() is True
        dt2 = DateTime.of_date(2023, 1, 1)
        assert dt2.is_leap_year() is False

    def test_is_last_day_of_month(self):
        dt = DateTime.of_date(2024, 2, 29)
        assert dt.is_last_day_of_month() is True
        dt2 = DateTime.of_date(2024, 2, 28)
        assert dt2.is_last_day_of_month() is False

    def test_length_of_month_v2(self):
        dt = DateTime.of_date(2024, 2, 1)
        assert dt.length_of_month() == 29
        dt2 = DateTime.of_date(2024, 1, 1)
        assert dt2.length_of_month() == 31

    def test_length_of_year_v2(self):
        dt = DateTime.of_date(2024, 1, 1)
        assert dt.length_of_year() == 366
        dt2 = DateTime.of_date(2023, 1, 1)
        assert dt2.length_of_year() == 365

    def test_offset_methods(self):
        dt = DateTime.of_date(2024, 1, 15)
        assert dt.offset_day(1).day_of_month() == 16
        assert dt.offset_week(1).day_of_month() == 22
        assert dt.offset_month(1).month() == 2
        assert dt.offset_year(1).year() == 2025

    def test_begin_of_second_v2(self):
        dt = DateTime.of_datetime(2024, 6, 15, 14, 30, 45)
        result = dt.begin_of_second()
        assert result.second() == 45

    def test_end_of_second_v2(self):
        dt = DateTime.of_datetime(2024, 6, 15, 14, 30, 45)
        result = dt.end_of_second()
        assert result.second() == 45

    def test_begin_of_hour_v2(self):
        dt = DateTime.of_datetime(2024, 6, 15, 14, 30, 45)
        result = dt.begin_of_hour()
        assert result.minute() == 0
        assert result.second() == 0

    def test_end_of_hour_v2(self):
        dt = DateTime.of_datetime(2024, 6, 15, 14, 30, 45)
        result = dt.end_of_hour()
        assert result.minute() == 59

    def test_begin_of_minute_v2(self):
        dt = DateTime.of_datetime(2024, 6, 15, 14, 30, 45)
        result = dt.begin_of_minute()
        assert result.second() == 0

    def test_end_of_minute_v2(self):
        dt = DateTime.of_datetime(2024, 6, 15, 14, 30, 45)
        result = dt.end_of_minute()
        assert result.second() == 59

    def test_format(self):
        dt = DateTime.of_datetime(2024, 6, 15, 14, 30, 45)
        assert dt.format("YYYY-MM-DD") == "2024-06-15"

    def test_to_local_datetime_str(self):
        dt = DateTime.of_datetime(2024, 6, 15, 14, 30, 45)
        assert dt.to_local_datetime_str() == "2024-06-15 14:30:45"

    def test_with_timezone(self):
        dt = DateTime.now_utc()
        shanghai = dt.with_timezone("Asia/Shanghai")
        assert shanghai is not None

    def test_timezone_name(self):
        dt = DateTime.now_utc()
        assert dt.timezone_name() == "UTC"
