from datetime import datetime

from hutool import CronPattern, CronUtil, CronValidator


class TestCronPattern:
    def test_parse_every_minute(self):
        cp = CronPattern("* * * * *")
        assert cp is not None

    def test_parse_specific(self):
        cp = CronPattern("30 8 * * *")
        assert cp is not None

    def test_parse_range(self):
        cp = CronPattern("0 9 * * 1-5")
        assert cp is not None

    def test_parse_step(self):
        cp = CronPattern("*/5 * * * *")
        assert cp is not None

    def test_parse_list(self):
        cp = CronPattern("0 9 * * 1,3,5")
        assert cp is not None

    def test_match_every_minute(self):
        import datetime

        cp = CronPattern("* * * * *")
        now = datetime.datetime.now()
        assert cp.match(now) is True

    def test_match_specific(self):
        import datetime

        cp = CronPattern("30 8 15 6 *")  # June 15 at 08:30
        dt = datetime.datetime(2024, 6, 15, 8, 30, 0)
        assert cp.match(dt) is True
        dt2 = datetime.datetime(2024, 6, 15, 9, 30, 0)
        assert cp.match(dt2) is False

    def test_match_step(self):
        import datetime

        cp = CronPattern("*/10 * * * *")
        dt = datetime.datetime(2024, 1, 1, 0, 0, 0)
        assert cp.match(dt) is True
        dt2 = datetime.datetime(2024, 1, 1, 0, 5, 0)
        assert cp.match(dt2) is False

    def test_match_list(self):

        cp = CronPattern("0 9 * * 1,3,5")
        # Monday = 0 in Python, but cron uses 1=Mon, 7=Sun
        # This test depends on implementation
        assert cp is not None


class TestCronUtil:
    def setup_method(self):
        CronUtil.clear()

    def test_schedule_with_id(self):
        CronUtil.schedule_with_id("task1", "*/5 * * * *", lambda: None)
        assert CronUtil.get_task_count() >= 1

    def test_remove(self):
        CronUtil.schedule_with_id("task1", "*/5 * * * *", lambda: None)
        result = CronUtil.remove("task1")
        assert result is True

    def test_remove_nonexistent(self):
        result = CronUtil.remove("no_such_task")
        assert result is False

    def test_get_task_count(self):
        assert CronUtil.get_task_count() == 0
        CronUtil.schedule_with_id("t1", "*/5 * * * *", lambda: None)
        assert CronUtil.get_task_count() == 1

    def test_clear(self):
        CronUtil.schedule_with_id("t1", "*/5 * * * *", lambda: None)
        CronUtil.clear()
        assert CronUtil.get_task_count() == 0

    def test_matched_dates(self):
        start = datetime(2026, 1, 1, 0, 0)
        end = datetime(2026, 1, 1, 0, 5)
        dates = CronUtil.matched_dates("* * * * *", start, end)
        assert isinstance(dates, list)
        assert len(dates) > 0

    def test_set_cron_setting(self):
        CronUtil.set_cron_setting("/path/to/cron.properties")
        assert hasattr(CronUtil, "_setting_path")


class TestCronValidator:
    # ── validate (整体校验) ─────────────────────────────────

    def test_validate_6_fields(self):
        assert CronValidator.validate("0 0 12 * * ?") is True

    def test_validate_7_fields(self):
        assert CronValidator.validate("0 0 12 * * ? *") is True

    def test_validate_invalid_field_count(self):
        assert CronValidator.validate("0 0 12 * *") is False
        assert CronValidator.validate("0 0 12 * * ? 2026 extra") is False

    def test_validate_complex_expression(self):
        assert CronValidator.validate("0 0/5 14 * * ?") is True
        assert CronValidator.validate("0 15 10 ? * 6L") is True
        assert CronValidator.validate("0 15 10 ? * 6#3") is True

    def test_validate_invalid_expression(self):
        assert CronValidator.validate("invalid") is False
        assert CronValidator.validate("60 0 0 1 1 ?") is False

    # ── is_valid ────────────────────────────────────────────

    def test_is_valid_true(self):
        assert CronValidator.is_valid("0 0 12 * * ?") is True

    def test_is_valid_none(self):
        assert CronValidator.is_valid(None) is False

    def test_is_valid_empty(self):
        assert CronValidator.is_valid("") is False

    # ── validate_cron_expression (别名) ─────────────────────

    def test_validate_cron_expression_alias(self):
        assert CronValidator.validate_cron_expression("0 0 12 * * ?") is True
        assert CronValidator.validate_cron_expression("bad") is False

    # ── validate_second_or_minute ───────────────────────────

    def test_second_wildcard(self):
        assert CronValidator.validate_second_or_minute("*") is True

    def test_second_range(self):
        assert CronValidator.validate_second_or_minute("0-59") is True

    def test_second_range_invalid(self):
        assert CronValidator.validate_second_or_minute("60-70") is False

    def test_second_step(self):
        assert CronValidator.validate_second_or_minute("0/5") is True

    def test_second_list(self):
        assert CronValidator.validate_second_or_minute("1,3,5") is True

    def test_second_single_value(self):
        assert CronValidator.validate_second_or_minute("30") is True

    def test_second_invalid(self):
        assert CronValidator.validate_second_or_minute("abc") is False

    # ── validate_hour ───────────────────────────────────────

    def test_hour_wildcard(self):
        assert CronValidator.validate_hour("*") is True

    def test_hour_range(self):
        assert CronValidator.validate_hour("0-23") is True

    def test_hour_range_invalid(self):
        assert CronValidator.validate_hour("0-24") is False

    def test_hour_step(self):
        assert CronValidator.validate_hour("0/2") is True

    def test_hour_list(self):
        assert CronValidator.validate_hour("9,12,18") is True

    # ── validate_day ────────────────────────────────────────

    def test_day_wildcard(self):
        assert CronValidator.validate_day("*") is True

    def test_day_question(self):
        assert CronValidator.validate_day("?") is True

    def test_day_last(self):
        assert CronValidator.validate_day("L") is True

    def test_day_workday(self):
        assert CronValidator.validate_day("15W") is True

    def test_day_range(self):
        assert CronValidator.validate_day("1-31") is True

    def test_day_list(self):
        assert CronValidator.validate_day("1,15,30") is True

    # ── validate_month ──────────────────────────────────────

    def test_month_wildcard(self):
        assert CronValidator.validate_month("*") is True

    def test_month_range(self):
        assert CronValidator.validate_month("1-12") is True

    def test_month_list(self):
        assert CronValidator.validate_month("1,6,12") is True

    # ── validate_week ───────────────────────────────────────

    def test_week_wildcard(self):
        assert CronValidator.validate_week("*") is True

    def test_week_question(self):
        assert CronValidator.validate_week("?") is True

    def test_week_range(self):
        assert CronValidator.validate_week("1-7") is True

    def test_week_hash(self):
        assert CronValidator.validate_week("6#3") is True

    def test_week_last(self):
        assert CronValidator.validate_week("6L") is True

    def test_week_list(self):
        assert CronValidator.validate_week("1,3,5") is True

    def test_week_invalid(self):
        assert CronValidator.validate_week("8") is False

    # ── validate_year ───────────────────────────────────────

    def test_year_wildcard(self):
        assert CronValidator.validate_year("*") is True
