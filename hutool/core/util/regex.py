"""正则表达式工具类，对应 Java cn.hutool.core.util.ReUtil"""

import re
from typing import Callable, Dict, List, Optional


class ReUtil:
    """正则表达式工具类，对应 Java cn.hutool.core.util.ReUtil

    提供常用的正则匹配、提取、替换、分割等静态方法。
    """

    @staticmethod
    def is_match(pattern: str, content: str) -> bool:
        """给定内容是否匹配正则（全匹配）

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :return: 是否全匹配
        """
        return re.fullmatch(pattern, content) is not None

    @staticmethod
    def contains(pattern: str, content: str) -> bool:
        """给定内容是否包含正则匹配

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :return: 是否包含匹配
        """
        return re.search(pattern, content) is not None

    @staticmethod
    def get(pattern: str, content: str, group_index: int = 0) -> Optional[str]:
        """获得匹配的字符串，group_index=0 返回整个匹配

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :param group_index: 匹配组索引，0表示整个匹配
        :return: 匹配的字符串，无匹配返回 None
        """
        match = re.search(pattern, content)
        if match is None:
            return None
        try:
            return match.group(group_index)
        except IndexError:
            return None

    @staticmethod
    def get_all(pattern: str, content: str, group_index: int = 0) -> List[str]:
        """获得所有匹配的字符串列表

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :param group_index: 匹配组索引，0表示整个匹配
        :return: 所有匹配的字符串列表
        """
        results: List[str] = []
        for match in re.finditer(pattern, content):
            try:
                results.append(match.group(group_index))
            except IndexError:
                pass
        return results

    @staticmethod
    def get_all_groups(pattern: str, content: str) -> List[List[str]]:
        """获得所有匹配，每个匹配返回所有分组

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :return: 二维列表，外层为每个匹配，内层为该匹配的所有捕获组（group(1) 至 group(N)）
        """
        results: List[List[str]] = []
        for match in re.finditer(pattern, content):
            results.append(list(match.groups(default="")))
        return results

    @staticmethod
    def match_all(pattern: str, content: str) -> List[str]:
        """获得匹配的全部内容（等价于 get_all group_index=0）

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :return: 所有完整匹配的字符串列表
        """
        return ReUtil.get_all(pattern, content, group_index=0)

    @staticmethod
    def replace_all(content: str, pattern: str, replacement: str) -> str:
        """替换所有匹配

        :param content: 被替换的内容
        :param pattern: 正则表达式
        :param replacement: 替换字符串，可使用 \\1 \\2 等反向引用
        :return: 替换后的字符串
        """
        return re.sub(pattern, replacement, content)

    @staticmethod
    def replace_first(content: str, pattern: str, replacement: str) -> str:
        """替换第一个匹配

        :param content: 被替换的内容
        :param pattern: 正则表达式
        :param replacement: 替换字符串，可使用 \\1 \\2 等反向引用
        :return: 替换后的字符串
        """
        return re.sub(pattern, replacement, content, count=1)

    @staticmethod
    def extract(pattern: str, content: str, template: str) -> Optional[str]:
        """提取匹配内容并按模板重组

        例如::

            extract(r"(\\d+)-(\\d+)", "123-456", "$2-$1")  -> "456-123"
            extract(r"(\\w+)@(\\w+)", "user@host", "$1")    -> "user"

        :param pattern: 正则表达式，应包含分组
        :param content: 被匹配的内容
        :param template: 模板字符串，使用 $1 $2 等引用分组
        :return: 按模板重组后的字符串，无匹配返回 None
        """
        match = re.search(pattern, content)
        if match is None:
            return None
        return ReUtil._apply_template(match, template)

    @staticmethod
    def extract_multi(pattern: str, content: str, template: str) -> List[str]:
        """提取所有匹配内容并按模板重组

        :param pattern: 正则表达式，应包含分组
        :param content: 被匹配的内容
        :param template: 模板字符串，使用 $1 $2 等引用分组
        :return: 所有按模板重组后的字符串列表
        """
        results: List[str] = []
        for match in re.finditer(pattern, content):
            results.append(ReUtil._apply_template(match, template))
        return results

    @staticmethod
    def count(pattern: str, content: str) -> int:
        """统计匹配次数

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :return: 匹配次数
        """
        return len(re.findall(pattern, content))

    @staticmethod
    def split(content: str, pattern: str) -> List[str]:
        """按正则分割字符串

        :param content: 被分割的字符串
        :param pattern: 分隔符正则表达式
        :return: 分割后的字符串列表
        """
        return re.split(pattern, content)

    @staticmethod
    def del_all(pattern: str, content: str) -> str:
        """删除所有匹配内容

        :param pattern: 正则表达式
        :param content: 被处理的字符串
        :return: 删除匹配内容后的字符串
        """
        return re.sub(pattern, "", content)

    @staticmethod
    def escape(characters: str) -> str:
        """转义正则特殊字符

        :param characters: 需要转义的字符串
        :return: 转义后的字符串
        """
        return re.escape(characters)

    @staticmethod
    def get_group0(pattern: str, content: str) -> Optional[str]:
        """获取第一个匹配的第 0 组（整个匹配）

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :return: 整个匹配的字符串，无匹配返回 None
        """
        return ReUtil.get(pattern, content, group_index=0)

    @staticmethod
    def get_group1(pattern: str, content: str) -> Optional[str]:
        """获取第一个匹配的第 1 组

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :return: 第 1 组匹配的字符串，无匹配返回 None
        """
        return ReUtil.get(pattern, content, group_index=1)

    # ------------------------------------------------------------------
    # 内部辅助方法
    # ------------------------------------------------------------------

    @staticmethod
    def _apply_template(match: re.Match, template: str) -> str:
        """将匹配对象按模板重组

        模板中 $n（n 为数字）会被替换为对应的捕获组内容。
        $$ 会被替换为字面量 $。

        :param match: 正则匹配对象
        :param template: 模板字符串
        :return: 重组后的字符串
        """

        def _replace_ref(m: re.Match) -> str:
            token = m.group(0)
            if token == "$$":
                return "$"
            # $0, $1, $2, ...
            idx = int(token[1:])
            try:
                return match.group(idx) if match.group(idx) is not None else ""
            except IndexError:
                return ""

        return re.sub(r"\$\$|\$\d+", _replace_ref, template)

    @staticmethod
    def find_all(pattern: str, content: str, group_index: int = 0) -> List[str]:
        """查找所有匹配（与 get_all 相同）。

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :param group_index: 匹配组索引
        :return: 所有匹配的字符串列表
        """
        return ReUtil.get_all(pattern, content, group_index)

    @staticmethod
    def find_all_group0(pattern: str, content: str) -> List[str]:
        """查找所有 group(0) 匹配。

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :return: 所有完整匹配的列表
        """
        return ReUtil.get_all(pattern, content, group_index=0)

    @staticmethod
    def find_all_group1(pattern: str, content: str) -> List[str]:
        """查找所有 group(1) 匹配。

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :return: 所有 group(1) 匹配的列表
        """
        return ReUtil.get_all(pattern, content, group_index=1)

    @staticmethod
    def find_first_number(content: str) -> Optional[str]:
        """查找第一个数字。

        :param content: 被匹配的内容
        :return: 第一个数字字符串，无匹配返回 None
        """
        return ReUtil.get(r"\d+", content)

    @staticmethod
    def index_of(pattern: str, content: str) -> int:
        """第一个匹配的起始位置。

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :return: 起始位置，无匹配返回 -1
        """
        match = re.search(pattern, content)
        return match.start() if match else -1

    @staticmethod
    def last_index_of(pattern: str, content: str) -> int:
        """最后一个匹配的起始位置。

        :param pattern: 正则表达式
        :param content: 被匹配的内容
        :return: 最后匹配的起始位置，无匹配返回 -1
        """
        matches = list(re.finditer(pattern, content))
        return matches[-1].start() if matches else -1

    @staticmethod
    def del_first(pattern: str, content: str) -> str:
        """删除第一个匹配。

        :param pattern: 正则表达式
        :param content: 被处理的字符串
        :return: 删除第一个匹配后的字符串
        """
        return re.sub(pattern, "", content, count=1)

    @staticmethod
    def del_last(pattern: str, content: str) -> str:
        """删除最后一个匹配。

        :param pattern: 正则表达式
        :param content: 被处理的字符串
        :return: 删除最后一个匹配后的字符串
        """
        matches = list(re.finditer(pattern, content))
        if not matches:
            return content
        last = matches[-1]
        return content[: last.start()] + content[last.end() :]

    @staticmethod
    def del_pre(pattern: str, content: str) -> Optional[str]:
        """删除匹配及其之前的内容。

        :param pattern: 正则表达式
        :param content: 被处理的字符串
        :return: 删除匹配前内容后的字符串，无匹配返回 None
        """
        match = re.search(pattern, content)
        if match is None:
            return None
        return content[match.end() :]

    @staticmethod
    def extract_multi_and_del_pre(pattern: str, content: str, group_index: int = 0) -> List[str]:
        """提取所有匹配并删除匹配前的内容（原地消费）。

        依次匹配，每次匹配后从内容中删除该匹配及其之前的部分，
        返回所有匹配结果。

        :param pattern: 正则表达式
        :param content: 被处理的字符串
        :param group_index: 匹配组索引
        :return: 所有匹配的列表
        """
        results: List[str] = []
        remaining = content
        while remaining:
            match = re.search(pattern, remaining)
            if match is None:
                break
            try:
                results.append(match.group(group_index))
            except IndexError:
                pass
            remaining = remaining[match.end() :]
        return results

    @staticmethod
    def get_all_group_names(pattern: str) -> Dict[str, int]:
        """获取正则表达式中所有命名捕获组。

        :param pattern: 正则表达式
        :return: 命名组名到组索引的映射字典
        """
        compiled = re.compile(pattern)
        return compiled.groupindex

    @staticmethod
    def replace_by_func(content: str, pattern: str, func: Callable[[re.Match], str]) -> str:
        """正则替换，使用回调函数处理每个匹配。

        :param content: 被替换的内容
        :param pattern: 正则表达式
        :param func: 回调函数，接受 re.Match 对象，返回替换字符串
        :return: 替换后的字符串
        """
        return re.sub(pattern, func, content)

    @staticmethod
    def find_first_pattern(content: str, patterns: List[str]) -> Optional[str]:
        """按优先级（列表顺序）查找第一个匹配的正则模式。

        :param content: 待检查的字符串
        :param patterns: 正则表达式列表
        :return: 第一个匹配的模式字符串，无匹配返回 ``None``
        """
        if not content:
            return None
        for pattern in patterns:
            if re.search(pattern, content):
                return pattern
        return None

    @staticmethod
    def find_all_patterns(content: str, patterns: List[str]) -> List[str]:
        """查找所有匹配的正则模式。

        :param content: 待检查的字符串
        :param patterns: 正则表达式列表
        :return: 所有匹配的模式列表
        """
        if not content:
            return []
        return [p for p in patterns if re.search(p, content)]
