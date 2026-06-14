# 缓存工具

## 概述

Hutool-cache 提供了多种缓存策略实现，适用于小型项目的简单缓存需求。

## CacheUtil 工厂方法

```python
from hutool import CacheUtil

cache = CacheUtil.new_lru_cache(capacity=100)
cache = CacheUtil.new_fifo_cache(capacity=100)
cache = CacheUtil.new_lfu_cache(capacity=100)
cache = CacheUtil.new_timed_cache(timeout=60)  # 60秒过期
```

## FIFOCache - 先进先出

FIFO (First In First Out) 策略。元素不断加入缓存直到缓存满，缓存满时先入的缓存被移除。

```python
from hutool import FIFOCache

cache = FIFOCache(capacity=3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)
cache.put("d", 4)  # "a" 被移除

cache.get("a")     # None
cache.get("d")     # 4
```

**优点**：简单快速
**缺点**：不灵活，不能保证常用对象被保留

## LFUCache - 最少使用

LFU (Least Frequently Used) 策略。根据使用次数判定，缓存满时清除最少访问的对象。

```python
from hutool import LFUCache

cache = LFUCache(capacity=3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)

cache.get("a")     # 1（a 的访问计数增加）
cache.get("a")     # 1
cache.put("d", 4)  # "b" 被移除（访问次数最少）
```

## LRUCache - 最近最久未使用

LRU (Least Recently Used) 策略。根据使用时间判定，最久未被使用的对象将被移除。

```python
from hutool import LRUCache

cache = LRUCache(capacity=3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)

cache.get("a")     # 1（a 被访问，移到最前）
cache.put("d", 4)  # "b" 被移除（最久未使用）
```

**优点**：简单快速，常用对象不容易被移除
**缺点**：缓存满时新对象不能被快速访问

## TimedCache - 定时缓存

对缓存对象定义过期时间，超过过期时间自动清理。无容量限制。

```python
from hutool import TimedCache

cache = TimedCache(timeout=5)  # 5秒过期
cache.put("key", "value")

cache.get("key")    # "value"

# 5秒后...
cache.get("key")    # None（已过期）

# 启动定时清理
cache.schedule_prune(delay_seconds=1)  # 每1秒清理一次过期缓存
```

## 通用方法

所有缓存类型都支持以下方法：

```python
cache.put("key", "value")
cache.get("key")              # 获取值
cache.get("key", "default")   # 获取值，不存在返回默认值
cache.remove("key")           # 移除
cache.size()                  # 当前大小
cache.capacity()              # 容量
cache.clear()                 # 清空
cache.is_full()               # 是否已满
```
