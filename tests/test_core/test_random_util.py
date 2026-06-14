from hutool import RandomUtil


class TestRandomUtil:
    def test_random_int(self):
        for _ in range(100):
            result = RandomUtil.random_int(1, 10)
            assert 1 <= result < 10

    def test_random_float(self):
        for _ in range(100):
            result = RandomUtil.random_float(1.0, 10.0)
            assert 1.0 <= result < 10.0

    def test_random_boolean(self):
        assert isinstance(RandomUtil.random_boolean(), bool)

    def test_random_bytes(self):
        result = RandomUtil.random_bytes(10)
        assert isinstance(result, bytes)
        assert len(result) == 10

    def test_random_ele(self):
        lst = [1, 2, 3, 4, 5]
        result = RandomUtil.random_ele(lst)
        assert result in lst

    def test_random_eles(self):
        lst = [1, 2, 3, 4, 5]
        result = RandomUtil.random_eles(lst, 3)
        assert len(result) == 3
        for r in result:
            assert r in lst

    def test_random_string(self):
        result = RandomUtil.random_string(10)
        assert len(result) == 10

    def test_random_string_upper(self):
        result = RandomUtil.random_string_upper(10)
        assert len(result) == 10
        assert result.isupper()
        assert result.isalpha()

    def test_random_string_lower(self):
        result = RandomUtil.random_string_lower(10)
        assert len(result) == 10
        assert result.islower()
        assert result.isalpha()

    def test_random_numbers(self):
        result = RandomUtil.random_numbers(6)
        assert len(result) == 6
        assert result.isdigit()

    def test_random_color(self):
        result = RandomUtil.random_color()
        assert result.startswith("#")
        assert len(result) == 7

    def test_random_string_with_base(self):
        result = RandomUtil.random_string(5, "AB")
        assert len(result) == 5
        for c in result:
            assert c in "AB"
