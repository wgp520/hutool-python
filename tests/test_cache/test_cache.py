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
