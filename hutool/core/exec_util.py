"""
并发执行工具类，提供线程池和进程池批量任务提交。
"""

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import Any, Callable, List


class ExecUtil:
    """并发执行工具类，提供线程池和进程池批量任务提交。

    所有方法使用 ``concurrent.futures`` 标准库实现。
    """

    @staticmethod
    def multi_thread_submit(
        func: Callable,
        items: list,
        max_workers: int = 10,
    ) -> List[Any]:
        """
        使用线程池批量提交任务并等待全部完成。

        *items* 中每个元素作为 ``func`` 的单个参数传入。

        Examples::

            def process(item):
                return item * 2

            results = ExecUtil.multi_thread_submit(process, [1, 2, 3, 4])
            # results 为 [2, 4, 6, 8]（顺序可能不同）

        :param func: 任务函数
        :param items: 参数列表，每个元素作为一次调用的参数
        :param max_workers: 最大线程数，默认 10
        :return: 所有任务结果的列表
        """
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_list = [executor.submit(func, item) for item in items]
            for future in as_completed(future_list):
                results.append(future.result())
        return results

    @staticmethod
    def multi_process_submit(
        func: Callable,
        items: list,
        max_workers: int = 10,
    ) -> List[Any]:
        """
        使用进程池批量提交任务并等待全部完成。

        *items* 中每个元素作为 ``func`` 的单个参数传入。
        注意：``func`` 和参数必须可 pickle 序列化。

        Examples::

            def process(item):
                return item ** 2

            results = ExecUtil.multi_process_submit(process, [1, 2, 3, 4])

        :param func: 任务函数
        :param items: 参数列表
        :param max_workers: 最大进程数，默认 10
        :return: 所有任务结果的列表
        """
        results = []
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_list = [executor.submit(func, item) for item in items]
            for future in as_completed(future_list):
                results.append(future.result())
        return results
