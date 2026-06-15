from datetime import date, datetime

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
