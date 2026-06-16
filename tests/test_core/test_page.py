from hutool import PageUtil


class TestPageUtil:
    def test_total_page(self):
        assert PageUtil.total_page(100, 10) == 10
        assert PageUtil.total_page(101, 10) == 11
        assert PageUtil.total_page(0, 10) == 0

    def test_rainbow(self):
        result = PageUtil.rainbow(5, 10, 5)
        assert isinstance(result, list)
        assert all(isinstance(x, int) for x in result)
        assert 5 in result

    def test_to_page(self):
        assert PageUtil.to_page(0, 10) == 1
        assert PageUtil.to_page(10, 10) == 2

    def test_first_page(self):
        assert PageUtil.first_page() == 1

    def test_get_start(self):
        assert PageUtil.get_start(1, 10) == 0
        assert PageUtil.get_start(2, 10) == 10

    def test_to_start_index(self):
        assert PageUtil.to_start_index(1, 10) == 0
        assert PageUtil.to_start_index(3, 10) == 20

    def test_set_first_page_no(self):
        PageUtil.set_first_page_no(1)
        assert PageUtil.get_first_page_no() == 1
        PageUtil.set_first_page_no(0)
        assert PageUtil.get_first_page_no() == 0
        # 恢复
        PageUtil.set_first_page_no(0)

    def test_get_end(self):
        assert PageUtil.get_end(1, 10) == 10
        assert PageUtil.get_end(3, 10) == 30

    def test_trans_to_start_end(self):
        start, end = PageUtil.trans_to_start_end(2, 10)
        assert start == 10
        assert end == 20

    def test_to_segment(self):
        assert PageUtil.to_segment(100, 10) == 10
        assert PageUtil.to_segment(101, 10) == 11
        assert PageUtil.to_segment(0, 10) == 0
        assert PageUtil.to_segment(100, 0) == 0
