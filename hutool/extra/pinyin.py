"""拼音工具类，基于pypinyin"""


class PinyinUtil:
    """拼音工具类，基于pypinyin"""

    @staticmethod
    def get_pinyin(str_val: str, separator: str = "") -> str:
        """获取拼音

        :param str_val: 中文字符串
        :param separator: 分隔符，默认为空字符串
        :return: 拼音字符串
        """
        from pypinyin import Style, pinyin

        result = pinyin(str_val, style=Style.TONE, errors="ignore")
        return separator.join([item[0] for item in result if item])

    @staticmethod
    def get_pinyin_first_letter(str_val: str) -> str:
        """获取拼音首字母

        :param str_val: 中文字符串
        :return: 拼音首字母字符串
        """
        from pypinyin import Style, lazy_pinyin

        result = lazy_pinyin(str_val, style=Style.FIRST_LETTER, errors="ignore")
        return "".join(result)

    @staticmethod
    def get_full_pinyin(str_val: str, separator: str = " ") -> str:
        """获取全拼

        :param str_val: 中文字符串
        :param separator: 分隔符，默认为空格
        :return: 全拼字符串
        """
        from pypinyin import Style, lazy_pinyin

        result = lazy_pinyin(str_val, style=Style.TONE, errors="ignore")
        return separator.join(result)

    @staticmethod
    def get_pinyin_char(char: str) -> str:
        """获取单个中文字符的拼音

        :param char: 单个中文字符
        :return: 拼音字符串
        """
        from pypinyin import Style, pinyin

        result = pinyin(char, style=Style.TONE, errors="ignore")
        return result[0][0] if result and result[0] else ""

    @staticmethod
    def get_first_letter(str_val: str) -> str:
        """获取拼音首字母（get_pinyin_first_letter的别名）

        :param str_val: 中文字符串
        :return: 首字母字符串
        """
        return PinyinUtil.get_pinyin_first_letter(str_val)

    @staticmethod
    def is_chinese(char: str) -> bool:
        """判断单个字符是否为中文字符

        :param char: 单个字符
        :return: 是否为中文
        """
        if len(char) != 1:
            return False
        return "一" <= char <= "鿿"

    @staticmethod
    def get_pinyin_with_tone(str_val: str, separator: str = "") -> str:
        """获取带声调的拼音

        :param str_val: 中文字符串
        :param separator: 分隔符
        :return: 带声调拼音字符串
        """
        from pypinyin import Style, pinyin

        result = pinyin(str_val, style=Style.TONE3, errors="ignore")
        return separator.join([item[0] for item in result if item])
