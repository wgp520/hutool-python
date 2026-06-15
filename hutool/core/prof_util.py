"""
性能分析工具类，提供基于 cProfile 的函数和代码块性能分析。
"""

import contextlib
import functools
import pstats
from cProfile import Profile
from typing import Callable


class ProfUtil:
    """性能分析工具类，提供 cProfile 装饰器和上下文管理器。

    所有分析结果会打印到标准输出。
    """

    @staticmethod
    def profile_deco(sort_by: str = "cumtime", limit: int = 10) -> Callable:
        """
        装饰器：对函数进行 cProfile 性能分析。

        每次调用被装饰的函数时，会自动运行 cProfile，
        并在函数返回后打印前 *limit* 行统计信息。

        Examples::

            @ProfUtil.profile_deco(sort_by="tottime", limit=5)
            def slow_func():
                ...

        :param sort_by: 排序字段，默认 ``"cumtime"``（累计时间）
            可选值：``"tottime"``（自身时间）、``"cumtime"``、``"calls"`` 等
        :param limit: 打印行数，默认 10
        :return: 装饰器函数
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                p = Profile()
                p.enable()
                try:
                    return func(*args, **kwargs)
                finally:
                    p.disable()
                    s = pstats.Stats(p).sort_stats(sort_by)
                    s.print_stats(limit)

            return wrapper

        return decorator

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
