from collections import defaultdict
from typing import Any


class LFUCache:
    """LFU（最不经常使用）缓存实现。

    当缓存满时，访问频率最低的元素会被淘汰。
    若有多个元素频率相同，淘汰最早插入的。
    """

    def __init__(self, capacity: int = 16) -> None:
        """初始化LFU缓存。

        :param capacity: 缓存最大容量，默认16
        """
        self._capacity: int = capacity
        self._cache: dict = {}  # key -> value
        self._freq: dict = {}  # key -> frequency
        self._freq_to_keys: dict = defaultdict(list)  # frequency -> [keys]
        self._min_freq: int = 0

    def get(self, key: Any, default: Any = None) -> Any:
        """获取缓存值，并更新访问频率。

        :param key: 缓存键
        :param default: 键不存在时返回的默认值
        :return: 缓存值，不存在时返回默认值
        """
        if key not in self._cache:
            return default
        self._update_freq(key)
        return self._cache[key]

    def put(self, key: Any, value: Any) -> None:
        """放入缓存。如果缓存已满，淘汰访问频率最低的元素。

        :param key: 缓存键
        :param value: 缓存值
        """
        if self._capacity <= 0:
            return

        if key in self._cache:
            self._cache[key] = value
            self._update_freq(key)
            return

        if len(self._cache) >= self._capacity:
            self._evict()

        self._cache[key] = value
        self._freq[key] = 1
        self._freq_to_keys[1].append(key)
        self._min_freq = 1

    def remove(self, key: Any) -> Any:
        """移除指定键的缓存。

        :param key: 缓存键
        :return: 被移除的值，键不存在时返回None
        """
        if key not in self._cache:
            return None

        freq = self._freq[key]
        self._freq_to_keys[freq].remove(key)
        if not self._freq_to_keys[freq]:
            del self._freq_to_keys[freq]
            if self._min_freq == freq:
                self._min_freq = min(self._freq_to_keys.keys()) if self._freq_to_keys else 0

        value = self._cache[key]
        del self._cache[key]
        del self._freq[key]
        return value

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
        self._freq.clear()
        self._freq_to_keys.clear()
        self._min_freq = 0

    def is_full(self) -> bool:
        """判断缓存是否已满。

        :return: 缓存已满返回True，否则返回False
        """
        return len(self._cache) >= self._capacity

    def _update_freq(self, key: Any) -> None:
        """更新键的访问频率。

        :param key: 缓存键
        """
        freq = self._freq[key]
        self._freq_to_keys[freq].remove(key)
        if not self._freq_to_keys[freq]:
            del self._freq_to_keys[freq]
            if self._min_freq == freq:
                self._min_freq = freq + 1

        new_freq = freq + 1
        self._freq[key] = new_freq
        self._freq_to_keys[new_freq].append(key)

    def _evict(self) -> None:
        """淘汰访问频率最低且最早插入的元素。"""
        keys = self._freq_to_keys[self._min_freq]
        evict_key = keys.pop(0)
        if not keys:
            del self._freq_to_keys[self._min_freq]
        del self._cache[evict_key]
        del self._freq[evict_key]
