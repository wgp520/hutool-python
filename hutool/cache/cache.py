from ..core.decorators import CacheFunction, FuncOnce, Memoize, TtlLruCache
from .fifo_cache import FIFOCache
from .lfu_cache import LFUCache
from .lru_cache import LRUCache
from .timed_cache import TimedCache
from .weak_cache import WeakCache


class CacheUtil:
    """缓存工厂类。

    提供各种缓存实现的便捷创建方法。
    """

    @staticmethod
    def new_fifo_cache(capacity: int = 16) -> FIFOCache:
        """创建FIFO（先进先出）缓存。

        :param capacity: 缓存最大容量，默认16
        :return: FIFOCache实例
        """
        return FIFOCache(capacity)

    @staticmethod
    def new_lfu_cache(capacity: int = 16) -> LFUCache:
        """创建LFU（最不经常使用）缓存。

        :param capacity: 缓存最大容量，默认16
        :return: LFUCache实例
        """
        return LFUCache(capacity)

    @staticmethod
    def new_lru_cache(capacity: int = 16) -> LRUCache:
        """创建LRU（最近最少使用）缓存。

        :param capacity: 缓存最大容量，默认16
        :return: LRUCache实例
        """
        return LRUCache(capacity)

    @staticmethod
    def new_timed_cache(timeout: int = 60) -> TimedCache:
        """创建定时缓存。

        :param timeout: 默认过期时间（秒），默认60秒
        :return: TimedCache实例
        """
        return TimedCache(timeout)

    @staticmethod
    def new_weak_cache(capacity: int = 16) -> WeakCache:
        """创建弱引用缓存

        使用WeakValueDictionary实现。

        :param capacity: 缓存最大容量
        :return: WeakCache实例
        """
        return WeakCache(capacity)


# 别名：class-based 装饰器
CacheUtil.cache_function = staticmethod(CacheFunction)
CacheUtil.memoize = staticmethod(Memoize)
CacheUtil.func_once = staticmethod(FuncOnce)
CacheUtil.lru_cache = staticmethod(TtlLruCache)
