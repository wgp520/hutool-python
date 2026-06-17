# 装饰器 - class-based 装饰器

## 由来

Hutool-Python 所有装饰器使用 class-based 实现，统一支持 **有括号/无括号**、**同步/协程** 四种组合，同时支持 Util 类的调用方式。

## TimeThis — 函数计时

统计函数执行耗时并打印到标准输出。

```python
from hutool import TimeThis

# 无括号
@TimeThis
def slow():
    time.sleep(0.1)

# 有括号
@TimeThis()
def also_slow():
    time.sleep(0.1)

# async 也适用
@TimeThis
async def async_slow():
    await asyncio.sleep(0.1)
```

Util方式调用：

```python
from hutool import timethis, TimingUtil

@timethis
def old_style():
    pass

@TimingUtil.timethis
def also_old():
    pass
```

## ProfileDeco — cProfile 性能分析

每次调用被装饰函数时自动运行 cProfile 并打印统计信息。

```python
from hutool import ProfileDeco

# 无括号（默认 cumtime, 10 行）
@ProfileDeco
def compute():
    return sum(range(100000))

# 有括号
@ProfileDeco(sort_by="tottime", limit=5)
def slow_func():
    ...

# async
@ProfileDeco(sort_by="tottime", limit=3)
async def async_compute():
    ...
```

Util方式调用：

```python
from hutool import ProfUtil

@ProfUtil.profile_deco(sort_by="tottime", limit=5)
def old_style():
    ...

@ProfUtil.prof_decorator(sort_by="tottime", limit=5)
def also_old():
    ...
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `sort_by` | `"cumtime"` | 排序字段 |
| `limit` | `10` | 打印行数 |

## CacheFunction — 函数缓存

基于字典的函数缓存装饰器，支持 TTL 过期。

```python
from hutool import CacheFunction

# 无括号（默认 TTL 300 秒）
@CacheFunction
def expensive(x):
    return x * 2

# 有括号
@CacheFunction(ttl=60)
def compute(x):
    return x * 2

# async
@CacheFunction(ttl=60)
async def async_fetch(url):
    return await aio_get(url)

# 访问内部缓存
compute.cache   # dict
```

Util方式调用：

```python
from hutool import CacheUtil

@CacheUtil.cache_function(ttl=60)
def old_style(x):
    return x * 2
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `ttl` | `300` | 缓存过期时间（秒） |

## Memoize — 记忆化装饰器

`CacheFunction` 的子类，语义上用于记忆化重复计算。默认 TTL 为 600 秒。

```python
from hutool import Memoize

@Memoize(ttl=600)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

Util方式调用：

```python
from hutool import CacheUtil

@CacheUtil.memoize(ttl=600)
def old_style(n):
    ...
```

## FuncOnce — 单次执行

函数只执行一次，后续调用直接返回缓存值。

```python
from hutool import FuncOnce

# 无括号
@FuncOnce
def init():
    return expensive_setup()

# 有括号
@FuncOnce()
def also_init():
    return expensive_setup()

# async
@FuncOnce
async def async_init():
    return await aio_setup()

init()   # 执行
init()   # 直接返回缓存结果
```

Util方式调用：

```python
from hutool import CacheUtil

@CacheUtil.func_once
def old_style():
    return "done"
```

## TtlLruCache — 带 TTL 的 LRU 缓存

结合 `functools.lru_cache` 的 LRU 淘汰策略与 TTL 过期机制。

```python
from hutool import TtlLruCache

# 无括号（默认 maxsize=128, ttl=300）
@TtlLruCache
def expensive(x):
    return x * 2

# 有括号
@TtlLruCache(maxsize=64, ttl=120)
def compute(x):
    return x * 2

# async
@TtlLruCache(ttl=60)
async def async_fetch(url):
    return await aio_get(url)

compute.cache_clear()   # 清空缓存
compute.cache_info()    # 查看命中信息
```

Util方式调用：

```python
from hutool import CacheUtil

@CacheUtil.lru_cache(maxsize=64, ttl=120)
def old_style(x):
    return x * 2
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `maxsize` | `128` | 最大缓存条目数 |
| `ttl` | `300` | 缓存过期时间（秒） |

## NoneOnException — 异常返回 None

函数抛异常时返回 `None`，而不是向上传播。

```python
from hutool import NoneOnException

# 无括号
@NoneOnException
def risky():
    raise ValueError("oops")

assert risky() is None

# 有括号
@NoneOnException()
def also_risky():
    raise RuntimeError("boom")

# async
@NoneOnException
async def async_risky():
    raise ValueError("oops")

assert await async_risky() is None
```

Util方式调用：

```python
from hutool import ObjectUtil

@ObjectUtil.none_on_exception
def old_style():
    raise ValueError()
```

---

## 统一设计模式

所有 class-based 装饰器均遵循同一模式：

1. **无括号** `@ClassName` — `__init__` 收到函数，直接包装
2. **有括号** `@ClassName(args)` — `__init__` 收到 `None`，`__call__` 收到函数后创建新实例
3. **async 检测** — 通过 `asyncio.iscoroutinefunction()` 自动选择同步/异步路径
4. **向后兼容** — 旧 Util 类的静态方法别名指向新类

```{note}
上下文管理器 `profile_context` / `prof_context` 不是装饰器，保持原有实现不变。
```
