from hutool import ReUtil


class TestReUtil:
    def test_is_match(self):
        assert ReUtil.is_match(r"\d+", "123") is True
        assert ReUtil.is_match(r"\d+", "abc") is False

    def test_contains(self):
        assert ReUtil.contains(r"\d+", "abc123def") is True
        assert ReUtil.contains(r"\d+", "abcdef") is False

    def test_get(self):
        result = ReUtil.get(r"\d+", "abc123def")
        assert result == "123"

    def test_get_group(self):
        result = ReUtil.get(r"(\d+)", "abc123def", group_index=1)
        assert result == "123"

    def test_get_all(self):
        result = ReUtil.get_all(r"\d+", "abc123def456")
        assert result == ["123", "456"]

    def test_match_all(self):
        result = ReUtil.match_all(r"\d+", "abc123def456")
        assert result == ["123", "456"]

    def test_replace_all(self):
        result = ReUtil.replace_all("abc123def456", r"\d+", "X")
        assert result == "abcXdefX"

    def test_replace_first(self):
        result = ReUtil.replace_first("abc123def456", r"\d+", "X")
        assert result == "abcXdef456"

    def test_count(self):
        assert ReUtil.count(r"\d+", "abc123def456") == 2

    def test_split(self):
        result = ReUtil.split("abc123def456ghi", r"\d+")
        assert result == ["abc", "def", "ghi"]

    def test_del_all(self):
        result = ReUtil.del_all(r"\d+", "abc123def456")
        assert result == "abcdef"

    def test_escape(self):
        result = ReUtil.escape("[test]")
        assert "[" in result and "]" in result

    def test_find_all(self):
        result = ReUtil.find_all(r"\d+", "abc123def456")
        assert result == ["123", "456"]

    def test_find_all_group0(self):
        result = ReUtil.find_all_group0(r"\d+", "a1b2c3")
        assert result == ["1", "2", "3"]

    def test_find_all_group1(self):
        result = ReUtil.find_all_group1(r"(\d+)", "a1b2c3")
        assert result == ["1", "2", "3"]

    def test_find_first_number(self):
        assert ReUtil.find_first_number("abc123def") == "123"

    def test_find_first_number_no_match(self):
        assert ReUtil.find_first_number("abcdef") is None

    def test_index_of(self):
        assert ReUtil.index_of(r"\d+", "abc123def") == 3

    def test_index_of_no_match(self):
        assert ReUtil.index_of(r"\d+", "abcdef") == -1

    def test_last_index_of(self):
        assert ReUtil.last_index_of(r"\d+", "a12b34") == 4

    def test_last_index_of_no_match(self):
        assert ReUtil.last_index_of(r"\d+", "abcdef") == -1

    def test_del_first(self):
        assert ReUtil.del_first(r"\d+", "a12b34c") == "ab34c"

    def test_del_last(self):
        assert ReUtil.del_last(r"\d+", "a12b34c") == "a12bc"

    def test_del_pre(self):
        assert ReUtil.del_pre(r"\d+", "abc123def") == "def"

    def test_del_pre_no_match(self):
        assert ReUtil.del_pre(r"\d+", "abcdef") is None

    def test_extract_multi_and_del_pre(self):
        result = ReUtil.extract_multi_and_del_pre(r"\d+", "a1b2c3")
        assert result == ["1", "2", "3"]

    def test_get_all_group_names(self):
        """测试获取命名捕获组"""
        names = ReUtil.get_all_group_names(r"(?P<year>\d{4})-(?P<month>\d{2})")
        assert names == {"year": 1, "month": 2}

    def test_get_all_group_names_no_names(self):
        """测试无命名组"""
        names = ReUtil.get_all_group_names(r"(\d+)")
        assert names == {}

    def test_replace_by_func(self):
        """测试正则替换+回调函数"""
        result = ReUtil.replace_by_func("hello123", r"\d+", lambda m: "[NUM]")
        assert result == "hello[NUM]"

    def test_replace_by_func_upper(self):
        """测试回调函数使用匹配内容"""
        result = ReUtil.replace_by_func("abc def", r"\b\w", lambda m: m.group(0).upper())
        assert result == "Abc Def"

    def test_find_first_pattern(self):
        patterns = [r"\d+", r"[a-z]+"]
        result = ReUtil.find_first_pattern("abc123", patterns)
        # 两个都匹配，返回第一个匹配的（\d+ 索引0）
        assert result == r"\d+"

    def test_find_first_pattern_none(self):
        assert ReUtil.find_first_pattern("!!!", [r"\d+", r"[a-z]+"]) is None

    def test_find_all_patterns(self):
        patterns = [r"\d+", r"[a-z]+", r"[A-Z]+"]
        result = ReUtil.find_all_patterns("Hello123", patterns)
        assert r"\d+" in result
        assert r"[A-Z]+" in result

    def test_find_all_patterns_none(self):
        assert ReUtil.find_all_patterns("!!!", [r"\d+", r"[a-z]+"]) == []
