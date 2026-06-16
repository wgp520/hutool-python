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
        result = RandomUtil.random_string_lower(100)
        assert len(result) == 100
        # 现在包含小写字母+数字
        for c in result:
            assert c.isalnum() and (c.islower() or c.isdigit())

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

    def test_random_chinese(self):
        result = RandomUtil.random_chinese(5)
        assert len(result) == 5
        for ch in result:
            assert 0x4E00 <= ord(ch) <= 0x9FFF

    def test_random_char(self):
        result = RandomUtil.random_char("abc")
        assert result in ("a", "b", "c")

    def test_random_char_empty_raises(self):
        import pytest

        with pytest.raises(ValueError):
            RandomUtil.random_char("")

    def test_random_day(self):
        from datetime import datetime

        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        day = RandomUtil.random_day(start, end)
        assert start <= day < end

    def test_random_ints(self):
        result = RandomUtil.random_ints(5, 1, 10)
        assert len(result) == 5
        assert all(1 <= x < 10 for x in result)

    def test_random_string_without_str(self):
        exclude = "aeiou"
        result = RandomUtil.random_string_without_str(20, exclude)
        assert len(result) == 20
        for ch in result:
            assert ch not in exclude

    def test_random_string_lower_without_str(self):
        exclude = "xyz"
        result = RandomUtil.random_string_lower_without_str(20, exclude)
        assert len(result) == 20
        for ch in result:
            assert ch not in exclude

    def test_random_element_weighted(self):
        """测试别名方法"""
        pairs = [(1, "a"), (9, "b")]
        results = {RandomUtil.random_element_weighted(pairs) for _ in range(50)}
        assert "b" in results

    def test_random_ele_with_condition(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = RandomUtil.random_ele_with_condition(data, lambda x: x > 5, 3)
        assert len(result) == 3
        assert all(x > 5 for x in result)

    def test_random_ele_with_condition_empty(self):
        result = RandomUtil.random_ele_with_condition([1, 2], lambda x: x > 10)
        assert result == []

    def test_random_eles_allow_duplicate(self):
        """测试允许重复选取"""
        lst = [1, 2, 3]
        result = RandomUtil.random_eles(lst, 5, allow_duplicate=True)
        assert len(result) == 5
        for r in result:
            assert r in lst

    def test_random_eles_no_duplicate(self):
        """测试不允许重复选取"""
        lst = [1, 2, 3, 4, 5]
        result = RandomUtil.random_eles(lst, 3, allow_duplicate=False)
        assert len(result) == 3
        assert len(set(result)) == 3

    def test_create_secure_random(self):
        """测试创建随机数生成器"""
        rng = RandomUtil.create_secure_random()
        assert isinstance(rng, type(RandomUtil.create_secure_random()))
        val = rng.randint(0, 100)
        assert 0 <= val <= 100

    def test_create_secure_random_with_seed(self):
        """测试带种子的随机数生成器可复现"""
        rng1 = RandomUtil.create_secure_random(b"test_seed")
        rng2 = RandomUtil.create_secure_random(b"test_seed")
        assert rng1.randint(0, 1000) == rng2.randint(0, 1000)

    def test_get_secure_random(self):
        """测试获取默认随机数生成器"""
        rng = RandomUtil.get_secure_random()
        val = rng.randint(0, 10)
        assert 0 <= val <= 10

    def test_get_secure_random_strong(self):
        """测试获取强随机数生成器"""
        rng = RandomUtil.get_secure_random_strong()
        val = rng.randint(0, 10)
        assert 0 <= val <= 10

    def test_random_int_with_bound_inclusive(self):
        """测试包含边界的随机整数"""
        for _ in range(100):
            val = RandomUtil.random_int_with_bound(1, 10, include_min=True, include_max=True)
            assert 1 <= val <= 10

    def test_random_int_with_bound_exclusive(self):
        """测试排除边界的随机整数"""
        for _ in range(100):
            val = RandomUtil.random_int_with_bound(1, 10, include_min=False, include_max=False)
            assert 2 <= val <= 9

    def test_random_long(self):
        """测试无参随机长整数"""
        val = RandomUtil.random_long()
        assert 0 <= val < 2**63

    def test_random_long_range(self):
        """测试指定范围随机长整数"""
        for _ in range(100):
            val = RandomUtil.random_long(10, 100)
            assert 10 <= val < 100

    def test_random_ints_permutation(self):
        """测试随机排列"""
        result = RandomUtil.random_ints_permutation(5)
        assert sorted(result) == [0, 1, 2, 3, 4]
        assert len(result) == 5

    def test_random_number_char(self):
        """测试随机数字字符"""
        for _ in range(100):
            ch = RandomUtil.random_number_char()
            assert ch in "0123456789"

    def test_random_char_no_arg(self):
        """测试无参随机字符"""
        base = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for _ in range(100):
            ch = RandomUtil.random_char_no_arg()
            assert ch in base

    def test_random_ele_list(self):
        """测试不重复随机元素列表"""
        lst = [1, 2, 3, 4, 5]
        result = RandomUtil.random_ele_list(lst, 3)
        assert len(result) == 3
        assert len(set(result)) == 3

    def test_random_ele_set(self):
        """测试不重复随机元素集合"""
        lst = [1, 2, 3, 4, 5]
        result = RandomUtil.random_ele_set(lst, 3)
        assert isinstance(result, set)
        assert len(result) == 3

    def test_random_ele_from_first_n(self):
        """测试从前 N 个元素中随机选取"""
        lst = [10, 20, 30, 40, 50]
        for _ in range(50):
            val = RandomUtil.random_ele_from_first_n(lst, 3)
            assert val in [10, 20, 30]

    def test_random_ele_from_first_n_empty_raises(self):
        """测试空序列抛异常"""
        import pytest

        with pytest.raises(ValueError):
            RandomUtil.random_ele_from_first_n([], 3)

    def test_weight_random(self):
        """测试 weight_random 别名"""
        pairs = [(1, "a"), (9, "b")]
        results = {RandomUtil.weight_random(pairs) for _ in range(50)}
        assert "b" in results
