import time

from hutool import TimingUtil


class TestTimethis:
    """测试顶层 timethis 装饰器"""

    def test_timethis_preserves_return(self):
        """测试装饰器不改变返回值"""

        @TimingUtil.timethis
        def add(a, b):
            return a + b

        assert add(1, 2) == 3

    def test_timethis_preserves_name(self):
        """测试保留函数名"""

        @TimingUtil.timethis
        def my_func():
            pass

        assert my_func.__name__ == "my_func"

    def test_timethis_prints_output(self, capsys):
        """测试打印耗时输出"""

        @TimingUtil.timethis
        def slow():
            time.sleep(0.05)

        slow()
        captured = capsys.readouterr()
        assert "耗时" in captured.out

    def test_backward_compat_timing_util_timethis(self):
        """测试 TimingUtil.timethis 仍可用"""

        @TimingUtil.timethis
        def add(a, b):
            return a + b

        assert add(1, 2) == 3


class TestTimingUtilTimer:
    """测试 Timer 类"""

    def test_timer_manual(self):
        """测试手动 start/stop"""
        timer = TimingUtil.Timer()
        timer.start()
        time.sleep(0.05)
        timer.stop()
        assert timer.elapsed > 0.0

    def test_timer_context_manager(self):
        """测试 with 语句"""
        with TimingUtil.Timer() as timer:
            time.sleep(0.05)
        assert timer.elapsed > 0.0

    def test_timer_reset(self):
        """测试重置"""
        timer = TimingUtil.Timer()
        timer.start()
        time.sleep(0.01)
        timer.stop()
        assert timer.elapsed > 0
        timer.reset()
        assert timer.elapsed == 0.0

    def test_timer_running_property(self):
        """测试 running 属性"""
        timer = TimingUtil.Timer()
        assert timer.running is False
        timer.start()
        assert timer.running is True
        timer.stop()
        assert timer.running is False

    def test_timer_start_twice_raises(self):
        """测试重复启动抛异常"""
        timer = TimingUtil.Timer()
        timer.start()
        try:
            timer.start()
            raise AssertionError("应抛出 RuntimeError")
        except RuntimeError:
            pass
        finally:
            timer.stop()

    def test_timer_stop_without_start_raises(self):
        """测试未启动就停止抛异常"""
        timer = TimingUtil.Timer()
        try:
            timer.stop()
            raise AssertionError("应抛出 RuntimeError")
        except RuntimeError:
            pass
