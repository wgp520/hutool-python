"""分页工具类"""

from __future__ import annotations

import math
from typing import List


class PageUtil:
    """分页工具类"""

    @staticmethod
    def total_page(total_count: int, page_size: int) -> int:
        """计算总页数"""
        if total_count <= 0 or page_size <= 0:
            return 0
        return math.ceil(total_count / page_size)

    @staticmethod
    def rainbow(page_num: int, total_page: int, display_count: int) -> List[int]:
        """彩虹分页，获取页码列表
        例如: rainbow(5, 10, 3) -> [3,4,5,6,7]
        """
        if page_num < 1 or total_page < 1 or display_count < 1:
            return []

        half = display_count // 2
        start = max(1, page_num - half)
        end = min(total_page, start + display_count - 1)

        # 修正起始位置
        if end - start + 1 < display_count:
            start = max(1, end - display_count + 1)

        return list(range(start, end + 1))

    @staticmethod
    def to_page(start_index: int, page_size: int) -> int:
        """起始索引转页码（从1开始）"""
        if page_size <= 0:
            return 1
        return start_index // page_size + 1

    @staticmethod
    def first_page() -> int:
        """第一页页码，始终返回1"""
        return 1

    @staticmethod
    def get_start(page: int, limit: int) -> int:
        """根据页码和每页条数计算起始行号（从0开始）"""
        if page < 1 or limit < 1:
            return 0
        return (page - 1) * limit

    @staticmethod
    def to_start_index(page_num: int, page_size: int) -> int:
        """页码转起始索引"""
        if page_num < 1 or page_size < 1:
            return 0
        return (page_num - 1) * page_size
