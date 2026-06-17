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

## 缓存装饰器

所有缓存装饰器为 class-based 实现，支持有括号/无括号、同步/协程。
详见 {doc}`装饰器文档 </modules/core/decorators>`。

### cache_function — 函数缓存

基于字典的函数缓存装饰器，支持 TTL 过期：

```python
from hutool import CacheFunction, CacheUtil

# class-based（推荐）
@CacheFunction(ttl=60)
def expensive(x):
    return x * 2

# 或者
@CacheUtil.cache_function(ttl=60)
def also_expensive(x):
    return x * 2

expensive(5)   # 计算并缓存
expensive(5)   # 直接返回缓存值

# 访问内部缓存
expensive.cache   # {(5,): (10, 1687000000.0)}

# async
@CacheFunction(ttl=60)
async def async_expensive(x):
    return x * 2
```

### lru_cache — 带 TTL 的 LRU 缓存

结合 `functools.lru_cache` 的 LRU 淘汰策略与 TTL 过期机制：

```python
from hutool import TtlLruCache, CacheUtil

# class-based（推荐）
@TtlLruCache(maxsize=128, ttl=300)
def compute(x):
    return x ** 2

# 或者
@CacheUtil.lru_cache(maxsize=128, ttl=300)
def also_compute(x):
    return x ** 2

compute(10)   # 计算并缓存
compute(10)   # 直接返回缓存值（300 秒内）

compute.cache_clear()   # 清空缓存
compute.cache_info()    # 查看缓存命中信息
```

### memoize — 记忆化装饰器

与 `cache_function` 相同，语义上用于记忆化重复计算：

```python
from hutool import Memoize, CacheUtil

@Memoize(ttl=600)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 或者
@CacheUtil.memoize(ttl=600)
def old_fibonacci(n):
    ...
```

### func_once — 单次执行

函数只执行一次，后续调用直接返回首次结果：

```python
from hutool import FuncOnce, CacheUtil

# class-based（推荐）
@FuncOnce
def init():
    print("初始化...")
    return "initialized"

# 或者
@CacheUtil.func_once
def old_init():
    return "initialized"

init()   # 打印 "初始化..."，返回 "initialized"
init()   # 直接返回 "initialized"（不再打印）
```
