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

    def test_prof_decorator_is_callable(self):
        assert callable(ProfUtil.prof_decorator)

    def test_prof_context_is_callable(self):
        assert callable(ProfUtil.prof_context)

    def test_prof_decorator_works(self):
        @ProfUtil.prof_decorator(sort_by="tottime", limit=1)
        def fast():
            return 42

        assert fast() == 42

    def test_prof_context_works(self):
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            with ProfUtil.prof_context(limit=1):
                pass
        finally:
            sys.stdout = old_stdout
        # 上下文管理器应正常执行
        assert True
