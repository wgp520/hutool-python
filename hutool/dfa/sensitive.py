"""敏感词过滤工具，基于DFA（确定性有限自动机）算法"""

from typing import List


class SensitiveUtil:
    """敏感词过滤工具，基于DFA（确定性有限自动机）算法"""

    _root: dict = {}
    _initialized: bool = False

    @classmethod
    def init(cls, words: List[str]) -> None:
        """初始化敏感词库

        :param words: 敏感词列表
        """
        cls._root = {}
        for word in words:
            node = cls._root
            for char in word:
                if char not in node:
                    node[char] = {}
                node = node[char]
            # 标记词结束
            node["__end__"] = True
        cls._initialized = True

    @classmethod
    def contains(cls, text: str) -> bool:
        """是否包含敏感词

        :param text: 待检测文本
        :return: 是否包含敏感词
        """
        if not cls._initialized:
            return False
        for i in range(len(text)):
            node = cls._root
            j = i
            while j < len(text) and text[j] in node:
                node = node[text[j]]
                if node.get("__end__"):
                    return True
                j += 1
        return False

    @classmethod
    def find_first(cls, text: str) -> str:
        """查找第一个敏感词

        :param text: 待检测文本
        :return: 第一个匹配的敏感词，未找到返回空字符串
        """
        if not cls._initialized:
            return ""
        for i in range(len(text)):
            node = cls._root
            j = i
            while j < len(text) and text[j] in node:
                node = node[text[j]]
                if node.get("__end__"):
                    return text[i : j + 1]
                j += 1
        return ""

    @classmethod
    def find_all(cls, text: str) -> List[str]:
        """查找所有敏感词

        :param text: 待检测文本
        :return: 所有匹配的敏感词列表
        """
        if not cls._initialized:
            return []
        result: List[str] = []
        for i in range(len(text)):
            node = cls._root
            j = i
            while j < len(text) and text[j] in node:
                node = node[text[j]]
                if node.get("__end__"):
                    result.append(text[i : j + 1])
                j += 1
        return result

    @classmethod
    def replace(cls, text: str, replace_char: str = "*") -> str:
        """替换敏感词

        :param text: 待处理文本
        :param replace_char: 替换字符，默认为 '*'
        :return: 替换后的文本
        """
        if not cls._initialized:
            return text
        chars = list(text)
        i = 0
        while i < len(chars):
            node = cls._root
            j = i
            match_end = -1
            while j < len(chars) and chars[j] in node:
                node = node[chars[j]]
                if node.get("__end__"):
                    match_end = j
                j += 1
            if match_end >= 0:
                for k in range(i, match_end + 1):
                    chars[k] = replace_char
                i = match_end + 1
            else:
                i += 1
        return "".join(chars)
