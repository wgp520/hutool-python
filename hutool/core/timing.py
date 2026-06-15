"""
计时工具类，提供函数计时装饰器和精确计时器。
"""

import time
from functools import wraps
from typing import Callable


def timethis(func: Callable) -> Callable:
    """
    装饰器：统计函数执行耗时并打印到标准输出。

    Examples::

        @timethis
        def slow_func():
            import time
            time.sleep(0.1)

        slow_func()
        # 打印: slow_func :  耗时 0.100...

    :param func: 被装饰的函数
    :return: 装饰后的函数
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} :\t耗时 {elapsed:.6f}")
        return result

    return wrapper


class TimingUtil:
    """计时工具类，提供精确计时器。"""

    # 向后兼容：TimingUtil.timethis 仍可使用
    timethis = staticmethod(timethis)

    class Timer:
        """
        精确计时器，支持 ``start/stop/reset`` 操作和 ``with`` 语句。

        Examples::

            # 用法一：手动控制
            timer = TimingUtil.Timer()
            timer.start()
            # ... 某些操作 ...
            timer.stop()
            print(timer.elapsed)

            # 用法二：with 语句
            with TimingUtil.Timer() as timer:
                # ... 某些操作 ...
                pass
            print(timer.elapsed)

        :param func: 计时函数，默认为 ``time.perf_counter``
        """

        def __init__(self, func: Callable = time.perf_counter):
            self._elapsed = 0.0
            self._func = func
            self._start = None

        def start(self):
            """
            开始计时。

            :raises RuntimeError: 计时器已在运行时
            """
            if self._start is not None:
                raise RuntimeError("计时器已在运行")
            self._start = self._func()

        def stop(self):
            """
            停止计时。

            :raises RuntimeError: 计时器未启动时
            """
            if self._start is None:
                raise RuntimeError("计时器未启动")
            end = self._func()
            self._elapsed += end - self._start
            self._start = None

        def reset(self):
            """重置计时器，将累计时间归零。"""
            self._elapsed = 0.0

        @property
        def elapsed(self) -> float:
            """
            获取累计耗时（秒）。

            :return: 累计耗时（浮点数，单位秒）
            """
            return self._elapsed

        @property
        def running(self) -> bool:
            """
            计时器是否正在运行。

            :return: 是否正在计时
            """
            return self._start is not None

        def __enter__(self):
            self.start()
            return self

        def __exit__(self, *args):
            self.stop()
