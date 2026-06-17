# 性能分析工具 - ProfUtil

## 由来

Python 内置的 `cProfile` 模块功能强大但使用繁琐。`ProfUtil` 提供装饰器和上下文管理器两种方式，一行代码即可对函数或代码块进行性能分析。

## ProfileDeco 装饰器（class-based）

`ProfileDeco` 是 class-based 装饰器，支持有括号/无括号、同步/协程：

```python
from hutool import ProfileDeco

# 无括号（默认 cumtime, 10 行）
@ProfileDeco
def compute():
    return sum(range(100000))

# 有括号
@ProfileDeco(sort_by="tottime", limit=5)
def slow_func():
    total = 0
    for i in range(100000):
        total += i
    return total

slow_func()
# 打印 cProfile 统计信息（按自身时间排序，前 5 行）

# async
@ProfileDeco(sort_by="tottime", limit=3)
async def async_compute():
    return sum(range(100000))
```

### 使用ProfUtil调用

`ProfUtil.profile_deco` 和 `ProfUtil.prof_decorator` 仍然可用，指向 `ProfileDeco`：

```python
from hutool import ProfUtil

@ProfUtil.profile_deco(sort_by="tottime", limit=5)
def old_style():
    ...

@ProfUtil.prof_decorator(sort_by="tottime", limit=5)
def also_old():
    ...
```

### 上下文管理器 profile_context

```python
with ProfUtil.profile_context(sort_by="cumtime", limit=10):
    # ... 需要分析的代码 ...
    data = [x ** 2 for x in range(100000)]
# 退出时打印 cProfile 统计信息
```

### 参数说明

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `sort_by` | `"cumtime"` | 排序字段：`"tottime"`（自身时间）、`"cumtime"`（累计时间）、`"calls"` 等 |
| `limit` | `10` | 打印行数 |

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
