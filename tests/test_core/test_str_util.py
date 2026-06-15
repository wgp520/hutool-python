from hutool import CharPool, CharUtil, StrUtil


class TestCharPool:
    def test_constants(self):
        assert CharPool.SPACE == " "
        assert CharPool.TAB == "\t"
        assert CharPool.DOT == "."
        assert CharPool.SLASH == "/"
        assert CharPool.BACKSLASH == "\\"
        assert CharPool.LF == "\n"
        assert CharPool.CR == "\r"
        assert CharPool.UNDERLINE == "_"
        assert CharPool.DASHED == "-"
        assert CharPool.COMMA == ","
        assert CharPool.COLON == ":"
        assert CharPool.AT == "@"
        assert CharPool.AMP == "&"
        assert CharPool.EMPTY == ""
        assert CharPool.DOUBLE_QUOTES == '"'
        assert CharPool.SINGLE_QUOTE == "'"


class TestCharUtil:
    def test_is_letter(self):
        assert CharUtil.is_letter("a") is True
        assert CharUtil.is_letter("Z") is True
        assert CharUtil.is_letter("5") is False

    def test_is_number(self):
        assert CharUtil.is_number("5") is True
        assert CharUtil.is_number("a") is False

    def test_is_letter_or_number(self):
        assert CharUtil.is_letter_or_number("a") is True
        assert CharUtil.is_letter_or_number("5") is True
        assert CharUtil.is_letter_or_number("@") is False

    def test_is_letter_upper(self):
        assert CharUtil.is_letter_upper("A") is True
        assert CharUtil.is_letter_upper("a") is False

    def test_is_letter_lower(self):
        assert CharUtil.is_letter_lower("a") is True
        assert CharUtil.is_letter_lower("A") is False

    def test_is_ascii(self):
        assert CharUtil.is_ascii("a") is True
        assert CharUtil.is_ascii("中") is False

    def test_is_blank_char(self):
        assert CharUtil.is_blank_char(" ") is True
        assert CharUtil.is_blank_char("\t") is True
        assert CharUtil.is_blank_char("a") is False

    def test_equals(self):
        assert CharUtil.equals("a", "a", False) is True
        assert CharUtil.equals("a", "A", True) is True

    def test_is_emoji(self):
        assert CharUtil.is_emoji("😀") is True
        assert CharUtil.is_emoji("a") is False


class TestStrUtil:
    def test_is_empty(self):
        assert StrUtil.is_empty("") is True
        assert StrUtil.is_empty(None) is True
        assert StrUtil.is_empty("abc") is False

    def test_is_not_empty(self):
        assert StrUtil.is_not_empty("abc") is True
        assert StrUtil.is_not_empty("") is False

    def test_is_blank(self):
        assert StrUtil.is_blank("") is True
        assert StrUtil.is_blank(None) is True
        assert StrUtil.is_blank("  ") is True
        assert StrUtil.is_blank("abc") is False

    def test_is_not_blank(self):
        assert StrUtil.is_not_blank("abc") is True
        assert StrUtil.is_not_blank("  ") is False

    def test_has_blank(self):
        assert StrUtil.has_blank("", "abc") is True
        assert StrUtil.has_blank("abc", "def") is False

    def test_is_all_blank(self):
        assert StrUtil.is_all_blank("", "  ") is True
        assert StrUtil.is_all_blank("", "abc") is False

    def test_trim(self):
        assert StrUtil.trim("  abc  ") == "abc"
        assert StrUtil.trim(None) is None

    def test_trim_to_empty(self):
        assert StrUtil.trim_to_empty(None) == ""
        assert StrUtil.trim_to_empty("  abc  ") == "abc"

    def test_trim_to_none(self):
        assert StrUtil.trim_to_none("  ") is None
        assert StrUtil.trim_to_none("abc") == "abc"

    def test_strip(self):
        assert StrUtil.strip("__abc__", "__") == "abc"

    def test_start_with(self):
        assert StrUtil.start_with("abc", "a") is True
        assert StrUtil.start_with("abc", "b") is False
        assert StrUtil.start_with_ignore_case("ABC", "a") is True

    def test_end_with(self):
        assert StrUtil.end_with("abc", "c") is True
        assert StrUtil.end_with("abc", "b") is False
        assert StrUtil.end_with_ignore_case("ABC", "c") is True

    def test_contains(self):
        assert StrUtil.contains("abc", "b") is True
        assert StrUtil.contains("abc", "d") is False
        assert StrUtil.contains_ignore_case("ABC", "b") is True

    def test_sub(self):
        assert StrUtil.sub("abcde", 1, 3) == "bc"
        assert StrUtil.sub("abcde", 1) == "bcde"

    def test_sub_before(self):
        assert StrUtil.sub_before("abc.def.ghi", ".", False) == "abc"
        assert StrUtil.sub_before("abc.def.ghi", ".", True) == "abc.def"

    def test_sub_after(self):
        assert StrUtil.sub_after("abc.def.ghi", ".", False) == "def.ghi"
        assert StrUtil.sub_after("abc.def.ghi", ".", True) == "ghi"

    def test_sub_between(self):
        assert StrUtil.sub_between("a[1]b", "[", "]") == "1"

    def test_sub_between_double_char(self):
        result = StrUtil.sub_between("((abc))", "((", "))")
        assert result == "abc"

    def test_count(self):
        assert StrUtil.count("abcabc", "a") == 2
        assert StrUtil.count("abcabc", "ab") == 2

    def test_replace(self):
        assert StrUtil.replace("aabbcc", "b", "d") == "aaddcc"
        assert StrUtil.replace("aabbcc", "b", "d", 1) == "aadbcc"

    def test_replace_first(self):
        assert StrUtil.replace_first("aabbcc", "b", "d") == "aadbcc"

    def test_replace_all(self):
        assert StrUtil.replace_all("aabbcc", "b", "d") == "aaddcc"

    def test_replace_chars(self):
        result = StrUtil.replace_chars("abcabc", "ac", "x")
        assert result == "xbxxbx"

    def test_repeat(self):
        assert StrUtil.repeat("ab", 3) == "ababab"

    def test_join(self):
        assert StrUtil.join(",", "a", "b", "c") == "a,b,c"

    def test_split(self):
        result = StrUtil.split("a,b,c", ",")
        assert result == ["a", "b", "c"]

    def test_split_trim(self):
        result = StrUtil.split("a, b, c", ",", is_trim=True)
        assert result == ["a", "b", "c"]

    def test_split_ignore_empty(self):
        result = StrUtil.split("a,,b,c", ",", ignore_empty=True)
        assert result == ["a", "b", "c"]

    def test_to_camel_case(self):
        assert StrUtil.to_camel_case("hello_world") == "helloWorld"
        assert StrUtil.to_camel_case("user_name") == "userName"

    def test_to_snake_case(self):
        assert StrUtil.to_snake_case("helloWorld") == "hello_world"
        assert StrUtil.to_snake_case("UserName") == "user_name"

    def test_to_under_score_case(self):
        assert StrUtil.to_under_score_case("helloWorld") == "hello_world"

    def test_pad(self):
        assert StrUtil.pad("abc", 5, "0") == "abc00"
        assert StrUtil.pad("abc", 5, "0", is_right=False) == "00abc"

    def test_center(self):
        result = StrUtil.center("abc", 7, "-")
        assert result == "--abc--"

    def test_is_numeric(self):
        assert StrUtil.is_numeric("123") is True
        assert StrUtil.is_numeric("abc") is False

    def test_is_number(self):
        assert StrUtil.is_number("123") is True
        assert StrUtil.is_number("12.3") is True
        assert StrUtil.is_number("abc") is False

    def test_is_alpha(self):
        assert StrUtil.is_alpha("abc") is True
        assert StrUtil.is_alpha("abc1") is False

    def test_is_alpha_upper(self):
        assert StrUtil.is_alpha_upper("ABC") is True
        assert StrUtil.is_alpha_upper("abc") is False

    def test_is_alpha_lower(self):
        assert StrUtil.is_alpha_lower("abc") is True
        assert StrUtil.is_alpha_lower("ABC") is False

    def test_upper_first(self):
        assert StrUtil.upper_first("abc") == "Abc"

    def test_lower_first(self):
        assert StrUtil.lower_first("ABC") == "aBC"

    def test_reverse(self):
        assert StrUtil.reverse("abc") == "cba"

    def test_repeat_and_join(self):
        assert StrUtil.repeat_and_join("ab", 3, ",") == "ab,ab,ab"

    def test_format(self):
        result = StrUtil.format("name={}, age={}", "test", 20)
        assert "test" in result

    def test_format_with_map(self):
        result = StrUtil.format_with_map("name={name}, age={age}", {"name": "test", "age": 20})
        assert result == "name=test, age=20"

    def test_remove_prefix(self):
        assert StrUtil.remove_prefix("abc", "ab") == "c"

    def test_remove_suffix(self):
        assert StrUtil.remove_suffix("abc", "bc") == "a"

    def test_clean_blank(self):
        assert StrUtil.clean_blank("a b c") == "abc"

    def test_sub_between_all(self):
        result = StrUtil.sub_between_all("[a][b][c]", "[", "]")
        assert result == ["a", "b", "c"]

    def test_similar(self):
        s = StrUtil.similar("abc", "abc")
        assert s == 1.0

    def test_join_array(self):
        assert StrUtil.join_array(["a", "b", "c"], ",") == "a,b,c"

    def test_none_to_empty(self):
        assert StrUtil.none_to_empty(None) == ""
        assert StrUtil.none_to_empty("abc") == "abc"

    def test_empty_to_none(self):
        assert StrUtil.empty_to_none("") is None
        assert StrUtil.empty_to_none("abc") == "abc"

    def test_index_of(self):
        assert StrUtil.index_of("abcabc", "b") == 1
        assert StrUtil.index_of("abcabc", "d") == -1

    def test_last_index_of(self):
        assert StrUtil.last_index_of("abcabc", "b") == 4

    def test_contains_any(self):
        assert StrUtil.contains_any("abc", "x", "b") is True
        assert StrUtil.contains_any("abc", "x", "y") is False

    def test_contains_all(self):
        assert StrUtil.contains_all("abcdef", "ab", "cd") is True
        assert StrUtil.contains_all("abcdef", "ab", "zz") is False

    def test_fill(self):
        result = StrUtil.fill("abc", "*", 6, False)
        assert len(result) == 6
        assert result == "abc***"

    def test_append_if_missing(self):
        assert StrUtil.append_if_missing("file.txt", ".txt") == "file.txt"
        assert StrUtil.append_if_missing("file", ".txt") == "file.txt"
        # Multiple suffixes: checks if string ends with ANY of them
        assert StrUtil.append_if_missing("file.txt", ".txt", ".xlsx") == "file.txt"
        assert StrUtil.append_if_missing("file.xlsx", ".txt", ".xlsx") == "file.xlsx"
        assert StrUtil.append_if_missing("file", ".txt", ".xlsx") == "file.txt"

    def test_prepend_if_missing(self):
        assert StrUtil.prepend_if_missing("prefile", "pre") == "prefile"
        assert StrUtil.prepend_if_missing("file", "pre") == "prefile"
        # Multiple prefixes: checks if string starts with ANY of them
        assert StrUtil.prepend_if_missing("prefile", "pre", "suf") == "prefile"
        assert StrUtil.prepend_if_missing("suffile", "pre", "suf") == "suffile"
        assert StrUtil.prepend_if_missing("file", "pre", "suf") == "prefile"


class TestStrUtilOnlyDigits:
    """测试 only_digits 方法"""

    def test_only_digits_basic(self):
        """测试基本数字提取"""
        assert StrUtil.only_digits("abc123def456") == "123456"

    def test_only_digits_all_digits(self):
        """测试纯数字字符串"""
        assert StrUtil.only_digits("12345") == "12345"

    def test_only_digits_no_digits(self):
        """测试无数字字符串"""
        assert StrUtil.only_digits("abcdef") == ""

    def test_only_digits_empty(self):
        """测试空字符串"""
        assert StrUtil.only_digits("") == ""

    def test_only_digits_none(self):
        """测试 None"""
        assert StrUtil.only_digits(None) == ""

    def test_only_digits_special_chars(self):
        """测试特殊字符"""
        assert StrUtil.only_digits("tel: 138-0000-1234") == "13800001234"

    def test_only_digits_with_spaces(self):
        """测试带空格"""
        assert StrUtil.only_digits("1 2 3 4 5") == "12345"


class TestStrUtilDeUmlaut:
    """测试 de_umlaut 方法"""

    def test_de_umlaut_basic(self):
        """测试基本变音符号转换"""
        assert StrUtil.de_umlaut("ä") == "ae"
        assert StrUtil.de_umlaut("ö") == "oe"
        assert StrUtil.de_umlaut("ü") == "ue"
        assert StrUtil.de_umlaut("ß") == "ss"

    def test_de_umlaut_uppercase(self):
        """测试大写变音符号"""
        assert StrUtil.de_umlaut("Ä") == "Ae"
        assert StrUtil.de_umlaut("Ö") == "Oe"
        assert StrUtil.de_umlaut("Ü") == "Ue"

    def test_de_umlaut_in_word(self):
        """测试单词中的变音符号"""
        assert StrUtil.de_umlaut("München") == "Muenchen"
        assert StrUtil.de_umlaut("Straße") == "Strasse"

    def test_de_umlaut_no_umlaut(self):
        """测试无变音符号"""
        assert StrUtil.de_umlaut("hello") == "hello"

    def test_de_umlaut_empty(self):
        """测试空字符串"""
        assert StrUtil.de_umlaut("") == ""


class TestStrUtilNewMethods:
    """hutoolpy 移植方法测试"""

    # ── 全角半角转换 ──────────────────────────────────────

    def test_full_to_half_width_basic(self):
        """测试全角转半角"""
        assert StrUtil.full_to_half_width("Ｈｅｌｌｏ") == "Hello"
        assert StrUtil.full_to_half_width("１２３") == "123"

    def test_full_to_half_width_space(self):
        """测试全角空格转半角"""
        assert StrUtil.full_to_half_width("Ａ　Ｂ") == "A B"

    def test_half_to_full_width_basic(self):
        """测试半角转全角"""
        assert StrUtil.half_to_full_width("Hello") == "Ｈｅｌｌｏ"
        assert StrUtil.half_to_full_width("123") == "１２３"

    def test_half_to_full_width_space(self):
        """测试半角空格转全角"""
        assert StrUtil.half_to_full_width("A B") == "Ａ　Ｂ"

    # ── Levenshtein 编辑距离 ──────────────────────────────

    def test_levenshtein_distance_same(self):
        """测试相同字符串"""
        assert StrUtil.levenshtein_distance("abc", "abc") == 0

    def test_levenshtein_distance_empty(self):
        """测试空字符串"""
        assert StrUtil.levenshtein_distance("", "abc") == 3
        assert StrUtil.levenshtein_distance("abc", "") == 3
        assert StrUtil.levenshtein_distance("", "") == 0

    def test_levenshtein_distance_one_edit(self):
        """测试单次编辑"""
        assert StrUtil.levenshtein_distance("abc", "abd") == 1  # 替换
        assert StrUtil.levenshtein_distance("abc", "abcd") == 1  # 插入
        assert StrUtil.levenshtein_distance("abcd", "abc") == 1  # 删除

    def test_levenshtein_distance_classic(self):
        """测试经典示例"""
        assert StrUtil.levenshtein_distance("kitten", "sitting") == 3
        assert StrUtil.levenshtein_distance("saturday", "sunday") == 3

    # ── 中文过滤 ──────────────────────────────────────────

    def test_filter_chinese_basic(self):
        """测试移除中文字符"""
        assert StrUtil.filter_chinese("Hello世界") == "Hello"
        assert StrUtil.filter_chinese("abc123") == "abc123"

    def test_filter_chinese_all_chinese(self):
        """测试全中文"""
        assert StrUtil.filter_chinese("你好世界") == ""

    def test_filter_chinese_empty(self):
        """测试空字符串"""
        assert StrUtil.filter_chinese("") == ""

    def test_filter_chinese_punctuations_basic(self):
        """测试移除标点"""
        result = StrUtil.filter_chinese_punctuations("Hello, World!")
        assert "Hello" in result
        assert "World" in result

    # ── left_space_count ────────────────────────────────────────────

    def test_left_space_count_spaces(self):
        """测试前导空格计数"""
        assert StrUtil.left_space_count("  hello") == 2

    def test_left_space_count_tab(self):
        """测试 Tab 算 4 个空格"""
        assert StrUtil.left_space_count("\thello") == 4

    def test_left_space_count_mixed(self):
        """测试混合前导空白"""
        assert StrUtil.left_space_count(" \t hello") == 6  # 1 space + 1 tab(=4) + 1 space

    def test_left_space_count_none(self):
        """测试无前导空白"""
        assert StrUtil.left_space_count("hello") == 0

    def test_left_space_count_empty(self):
        """测试空字符串"""
        assert StrUtil.left_space_count("") == 0

    # ── find_all_indices ────────────────────────────────────────────

    def test_find_all_indices_basic(self):
        """测试查找所有子串位置"""
        assert StrUtil.find_all_indices("abcabc", "b") == [1, 4]

    def test_find_all_indices_no_match(self):
        """测试无匹配"""
        assert StrUtil.find_all_indices("abcabc", "x") == []

    def test_find_all_indices_overlapping(self):
        """测试重叠子串（非重叠查找）"""
        assert StrUtil.find_all_indices("aaa", "aa") == [0]

    def test_find_all_indices_empty_text(self):
        """测试空文本"""
        assert StrUtil.find_all_indices("", "a") == []

    def test_find_all_indices_empty_sub(self):
        """测试空子串"""
        assert StrUtil.find_all_indices("abc", "") == []

    def test_find_all_indices_single(self):
        """测试单次匹配"""
        assert StrUtil.find_all_indices("hello world", "world") == [6]
