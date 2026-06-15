# 计时工具 - TimingUtil / timethis

## 由来

性能优化的第一步是测量。`timethis` 装饰器和 `TimingUtil.Timer` 精确计时器方便快速定位性能瓶颈。

## timethis 装饰器

`timethis` 是一个顶层装饰器，可以直接通过 `@timethis` 使用：

```python
from hutool import timethis

@timethis
def slow_func():
    import time
    time.sleep(0.1)

slow_func()
# 打印: slow_func :  耗时 0.100...
```

也可以通过 `TimingUtil.timethis` 调用（向后兼容）：

```python
from hutool import TimingUtil

@TimingUtil.timethis
def another_func():
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
|---|---|
| `start()` | 开始计时（已在运行时抛 `RuntimeError`） |
| `stop()` | 停止计时（未启动时抛 `RuntimeError`） |
| `reset()` | 重置累计时间为零 |
| `elapsed` | 累计耗时（秒，`float`） |
| `running` | 是否正在计时（`bool`） |

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
