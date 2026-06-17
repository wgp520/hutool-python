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

# setCronSetting — 加载 Cron 配置文件
CronUtil.set_cron_setting("/path/to/cron.properties")

# updatePattern — 更新 Cron 表达式
CronUtil.update_pattern("0 */10 * * *")  # 改为每 10 分钟
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

```text
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
| ------ | ---- |
| `0 */5 * * *` | 每5分钟 |
| `0 9 * * *` | 每天9点 |
| `0 9 * * 1-5` | 工作日9点 |
| `0 0 1 * *` | 每月1号0点 |
| `*/10 * * * *` | 每10秒（特殊支持） |

## CronValidator

Quartz 风格 6-7 字段 Cron 表达式校验：

```python
from hutool import CronValidator

# 整体校验
CronValidator.validate("0 0 12 * * ?")       # True — 每天中午
CronValidator.validate("0 0/5 14 * * ?")      # True — 14:00 起每5分钟
CronValidator.validate("0 15 10 ? * 6L")      # True — 每月最后一个周五
CronValidator.validate("0 15 10 ? * 6#3")     # True — 第三个周五

# 便捷方法
CronValidator.is_valid("0 0 12 * * ?")        # True
CronValidator.is_valid(None)                  # False
CronValidator.is_valid("")                    # False

# 单字段校验
CronValidator.validate_second_or_minute("0/5")  # True
CronValidator.validate_hour("9,12,18")          # True
CronValidator.validate_day("15W")               # True — 最近工作日
CronValidator.validate_week("6#3")              # True — 第三个周五
```

### 字段格式

```text
┌───────────── 秒 (0-59)
│ ┌───────────── 分 (0-59)
│ │ ┌───────────── 时 (0-23)
│ │ │ ┌───────────── 日 (1-31, ? L W)
│ │ │ │ ┌───────────── 月 (1-12)
│ │ │ │ │ ┌───────────── 周 (1-7, ? L #)
│ │ │ │ │ │ ┌───────────── 年 (可选, 1970-2099)
│ │ │ │ │ │ │
* * * * * * *
```

### 特殊字符

| 字符 | 说明 | 示例 |
| ---- | ---- | ---- |
| `*` | 匹配任意值 | `* * * * * ?` |
| `?` | 不指定（日/周字段） | `0 0 12 * * ?` |
| `-` | 范围 | `1-5` |
| `,` | 枚举 | `1,3,5` |
| `/` | 步长 | `0/5` |
| `L` | 最后 | `L`（月末）、`6L`（最后一个周五） |
| `W` | 最近工作日 | `15W` |
| `#` | 第几个星期几 | `6#3`（第三个周五） |
