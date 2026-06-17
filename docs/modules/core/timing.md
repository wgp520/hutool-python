# 计时工具 - TimingUtil / timethis

## 由来

性能优化的第一步是测量。`timethis` 装饰器和 `TimingUtil.Timer` 精确计时器方便快速定位性能瓶颈。

## TimeThis 装饰器（class-based）

`TimeThis` 是一个 class-based 装饰器，支持有括号/无括号、同步/协程四种用法：

```python
from hutool import TimeThis

# 无括号
@TimeThis
def slow_func():
    import time
    time.sleep(0.1)

slow_func()
# 打印: slow_func :  耗时 0.100...

# 有括号
@TimeThis()
def also_slow():
    time.sleep(0.1)

# async
@TimeThis
async def async_slow():
    await asyncio.sleep(0.1)
```

### 使用TimingUtil调用

`timethis` 和 `TimingUtil.timethis` 仍然可用，指向 `TimeThis` 的实例/类：

```python
from hutool import TimingUtil


@TimingUtil.timethis
def also_old():
    pass
```

## Timer 计时器

`Timer` 是精确计时器，支持手动控制和 `with` 语句两种用法：

```python
from hutool import TimingUtil

# 用法一：手动控制
timer = TimingUtil.Timer()
timer.start()
# ... 某些操作 ...
timer.stop()
print(timer.elapsed)   # 累计耗时（秒）

# 用法二：with 语句
with TimingUtil.Timer() as timer:
    # ... 某些操作 ...
    pass
print(timer.elapsed)
```

### Timer 属性与方法

| 方法/属性 | 说明 |
| --- | --- |
| `start()` | 开始计时（已在运行时抛 `RuntimeError`） |
| `stop()` | 停止计时（未启动时抛 `RuntimeError`） |
| `reset()` | 重置累计时间为零 |
| `elapsed` | 累计耗时（秒，`float`） |
| `running` | 是否正在计时（`bool`） |

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
