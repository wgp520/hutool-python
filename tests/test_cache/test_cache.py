import time

from hutool import CacheUtil, FIFOCache, LFUCache, LRUCache, TimedCache, WeakCache


class TestFIFOCache:
    def test_put_get(self):
        cache = FIFOCache(3)
        cache.put("a", 1)
        assert cache.get("a") == 1

    def test_capacity(self):
        cache = FIFOCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)  # Should evict "a"
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_size(self):
        cache = FIFOCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        assert cache.size() == 2

    def test_remove(self):
        cache = FIFOCache(3)
        cache.put("a", 1)
        cache.remove("a")
        assert cache.get("a") is None

    def test_clear(self):
        cache = FIFOCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.clear()
        assert cache.size() == 0

    def test_is_full(self):
        cache = FIFOCache(2)
        assert cache.is_full() is False
        cache.put("a", 1)
        cache.put("b", 2)
        assert cache.is_full() is True


class TestLFUCache:
    def test_put_get(self):
        cache = LFUCache(3)
        cache.put("a", 1)
        assert cache.get("a") == 1

    def test_eviction(self):
        cache = LFUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")  # "a" gets 1 access
        cache.put("c", 3)  # Should evict "b" (0 accesses)
        assert cache.get("a") == 1
        assert cache.get("b") is None

    def test_size(self):
        cache = LFUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        assert cache.size() == 2

    def test_remove(self):
        cache = LFUCache(3)
        cache.put("a", 1)
        cache.remove("a")
        assert cache.get("a") is None


class TestLRUCache:
    def test_put_get(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        assert cache.get("a") == 1

    def test_eviction(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")  # "a" is now recently used
        cache.put("c", 3)  # Should evict "b" (least recently used)
        assert cache.get("a") == 1
        assert cache.get("b") is None
        assert cache.get("c") == 3

    def test_size(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        assert cache.size() == 2

    def test_clear(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.clear()
        assert cache.size() == 0


class TestTimedCache:
    def test_put_get(self):
        cache = TimedCache(1)  # 1 second timeout
        cache.put("a", 1)
        assert cache.get("a") == 1

    def test_expiry(self):
        cache = TimedCache(0.1)  # 100ms timeout
        cache.put("a", 1)
        assert cache.get("a") == 1
        time.sleep(0.2)
        assert cache.get("a") is None

    def test_remove_expired(self):
        cache = TimedCache(0.1)
        cache.put("a", 1)
        cache.put("b", 2)
        time.sleep(0.2)
        removed = cache.prune()
        assert removed == 2
        assert cache.size() == 0


class TestWeakCache:
    def test_basic_ops(self):
        cache = WeakCache(10)
        cache.put("key1", "value1")
        assert cache.get("key1") == "value1"
        assert cache.size() == 1

    def test_get_miss(self):
        cache = WeakCache()
        assert cache.get("missing", "default") == "default"

    def test_remove(self):
        cache = WeakCache()
        cache.put("k", "v")
        cache.remove("k")
        assert cache.get("k") is None

    def test_clear(self):
        cache = WeakCache()
        cache.put("a", 1)
        cache.put("b", 2)
        cache.clear()
        assert cache.size() == 0

    def test_is_empty(self):
        cache = WeakCache()
        assert cache.is_empty() is True
        cache.put("x", 1)
        assert cache.is_empty() is False

    def test_hit_miss_count(self):
        cache = WeakCache()
        cache.put("a", 1)
        cache.get("a")
        cache.get("b")
        assert cache.get_hit_count() == 1
        assert cache.get_miss_count() == 1

    def test_key_set(self):
        cache = WeakCache()
        cache.put("x", 1)
        cache.put("y", 2)
        keys = cache.key_set()
        assert "x" in keys
        assert "y" in keys

    def test_contains(self):
        cache = WeakCache()
        cache.put("k", "v")
        assert "k" in cache
        assert "m" not in cache

    def test_len(self):
        cache = WeakCache()
        cache.put("a", 1)
        assert len(cache) == 1


class TestCacheUtil:
    def test_new_fifo_cache(self):
        cache = CacheUtil.new_fifo_cache(10)
        assert isinstance(cache, FIFOCache)

    def test_new_lfu_cache(self):
        cache = CacheUtil.new_lfu_cache(10)
        assert isinstance(cache, LFUCache)

    def test_new_lru_cache(self):
        cache = CacheUtil.new_lru_cache(10)
        assert isinstance(cache, LRUCache)

    def test_new_timed_cache(self):
        cache = CacheUtil.new_timed_cache(60)
        assert isinstance(cache, TimedCache)

    def test_new_weak_cache(self):
        cache = CacheUtil.new_weak_cache(10)
        assert isinstance(cache, WeakCache)

    def test_basic(self):
        call_count = 0

        @CacheUtil.lru_cache(maxsize=16, ttl=60)
        def add(a, b):
            nonlocal call_count
            call_count += 1
            return a + b

        assert add(1, 2) == 3
        assert add(1, 2) == 3
        assert call_count == 1

    def test_different_args(self):
        @CacheUtil.lru_cache(maxsize=16, ttl=60)
        def double(x):
            return x * 2

        assert double(5) == 10
        assert double(3) == 6

    def test_ttl_expiry(self):
        import time

        call_count = 0

        @CacheUtil.lru_cache(maxsize=16, ttl=1)
        def compute(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert compute(5) == 10
        assert call_count == 1
        time.sleep(1.1)
        assert compute(5) == 10
        assert call_count == 2

    def test_has_cache_clear(self):
        @CacheUtil.lru_cache(maxsize=16, ttl=60)
        def f(x):
            return x

        assert hasattr(f, "cache_clear")

    def test_has_cache_info(self):
        @CacheUtil.lru_cache(maxsize=16, ttl=60)
        def f(x):
            return x

        assert hasattr(f, "cache_info")

    def test_cache_function(self):
        call_count = 0

        @CacheUtil.cache_function(ttl=60)
        def add(a, b):
            nonlocal call_count
            call_count += 1
            return a + b

        assert add(1, 2) == 3
        assert add(1, 2) == 3
        assert call_count == 1  # only called once

    def test_cache_function_kwargs(self):
        @CacheUtil.cache_function(ttl=60)
        def greet(name="world"):
            return f"hello {name}"

        assert greet(name="test") == "hello test"
        assert greet(name="test") == "hello test"

    def test_memoize(self):
        call_count = 0

        @CacheUtil.memoize(ttl=60)
        def double(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert double(5) == 10
        assert double(5) == 10
        assert call_count == 1

    def test_func_once(self):
        call_count = 0

        @CacheUtil.func_once
        def init():
            nonlocal call_count
            call_count += 1
            return "initialized"

        assert init() == "initialized"
        assert init() == "initialized"
        assert call_count == 1
