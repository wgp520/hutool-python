from collections import OrderedDict
from typing import Any, KeysView


class FIFOCache:
    """FIFO（先进先出）缓存实现。

    当缓存满时，最早插入的元素会被淘汰。
    """

    def __init__(self, capacity: int = 16) -> None:
        """初始化FIFO缓存。

        :param capacity: 缓存最大容量，默认16
        """
        self._capacity: int = capacity
        self._cache: OrderedDict = OrderedDict()

    def get(self, key: Any, default: Any = None) -> Any:
        """获取缓存值。

        :param key: 缓存键
        :param default: 键不存在时返回的默认值
        :return: 缓存值，不存在时返回默认值
        """
        return self._cache.get(key, default)

    def put(self, key: Any, value: Any) -> None:
        """放入缓存。如果缓存已满，淘汰最早插入的元素。

        :param key: 缓存键
        :param value: 缓存值
        """
        if key in self._cache:
            self._cache[key] = value
            return
        if len(self._cache) >= self._capacity:
            self._cache.popitem(last=False)
        self._cache[key] = value

    def remove(self, key: Any) -> Any:
        """移除指定键的缓存。

        :param key: 缓存键
        :return: 被移除的值，键不存在时返回None
        """
        return self._cache.pop(key, None)

    def size(self) -> int:
        """获取当前缓存大小。

        :return: 当前缓存条目数
        """
        return len(self._cache)

    def capacity(self) -> int:
        """获取缓存最大容量。

        :return: 缓存最大容量
        """
        return self._capacity

    def clear(self) -> None:
        """清空所有缓存。"""
        self._cache.clear()

    def is_full(self) -> bool:
        """判断缓存是否已满。

        :return: 缓存已满返回True，否则返回False
        """
        return len(self._cache) >= self._capacity

    def keys(self) -> KeysView:
        """获取所有缓存键。

        :return: 缓存键的视图
        """
        return self._cache.keys()

    def __contains__(self, key: Any) -> bool:
        """判断键是否存在于缓存中。"""
        return key in self._cache

    def __len__(self) -> int:
        """返回缓存大小。"""
        return len(self._cache)
