"""分页工具类"""

from __future__ import annotations

import math
from typing import List


class PageUtil:
    """分页工具类，提供分页计算相关的工具方法。"""

    _FIRST_PAGE_NO = 0

    @staticmethod
    def total_page(total_count: int, page_size: int) -> int:
        """
        根据总记录数和每页条数计算总页数。

        :param total_count: 总记录数
        :param page_size: 每页条数
        :return: 总页数，参数非法时返回 0
        """
        if total_count <= 0 or page_size <= 0:
            return 0
        return math.ceil(total_count / page_size)

    @staticmethod
    def rainbow(page_num: int, total_page: int, display_count: int) -> List[int]:
        """
        彩虹分页算法，获取当前页周围的页码列表。

        例如: ``rainbow(5, 10, 3)`` 返回 ``[3, 4, 5, 6, 7]``

        :param page_num: 当前页码
        :param total_page: 总页数
        :param display_count: 显示的页码个数
        :return: 页码列表
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
        """
        将起始索引转换为页码（从 1 开始）。

        :param start_index: 起始索引
        :param page_size: 每页条数
        :return: 页码，page_size 非法时返回 1
        """
        if page_size <= 0:
            return 1
        return start_index // page_size + 1

    @staticmethod
    def first_page() -> int:
        """
        获取第一页页码。

        :return: 始终返回 1
        """
        return 1

    @staticmethod
    def get_start(page: int, limit: int) -> int:
        """
        根据页码和每页条数计算起始行号（从 0 开始）。

        :param page: 页码（从 1 开始）
        :param limit: 每页条数
        :return: 起始行号
        """
        if page < 1 or limit < 1:
            return 0
        return (page - 1) * limit

    @staticmethod
    def to_start_index(page_num: int, page_size: int) -> int:
        """
        将页码转换为起始索引（从 0 开始）。

        :param page_num: 页码（从 1 开始）
        :param page_size: 每页条数
        :return: 起始索引
        """
        if page_num < 1 or page_size < 1:
            return 0
        return (page_num - 1) * page_size

    @staticmethod
    def set_first_page_no(first_page_no: int) -> None:
        """设置第一页的页码（默认为 0，Java 惯例；Python 通常从 1 开始）。

        :param first_page_no: 第一页页码
        """
        PageUtil._FIRST_PAGE_NO = first_page_no

    @staticmethod
    def get_first_page_no() -> int:
        """获取第一页页码。"""
        return PageUtil._FIRST_PAGE_NO

    @staticmethod
    def get_end(page_num: int, page_size: int) -> int:
        """获取分页结束位置。

        :param page_num: 页码
        :param page_size: 每页大小
        :return: 结束位置
        """
        return page_num * page_size

    @staticmethod
    def trans_to_start_end(page_num: int, page_size: int) -> tuple:
        """将页码转换为起始和结束索引。

        :param page_num: 页码
        :param page_size: 每页大小
        :return: (start, end) 元组
        """
        start = PageUtil.to_start_index(page_num, page_size)
        end = start + page_size
        return (start, end)

    @staticmethod
    def to_segment(total: int, page_size: int) -> int:
        """计算总页数。

        :param total: 总记录数
        :param page_size: 每页大小
        :return: 总页数
        """
        if total <= 0:
            return 0
        if page_size <= 0:
            return 0
        return (total + page_size - 1) // page_size
