"""WorkdayUtil 测试"""

from datetime import date, datetime

from hutool import WorkdayUtil


class TestWorkdayUtil:
    """WorkdayUtil 测试类"""

    def setup_method(self):
        """每个测试前重置自定义假日"""
        WorkdayUtil.set_custom_holidays(None)

    # ── holidays ────────────────────────────────────────────

    def test_holidays_2024(self):
        """测试获取 2024 年假日列表"""
        holidays = WorkdayUtil.holidays(2024)
        assert date(2024, 1, 1) in holidays  # 元旦
        assert date(2024, 5, 1) in holidays  # 劳动节
        assert date(2024, 10, 1) in holidays  # 国庆节
        assert date(2024, 10, 2) in holidays  # 国庆节
        assert date(2024, 2, 10) in holidays  # 春节

    def test_holidays_custom(self):
        """测试自定义假日"""
        custom = [date(2024, 3, 15), date(2024, 7, 4)]
        WorkdayUtil.set_custom_holidays(custom)
        holidays = WorkdayUtil.holidays(2024)
        assert date(2024, 3, 15) in holidays
        assert date(2024, 7, 4) in holidays
        # 默认假日不在自定义列表中
        assert date(2024, 1, 1) not in holidays

    def test_holidays_clear_custom(self):
        """测试清除自定义假日恢复默认"""
        WorkdayUtil.set_custom_holidays([date(2024, 3, 15)])
        WorkdayUtil.set_custom_holidays(None)
        holidays = WorkdayUtil.holidays(2024)
        assert date(2024, 1, 1) in holidays  # 默认假日恢复

    # ── is_workday ──────────────────────────────────────────

    def test_is_workday_normal_weekday(self):
        """测试普通工作日"""
        # 2024-01-02 周二，非假日
        assert WorkdayUtil.is_workday(date(2024, 1, 2)) is True

    def test_is_workday_weekend(self):
        """测试周末"""
        # 2024-01-06 周六
        assert WorkdayUtil.is_workday(date(2024, 1, 6)) is False

    def test_is_workday_holiday(self):
        """测试法定假日"""
        # 2024-01-01 元旦
        assert WorkdayUtil.is_workday(date(2024, 1, 1)) is False

    def test_is_workday_datetime(self):
        """测试 datetime 类型输入"""
        assert WorkdayUtil.is_workday(datetime(2024, 1, 2, 10, 30)) is True
        assert WorkdayUtil.is_workday(datetime(2024, 1, 1, 10, 30)) is False

    # ── next_workday ────────────────────────────────────────

    def test_next_workday_from_friday(self):
        """测试从周五获取下一个工作日"""
        # 2024-01-05 周五 -> 2024-01-08 周一
        result = WorkdayUtil.next_workday(date(2024, 1, 5))
        assert result == date(2024, 1, 8)

    def test_next_workday_from_weekday(self):
        """测试从普通工作日获取下一个工作日"""
        result = WorkdayUtil.next_workday(date(2024, 1, 2))
        assert result == date(2024, 1, 3)

    def test_next_workday_from_holiday(self):
        """测试从假日获取下一个工作日"""
        # 2024-01-01 元旦 -> 跳过假日和周末
        result = WorkdayUtil.next_workday(date(2024, 1, 1))
        # 元旦后是 1/2 周二，是非假日工作日
        assert result == date(2024, 1, 2)

    def test_next_workday_datetime(self):
        """测试 datetime 类型输入"""
        result = WorkdayUtil.next_workday(datetime(2024, 1, 5, 14, 0))
        assert result == date(2024, 1, 8)

    # ── previous_workday ────────────────────────────────────

    def test_previous_workday_from_monday(self):
        """测试从周一获取上一个工作日"""
        # 2024-01-08 周一 -> 2024-01-05 周五
        result = WorkdayUtil.previous_workday(date(2024, 1, 8))
        assert result == date(2024, 1, 5)

    def test_previous_workday_from_weekday(self):
        """测试从普通工作日获取上一个工作日"""
        result = WorkdayUtil.previous_workday(date(2024, 1, 3))
        assert result == date(2024, 1, 2)

    # ── workdays ────────────────────────────────────────────

    def test_workdays_same_day(self):
        """测试同一天"""
        assert WorkdayUtil.workdays(date(2024, 1, 2), date(2024, 1, 2)) == 1

    def test_workdays_week_range(self):
        """测试一周范围"""
        # 2024-01-01(周一,元旦) 到 2024-01-05(周五) = 4 个工作日（元旦不算）
        assert WorkdayUtil.workdays(date(2024, 1, 1), date(2024, 1, 5)) == 4

    def test_workdays_weekend_only(self):
        """测试只有周末"""
        # 2024-01-06(周六) 到 2024-01-07(周日) = 0
        assert WorkdayUtil.workdays(date(2024, 1, 6), date(2024, 1, 7)) == 0

    def test_workdays_reverse(self):
        """测试反向计算（start > end）"""
        result = WorkdayUtil.workdays(date(2024, 1, 5), date(2024, 1, 2))
        assert result < 0

    def test_workdays_datetime(self):
        """测试 datetime 输入"""
        result = WorkdayUtil.workdays(datetime(2024, 1, 2, 9, 0), datetime(2024, 1, 5, 18, 0))
        assert result == 4

    # ── add_workdays ────────────────────────────────────────

    def test_add_workdays_positive(self):
        """测试向后加工作日"""
        # 2024-01-02 周二 + 5 个工作日
        result = WorkdayUtil.add_workdays(date(2024, 1, 2), 5)
        assert result == date(2024, 1, 9)

    def test_add_workdays_zero(self):
        """测试加 0 个工作日"""
        result = WorkdayUtil.add_workdays(date(2024, 1, 2), 0)
        assert result == date(2024, 1, 2)

    def test_add_workdays_negative(self):
        """测试向前减工作日"""
        # 2024-01-09 周二 - 5 个工作日
        result = WorkdayUtil.add_workdays(date(2024, 1, 9), -5)
        assert result == date(2024, 1, 2)

    def test_add_workdays_across_weekend(self):
        """测试跨越周末"""
        # 2024-01-05 周五 + 1 个工作日 = 2024-01-08 周一
        result = WorkdayUtil.add_workdays(date(2024, 1, 5), 1)
        assert result == date(2024, 1, 8)

    def test_add_workdays_across_holiday(self):
        """测试跨越假日"""
        # 2024-12-30 周一 + 5 个工作日（跨越元旦 1/1）
        result = WorkdayUtil.add_workdays(date(2024, 12, 30), 5)
        # 12/31(二,1st), 1/1(三,元旦跳过), 1/2(四,2nd), 1/3(五,3rd),
        # 1/6(一,4th), 1/7(二,5th)
        assert result == date(2025, 1, 7)

    def test_add_workdays_datetime(self):
        """测试 datetime 输入"""
        result = WorkdayUtil.add_workdays(datetime(2024, 1, 2, 14, 0), 3)
        assert result == date(2024, 1, 5)
