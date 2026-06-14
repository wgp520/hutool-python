import threading
import time
from typing import Any, Optional


class TimedCache:
    """定时缓存实现。

    每个缓存条目可以设置独立的过期时间，过期后自动失效。
    支持定时清理过期条目以释放内存。
    """

    def __init__(self, timeout: int = 60) -> None:
        """初始化定时缓存。

        :param timeout: 默认过期时间（秒），默认60秒
        """
        self._timeout: int = timeout
        self._cache: dict = {}  # key -> (value, expire_time)
        self._lock: threading.Lock = threading.Lock()
        self._prune_timer: Optional[threading.Timer] = None

    def get(self, key: Any, default: Any = None) -> Any:
        """获取缓存值。若已过期则返回默认值。

        :param key: 缓存键
        :param default: 键不存在或已过期时返回的默认值
        :return: 缓存值，不存在或已过期时返回默认值
        """
        with self._lock:
            if key not in self._cache:
                return default
            value, expire_time = self._cache[key]
            if time.time() > expire_time:
                del self._cache[key]
                return default
            return value

    def put(self, key: Any, value: Any, timeout: Optional[int] = None) -> None:
        """放入缓存。

        :param key: 缓存键
        :param value: 缓存值
        :param timeout: 过期时间（秒），为None时使用默认过期时间
        """
        expire_time = time.time() + (timeout if timeout is not None else self._timeout)
        with self._lock:
            self._cache[key] = (value, expire_time)

    def remove(self, key: Any) -> Any:
        """移除指定键的缓存。

        :param key: 缓存键
        :return: 被移除的值，键不存在时返回None
        """
        with self._lock:
            entry = self._cache.pop(key, None)
            if entry is None:
                return None
            value, _ = entry
            return value

    def size(self) -> int:
        """获取当前缓存大小（包含已过期但未清理的条目）。

        :return: 当前缓存条目数
        """
        with self._lock:
            return len(self._cache)

    def clear(self) -> None:
        """清空所有缓存。"""
        with self._lock:
            self._cache.clear()

    def prune(self) -> int:
        """清理过期缓存条目。

        :return: 被清理的条目数
        """
        now = time.time()
        expired_keys: list = []
        with self._lock:
            for key, (_, expire_time) in self._cache.items():
                if now > expire_time:
                    expired_keys.append(key)
            for key in expired_keys:
                del self._cache[key]
        return len(expired_keys)

    def schedule_prune(self, delay_seconds: int = 60) -> None:
        """启动定时清理线程，定期清理过期缓存。

        :param delay_seconds: 清理间隔（秒），默认60秒
        """
        self._cancel_prune_timer()
        self._prune_timer = threading.Timer(delay_seconds, self._prune_callback, args=(delay_seconds,))
        self._prune_timer.daemon = True
        self._prune_timer.start()

    def _prune_callback(self, delay_seconds: int) -> None:
        """清理回调，执行清理后重新调度。

        :param delay_seconds: 下次清理间隔（秒）
        """
        self.prune()
        self._prune_timer = threading.Timer(delay_seconds, self._prune_callback, args=(delay_seconds,))
        self._prune_timer.daemon = True
        self._prune_timer.start()

    def _cancel_prune_timer(self) -> None:
        """取消定时清理线程。"""
        if self._prune_timer is not None:
            self._prune_timer.cancel()
            self._prune_timer = None
