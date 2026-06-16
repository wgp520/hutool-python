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

    def test_arrangement_count(self):
        # A(5,3) = 5*4*3 = 60
        assert MathUtil.arrangement_count(5, 3) == 60
        assert MathUtil.arrangement_count(5, 0) == 1
        assert MathUtil.arrangement_count(-1, 3) == 0

    def test_arrangement_select(self):
        assert MathUtil.arrangement_select(5, 3) == 60

    def test_combination_count(self):
        # C(5,3) = 10
        assert MathUtil.combination_count(5, 3) == 10
        assert MathUtil.combination_count(5, 0) == 1
        assert MathUtil.combination_count(5, 5) == 1
        assert MathUtil.combination_count(-1, 3) == 0

    def test_combination_select(self):
        assert MathUtil.combination_select(5, 3) == 10

    def test_yuan_to_cent(self):
        assert MathUtil.yuan_to_cent(1.23) == 123
        assert MathUtil.yuan_to_cent(0.01) == 1
        assert MathUtil.yuan_to_cent(0) == 0

    def test_cent_to_yuan(self):
        assert MathUtil.cent_to_yuan(123) == 1.23
        assert MathUtil.cent_to_yuan(1) == 0.01
        assert MathUtil.cent_to_yuan(0) == 0.0
