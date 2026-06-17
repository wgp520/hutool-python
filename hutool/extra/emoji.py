"""Emoji工具类"""

import re

# 匹配emoji的正则表达式
_EMOJI_PATTERN = re.compile(
    "["
    "\U0001f600-\U0001f64f"  # 表情符号
    "\U0001f300-\U0001f5ff"  # 符号和象形文字
    "\U0001f680-\U0001f6ff"  # 交通和地图符号
    "\U0001f1e0-\U0001f1ff"  # 旗帜
    "\U00002702-\U000027b0"  # 杂项符号
    "\U000024c2-\U0001f251"  # 封闭字符
    "\U0001f926-\U0001f937"  # 补充表情
    "\U00010000-\U0010ffff"  # 补充平面
    "♀-♂"  # 性别符号
    "☀-⭕"  # 杂项符号
    "‍"  # 零宽连接符
    "⏏"
    "⏩-⏳"
    "⏸-⏺"
    "️"  # 变体选择符
    "⤴-⤵"
    "▪-◾"
    "⬅-⬇"
    "⬛-⬜"
    "⭐"
    "〰"
    "〽"
    "㊗"
    "㊙"
    "]+",
    flags=re.UNICODE,
)


class EmojiUtil:
    """Emoji工具类"""

    @staticmethod
    def contains_emoji(str_val: str) -> bool:
        """判断是否包含emoji

        :param str_val: 待检测字符串
        :return: 是否包含emoji
        """
        return bool(_EMOJI_PATTERN.search(str_val))

    @staticmethod
    def emoji_to_unicode(emoji_str: str) -> str:
        """将emoji转换为Unicode编码

        :param emoji_str: 包含emoji的字符串
        :return: Unicode编码字符串（格式：\\U0001F600）
        """
        result = []
        for char in emoji_str:
            code_point = ord(char)
            if code_point > 0xFFFF:
                result.append(f"\\U{code_point:08X}")
            elif code_point > 0xFF:
                result.append(f"\\u{code_point:04X}")
            else:
                result.append(char)
        return "".join(result)

    @staticmethod
    def unicode_to_emoji(unicode_str: str) -> str:
        """将Unicode编码转换为emoji

        :param unicode_str: Unicode编码字符串（格式：\\U0001F600 或 \\u2764）
        :return: 包含emoji的字符串
        """

        def _replace(match: re.Match) -> str:
            code_point = int(match.group(1), 16)
            return chr(code_point)

        # 匹配 \\U 开头的8位和 \\u 开头的4位十六进制
        result = re.sub(r"\\[Uu]([0-9a-fA-F]{4,8})", _replace, unicode_str)
        return result

    @staticmethod
    def remove_emojis(str_val: str) -> str:
        """移除字符串中的所有emoji

        :param str_val: 待处理字符串
        :return: 移除emoji后的字符串
        """
        return _EMOJI_PATTERN.sub("", str_val)

    @staticmethod
    def is_emoji(char: str) -> bool:
        """判断单个字符是否为emoji

        :param char: 单个字符
        :return: 是否为emoji
        """
        return bool(_EMOJI_PATTERN.fullmatch(char))

    @staticmethod
    def extract_emojis(str_val: str) -> list:
        """提取字符串中的所有emoji

        :param str_val: 输入字符串
        :return: emoji列表
        """
        return _EMOJI_PATTERN.findall(str_val)

    @staticmethod
    def to_alias(emoji: str) -> str:
        """将emoji转换为别名格式

        :param emoji: emoji字符串
        :return: 别名字符串（如 :smile:）
        """
        try:
            import emoji as emoji_lib

            return emoji_lib.demojize(emoji, language="en")
        except ImportError:
            # 回退方案：返回Unicode编码的别名格式
            code_points = []
            for char in emoji:
                code_points.append(f"U+{ord(char):04X}")
            return ":" + "_".join(code_points) + ":"

    @staticmethod
    def to_html(emoji: str) -> str:
        """将emoji转换为HTML实体

        :param emoji: emoji字符串
        :return: HTML实体字符串
        """
        result = []
        for char in emoji:
            code_point = ord(char)
            result.append(f"&#x{code_point:X};")
        return "".join(result)

    @staticmethod
    def remove_all_emojis(text: str) -> str:
        """移除所有 emoji（与 remove_emojis 相同）。

        :param text: 输入字符串
        :return: 移除 emoji 后的字符串
        """
        return EmojiUtil.remove_emojis(text)

    @staticmethod
    def to_html_hex(emoji_char: str) -> str:
        """将 emoji 转为 HTML 十六进制实体（如 &#x1F600;）。

        :param emoji_char: emoji 字符
        :return: HTML 十六进制实体字符串
        """
        result = []
        for char in emoji_char:
            code_point = ord(char)
            result.append(f"&#x{code_point:X};")
        return "".join(result)

    @staticmethod
    def to_unicode(emoji_char: str) -> str:
        """将 emoji 转为 Unicode 表示（如 U+1F600）。

        :param emoji_char: emoji 字符
        :return: Unicode 表示字符串
        """
        result = []
        for char in emoji_char:
            code_point = ord(char)
            result.append(f"U+{code_point:04X}")
        return "".join(result)
