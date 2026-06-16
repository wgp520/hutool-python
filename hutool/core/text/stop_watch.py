"""秒表计时器模块，对应 Java Hutool 的 cn.hutool.core.date.StopWatch。"""

from __future__ import annotations

import time
from typing import List, Optional


class TaskInfo:
    """任务信息，记录单个任务的名称和耗时。"""

    def __init__(self, task_name: str, time_nanos: int):
        self.task_name = task_name
        self.time_nanos = time_nanos

    @property
    def time_seconds(self) -> float:
        """耗时（秒）。"""
        return self.time_nanos / 1_000_000_000

    @property
    def time_millis(self) -> float:
        """耗时（毫秒）。"""
        return self.time_nanos / 1_000_000

    def __repr__(self) -> str:
        return f"TaskInfo('{self.task_name}', {self.time_millis:.2f}ms)"


class StopWatch:
    """秒表封装，用于存储一组任务的耗时时间并一次性打印对比。

    与 Java Hutool 的 cn.hutool.core.date.StopWatch 对应。

    用法::

        sw = StopWatch("my_task")
        sw.start("step1")
        # ... 操作 ...
        sw.stop()

        sw.start("step2")
        # ... 操作 ...
        sw.stop()

        print(sw.pretty_print())

    :param id_: 秒表标识
    :param keep_task_list: 是否保留任务列表
    """

    def __init__(self, id_: str = "", keep_task_list: bool = True):
        self._id = id_
        self._task_list: Optional[List[TaskInfo]] = [] if keep_task_list else None
        self._current_task_name: Optional[str] = None
        self._start_time_nanos: int = 0
        self._last_task_info: Optional[TaskInfo] = None
        self._task_count: int = 0
        self._total_time_nanos: int = 0

    @property
    def id(self) -> str:
        """获取秒表标识。"""
        return self._id

    def set_keep_task_list(self, keep: bool) -> None:
        """设置是否保留任务列表。

        :param keep: 是否保留
        """
        if keep:
            if self._task_list is None:
                self._task_list = []
        else:
            self._task_list = None

    def start(self, task_name: str = "") -> None:
        """开始新任务。

        :param task_name: 任务名称
        :raises RuntimeError: 前一个任务未结束
        """
        if self._current_task_name is not None:
            raise RuntimeError("Can't start StopWatch: it's already running")
        self._current_task_name = task_name
        self._start_time_nanos = time.perf_counter_ns()

    def stop(self) -> None:
        """停止当前任务。

        :raises RuntimeError: 没有运行中的任务
        """
        if self._current_task_name is None:
            raise RuntimeError("Can't stop StopWatch: it's not running")
        last_time = max(0, time.perf_counter_ns() - self._start_time_nanos)
        self._total_time_nanos += last_time
        self._last_task_info = TaskInfo(self._current_task_name, last_time)
        if self._task_list is not None:
            self._task_list.append(self._last_task_info)
        self._task_count += 1
        self._current_task_name = None

    def is_running(self) -> bool:
        """是否有运行中的任务。"""
        return self._current_task_name is not None

    def current_task_name(self) -> Optional[str]:
        """获取当前任务名，None 表示无任务。"""
        return self._current_task_name

    @property
    def last_task_info(self) -> Optional[TaskInfo]:
        """获取最后一个任务信息。"""
        return self._last_task_info

    @property
    def total_time_nanos(self) -> int:
        """总耗时（纳秒）。"""
        return self._total_time_nanos

    @property
    def total_time_millis(self) -> float:
        """总耗时（毫秒）。"""
        return self._total_time_nanos / 1_000_000

    @property
    def total_time_seconds(self) -> float:
        """总耗时（秒）。"""
        return self._total_time_nanos / 1_000_000_000

    @property
    def task_count(self) -> int:
        """已完成任务数。"""
        return self._task_count

    @property
    def task_list(self) -> List[TaskInfo]:
        """获取任务列表。"""
        if self._task_list is None:
            raise RuntimeError("Task list not kept")
        return list(self._task_list)

    def get_task_info(self, task_name: str) -> Optional[TaskInfo]:
        """根据任务名获取任务信息。

        :param task_name: 任务名称
        :return: TaskInfo 或 None
        """
        if self._task_list is None:
            return None
        for info in self._task_list:
            if info.task_name == task_name:
                return info
        return None

    def pretty_print(self) -> str:
        """以可读格式打印所有任务耗时。

        :return: 格式化的任务耗时字符串
        """
        lines = []
        if self._id:
            lines.append(f"StopWatch '{self._id}': running time = {self.total_time_millis:.2f} ms")
        else:
            lines.append(f"StopWatch: running time = {self.total_time_millis:.2f} ms")
        lines.append("---------------------------------------------")
        lines.append("ms         %     Task name")
        lines.append("---------------------------------------------")
        if self._task_list:
            total = self._total_time_nanos
            for info in self._task_list:
                pct = (info.time_nanos / total * 100) if total > 0 else 0
                lines.append(f"{info.time_millis:>10.2f}  {pct:>5.1f}%  {info.task_name}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"StopWatch('{self._id}', tasks={self._task_count})"
