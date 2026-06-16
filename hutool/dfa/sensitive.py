"""敏感词过滤工具，基于DFA（确定性有限自动机）算法"""

from typing import List


class SensitiveUtil:
    """敏感词过滤工具，基于DFA（确定性有限自动机）算法"""

    _root: dict = {}
    _initialized: bool = False
    _char_filter = None  # type: Optional[Callable[[str], str]]

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
        if cls._char_filter is not None:
            text = cls._char_filter(text)
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
        if cls._char_filter is not None:
            text = cls._char_filter(text)
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
        if cls._char_filter is not None:
            text = cls._char_filter(text)
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
        if cls._char_filter is not None:
            filtered = cls._char_filter(text)
        else:
            filtered = text
        chars = list(filtered)
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

    # ------------------------------------------------------------------ #
    #  扩展方法
    # ------------------------------------------------------------------ #

    @classmethod
    def is_inited(cls) -> bool:
        """是否已初始化敏感词库

        :return: 是否已初始化
        """
        return cls._initialized

    @classmethod
    def set_char_filter(cls, func):
        # type: (Callable[[str], str]) -> None
        """设置字符过滤器（在匹配前预处理文本）

        :param func: 过滤函数，接收str返回str
        """
        cls._char_filter = func

    @classmethod
    def contains_sensitive(cls, obj):
        # type: (Any) -> bool
        """检查对象中是否包含敏感词（支持str/list/dict）

        :param obj: 待检查对象
        :return: 是否包含敏感词
        """
        if isinstance(obj, str):
            return cls.contains(obj)
        elif isinstance(obj, list):
            for item in obj:
                if cls.contains_sensitive(item):
                    return True
            return False
        elif isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(key, str) and cls.contains(key):
                    return True
                if cls.contains_sensitive(value):
                    return True
            return False
        return False

    @classmethod
    def get_found_first_sensitive(cls, text: str) -> dict:
        """获取第一个敏感词及其位置

        :param text: 待检测文本
        :return: 包含word, start, end的字典，未找到返回空字典
        """
        if not cls._initialized:
            return {}
        if cls._char_filter is not None:
            text = cls._char_filter(text)
        for i in range(len(text)):
            node = cls._root
            j = i
            while j < len(text) and text[j] in node:
                node = node[text[j]]
                if node.get("__end__"):
                    return {"word": text[i : j + 1], "start": i, "end": j + 1}
                j += 1
        return {}

    @classmethod
    def get_found_all_sensitive(cls, text: str) -> list:
        """获取所有敏感词及其位置

        :param text: 待检测文本
        :return: 列表，每个元素包含word, start, end的字典
        """
        if not cls._initialized:
            return []
        if cls._char_filter is not None:
            text = cls._char_filter(text)
        result = []
        for i in range(len(text)):
            node = cls._root
            j = i
            while j < len(text) and text[j] in node:
                node = node[text[j]]
                if node.get("__end__"):
                    result.append({"word": text[i : j + 1], "start": i, "end": j + 1})
                j += 1
        return result

    @classmethod
    def init_from_delimited(cls, text: str, delimiter: str = ",") -> None:
        """从分隔符字符串初始化敏感词库

        :param text: 敏感词文本
        :param delimiter: 分隔符
        """
        words = [w.strip() for w in text.split(delimiter) if w.strip()]
        cls.init(words)
