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

    # ── 比较与判断 ──────────────────────────────────────────────

    def test_equals_any_match(self):
        assert StrUtil.equals_any("hello", "hi", "hello", "hey") is True

    def test_equals_any_no_match(self):
        assert StrUtil.equals_any("hello", "hi", "hey") is False

    def test_equals_any_none(self):
        assert StrUtil.equals_any(None, "hi", None) is True

    def test_equals_any_ignore_case_match(self):
        assert StrUtil.equals_any_ignore_case("Hello", "hi", "HELLO") is True

    def test_equals_any_ignore_case_no_match(self):
        assert StrUtil.equals_any_ignore_case("Hello", "hi", "hey") is False

    def test_equals_char_at_match(self):
        assert StrUtil.equals_char_at("hello", 0, "h") is True

    def test_equals_char_at_no_match(self):
        assert StrUtil.equals_char_at("hello", 0, "x") is False

    def test_equals_char_at_out_of_range(self):
        assert StrUtil.equals_char_at("hi", 5, "x") is False
        assert StrUtil.equals_char_at(None, 0, "x") is False

    def test_contains_only_true(self):
        assert StrUtil.contains_only("abc", "abcdef") is True

    def test_contains_only_false(self):
        assert StrUtil.contains_only("abc", "ab") is False

    def test_contains_only_empty(self):
        assert StrUtil.contains_only("", "abc") is False

    def test_has_letter_true(self):
        assert StrUtil.has_letter("hello123") is True

    def test_has_letter_false(self):
        assert StrUtil.has_letter("12345") is False

    def test_has_letter_none(self):
        assert StrUtil.has_letter(None) is False

    def test_is_sub_equals_match(self):
        assert StrUtil.is_sub_equals("hello world", "world", 6) is True

    def test_is_sub_equals_no_match(self):
        assert StrUtil.is_sub_equals("hello world", "xyz", 6) is False

    def test_is_sub_equals_ignore_case(self):
        assert StrUtil.is_sub_equals("Hello World", "WORLD", 6, ignore_case=True) is True

    def test_is_surround_true(self):
        assert StrUtil.is_surround("[hello]", "[", "]") is True

    def test_is_surround_false(self):
        assert StrUtil.is_surround("hello", "[", "]") is False

    def test_is_wrap_true(self):
        assert StrUtil.is_wrap("***hello***", "***") is True

    def test_is_wrap_false(self):
        assert StrUtil.is_wrap("*hello*", "***") is False

    def test_is_lower_case_true(self):
        assert StrUtil.is_lower_case("hello") is True

    def test_is_lower_case_false(self):
        assert StrUtil.is_lower_case("Hello") is False

    def test_is_lower_case_no_letter(self):
        assert StrUtil.is_lower_case("123") is False

    def test_is_upper_case_true(self):
        assert StrUtil.is_upper_case("HELLO") is True

    def test_is_upper_case_false(self):
        assert StrUtil.is_upper_case("Hello") is False

    def test_is_all_char_match_true(self):
        assert StrUtil.is_all_char_match("123", str.isdigit) is True

    def test_is_all_char_match_false(self):
        assert StrUtil.is_all_char_match("12a", str.isdigit) is False

    # ── 公共前缀/后缀 & 比较 ────────────────────────────────────

    def test_common_prefix(self):
        assert StrUtil.common_prefix("flower", "flow", "flight") == "fl"

    def test_common_prefix_no_common(self):
        assert StrUtil.common_prefix("abc", "xyz") == ""

    def test_common_suffix(self):
        assert StrUtil.common_suffix("testing", "running", "ing") == "ing"

    def test_common_suffix_no_common(self):
        assert StrUtil.common_suffix("abc", "xyz") == ""

    def test_compare_equal(self):
        assert StrUtil.compare("abc", "abc") == 0

    def test_compare_less(self):
        assert StrUtil.compare("abc", "abd") < 0

    def test_compare_greater(self):
        assert StrUtil.compare("abd", "abc") > 0

    def test_compare_none(self):
        assert StrUtil.compare(None, "abc") < 0
        assert StrUtil.compare(None, "abc", null_is_greater=True) > 0

    def test_compare_ignore_case(self):
        assert StrUtil.compare_ignore_case("ABC", "abc") == 0

    def test_concat(self):
        assert StrUtil.concat("a", None, "b", "c") == "abc"

    # ── 截取与格式化 ────────────────────────────────────────────

    def test_brief(self):
        assert StrUtil.brief("hello world", 8) == "hello..."

    def test_brief_short(self):
        assert StrUtil.brief("hi", 8) == "hi"

    def test_brief_none(self):
        assert StrUtil.brief(None, 8) is None

    def test_max_length(self):
        # 截断时追加 "..."，总长度 = max_length
        assert StrUtil.max_length("hello world", 8) == "hello..."

    def test_max_length_short(self):
        assert StrUtil.max_length("hi", 5) == "hi"

    def test_max_length_exact(self):
        assert StrUtil.max_length("hello", 5) == "hello"

    def test_max_length_very_short(self):
        # max_length <= 3 时直接截断
        assert StrUtil.max_length("hello", 2) == "he"

    def test_fix_length_pad(self):
        assert StrUtil.fix_length("hi", 5) == "hi   "

    def test_fix_length_truncate(self):
        assert StrUtil.fix_length("hello world", 5) == "hello"

    def test_fix_length_none(self):
        assert StrUtil.fix_length(None, 3, "x") == "xxx"

    def test_hide(self):
        assert StrUtil.hide("13812345678", 3, 7) == "138****5678"

    def test_hide_short(self):
        assert StrUtil.hide("hi", 0, 5) == "**"

    def test_move_basic(self):
        assert StrUtil.move("abcde", 1, 3, 2) == "adebc"

    def test_move_none(self):
        assert StrUtil.move(None, 0, 1, 1) is None

    def test_normalize(self):
        assert StrUtil.normalize("  hello   world  ") == "hello world"

    def test_normalize_none(self):
        assert StrUtil.normalize(None) is None

    def test_total_length(self):
        assert StrUtil.total_length("abc", None, "de") == 5

    def test_indexed_format(self):
        assert StrUtil.indexed_format("{0} + {1} = {2}", 1, 2, 3) == "1 + 2 = 3"

    # ── 包裹与填充 ──────────────────────────────────────────────

    def test_wrap(self):
        assert StrUtil.wrap("hello", "***") == "***hello***"

    def test_wrap_different(self):
        assert StrUtil.wrap("hello", "[", "]") == "[hello]"

    def test_wrap_none(self):
        assert StrUtil.wrap(None, "x") is None

    def test_wrap_if_missing_already_wrapped(self):
        assert StrUtil.wrap_if_missing("***hello***", "***") == "***hello***"

    def test_wrap_if_missing_not_wrapped(self):
        assert StrUtil.wrap_if_missing("hello", "***") == "***hello***"

    def test_wrap_all(self):
        assert StrUtil.wrap_all(["a", "b"], "[", "]") == ["[a]", "[b]"]

    def test_wrap_all_none_list(self):
        assert StrUtil.wrap_all(None, "[", "]") is None

    def test_wrap_all_if_missing(self):
        result = StrUtil.wrap_all_if_missing(["[a]", "b"], "[", "]")
        assert result == ["[a]", "[b]"]

    def test_pad_after(self):
        assert StrUtil.pad_after("hi", 5) == "hi   "

    def test_pad_pre(self):
        assert StrUtil.pad_pre("hi", 5) == "   hi"

    def test_repeat_by_length(self):
        assert StrUtil.repeat_by_length("abc", 7) == "abcabca"

    def test_repeat_by_length_none(self):
        assert StrUtil.repeat_by_length(None, 5) is None

    # ── 替换与移除 ──────────────────────────────────────────────

    def test_replace_ignore_case(self):
        assert StrUtil.replace_ignore_case("Hello HELLO", "hello", "hi") == "hi hi"

    def test_replace_last(self):
        # search_str 视为字面量，"." 匹配字面量点号
        assert StrUtil.replace_last("a.b.c", ".", "-") == "a.b-c"

    def test_replace_last_no_match(self):
        assert StrUtil.replace_last("abc", "x", "y") == "abc"

    def test_replace_first_literal(self):
        # search_str 视为字面量，不会被当作正则
        assert StrUtil.replace_first("a.b.c", ".", "-") == "a-b.c"

    def test_replace_first_ignore_case(self):
        assert StrUtil.replace_first("Hello HELLO", "hello", "hi", ignore_case=True) == "hi HELLO"

    def test_replace_last_ignore_case(self):
        assert StrUtil.replace_last("Hello HELLO", "hello", "hi", ignore_case=True) == "Hello hi"

    def test_remove_all_prefix(self):
        assert StrUtil.remove_all_prefix("///path", "/") == "path"

    def test_remove_all_suffix(self):
        assert StrUtil.remove_all_suffix("path///", "/") == "path"

    def test_remove_suf_and_lower_first(self):
        assert StrUtil.remove_suf_and_lower_first("UserNameDTO", "DTO") == "userName"

    # ── 分割与转换 ──────────────────────────────────────────────

    def test_split_trim_v2(self):
        assert StrUtil.split_trim(" a , b , c ") == ["a", "b", "c"]

    def test_split_trim_semicolon(self):
        assert StrUtil.split_trim("a;b ;c", ";") == ["a", "b", "c"]

    def test_strip_all(self):
        assert StrUtil.strip_all(" a ", " b ", None) == ["a", "b", None]

    def test_swap_case(self):
        assert StrUtil.swap_case("Hello World") == "hELLO wORLD"

    def test_swap_case_none(self):
        assert StrUtil.swap_case(None) is None

    def test_to_symbol_case(self):
        assert StrUtil.to_symbol_case("helloWorld", "-") == "hello-world"

    def test_to_symbol_case_underscore(self):
        assert StrUtil.to_symbol_case("helloWorld", "_") == "hello_world"

    def test_trim_to_null_has_value(self):
        assert StrUtil.trim_to_null(" hello ") == "hello"

    def test_trim_to_null_empty(self):
        assert StrUtil.trim_to_null("   ") is None

    def test_trim_to_null_none(self):
        assert StrUtil.trim_to_null(None) is None

    # ── 空值处理 & 杂项 ─────────────────────────────────────────

    def test_empty_if_null_none(self):
        assert StrUtil.empty_if_null(None) == ""

    def test_empty_if_null_value(self):
        assert StrUtil.empty_if_null("hello") == "hello"

    def test_desensitized(self):
        assert StrUtil.desensitized("13812345678", 3, 4) == "138****5678"

    def test_desensitized_short(self):
        assert StrUtil.desensitized("hi", 3, 3) == "**"

    def test_compare_version(self):
        assert StrUtil.compare_version("1.2.3", "1.2.4") < 0
        assert StrUtil.compare_version("1.2.3", "1.2.3") == 0
        assert StrUtil.compare_version("2.0", "1.9.9") > 0

    def test_compare_version_none(self):
        assert StrUtil.compare_version(None, "1.0") < 0
        assert StrUtil.compare_version("1.0", None) > 0

    # ── Unicode / CodePoint ───────────────────────────────────

    def test_sub_by_code_point_ascii(self):
        assert StrUtil.sub_by_code_point("hello", 1, 4) == "ell"

    def test_sub_by_code_point_emoji(self):
        """emoji 安全截取"""
        s = "a😀b😂c"
        assert StrUtil.sub_by_code_point(s, 1, 3) == "😀b"

    def test_sub_by_code_point_none(self):
        assert StrUtil.sub_by_code_point(None, 0, 5) is None

    def test_sub_suf_by_length(self):
        assert StrUtil.sub_suf_by_length("hello", 3) == "llo"

    def test_sub_suf_by_length_longer(self):
        assert StrUtil.sub_suf_by_length("hi", 10) == "hi"

    def test_sub_suf_by_length_none(self):
        assert StrUtil.sub_suf_by_length(None, 3) is None

    def test_sub_with_length(self):
        assert StrUtil.sub_with_length("hello", 1, 3) == "ell"

    def test_sub_with_length_none(self):
        assert StrUtil.sub_with_length(None, 0, 3) is None

    def test_sub_pre_gbk_ascii(self):
        assert StrUtil.sub_pre_gbk("hello", 3) == "hel"

    def test_sub_pre_gbk_chinese(self):
        """中文占 2 字节"""
        result = StrUtil.sub_pre_gbk("你好世界", 6)
        assert len(result.encode("gbk")) <= 6

    def test_sub_pre_gbk_none(self):
        assert StrUtil.sub_pre_gbk(None, 5) is None

    def test_reverse_by_code_point(self):
        assert StrUtil.reverse_by_code_point("abc") == "cba"

    def test_reverse_by_code_point_emoji(self):
        s = "a😀b"
        assert StrUtil.reverse_by_code_point(s) == "b😀a"

    def test_reverse_by_code_point_none(self):
        assert StrUtil.reverse_by_code_point(None) is None

    def test_byte_length_utf8(self):
        assert StrUtil.byte_length("hello") == 5
        assert StrUtil.byte_length("你好") == 6  # 每个中文 3 字节

    def test_byte_length_none(self):
        assert StrUtil.byte_length(None) == 0

    def test_length_normal(self):
        assert StrUtil.length("hello") == 5

    def test_length_none(self):
        assert StrUtil.length(None) == 0

    # ── 分割扩展 ─────────────────────────────────────────────

    def test_split_to_long(self):
        assert StrUtil.split_to_long("1,2,3") == [1, 2, 3]

    def test_split_to_long_with_spaces(self):
        assert StrUtil.split_to_long(" 1 , 2 , 3 ") == [1, 2, 3]

    def test_split_to_long_empty(self):
        assert StrUtil.split_to_long("") == []
        assert StrUtil.split_to_long(None) == []

    def test_split_to_int(self):
        assert StrUtil.split_to_int("10,20,30") == [10, 20, 30]

    def test_split_by_length(self):
        assert StrUtil.split_by_length("abcdef", 2) == ["ab", "cd", "ef"]

    def test_split_by_length_remainder(self):
        assert StrUtil.split_by_length("abcde", 2) == ["ab", "cd", "e"]

    def test_split_by_length_none(self):
        assert StrUtil.split_by_length(None, 3) == []

    def test_split_ignore_case(self):
        result = StrUtil.split_ignore_case("aAbBcC", "b")
        assert result == ["aA", "", "cC"]

    # ── 替换扩展 ─────────────────────────────────────────────

    def test_replace_from(self):
        assert StrUtil.replace_from("aabbcc", 2, "b", "d") == "aadbcc"

    def test_replace_from_none(self):
        assert StrUtil.replace_from(None, 0, "a", "b") is None

    def test_replace_by_func(self):

        result = StrUtil.replace_by_func("hello123world456", r"\d+", lambda m: "[NUM]")
        assert result == "hello[NUM]world[NUM]"

    def test_replace_by_func_none(self):
        assert StrUtil.replace_by_func(None, r"\d+", lambda m: "x") is None

    # ── 大小写转换（null 安全）────────────────────────────────

    def test_to_lower_case(self):
        assert StrUtil.to_lower_case("HELLO") == "hello"
        assert StrUtil.to_lower_case(None) is None

    def test_to_upper_case(self):
        assert StrUtil.to_upper_case("hello") == "HELLO"
        assert StrUtil.to_upper_case(None) is None

    # ── 空值安全查找 ─────────────────────────────────────────

    def test_first_non_null(self):
        assert StrUtil.first_non_null(None, "b", "c") == "b"
        assert StrUtil.first_non_null(None, None) is None

    def test_first_non_empty(self):
        assert StrUtil.first_non_empty("", None, "b") == "b"
        assert StrUtil.first_non_empty("", None) is None

    def test_first_non_blank(self):
        assert StrUtil.first_non_blank("  ", None, "b") == "b"
        assert StrUtil.first_non_blank("  ", "") is None

    # ── 包裹/解包裹 ─────────────────────────────────────────

    def test_unwrap(self):
        assert StrUtil.unwrap("[hello]", "[", "]") == "hello"

    def test_unwrap_no_prefix(self):
        assert StrUtil.unwrap("hello]", "[", "]") == "hello"

    def test_unwrap_no_suffix(self):
        assert StrUtil.unwrap("[hello", "[", "]") == "hello"

    def test_unwrap_none(self):
        assert StrUtil.unwrap(None, "[", "]") is None

    # ── 字符级比较 ──────────────────────────────────────────

    def test_is_char_equals_true(self):
        assert StrUtil.is_char_equals("aaa") is True

    def test_is_char_equals_false(self):
        assert StrUtil.is_char_equals("aab") is False

    def test_is_char_equals_empty(self):
        assert StrUtil.is_char_equals("") is True
        assert StrUtil.is_char_equals(None) is True

    # ── 转换工具 ────────────────────────────────────────────

    def test_to_string(self):
        assert StrUtil.to_string(123) == "123"
        assert StrUtil.to_string(None) == "null"
        assert StrUtil.to_string("abc") == "abc"


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


class TestStrUtilBehaviorFixes:
    """行为修复测试"""

    # ── center 多字符填充 ──────────────────────────────────────

    def test_center_multi_char_pad(self):
        """center 支持多字符 pad_str"""
        # left_pads = 1 -> "y", right_pads = 2 -> "yz"
        assert StrUtil.center("a", 4, "yz") == "yayz"

    def test_center_single_char_pad(self):
        """center 单字符填充仍然正常"""
        assert StrUtil.center("abc", 7, "-") == "--abc--"

    def test_center_size_less_than_str(self):
        """size 小于字符串长度时返回原串"""
        assert StrUtil.center("abcde", 3, "-") == "abcde"

    def test_center_none(self):
        assert StrUtil.center(None, 5, "*") == "*****"

    def test_center_empty_pad(self):
        """pad_str 为空时默认用空格"""
        assert StrUtil.center("a", 4, "") == " a  "

    # ── pad_pre/pad_after 多字符填充 ─────────────────────────

    def test_pad_after_multi_char(self):
        assert StrUtil.pad_after("hi", 7, "xy") == "hixyxyx"

    def test_pad_pre_multi_char(self):
        assert StrUtil.pad_pre("hi", 7, "xy") == "xyxyxhi"

    def test_pad_after_single_char(self):
        assert StrUtil.pad_after("hi", 5, "0") == "hi000"

    def test_pad_pre_single_char(self):
        assert StrUtil.pad_pre("hi", 5, "0") == "000hi"

    def test_pad_after_none(self):
        assert StrUtil.pad_after(None, 3, "x") == "xxx"

    def test_pad_pre_none(self):
        assert StrUtil.pad_pre(None, 3, "x") == "xxx"

    # ── replace_first/replace_last 字面量模式 ────────────────

    def test_replace_first_dot_literal(self):
        """点号应视为字面量，不匹配任意字符"""
        assert StrUtil.replace_first("1.2.3", ".", "-") == "1-2.3"

    def test_replace_last_dot_literal(self):
        assert StrUtil.replace_last("1.2.3", ".", "-") == "1.2-3"

    def test_replace_first_special_chars(self):
        """特殊正则字符应视为字面量"""
        assert StrUtil.replace_first("a+b+c", "+", "-") == "a-b+c"

    def test_replace_last_special_chars(self):
        assert StrUtil.replace_last("a+b+c", "+", "-") == "a+b-c"
