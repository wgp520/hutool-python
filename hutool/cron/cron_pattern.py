"""Cron表达式解析与匹配"""

from datetime import datetime, timedelta
from typing import List, Optional, Set


class CronPattern:
    r"""Cron表达式解析与匹配

    支持标准5位cron: 分 时 日 月 周

    特殊字符说明:

    - ``*`` : 匹配任意值
    - ``,`` : 列举多个值 (如 1,3,5)
    - ``-`` : 范围 (如 1-5)
    - ``/`` : 步长 (如 ``\*/5`` 表示每5个单位)
    """

    def __init__(self, pattern: str) -> None:
        """初始化CronPattern

        :param pattern: cron表达式字符串，格式为 "分 时 日 月 周"
        :raises ValueError: 表达式格式不正确
        """
        self._pattern: str = pattern
        self._fields: List[str] = pattern.strip().split()
        if len(self._fields) != 5:
            raise ValueError(f"无效的cron表达式 '{pattern}'，必须包含5个字段: 分 时 日 月 周")

    def match(self, dt: datetime) -> bool:
        """判断给定时间是否匹配

        :param dt: 待匹配的时间
        :return: 是否匹配cron表达式
        """
        minute_set = self._parse_field(self._fields[0], 0, 59)
        hour_set = self._parse_field(self._fields[1], 0, 23)
        day_set = self._parse_field(self._fields[2], 1, 31)
        month_set = self._parse_field(self._fields[3], 1, 12)
        weekday_set = self._parse_field(self._fields[4], 0, 6)

        return (
            dt.minute in minute_set
            and dt.hour in hour_set
            and dt.day in day_set
            and dt.month in month_set
            and dt.weekday() % 7 in weekday_set
        )

    def next_match_time(self, after: Optional[datetime] = None) -> datetime:
        """获取下一次匹配时间

        :param after: 基准时间，默认为当前时间
        :return: 下一次匹配的时间
        :raises RuntimeError: 超过搜索上限仍未找到匹配时间
        """
        if after is None:
            after = datetime.now()
        # 从下一分钟开始搜索
        current = after.replace(second=0, microsecond=0) + timedelta(minutes=1)
        # 最多搜索2年内的匹配
        max_search = 366 * 24 * 60
        for _ in range(max_search):
            if self.match(current):
                return current
            current += timedelta(minutes=1)
        raise RuntimeError(f"在2年内未找到匹配 '{self._pattern}' 的时间")

    @staticmethod
    def _parse_field(field: str, min_val: int, max_val: int) -> Set[int]:
        """解析单个cron字段

        :param field: 字段字符串
        :param min_val: 最小值
        :param max_val: 最大值
        :return: 匹配的值集合
        :raises ValueError: 字段格式不正确
        """
        values: Set[int] = set()

        parts = field.split(",")
        for part in parts:
            step: Optional[int] = None
            if "/" in part:
                range_part, step_str = part.split("/", 1)
                step = int(step_str)
                if step <= 0:
                    raise ValueError(f"步长必须大于0: {part}")
            else:
                range_part = part

            if range_part == "*":
                start = min_val
                end = max_val
            elif "-" in range_part:
                start_str, end_str = range_part.split("-", 1)
                start = int(start_str)
                end = int(end_str)
            else:
                val = int(range_part)
                if step is not None:
                    start = val
                    end = max_val
                else:
                    if val < min_val or val > max_val:
                        raise ValueError(f"值 {val} 超出范围 [{min_val}, {max_val}]")
                    values.add(val)
                    continue

            if step is None:
                step = 1

            for v in range(start, end + 1, step):
                if v < min_val or v > max_val:
                    raise ValueError(f"值 {v} 超出范围 [{min_val}, {max_val}]")
                values.add(v)

        return values

    def __str__(self) -> str:
        """返回cron表达式字符串"""
        return self._pattern
