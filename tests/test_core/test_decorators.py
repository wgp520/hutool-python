"""class-based 装饰器全面测试。

覆盖 7 个装饰器的无括号、有括号、async 三种用法，
以及通过 Util 类的调用。
"""

import asyncio
import time

from hutool import (
    CacheFunction,
    CacheUtil,
    FuncOnce,
    Memoize,
    NoneOnException,
    ObjectUtil,
    ProfileDeco,
    ProfUtil,
    TimeThis,
    TimingUtil,
    TtlLruCache,
)

# ── TimeThis ────────────────────────────────────────────────────


class TestTimeThis:
    """TimeThis 装饰器测试。"""

    def test_no_parens(self):
        @TimeThis
        def add(a, b):
            return a + b

        assert add(1, 2) == 3

    def test_with_parens(self):
        @TimeThis()
        def add(a, b):
            return a + b

        assert add(1, 2) == 3

    def test_async_no_parens(self):
        @TimeThis
        async def async_add(a, b):
            return a + b

        result = asyncio.get_event_loop().run_until_complete(async_add(1, 2))
        assert result == 3

    def test_async_with_parens(self):
        @TimeThis()
        async def async_add(a, b):
            return a + b

        result = asyncio.get_event_loop().run_until_complete(async_add(1, 2))
        assert result == 3

    def test_preserves_name(self):
        @TimeThis
        def my_func():
            return 42

        assert my_func.__name__ == "my_func"

    def test_backward_compat_timing_util(self):
        @TimingUtil.timethis
        def slow():
            return 77

        assert slow() == 77

    def test_time_elapsed_printed(self, capsys):
        @TimeThis
        def hello():
            return "hi"

        hello()
        captured = capsys.readouterr()
        assert "hello" in captured.out
        assert "耗时" in captured.out


# ── ProfileDeco ─────────────────────────────────────────────────


class TestProfileDeco:
    """ProfileDeco 装饰器测试。"""

    def test_no_parens(self):
        @ProfileDeco
        def compute():
            return sum(range(100))

        assert compute() == 4950

    def test_with_parens(self):
        @ProfileDeco(sort_by="tottime", limit=1)
        def compute():
            return sum(range(100))

        assert compute() == 4950

    def test_async_no_parens(self):
        @ProfileDeco
        async def async_compute():
            return sum(range(100))

        result = asyncio.get_event_loop().run_until_complete(async_compute())
        assert result == 4950

    def test_async_with_parens(self):
        @ProfileDeco(sort_by="tottime", limit=1)
        async def async_compute():
            return sum(range(100))

        result = asyncio.get_event_loop().run_until_complete(async_compute())
        assert result == 4950

    def test_backward_compat_prof_decorator(self):
        @ProfUtil.prof_decorator(sort_by="tottime", limit=1)
        def compute():
            return 42

        assert compute() == 42

    def test_backward_compat_profile_deco(self):
        @ProfUtil.profile_deco(sort_by="cumtime", limit=1)
        def compute():
            return 42

        assert compute() == 42

    def test_is_callable(self):
        assert callable(ProfileDeco)


# ── CacheFunction ───────────────────────────────────────────────


class TestCacheFunction:
    """CacheFunction 装饰器测试。"""

    def test_no_parens(self):
        call_count = 0

        @CacheFunction
        def double(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert double(5) == 10
        assert double(5) == 10
        assert call_count == 1

    def test_with_parens(self):
        call_count = 0

        @CacheFunction(ttl=60)
        def double(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert double(5) == 10
        assert double(5) == 10
        assert call_count == 1

    def test_async_no_parens(self):
        call_count = 0

        @CacheFunction
        async def async_double(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        loop = asyncio.get_event_loop()
        assert loop.run_until_complete(async_double(5)) == 10
        assert loop.run_until_complete(async_double(5)) == 10
        assert call_count == 1

    def test_async_with_parens(self):
        call_count = 0

        @CacheFunction(ttl=60)
        async def async_double(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        loop = asyncio.get_event_loop()
        assert loop.run_until_complete(async_double(5)) == 10
        assert loop.run_until_complete(async_double(5)) == 10
        assert call_count == 1

    def test_ttl_expiry(self):
        call_count = 0

        @CacheFunction(ttl=1)
        def compute(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert compute(5) == 10
        assert call_count == 1
        time.sleep(1.1)
        assert compute(5) == 10
        assert call_count == 2

    def test_different_args(self):
        @CacheFunction(ttl=60)
        def double(x):
            return x * 2

        assert double(5) == 10
        assert double(3) == 6

    def test_has_cache_property(self):
        @CacheFunction(ttl=60)
        def f(x):
            return x

        f(1)
        assert isinstance(f.cache, dict)
        assert len(f.cache) == 1

    def test_backward_compat_cache_function(self):
        @CacheUtil.cache_function(ttl=60)
        def double(x):
            return x * 2

        assert double(5) == 10
        assert double(5) == 10

    def test_preserves_name(self):
        @CacheFunction(ttl=60)
        def my_func():
            return 42

        assert my_func.__name__ == "my_func"


# ── Memoize ─────────────────────────────────────────────────────


class TestMemoize:
    """Memoize 装饰器测试。"""

    def test_no_parens(self):
        call_count = 0

        @Memoize
        def fib(n):
            nonlocal call_count
            call_count += 1
            if n < 2:
                return n
            return fib(n - 1) + fib(n - 2)

        assert fib(10) == 55

    def test_with_parens(self):
        call_count = 0

        @Memoize(ttl=600)
        def double(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert double(5) == 10
        assert double(5) == 10
        assert call_count == 1

    def test_default_ttl_is_600(self):
        deco = Memoize(ttl=600)
        assert deco._ttl == 600

    def test_backward_compat_memoize(self):
        @CacheUtil.memoize(ttl=600)
        def double(x):
            return x * 2

        assert double(5) == 10


# ── FuncOnce ────────────────────────────────────────────────────


class TestFuncOnce:
    """FuncOnce 装饰器测试。"""

    def test_no_parens(self):
        call_count = 0

        @FuncOnce
        def init():
            nonlocal call_count
            call_count += 1
            return 42

        assert init() == 42
        assert init() == 42
        assert call_count == 1

    def test_with_parens(self):
        call_count = 0

        @FuncOnce()
        def init():
            nonlocal call_count
            call_count += 1
            return "done"

        assert init() == "done"
        assert init() == "done"
        assert call_count == 1

    def test_async_no_parens(self):
        call_count = 0

        @FuncOnce
        async def async_init():
            nonlocal call_count
            call_count += 1
            return 99

        loop = asyncio.get_event_loop()
        assert loop.run_until_complete(async_init()) == 99
        assert loop.run_until_complete(async_init()) == 99
        assert call_count == 1

    def test_async_with_parens(self):
        call_count = 0

        @FuncOnce()
        async def async_init():
            nonlocal call_count
            call_count += 1
            return 99

        loop = asyncio.get_event_loop()
        assert loop.run_until_complete(async_init()) == 99
        assert loop.run_until_complete(async_init()) == 99
        assert call_count == 1

    def test_backward_compat_func_once(self):
        call_count = 0

        @CacheUtil.func_once
        def init():
            nonlocal call_count
            call_count += 1
            return 77

        assert init() == 77
        assert init() == 77
        assert call_count == 1

    def test_preserves_name(self):
        @FuncOnce
        def my_init():
            return 1

        assert my_init.__name__ == "my_init"


# ── TtlLruCache ────────────────────────────────────────────────


class TestTtlLruCache:
    """TtlLruCache 装饰器测试。"""

    def test_no_parens(self):
        call_count = 0

        @TtlLruCache
        def double(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert double(5) == 10
        assert double(5) == 10
        assert call_count == 1

    def test_with_parens(self):
        call_count = 0

        @TtlLruCache(maxsize=64, ttl=120)
        def double(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert double(5) == 10
        assert double(5) == 10
        assert call_count == 1

    def test_async_no_parens(self):
        @TtlLruCache
        async def async_double(x):
            return x * 2

        loop = asyncio.get_event_loop()
        assert loop.run_until_complete(async_double(5)) == 10

    def test_async_with_parens(self):
        @TtlLruCache(maxsize=64, ttl=120)
        async def async_double(x):
            return x * 2

        loop = asyncio.get_event_loop()
        assert loop.run_until_complete(async_double(5)) == 10

    def test_ttl_expiry(self):
        call_count = 0

        @TtlLruCache(maxsize=16, ttl=1)
        def compute(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert compute(5) == 10
        assert call_count == 1
        time.sleep(1.1)
        assert compute(5) == 10
        assert call_count == 2

    def test_cache_clear(self):
        call_count = 0

        @TtlLruCache(maxsize=16, ttl=60)
        def f(x):
            nonlocal call_count
            call_count += 1
            return x

        f(1)
        assert call_count == 1
        f.cache_clear()
        f(1)
        assert call_count == 2

    def test_cache_info(self):
        @TtlLruCache(maxsize=16, ttl=60)
        def f(x):
            return x

        f(1)
        info = f.cache_info()
        assert info is not None
        assert hasattr(info, "hits")
        assert hasattr(info, "misses")

    def test_different_args(self):
        @TtlLruCache(maxsize=16, ttl=60)
        def double(x):
            return x * 2

        assert double(5) == 10
        assert double(3) == 6

    def test_backward_compat_lru_cache(self):
        @CacheUtil.lru_cache(maxsize=16, ttl=60)
        def double(x):
            return x * 2

        assert double(5) == 10
        assert double(5) == 10

    def test_preserves_name(self):
        @TtlLruCache(maxsize=16, ttl=60)
        def my_func():
            return 42

        assert my_func.__name__ == "my_func"


# ── NoneOnException ─────────────────────────────────────────────


class TestNoneOnException:
    """NoneOnException 装饰器测试。"""

    def test_no_parens_normal(self):
        @NoneOnException
        def safe():
            return 42

        assert safe() == 42

    def test_no_parens_exception(self):
        @NoneOnException
        def risky():
            raise ValueError("oops")

        assert risky() is None

    def test_with_parens_normal(self):
        @NoneOnException()
        def safe():
            return 42

        assert safe() == 42

    def test_with_parens_exception(self):
        @NoneOnException()
        def risky():
            raise ValueError("oops")

        assert risky() is None

    def test_async_no_parens_normal(self):
        @NoneOnException
        async def safe():
            return 42

        result = asyncio.get_event_loop().run_until_complete(safe())
        assert result == 42

    def test_async_no_parens_exception(self):
        @NoneOnException
        async def risky():
            raise ValueError("oops")

        result = asyncio.get_event_loop().run_until_complete(risky())
        assert result is None

    def test_async_with_parens_normal(self):
        @NoneOnException()
        async def safe():
            return 42

        result = asyncio.get_event_loop().run_until_complete(safe())
        assert result == 42

    def test_async_with_parens_exception(self):
        @NoneOnException()
        async def risky():
            raise ValueError("oops")

        result = asyncio.get_event_loop().run_until_complete(risky())
        assert result is None

    def test_backward_compat_object_util(self):
        @ObjectUtil.none_on_exception
        def risky():
            raise RuntimeError("boom")

        assert risky() is None

    def test_backward_compat_normal_return(self):
        @ObjectUtil.none_on_exception
        def safe():
            return 99

        assert safe() == 99

    def test_preserves_name(self):
        @NoneOnException
        def my_func():
            return 1

        assert my_func.__name__ == "my_func"


# ── 综合兼容性测试 ─────────────────────────────────────────────


class TestBackwardCompat:
    """验证所有旧 Util 类的装饰器调用方式仍然可用。"""

    def test_timing_util_timethis(self):
        @TimingUtil.timethis
        def fast():
            return 1

        assert fast() == 1

    def test_prof_util_profile_deco(self):
        @ProfUtil.profile_deco(sort_by="tottime", limit=1)
        def fast():
            return 1

        assert fast() == 1

    def test_prof_util_prof_decorator(self):
        @ProfUtil.prof_decorator(sort_by="tottime", limit=1)
        def fast():
            return 1

        assert fast() == 1

    def test_cache_util_cache_function(self):
        @CacheUtil.cache_function(ttl=60)
        def fast(x):
            return x

        assert fast(1) == 1

    def test_cache_util_memoize(self):
        @CacheUtil.memoize(ttl=600)
        def fast(x):
            return x

        assert fast(1) == 1

    def test_cache_util_func_once(self):
        @CacheUtil.func_once
        def fast():
            return 1

        assert fast() == 1

    def test_cache_util_lru_cache(self):
        @CacheUtil.lru_cache(maxsize=16, ttl=60)
        def fast(x):
            return x

        assert fast(1) == 1

    def test_object_util_none_on_exception(self):
        @ObjectUtil.none_on_exception
        def fast():
            raise ValueError()

        assert fast() is None

    def test_timethis_standalone(self):
        @TimeThis
        def fast():
            return 1

        assert fast() == 1
