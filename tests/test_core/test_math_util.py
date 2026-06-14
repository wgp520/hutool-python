from hutool import BitStatusUtil, MathUtil


class TestMathUtil:
    def test_add(self):
        result = MathUtil.add(1, 2)
        assert float(result) == 3.0

    def test_point_to_radians(self):
        result = MathUtil.point_to_radians((1.0, 0.0))
        assert abs(result) < 0.01  # Should be ~0

    def test_radians_to_point(self):

        result = MathUtil.radians_to_point(0)
        assert abs(result[0] - 1.0) < 0.01


class TestBitStatusUtil:
    def test_add(self):
        status = BitStatusUtil.add(0, 1, 2)
        assert status == 3

    def test_has(self):
        status = 3  # binary 11
        assert BitStatusUtil.has(status, 1) is True
        assert BitStatusUtil.has(status, 2) is True
        assert BitStatusUtil.has(status, 4) is False

    def test_remove(self):
        status = 7  # binary 111
        result = BitStatusUtil.remove(status, 2)
        assert result == 5  # binary 101

    def test_to_binary_string(self):
        result = BitStatusUtil.to_binary_string(5)
        assert result == "101"
