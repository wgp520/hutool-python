# 日期时间工具 - DateUtil / DateTime

## 由来

Java 中的日期操作一直为人诟病，Hutool 的 `DateUtil` 极大简化了日期操作。Python 版基于 `pendulum` 库实现，保留了 Hutool 的 API 风格。

## DateTime

`DateTime` 是对 `pendulum.DateTime` 的封装，支持所有 pendulum 的日期操作：

```python
from hutool import DateUtil, DateTime

dt = DateUtil.date()  # 获取当前 DateTime
```

## DateUtil

### 获取当前时间

```python
DateUtil.now()                  # "2024-01-01 12:00:00"
DateUtil.today()                # "2024-01-01"
DateUtil.current()              # 毫秒时间戳
DateUtil.current_seconds()      # 秒时间戳
```

### 解析

```python
dt = DateUtil.parse("2024-01-01")
dt = DateUtil.parse("2024-01-01 12:00:00")
dt = DateUtil.parse("20240101", "yyyyMMdd")
dt = DateUtil.parse_iso8601("2024-01-01T12:00:00Z")
```

### 格式化

```python
dt = DateUtil.parse("2024-01-01 12:30:45")
DateUtil.format(dt, "yyyy/MM/dd")          # "2024/01/01"
DateUtil.format_date(dt)                   # "2024-01-01"
DateUtil.format_time(dt)                   # "12:30:45"
DateUtil.format_date_time(dt)              # "2024-01-01 12:30:45"
```

### 日期部分

```python
dt = DateUtil.parse("2024-03-15 14:30:00")
DateUtil.year(dt)           # 2024
DateUtil.month(dt)          # 3
DateUtil.day_of_month(dt)   # 15
DateUtil.hour(dt)           # 14
DateUtil.minute(dt)         # 30
DateUtil.second(dt)         # 0
DateUtil.day_of_week(dt)    # 5（周五）
DateUtil.quarter(dt)        # 1（第一季度）
DateUtil.is_weekend(dt)     # False
```

### 日期偏移

```python
dt = DateUtil.parse("2024-01-15")

DateUtil.offset_day(dt, 7)      # 2024-01-22
DateUtil.offset_month(dt, 2)    # 2024-03-15
DateUtil.offset_year(dt, 1)     # 2025-01-15
DateUtil.offset_hour(dt, 3)     # 加3小时

DateUtil.tomorrow()              # 明天
DateUtil.yesterday()             # 昨天
DateUtil.next_week()             # 下周
DateUtil.last_month()            # 上月
```

### 开始/结束时间

```python
dt = DateUtil.parse("2024-03-15 14:30:00")

DateUtil.begin_of_day(dt)       # 2024-03-15 00:00:00
DateUtil.end_of_day(dt)         # 2024-03-15 23:59:59
DateUtil.begin_of_month(dt)     # 2024-03-01 00:00:00
DateUtil.end_of_month(dt)       # 2024-03-31 23:59:59
DateUtil.begin_of_year(dt)      # 2024-01-01 00:00:00
DateUtil.end_of_year(dt)        # 2024-12-31 23:59:59
```

### 时间差

```python
start = DateUtil.parse("2024-01-01")
end = DateUtil.parse("2024-03-15")

DateUtil.between_day(start, end)    # 74
DateUtil.between_month(start, end)  # 2
DateUtil.between_year(start, end)   # 0
DateUtil.format_between(start, end) # "2个月14天"
```

### 比较

```python
dt1 = DateUtil.parse("2024-01-01")
dt2 = DateUtil.parse("2024-01-01 12:00:00")

DateUtil.is_same_day(dt1, dt2)      # True
DateUtil.is_same_time(dt1, dt2)     # False
DateUtil.is_leap_year(2024)         # True
```
