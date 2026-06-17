"""
性能分析工具类，提供基于 cProfile 的函数和代码块性能分析。
"""

import contextlib
import pstats
from cProfile import Profile

from .decorators import ProfileDeco


class ProfUtil:
    """性能分析工具类，提供 cProfile 装饰器和上下文管理器。

    所有分析结果会打印到标准输出。
    """

    @staticmethod
    @contextlib.contextmanager
    def profile_context(sort_by: str = "cumtime", limit: int = 10):
        """
        上下文管理器：对代码块进行 cProfile 性能分析。

        Examples::

            with ProfUtil.profile_context(sort_by="tottime", limit=5):
                # ... 需要分析的代码 ...
                pass

        :param sort_by: 排序字段，默认 ``"cumtime"``
        :param limit: 打印行数，默认 10
        """
        p = Profile()
        p.enable()
        try:
            yield
        finally:
            p.disable()
            s = pstats.Stats(p).sort_stats(sort_by)
            s.print_stats(limit)

    @staticmethod
    @contextlib.contextmanager
    def prof_context(sort_by: str = "cumtime", limit: int = 10):
        """``profile_context`` 别名。

        :param sort_by: 排序字段，默认 ``"cumtime"``
        :param limit: 打印行数，默认 10
        """
        with ProfUtil.profile_context(sort_by=sort_by, limit=limit):
            yield


# 别名
ProfUtil.profile_deco = staticmethod(ProfileDeco)
ProfUtil.prof_decorator = staticmethod(ProfileDeco)
