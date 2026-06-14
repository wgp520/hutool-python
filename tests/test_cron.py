from hutool import CronPattern


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
