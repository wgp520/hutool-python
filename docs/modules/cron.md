# 定时任务 - CronUtil / CronPattern

## 由来

定时任务是后端开发的常见需求。`CronUtil` 提供了基于 Cron 表达式的定时任务调度功能。

## CronUtil

```python
from hutool import CronUtil

# 注册定时任务
CronUtil.schedule("0 */5 * * *", lambda: print("每5分钟执行一次"))
CronUtil.schedule("0 9 * * 1-5", lambda: print("工作日9点执行"))

# 固定频率执行
CronUtil.schedule_at_fixed_rate(lambda: print("每10秒"), period_seconds=10)

# 停止/重启
CronUtil.stop()
CronUtil.restart()
```

## CronPattern

Cron 表达式解析和匹配：

```python
from hutool import CronPattern

# 创建 Cron 表达式
pattern = CronPattern("0 9 * * 1-5")  # 工作日9点

# 判断当前时间是否匹配
from datetime import datetime
pattern.match(datetime.now())

# 获取下一次匹配时间
next_time = pattern.next_match_time()
```

## Cron 表达式格式

```
┌───────────── 分 (0-59)
│ ┌───────────── 时 (0-23)
│ │ ┌───────────── 日 (1-31)
│ │ │ ┌───────────── 月 (1-12)
│ │ │ │ ┌───────────── 周 (0-7, 0和7都是周日)
│ │ │ │ │
* * * * *
```

### 常用表达式

| 表达式 | 含义 |
|--------|------|
| `0 */5 * * *` | 每5分钟 |
| `0 9 * * *` | 每天9点 |
| `0 9 * * 1-5` | 工作日9点 |
| `0 0 1 * *` | 每月1号0点 |
| `*/10 * * * *` | 每10秒（特殊支持） |
