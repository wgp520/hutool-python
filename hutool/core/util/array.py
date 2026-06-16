"""数组工具类，对应 Java cn.hutool.core.util.ArrayUtil"""

from typing import Any, Callable


class ArrayUtil:
    """数组工具类，对应 Java cn.hutool.core.util.ArrayUtil"""

    # ==================== 判断 ====================

    @staticmethod
    def is_empty(array) -> bool:
        """数组是否为空，None也视为空

        :param array: 待检查的数组或列表
        :return: 如果 array 为 None 或长度为 0 则返回 True
        """
        if array is None:
            return True
        try:
            return len(array) == 0
        except TypeError:
            # 不可迭代对象视为空
            return True

    @staticmethod
    def is_not_empty(array) -> bool:
        """数组是否为非空

        :param array: 待检查的数组或列表
        :return: 如果 array 非 None 且长度大于 0 则返回 True
        """
        return not ArrayUtil.is_empty(array)

    @staticmethod
    def has_null(*args) -> bool:
        """是否有null元素

        :param args: 任意数量的参数
        :return: 如果存在任意一个参数为 None 则返回 True
        """
        for arg in args:
            if arg is None:
                return True
        return False

    @staticmethod
    def is_all_null(*args) -> bool:
        """是否全部为null

        :param args: 任意数量的参数
        :return: 如果所有参数均为 None 则返回 True
        """
        for arg in args:
            if arg is not None:
                return False
        return True

    @staticmethod
    def first_non_null(*args):
        """返回第一个非null值

        :param args: 任意数量的参数
        :return: 第一个不为 None 的值，全部为 None 则返回 None
        """
        for arg in args:
            if arg is not None:
                return arg
        return None

    # ==================== 操作 ====================

    @staticmethod
    def append(array: list, *new_elements) -> list:
        """追加元素，返回新数组

        :param array: 原始列表
        :param new_elements: 要追加的元素
        :return: 追加后的新列表
        """
        if array is None:
            return list(new_elements)
        result = list(array)
        result.extend(new_elements)
        return result

    @staticmethod
    def insert(array: list, index: int, *new_elements) -> list:
        """在指定位置插入元素

        :param array: 原始列表
        :param index: 插入位置索引，支持负索引
        :param new_elements: 要插入的元素
        :return: 插入后的新列表
        :raises IndexError: 索引越界时抛出
        """
        if array is None:
            if index != 0:
                raise IndexError(f"索引 {index} 越界，数组为 None")
            return list(new_elements)
        result = list(array)
        # 处理负索引
        actual_index = index
        if actual_index < 0:
            actual_index = len(result) + actual_index
        if actual_index < 0 or actual_index > len(result):
            raise IndexError(f"索引 {index} 越界，数组长度为 {len(array)}")
        for i, elem in enumerate(new_elements):
            result.insert(actual_index + i, elem)
        return result

    @staticmethod
    def remove(array: list, index: int) -> list:
        """移除指定位置元素

        :param array: 原始列表
        :param index: 要移除的位置索引，支持负索引
        :return: 移除后的新列表
        :raises IndexError: 索引越界时抛出
        """
        if array is None:
            raise IndexError("数组为 None，无法移除元素")
        if index < 0 or index >= len(array):
            raise IndexError(f"索引 {index} 越界，数组长度为 {len(array)}")
        result = list(array)
        result.pop(index)
        return result

    @staticmethod
    def remove_ele(array: list, element) -> list:
        """移除指定元素（第一个匹配）

        :param array: 原始列表
        :param element: 要移除的元素
        :return: 移除后的新列表，如果元素不存在则返回原列表的副本
        """
        if array is None:
            return []
        result = list(array)
        try:
            result.remove(element)
        except ValueError:
            pass
        return result

    # ==================== 查找 ====================

    @staticmethod
    def index_of(array, value) -> int:
        """查找元素位置，不存在返回-1

        :param array: 要搜索的列表或可迭代对象
        :param value: 要查找的值
        :return: 元素首次出现的索引，不存在返回 -1
        """
        if array is None:
            return -1
        try:
            for i, item in enumerate(array):
                if item == value:
                    return i
        except TypeError:
            return -1
        return -1

    @staticmethod
    def last_index_of(array, value) -> int:
        """从后向前查找

        :param array: 要搜索的列表或可迭代对象
        :param value: 要查找的值
        :return: 元素最后出现的索引，不存在返回 -1
        """
        if array is None:
            return -1
        result = -1
        try:
            for i, item in enumerate(array):
                if item == value:
                    result = i
        except TypeError:
            return -1
        return result

    @staticmethod
    def contains(array, value) -> bool:
        """是否包含指定元素

        :param array: 要搜索的列表或可迭代对象
        :param value: 要查找的值
        :return: 如果包含该元素则返回 True
        """
        return ArrayUtil.index_of(array, value) >= 0

    @staticmethod
    def contains_any(array, *values) -> bool:
        """是否包含任意一个

        :param array: 要搜索的列表或可迭代对象
        :param values: 要查找的值（可多个）
        :return: 如果包含任意一个值则返回 True
        """
        if array is None:
            return False
        for v in values:
            if ArrayUtil.contains(array, v):
                return True
        return False

    @staticmethod
    def contains_all(array, *values) -> bool:
        """是否包含全部

        :param array: 要搜索的列表或可迭代对象
        :param values: 要查找的值（可多个）
        :return: 如果包含全部值则返回 True
        """
        if array is None:
            return len(values) == 0
        for v in values:
            if not ArrayUtil.contains(array, v):
                return False
        return True

    # ==================== 子数组 ====================

    @staticmethod
    def sub(array: list, start: int, end: int) -> list:
        """获取子数组，支持负索引

        :param array: 原始列表
        :param start: 起始索引（包含），支持负索引
        :param end: 结束索引（不包含），支持负索引
        :return: 子列表
        :raises IndexError: 索引越界时抛出
        """
        if array is None:
            raise IndexError("数组为 None，无法获取子数组")
        length = len(array)
        # 处理负索引
        actual_start = start if start >= 0 else max(length + start, 0)
        actual_end = end if end >= 0 else max(length + end, 0)
        # 边界修正
        actual_start = min(actual_start, length)
        actual_end = min(actual_end, length)
        if actual_start > actual_end:
            raise IndexError(f"起始索引 {start} 大于结束索引 {end}")
        return list(array[actual_start:actual_end])

    # ==================== 转换 ====================

    @staticmethod
    def join(array, conjunction: str) -> str:
        """数组转字符串，用连接符连接

        :param array: 要连接的列表或可迭代对象
        :param conjunction: 连接符
        :return: 连接后的字符串，空数组返回空字符串
        """
        if array is None:
            return ""
        return conjunction.join(str(item) for item in array)

    @staticmethod
    def zip_list(keys: list, values: list) -> dict:
        """两个列表合并为字典

        :param keys: 键列表
        :param values: 值列表
        :return: 合并后的字典，长度以较短的列表为准
        """
        if keys is None or values is None:
            return {}
        return dict(zip(keys, values))

    @staticmethod
    def to_list(iterable) -> list:
        """转为列表

        :param iterable: 可迭代对象
        :return: 转换后的列表，None 返回空列表
        """
        if iterable is None:
            return []
        if isinstance(iterable, list):
            return list(iterable)
        try:
            return list(iterable)
        except TypeError:
            return [iterable]

    @staticmethod
    def reverse(array: list) -> list:
        """反转数组，返回新数组

        :param array: 原始列表
        :return: 反转后的新列表
        """
        if array is None:
            return []
        return list(reversed(array))

    # ==================== 工具 ====================

    @staticmethod
    def shuffle(array: list) -> list:
        """随机打乱，返回新数组

        :param array: 原始列表
        :return: 随机打乱后的新列表
        """
        import random

        if array is None:
            return []
        result = list(array)
        random.shuffle(result)
        return result

    @staticmethod
    def swap(array: list, index1: int, index2: int) -> list:
        """交换两个位置的元素

        :param array: 原始列表
        :param index1: 第一个位置索引
        :param index2: 第二个位置索引
        :return: 交换后的新列表
        :raises IndexError: 索引越界时抛出
        """
        if array is None:
            raise IndexError("数组为 None，无法交换元素")
        length = len(array)
        # 处理负索引
        i1 = index1 if index1 >= 0 else length + index1
        i2 = index2 if index2 >= 0 else length + index2
        if i1 < 0 or i1 >= length:
            raise IndexError(f"索引 {index1} 越界，数组长度为 {length}")
        if i2 < 0 or i2 >= length:
            raise IndexError(f"索引 {index2} 越界，数组长度为 {length}")
        result = list(array)
        result[i1], result[i2] = result[i2], result[i1]
        return result

    @staticmethod
    def length(array) -> int:
        """获取数组长度

        :param array: 数组或列表，None 返回 0
        :return: 数组长度
        """
        if array is None:
            return 0
        try:
            return len(array)
        except TypeError:
            return 0

    @staticmethod
    def min(array) -> Any:
        """取最小值

        :param array: 非空列表或可迭代对象
        :return: 最小值
        :raises ValueError: 数组为空时抛出
        """
        if array is None or (hasattr(array, "__len__") and len(array) == 0):
            raise ValueError("数组为空，无法获取最小值")
        return min(array)

    @staticmethod
    def max(array) -> Any:
        """取最大值

        :param array: 非空列表或可迭代对象
        :return: 最大值
        :raises ValueError: 数组为空时抛出
        """
        if array is None or (hasattr(array, "__len__") and len(array) == 0):
            raise ValueError("数组为空，无法获取最大值")
        return max(array)

    @staticmethod
    def empty_count(*args) -> int:
        """空值数量

        空值定义：None、空字符串、空列表/元组/字典/集合等。

        :param args: 任意数量的参数
        :return: 空值的个数
        """
        count = 0
        for arg in args:
            if arg is None:
                count += 1
            elif isinstance(arg, (str, list, tuple, dict, set, frozenset, bytes)):
                if len(arg) == 0:
                    count += 1
        return count

    @staticmethod
    def has_empty(*args) -> bool:
        """是否有空值

        空值定义：None、空字符串、空列表/元组/字典/集合等。

        :param args: 任意数量的参数
        :return: 如果存在任意一个空值则返回 True
        """
        for arg in args:
            if arg is None:
                return True
            if isinstance(arg, (str, list, tuple, dict, set, frozenset, bytes)):
                if len(arg) == 0:
                    return True
        return False

    @staticmethod
    def filter(array: list, filter_func: Callable[[Any], bool]) -> list:
        """过滤数组

        :param array: 原始列表
        :param filter_func: 过滤函数，返回 True 保留，False 过滤
        :return: 过滤后的新列表
        """
        if array is None:
            return []
        return [item for item in array if filter_func(item)]

    @staticmethod
    def map(array: list, map_func: Callable[[Any], Any]) -> list:
        """映射数组

        :param array: 原始列表
        :param map_func: 映射函数，对每个元素进行转换
        :return: 映射后的新列表
        """
        if array is None:
            return []
        return [map_func(item) for item in array]

    @staticmethod
    def flatten(nested_list) -> list:
        """展平嵌套列表

        将多层嵌套的列表展平为一维列表。字符串和字节类型不会被展开。

        :param nested_list: 嵌套列表
        :return: 展平后的一维列表
        """
        result: list = []

        def _flatten(item):
            if isinstance(item, (str, bytes)):
                result.append(item)
                return
            try:
                for sub_item in item:
                    _flatten(sub_item)
            except TypeError:
                result.append(item)

        if nested_list is not None:
            _flatten(nested_list)
        return result

    @staticmethod
    def distinct(array: list) -> list:
        """去重，保持顺序

        :param array: 原始列表
        :return: 去重后的新列表，保持原有顺序
        """
        if array is None:
            return []
        seen = set()
        result = []
        for item in array:
            # 尝试用 hash 加速查找，不可 hash 的元素回退到线性查找
            try:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            except TypeError:
                # item 不可 hash（如 list、dict），使用线性查找
                if item not in result:
                    result.append(item)
        return result

    @staticmethod
    def fill(value, size: int) -> list:
        """用指定值填充指定大小的列表

        注意：如果 value 是可变对象（如 list、dict），列表中的每个元素将是同一个引用。
        如需独立副本，请对每个元素单独复制。

        :param value: 填充的值
        :param size: 列表大小
        :return: 填充后的列表
        :raises ValueError: size 为负数时抛出
        """
        if size < 0:
            raise ValueError(f"大小不能为负数: {size}")
        return [value] * size

    @staticmethod
    def default_if_empty(arr, default=None):
        """如果数组为空则返回默认值。

        :param arr: 数组（可为 None）
        :param default: 默认值
        :return: 原数组或默认值
        """
        if arr is None or len(arr) == 0:
            return default if default is not None else []
        return arr

    @staticmethod
    def first_match(arr, predicate):
        """返回数组中第一个满足条件的元素。

        :param arr: 数组
        :param predicate: 条件函数
        :return: 满足条件的元素，无匹配返回 None
        """
        if arr is None:
            return None
        for item in arr:
            if predicate(item):
                return item
        return None

    @staticmethod
    def match_index(arr, predicate):
        """返回数组中第一个满足条件的元素索引。

        :param arr: 数组
        :param predicate: 条件函数
        :return: 索引，无匹配返回 -1
        """
        if arr is None:
            return -1
        for i, item in enumerate(arr):
            if predicate(item):
                return i
        return -1

    @staticmethod
    def set_or_append(arr: list, index: int, value) -> list:
        """设置值到指定索引，越界时追加到末尾。

        :param arr: 列表
        :param index: 索引
        :param value: 值
        :return: 修改后的列表
        """
        if arr is None:
            arr = []
        if 0 <= index < len(arr):
            arr[index] = value
        else:
            arr.append(value)
        return arr

    @staticmethod
    def replace(arr: list, index: int, value) -> Any:
        """替换指定索引的值并返回旧值。

        :param arr: 列表
        :param index: 索引
        :param value: 新值
        :return: 旧值
        """
        old = arr[index]
        arr[index] = value
        return old

    @staticmethod
    def resize(arr: list, new_size: int, fill_value=None) -> list:
        """调整数组大小。

        :param arr: 列表
        :param new_size: 新大小
        :param fill_value: 填充值（当需要扩展时）
        :return: 调整后的列表
        """
        if arr is None:
            arr = []
        current = len(arr)
        if new_size > current:
            arr.extend([fill_value] * (new_size - current))
        elif new_size < current:
            del arr[new_size:]
        return arr

    @staticmethod
    def add_all(arr: list, *elements) -> list:
        """向数组中添加多个元素。

        :param arr: 列表
        :param elements: 要添加的元素
        :return: 添加后的列表
        """
        if arr is None:
            arr = []
        arr.extend(elements)
        return arr

    @staticmethod
    def copy(arr, new_size: int = -1):
        """复制数组。

        :param arr: 原数组
        :param new_size: 新数组大小，-1 表示与原数组相同
        :return: 复制后的新数组
        """
        if arr is None:
            return []
        if new_size < 0:
            return list(arr)
        result = list(arr)[:new_size]
        while len(result) < new_size:
            result.append(None)
        return result

    @staticmethod
    def clone(arr):
        """浅克隆数组。

        :param arr: 原数组
        :return: 克隆后的新数组
        """
        if arr is None:
            return []
        return list(arr)

    @staticmethod
    def edit(arr, func):
        """对数组中每个元素应用函数。

        :param arr: 数组
        :param func: 转换函数
        :return: 转换后的新数组
        """
        if arr is None:
            return []
        return [func(item) for item in arr]

    @staticmethod
    def remove_null(arr: list) -> list:
        """移除数组中的 None 元素。

        :param arr: 原数组
        :return: 移除 None 后的新数组
        """
        if arr is None:
            return []
        return [item for item in arr if item is not None]

    @staticmethod
    def remove_empty(arr: list) -> list:
        """移除数组中的空元素（None、空字符串、空列表等）。

        :param arr: 原数组
        :return: 移除空元素后的新数组
        """
        if arr is None:
            return []
        return [item for item in arr if item]

    @staticmethod
    def remove_blank(arr: list) -> list:
        """移除数组中的空白字符串元素。

        :param arr: 原数组
        :return: 移除空白字符串后的新数组
        """
        if arr is None:
            return []
        return [item for item in arr if not isinstance(item, str) or item.strip()]

    @staticmethod
    def null_to_empty(arr):
        """None 转空数组。

        :param arr: 数组（可为 None）
        :return: 原数组或空列表
        """
        return arr if arr is not None else []

    @staticmethod
    def index_of_ignore_case(arr, element: str) -> int:
        """忽略大小写查找字符串在数组中的索引。

        :param arr: 字符串数组
        :param element: 要查找的字符串
        :return: 索引，不存在返回 -1
        """
        if arr is None or element is None:
            return -1
        for i, item in enumerate(arr):
            if isinstance(item, str) and item.lower() == element.lower():
                return i
        return -1

    @staticmethod
    def contains_ignore_case(arr, element: str) -> bool:
        """忽略大小写判断数组是否包含字符串。

        :param arr: 字符串数组
        :param element: 要查找的字符串
        :return: 是否包含
        """
        return ArrayUtil.index_of_ignore_case(arr, element) >= 0

    @staticmethod
    def wrap(arr) -> list:
        """将单个元素包装为数组。

        :param arr: 元素或数组
        :return: 数组
        """
        if arr is None:
            return []
        if isinstance(arr, (list, tuple)):
            return list(arr)
        return [arr]

    @staticmethod
    def is_array(obj) -> bool:
        """判断对象是否为数组（list 或 tuple）。

        :param obj: 对象
        :return: 是否为数组
        """
        return isinstance(obj, (list, tuple))

    @staticmethod
    def get(arr, index: int):
        """安全地获取数组中指定索引的元素。

        :param arr: 数组
        :param index: 索引
        :return: 元素，越界返回 None
        """
        if arr is None or index < 0 or index >= len(arr):
            return None
        return arr[index]

    @staticmethod
    def get_any(arr):
        """获取数组中任意一个元素。

        :param arr: 数组
        :return: 任意元素，为空返回 None
        """
        if arr is None or len(arr) == 0:
            return None
        return arr[0]
