from hutool import ProfUtil


class TestProfUtil:
    def test_profile_deco(self, capsys):
        """测试性能分析装饰器"""

        @ProfUtil.profile_deco(sort_by="tottime", limit=5)
        def compute():
            return sum(range(1000))

        result = compute()
        assert result == sum(range(1000))
        captured = capsys.readouterr()
        # cProfile 输出包含函数名
        assert "compute" in captured.out or "ncalls" in captured.out

    def test_profile_context(self, capsys):
        """测试性能分析上下文管理器"""
        with ProfUtil.profile_context(sort_by="tottime", limit=5):
            total = sum(range(1000))
        assert total == sum(range(1000))
        captured = capsys.readouterr()
        assert "ncalls" in captured.out
