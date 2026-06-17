"""class-based 装饰器模块。

所有装饰器均支持有括号/无括号、同步/协程四种组合。

使用方式::

    # 无括号
    @TimeThis
    def func(): ...

    # 有括号
    @ProfileDeco(sort_by="tottime", limit=5)
    def func(): ...

    # async 也适用
    @CacheFunction(ttl=60)
    async def fetch(url): ...
"""

import asyncio
import functools
import time
from cProfile import Profile
from typing import Any, Callable, Optional


class TimeThis:
    """统计函数执行耗时并打印到标准输出。

    支持无括号 ``@TimeThis`` 和有括号 ``@TimeThis()`` 两种用法，
    同时支持同步和异步函数。

    Examples::

        @TimeThis
        def slow():
            time.sleep(0.1)

        @TimeThis()
        def also_slow():
            time.sleep(0.1)

        @TimeThis
        async def async_slow():
            await asyncio.sleep(0.1)
    """

    def __init__(self, func: Optional[Callable] = None):
        if func is not None:
            functools.update_wrapper(self, func)
        self._func = func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._func is None:
            # @TimeThis() 有括号 — args[0] 是被装饰的函数
            return type(self)(args[0])
        if asyncio.iscoroutinefunction(self._func):
            return self._async_call(*args, **kwargs)
        return self._sync_call(*args, **kwargs)

    def _sync_call(self, *args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = self._func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{self._func.__name__} :\t耗时 {elapsed:.6f}")
        return result

    async def _async_call(self, *args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = await self._func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{self._func.__name__} :\t耗时 {elapsed:.6f}")
        return result


class ProfileDeco:
    """cProfile 性能分析装饰器。

    每次调用被装饰的函数时，自动运行 cProfile 并打印统计信息。
    支持无括号 ``@ProfileDeco`` 和有括号 ``@ProfileDeco(sort_by=...)`` 两种用法。

    :param sort_by: 排序字段，默认 ``"cumtime"``
    :param limit: 打印行数，默认 10

    Examples::

        @ProfileDeco
        def compute(): ...

        @ProfileDeco(sort_by="tottime", limit=5)
        def compute(): ...

        @ProfileDeco
        async def async_compute(): ...
    """

    def __init__(
        self,
        func: Optional[Callable] = None,
        *,
        sort_by: str = "cumtime",
        limit: int = 10,
    ):
        if func is not None:
            functools.update_wrapper(self, func)
        self._func = func
        self._sort_by = sort_by
        self._limit = limit

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._func is None:
            return type(self)(args[0], sort_by=self._sort_by, limit=self._limit)
        if asyncio.iscoroutinefunction(self._func):
            return self._async_call(*args, **kwargs)
        return self._sync_call(*args, **kwargs)

    def _sync_call(self, *args: Any, **kwargs: Any) -> Any:
        import pstats

        p = Profile()
        p.enable()
        try:
            return self._func(*args, **kwargs)
        finally:
            p.disable()
            pstats.Stats(p).sort_stats(self._sort_by).print_stats(self._limit)

    async def _async_call(self, *args: Any, **kwargs: Any) -> Any:
        import pstats

        p = Profile()
        p.enable()
        try:
            return await self._func(*args, **kwargs)
        finally:
            p.disable()
            pstats.Stats(p).sort_stats(self._sort_by).print_stats(self._limit)


class CacheFunction:
    """函数缓存装饰器（dict + TTL）。

    使用字典缓存函数返回值，超过 TTL 秒后自动失效。
    支持无括号 ``@CacheFunction`` 和有括号 ``@CacheFunction(ttl=60)`` 两种用法。

    :param ttl: 缓存过期时间（秒），默认 300

    Examples::

        @CacheFunction(ttl=60)
        def expensive(x):
            return x * 2

        @CacheFunction
        def also_expensive(x):
            return x * 2

        @CacheFunction(ttl=60)
        async def async_fetch(url):
            return await aio_get(url)
    """

    def __init__(self, func: Optional[Callable] = None, *, ttl: int = 300):
        if func is not None:
            functools.update_wrapper(self, func)
        self._func = func
        self._ttl = ttl
        self._cache: dict = {}

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._func is None:
            # @CacheFunction(ttl=60) — args[0] 是被装饰的函数
            return type(self)(args[0], ttl=self._ttl)
        if asyncio.iscoroutinefunction(self._func):
            return self._async_call(*args, **kwargs)
        return self._sync_call(*args, **kwargs)

    def _sync_call(self, *args: Any, **kwargs: Any) -> Any:
        key = (args, tuple(sorted(kwargs.items())))
        entry = self._cache.get(key)
        if entry is not None:
            result, expire_at = entry
            if time.time() < expire_at:
                return result
        result = self._func(*args, **kwargs)
        self._cache[key] = (result, time.time() + self._ttl)
        return result

    async def _async_call(self, *args: Any, **kwargs: Any) -> Any:
        key = (args, tuple(sorted(kwargs.items())))
        entry = self._cache.get(key)
        if entry is not None:
            result, expire_at = entry
            if time.time() < expire_at:
                return result
        result = await self._func(*args, **kwargs)
        self._cache[key] = (result, time.time() + self._ttl)
        return result

    @property
    def cache(self) -> dict:
        """获取内部缓存字典。"""
        return self._cache


class Memoize(CacheFunction):
    """记忆化装饰器（CacheFunction 子类）。

    与 ``CacheFunction`` 相同，语义上用于记忆化重复计算。
    默认 TTL 为 600 秒。

    :param ttl: 缓存过期时间（秒），默认 600

    Examples::

        @Memoize(ttl=600)
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)
    """

    def __init__(self, func: Optional[Callable] = None, *, ttl: int = 600):
        super().__init__(func, ttl=ttl)


class FuncOnce:
    """函数只执行一次装饰器。

    首次调用后缓存结果，后续调用直接返回缓存值。
    支持无括号 ``@FuncOnce`` 和有括号 ``@FuncOnce()`` 两种用法。

    Examples::

        @FuncOnce
        def init():
            return expensive_setup()

        @FuncOnce()
        def also_init():
            return expensive_setup()

        @FuncOnce
        async def async_init():
            return await aio_setup()
    """

    _sentinel = object()

    def __init__(self, func: Optional[Callable] = None):
        if func is not None:
            functools.update_wrapper(self, func)
        self._func = func
        self._result: Any = self._sentinel

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._func is None:
            # @FuncOnce() 有括号 — args[0] 是被装饰的函数
            return type(self)(args[0])
        if asyncio.iscoroutinefunction(self._func):
            # 始终返回协程，确保 await / run_until_complete 始终可用
            return self._async_call(*args, **kwargs)
        if self._result is not self._sentinel:
            return self._result
        self._result = self._func(*args, **kwargs)
        return self._result

    async def _async_call(self, *args: Any, **kwargs: Any) -> Any:
        if self._result is not self._sentinel:
            return self._result
        self._result = await self._func(*args, **kwargs)
        return self._result


class TtlLruCache:
    """带 TTL 的 LRU 缓存装饰器。

    结合 ``functools.lru_cache`` 的 LRU 淘汰策略与 TTL 过期机制。
    支持无括号 ``@TtlLruCache`` 和有括号 ``@TtlLruCache(maxsize=64, ttl=120)`` 两种用法。

    :param maxsize: 最大缓存条目数，默认 128
    :param ttl: 缓存过期时间（秒），默认 300

    Examples::

        @TtlLruCache(maxsize=64, ttl=120)
        def expensive(x):
            return x * 2

        @TtlLruCache
        def also_expensive(x):
            return x * 2

        @TtlLruCache(ttl=60)
        async def async_fetch(url):
            return await aio_get(url)
    """

    def __init__(
        self,
        func: Optional[Callable] = None,
        *,
        maxsize: int = 128,
        ttl: int = 300,
    ):
        if func is not None:
            functools.update_wrapper(self, func)
        self._func = func
        self._maxsize = maxsize
        self._ttl = ttl
        self._timestamps: dict = {}
        self._cached_func: Optional[Callable] = None
        if func is not None:
            self._build_cache()

    def _build_cache(self) -> None:
        """构建内部 lru_cache。"""
        func = self._func
        maxsize = self._maxsize

        @functools.lru_cache(maxsize=maxsize)
        def cached(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        self._cached_func = cached

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._func is None:
            # @TtlLruCache(maxsize=64, ttl=120) — args[0] 是被装饰的函数
            return type(self)(args[0], maxsize=self._maxsize, ttl=self._ttl)
        if asyncio.iscoroutinefunction(self._func):
            return self._async_call(*args, **kwargs)
        return self._sync_call(*args, **kwargs)

    def _get_key(self, args: tuple, kwargs: dict) -> tuple:
        if kwargs:
            return (args, tuple(sorted(kwargs.items())))
        return args

    def _check_ttl(self, key: tuple) -> None:
        now = time.time()
        expire_at = self._timestamps.get(key, 0)
        if now >= expire_at:
            self._cached_func.cache_clear()  # type: ignore[union-attr]
            self._timestamps.clear()
        self._timestamps[key] = now + self._ttl

    def _sync_call(self, *args: Any, **kwargs: Any) -> Any:
        key = self._get_key(args, kwargs)
        self._check_ttl(key)
        return self._cached_func(*args, **kwargs)  # type: ignore[misc]

    async def _async_call(self, *args: Any, **kwargs: Any) -> Any:
        key = self._get_key(args, kwargs)
        self._check_ttl(key)
        return await self._func(*args, **kwargs)

    def cache_clear(self) -> None:
        """清空缓存。"""
        if self._cached_func is not None:
            self._cached_func.cache_clear()  # type: ignore[union-attr]

    def cache_info(self) -> Any:
        """获取缓存命中信息。"""
        if self._cached_func is not None:
            return self._cached_func.cache_info()  # type: ignore[union-attr]
        return None


class NoneOnException:
    """函数抛异常时返回 None。

    支持无括号 ``@NoneOnException`` 和有括号 ``@NoneOnException()`` 两种用法。

    Examples::

        @NoneOnException
        def risky():
            raise ValueError("oops")

        assert risky() is None

        @NoneOnException
        async def async_risky():
            raise ValueError("oops")

        assert await async_risky() is None
    """

    def __init__(self, func: Optional[Callable] = None):
        if func is not None:
            functools.update_wrapper(self, func)
        self._func = func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._func is None:
            # @NoneOnException() 有括号 — args[0] 是被装饰的函数
            return type(self)(args[0])
        if asyncio.iscoroutinefunction(self._func):
            return self._async_call(*args, **kwargs)
        try:
            return self._func(*args, **kwargs)
        except Exception:
            return None

    async def _async_call(self, *args: Any, **kwargs: Any) -> Any:
        try:
            return await self._func(*args, **kwargs)
        except Exception:
            return None
