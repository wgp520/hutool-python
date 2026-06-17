"""定时任务工具类"""

import threading
import time
from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional

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
    _task_ids: Dict[str, int] = {}
    _running: bool = False
    _thread: Optional[threading.Thread] = None
    _lock = threading.Lock()

    @classmethod
    def schedule(cls, cron_pattern: str, func: Callable) -> None:
        """
        添加定时任务。

        :param cron_pattern: cron表达式字符串，格式为 "分 时 日 月 周"
        :param func: 定时执行的函数
        """
        pattern = CronPattern(cron_pattern)
        with cls._lock:
            cls._tasks.append(_CronTask(pattern, func))

    @classmethod
    def schedule_at_fixed_rate(cls, func: Callable, period_seconds: int) -> None:
        """
        添加固定频率任务。

        :param func: 定时执行的函数
        :param period_seconds: 执行间隔（秒）
        """
        with cls._lock:
            task = _FixedRateTask(func, period_seconds)
            cls._fixed_tasks.append(task)

    @classmethod
    def start(cls) -> None:
        """
        启动调度器。

        调度器在后台线程中运行，每秒检查一次是否有需要执行的任务。
        """
        if cls._running:
            return
        cls._running = True
        cls._thread = threading.Thread(target=cls._run_loop, daemon=True)
        cls._thread.start()

    @classmethod
    def stop(cls) -> None:
        """停止调度器。"""
        cls._running = False
        if cls._thread is not None:
            cls._thread.join(timeout=5)
            cls._thread = None

    @classmethod
    def restart(cls) -> None:
        """重启调度器。"""
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

    @classmethod
    def schedule_with_id(cls, task_id: str, cron_pattern: str, func: Callable) -> None:
        """添加带ID的定时任务

        :param task_id: 任务ID
        :param cron_pattern: cron表达式
        :param func: 执行函数
        """
        pattern = CronPattern(cron_pattern)
        with cls._lock:
            index = len(cls._tasks)
            cls._tasks.append(_CronTask(pattern, func))
            cls._task_ids[task_id] = index

    @classmethod
    def remove(cls, task_id: str) -> bool:
        """移除指定ID的任务

        :param task_id: 任务ID
        :return: 是否成功移除
        """
        with cls._lock:
            if task_id in cls._task_ids:
                index = cls._task_ids[task_id]
                if 0 <= index < len(cls._tasks):
                    cls._tasks.pop(index)
                del cls._task_ids[task_id]
                # 重建索引
                new_ids: Dict[str, int] = {}
                for k, v in cls._task_ids.items():
                    if v > index:
                        new_ids[k] = v - 1
                    else:
                        new_ids[k] = v
                cls._task_ids = new_ids
                return True
            return False

    @classmethod
    def get_task_count(cls) -> int:
        """获取任务数量

        :return: 任务总数
        """
        with cls._lock:
            return len(cls._tasks) + len(cls._fixed_tasks)

    @classmethod
    def clear(cls) -> None:
        """清空所有任务"""
        with cls._lock:
            cls._tasks.clear()
            cls._fixed_tasks.clear()
            cls._task_ids.clear()

    @classmethod
    def matched_dates(cls, cron_pattern: str, start, end) -> list:
        """获取指定时间范围内匹配cron表达式的日期列表

        :param cron_pattern: cron表达式
        :param start: 开始时间（datetime）
        :param end: 结束时间（datetime）
        :return: 匹配的datetime列表
        """
        pattern = CronPattern(cron_pattern)
        result = []
        # 从start开始，逐分钟遍历到end
        current = start.replace(second=0, microsecond=0)
        while current <= end:
            if pattern.match(current):
                result.append(current)
            current += timedelta(minutes=1)
        return result

    @classmethod
    def set_cron_setting(cls, setting_path: str) -> None:
        """加载 Cron 配置文件。

        配置文件每行格式为 ``cron_pattern=task_name`` （暂仅记录路径）。

        :param setting_path: 配置文件路径
        """
        cls._setting_path = setting_path

    @classmethod
    def update_pattern(cls, task_index: int, new_pattern: str) -> None:
        """更新已有任务的 Cron 表达式。

        :param task_index: 任务索引（从 0 开始）
        :param new_pattern: 新的 cron 表达式
        :raises IndexError: 索引越界时
        :raises ValueError: 表达式不合法时
        """
        with cls._lock:
            if task_index < 0 or task_index >= len(cls._tasks):
                raise IndexError(f"任务索引越界: {task_index}")
            cls._tasks[task_index].pattern = CronPattern(new_pattern)
