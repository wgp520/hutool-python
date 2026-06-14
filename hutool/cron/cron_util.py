"""定时任务工具类"""

import threading
import time
from datetime import datetime
from typing import Callable, List, Optional

from .cron_pattern import CronPattern


class _CronTask:
    """内部Cron任务"""

    def __init__(self, pattern: CronPattern, func: Callable) -> None:
        self.pattern = pattern
        self.func = func


class _FixedRateTask:
    """内部固定频率任务"""

    def __init__(self, func: Callable, period_seconds: int) -> None:
        self.func = func
        self.period_seconds = period_seconds
        self.last_run: Optional[float] = None


class CronUtil:
    """定时任务工具类"""

    _tasks: List[_CronTask] = []
    _fixed_tasks: List[_FixedRateTask] = []
    _running: bool = False
    _thread: Optional[threading.Thread] = None
    _lock = threading.Lock()

    @classmethod
    def schedule(cls, cron_pattern: str, func: Callable) -> None:
        """添加定时任务

        :param cron_pattern: cron表达式字符串，格式为 "分 时 日 月 周"
        :param func: 定时执行的函数
        """
        pattern = CronPattern(cron_pattern)
        with cls._lock:
            cls._tasks.append(_CronTask(pattern, func))

    @classmethod
    def schedule_at_fixed_rate(cls, func: Callable, period_seconds: int) -> None:
        """添加固定频率任务

        :param func: 定时执行的函数
        :param period_seconds: 执行间隔（秒）
        """
        with cls._lock:
            task = _FixedRateTask(func, period_seconds)
            cls._fixed_tasks.append(task)

    @classmethod
    def start(cls) -> None:
        """启动调度器

        调度器在后台线程中运行，每秒检查一次是否有需要执行的任务。
        """
        if cls._running:
            return
        cls._running = True
        cls._thread = threading.Thread(target=cls._run_loop, daemon=True)
        cls._thread.start()

    @classmethod
    def stop(cls) -> None:
        """停止调度器"""
        cls._running = False
        if cls._thread is not None:
            cls._thread.join(timeout=5)
            cls._thread = None

    @classmethod
    def restart(cls) -> None:
        """重启调度器"""
        cls.stop()
        cls.start()

    @classmethod
    def _run_loop(cls) -> None:
        """调度器主循环"""
        while cls._running:
            now = datetime.now()
            # 检查cron任务
            with cls._lock:
                tasks_snapshot = list(cls._tasks)
                fixed_tasks_snapshot = list(cls._fixed_tasks)

            for task in tasks_snapshot:
                try:
                    if task.pattern.match(now):
                        task.func()
                except Exception as e:
                    print(f"[CronUtil] 执行cron任务时发生异常: {e}")

            # 检查固定频率任务
            for task in fixed_tasks_snapshot:
                try:
                    current_time = time.time()
                    if task.last_run is None or (current_time - task.last_run >= task.period_seconds):
                        task.func()
                        task.last_run = current_time
                except Exception as e:
                    print(f"[CronUtil] 执行固定频率任务时发生异常: {e}")

            # 休眠到下一个分钟的开始
            now = datetime.now()
            seconds_until_next_minute = 60 - now.second
            time.sleep(max(1, seconds_until_next_minute))
