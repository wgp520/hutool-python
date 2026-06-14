from typing import List, Optional


class StrBuilder:
    """字符串构建器，类似Java StringBuilder

    提供高效的字符串拼接操作，内部使用列表缓存各段字符串，
    最终在 to_string 时一次性拼接，避免频繁字符串拼接带来的性能问题。
    """

    def __init__(self, capacity: int = 16):
        """初始化字符串构建器

        :param capacity: 初始容量（提示性，不强制约束）
        """
        self._parts: List[str] = []
        self._length: int = 0

    def _to_str(self) -> str:
        """内部方法：将当前所有片段拼接为完整字符串"""
        return "".join(self._parts)

    def append(self, *args: object) -> "StrBuilder":
        """追加内容

        支持追加任意类型，会自动调用 str() 转换。
        可一次追加多个对象，也可追加列表/元组（展开其元素）。

        :param args: 要追加的一个或多个对象
        :return: self，支持链式调用
        """
        for arg in args:
            if isinstance(arg, (list, tuple)):
                for item in arg:
                    s = str(item)
                    self._parts.append(s)
                    self._length += len(s)
            else:
                s = str(arg)
                self._parts.append(s)
                self._length += len(s)
        return self

    def insert(self, index: int, obj: object) -> "StrBuilder":
        """在指定位置插入内容

        :param index: 插入位置索引
        :param obj: 要插入的对象，会被转换为字符串
        :return: self，支持链式调用
        :raises IndexError: 索引越界
        """
        current = self._to_str()
        if index < 0 or index > len(current):
            raise IndexError(f"索引越界: {index}, 当前长度: {len(current)}")
        s = str(obj)
        self._parts = [current[:index], s, current[index:]]
        self._length += len(s)
        return self

    def delete(self, start: int, end: int) -> "StrBuilder":
        """删除指定范围的内容 [start, end)

        :param start: 起始索引（包含）
        :param end: 结束索引（不包含）
        :return: self，支持链式调用
        :raises IndexError: 索引越界
        """
        current = self._to_str()
        if start < 0 or start > len(current):
            raise IndexError(f"起始索引越界: {start}")
        if end < 0 or end > len(current):
            raise IndexError(f"结束索引越界: {end}")
        if start > end:
            raise ValueError(f"起始索引 {start} 大于结束索引 {end}")
        deleted = current[start:end]
        self._parts = [current[:start], current[end:]]
        self._length -= len(deleted)
        return self

    def replace(self, start: int, end: int, string: str) -> "StrBuilder":
        """替换指定范围的内容 [start, end)

        :param start: 起始索引（包含）
        :param end: 结束索引（不包含）
        :param string: 替换内容
        :return: self，支持链式调用
        :raises IndexError: 索引越界
        """
        current = self._to_str()
        if start < 0 or start > len(current):
            raise IndexError(f"起始索引越界: {start}")
        if end < 0 or end > len(current):
            raise IndexError(f"结束索引越界: {end}")
        if start > end:
            raise ValueError(f"起始索引 {start} 大于结束索引 {end}")
        removed_len = end - start
        self._parts = [current[:start], string, current[end:]]
        self._length = self._length - removed_len + len(string)
        return self

    def reverse(self) -> "StrBuilder":
        """反转字符串内容

        :return: self，支持链式调用
        """
        current = self._to_str()
        self._parts = [current[::-1]]
        return self

    def to_string(self) -> str:
        """转为字符串

        :return: 当前构建器中的完整字符串
        """
        return self._to_str()

    def length(self) -> int:
        """获取当前字符串长度

        :return: 字符串长度
        """
        return self._length

    def is_empty(self) -> bool:
        """判断构建器是否为空

        :return: 为空返回 True，否则返回 False
        """
        return self._length == 0

    def char_at(self, index: int) -> str:
        """获取指定位置的字符

        :param index: 字符索引
        :return: 指定位置的字符
        :raises IndexError: 索引越界
        """
        if index < 0 or index >= self._length:
            raise IndexError(f"索引越界: {index}, 当前长度: {self._length}")
        current = self._to_str()
        return current[index]

    def index_of(self, string: str, start: int = 0) -> int:
        """查找子串首次出现的位置

        :param string: 要查找的子串
        :param start: 起始搜索位置，默认为0
        :return: 子串首次出现的索引，未找到返回 -1
        """
        current = self._to_str()
        return current.find(string, start)

    def last_index_of(self, string: str) -> int:
        """从后查找子串最后一次出现的位置

        :param string: 要查找的子串
        :return: 子串最后一次出现的索引，未找到返回 -1
        """
        current = self._to_str()
        return current.rfind(string)

    def substring(self, start: int, end: Optional[int] = None) -> str:
        """获取子串

        :param start: 起始索引（包含）
        :param end: 结束索引（不包含），默认到末尾
        :return: 截取的子串
        """
        current = self._to_str()
        if end is None:
            return current[start:]
        return current[start:end]

    def starts_with(self, prefix: str) -> bool:
        """判断是否以指定字符串开头

        :param prefix: 前缀字符串
        :return: 是返回 True，否则返回 False
        """
        return self._to_str().startswith(prefix)

    def ends_with(self, suffix: str) -> bool:
        """判断是否以指定字符串结尾

        :param suffix: 后缀字符串
        :return: 是返回 True，否则返回 False
        """
        return self._to_str().endswith(suffix)

    def contains(self, string: str) -> bool:
        """判断是否包含指定字符串

        :param string: 要查找的子串
        :return: 包含返回 True，否则返回 False
        """
        return string in self._to_str()

    def trim(self) -> "StrBuilder":
        """去除首尾空白字符

        :return: self，支持链式调用
        """
        current = self._to_str().strip()
        self._parts = [current]
        self._length = len(current)
        return self

    def clear(self) -> "StrBuilder":
        """清空构建器

        :return: self，支持链式调用
        """
        self._parts.clear()
        self._length = 0
        return self

    def __str__(self) -> str:
        return self._to_str()

    def __len__(self) -> int:
        return self._length

    def __repr__(self) -> str:
        return f"StrBuilder({self._to_str()!r})"
