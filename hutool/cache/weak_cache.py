"""弱引用缓存实现"""

import weakref


class WeakCache:
    """弱引用缓存

    使用弱引用存储值，当值没有其他引用时自动清理。
    不支持弱引用的类型（int、str 等）会回退到强引用存储。
    """

    def __init__(self, capacity: int = 16) -> None:
        """初始化弱引用缓存。

        :param capacity: 缓存最大容量，默认16
        """
        self._capacity = capacity
        self._weak_data = weakref.WeakValueDictionary()
        self._strong_data = {}  # type: dict  # 回退存储（不支持弱引用的值）
        self._keys_order = []  # type: list
        self._hit_count = 0
        self._miss_count = 0

    def _total_size(self):
        return len(self._weak_data) + len(self._strong_data)

    def get(self, key, default=None):
        # type: (str, object) -> object
        """获取缓存值

        :param key: 缓存键
        :param default: 默认值
        :return: 缓存值
        """
        value = self._weak_data.get(key)
        if value is not None:
            self._hit_count += 1
            return value
        value = self._strong_data.get(key)
        if value is not None:
            self._hit_count += 1
            return value
        self._miss_count += 1
        return default

    def put(self, key, value):
        # type: (str, object) -> None
        """设置缓存值

        :param key: 缓存键
        :param value: 缓存值
        """
        if self._total_size() >= self._capacity and key not in self._weak_data and key not in self._strong_data:
            # Remove oldest
            if self._keys_order:
                old_key = self._keys_order.pop(0)
                self._weak_data.pop(old_key, None)
                self._strong_data.pop(old_key, None)
        try:
            self._weak_data[key] = value
            self._strong_data.pop(key, None)
        except TypeError:
            # 不支持弱引用的类型，使用强引用
            self._strong_data[key] = value
        if key not in self._keys_order:
            self._keys_order.append(key)

    def remove(self, key):
        # type: (str) -> None
        """移除缓存

        :param key: 缓存键
        """
        self._weak_data.pop(key, None)
        self._strong_data.pop(key, None)
        if key in self._keys_order:
            self._keys_order.remove(key)

    def clear(self):
        # type: () -> None
        """清空缓存"""
        self._weak_data.clear()
        self._strong_data.clear()
        self._keys_order.clear()

    def size(self):
        # type: () -> int
        """缓存大小

        :return: 缓存条目数
        """
        return self._total_size()

    def is_empty(self):
        # type: () -> bool
        """是否为空

        :return: 缓存是否为空
        """
        return self._total_size() == 0

    def get_hit_count(self):
        # type: () -> int
        """获取命中次数

        :return: 命中次数
        """
        return self._hit_count

    def get_miss_count(self):
        # type: () -> int
        """获取未命中次数

        :return: 未命中次数
        """
        return self._miss_count

    def key_set(self):
        """获取所有键

        :return: 键列表
        """
        return list(self._weak_data.keys()) + list(self._strong_data.keys())

    def __contains__(self, key):
        # type: (str) -> bool
        return key in self._weak_data or key in self._strong_data

    def __len__(self):
        # type: () -> int
        return self._total_size()
