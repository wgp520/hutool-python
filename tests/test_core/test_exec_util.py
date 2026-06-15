import sys

import pytest

from hutool import ExecUtil


def _double(x):
    return x * 2


def _square(x):
    return x**2


class TestExecUtil:
    def test_multi_thread_submit(self):
        """测试线程池批量提交"""
        results = ExecUtil.multi_thread_submit(_double, [1, 2, 3, 4])
        assert sorted(results) == [2, 4, 6, 8]

    def test_multi_thread_submit_single(self):
        """测试单个任务"""
        results = ExecUtil.multi_thread_submit(lambda x: x + 1, [10])
        assert results == [11]

    def test_multi_thread_submit_empty(self):
        """测试空列表"""
        results = ExecUtil.multi_thread_submit(lambda x: x, [])
        assert results == []

    @pytest.mark.skipif(sys.platform == "win32", reason="multiprocessing pickling issues in test env")
    def test_multi_process_submit(self):
        """测试进程池批量提交"""
        results = ExecUtil.multi_process_submit(_square, [1, 2, 3, 4])
        assert sorted(results) == [1, 4, 9, 16]

    @pytest.mark.skipif(sys.platform == "win32", reason="multiprocessing pickling issues in test env")
    def test_multi_process_submit_empty(self):
        """测试空列表"""
        results = ExecUtil.multi_process_submit(_square, [])
        assert results == []
