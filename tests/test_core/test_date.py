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
