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

    # ── weighted_choice ────────────────────────────────────────

    def test_weighted_choice_basic(self):
        """测试加权随机选择"""
        pairs = [(1, "a"), (1, "b"), (8, "c")]
        counts = {"a": 0, "b": 0, "c": 0}
        for _ in range(10000):
            result = RandomUtil.weighted_choice(pairs)
            counts[result] += 1
        # c 的权重占 80%，应远多于 a 和 b
        assert counts["c"] > counts["a"]
        assert counts["c"] > counts["b"]

    def test_weighted_choice_single(self):
        """测试单元素"""
        result = RandomUtil.weighted_choice([(1, "only")])
        assert result == "only"

    def test_weighted_choice_all_values(self):
        """测试返回值必须在候选列表中"""
        pairs = [(1, "x"), (2, "y"), (3, "z")]
        for _ in range(100):
            assert RandomUtil.weighted_choice(pairs) in ("x", "y", "z")
