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

### 截断

```python
from datetime import date, datetime

# 截断到天/月/年/季度/周/小时
DateUtil.date_trunc("day", datetime(2024, 3, 15, 14, 30))
# datetime(2024, 3, 15, 0, 0)

DateUtil.date_trunc("month", date(2024, 3, 15))
# date(2024, 3, 1)

DateUtil.date_trunc("year", date(2024, 6, 15))
# date(2024, 1, 1)

DateUtil.date_trunc("quarter", date(2024, 5, 15))
# date(2024, 4, 1)

DateUtil.date_trunc("week", date(2024, 3, 15))
# date(2024, 3, 11)（周一）
```

### 时间跨度

```python
# 获取周号
DateUtil.get_week(date(2024, 1, 1))  # (1, 2024)

# 获取月首末日
first, last = DateUtil.get_monthspan(date(2024, 3, 15))
# first=date(2024, 3, 1), last=date(2024, 3, 31)

# 获取周首末日
monday, sunday = DateUtil.get_weekspan(date(2024, 3, 15))
# monday=date(2024, 3, 11), sunday=date(2024, 3, 17)

# 获取季度首末日
first, last = DateUtil.get_quarterspan(date(2024, 5, 15))
# first=date(2024, 4, 1), last=date(2024, 6, 30)

# 获取年首末日
first, last = DateUtil.get_yearspan(date(2024, 6, 15))
# first=date(2024, 1, 1), last=date(2024, 12, 31)
```

### 月份加减

```python
DateUtil.month_add(date(2024, 1, 15), 1)    # date(2024, 2, 15)
DateUtil.month_add(date(2024, 1, 31), 1)    # date(2024, 2, 29)（月末溢出）
DateUtil.month_add(date(2024, 3, 15), -2)   # date(2024, 1, 15)
DateUtil.month_add(date(2024, 11, 15), 3)   # date(2025, 2, 15)（跨年）
```

### RFC 格式

```python
from datetime import datetime

# RFC 3339
DateUtil.rfc3339_date(datetime(2024, 3, 15, 14, 30))  # "2024-03-15T14:30:00+08:00"
DateUtil.rfc3339_date_parse("2024-03-15T14:30:00")     # datetime 对象

# RFC 2616（HTTP 头日期格式）
DateUtil.rfc2616_date(datetime(2024, 3, 15, 14, 30))   # "Fri, 15 Mar 2024 14:30:00 GMT"
DateUtil.rfc2616_date_parse("Fri, 15 Mar 2024 14:30:00 GMT")  # datetime 对象
```

### 通用转换

```python
# 字符串 → date
DateUtil.convert_to_date("2024-03-15")          # date(2024, 3, 15)
DateUtil.convert_to_date(datetime(2024, 3, 15)) # date(2024, 3, 15)

# 字符串 → datetime
DateUtil.convert_to_datetime("2024-03-15 14:30:00")  # datetime 对象
DateUtil.convert_to_datetime("20240315")              # datetime 对象
DateUtil.convert_to_datetime(date(2024, 3, 15))       # datetime 对象
```

### 实用方法

```python
import time

# 根据生日计算年龄
DateUtil.age_by_birthday("1990-06-15")          # 34
DateUtil.age_by_birthday(date(1990, 6, 15))     # 34

# 判断同月/同周
DateUtil.is_same_month(date(2024, 3, 1), date(2024, 3, 31))  # True
DateUtil.is_same_week(date(2024, 1, 15), date(2024, 1, 17))  # True

# 相对时间
DateUtil.time_ago(time.time())           # "刚刚"
DateUtil.time_ago(time.time() - 300)     # "5分钟前"
DateUtil.time_ago(time.time() - 7200)    # "2小时前"
DateUtil.time_ago(time.time() - 86400*3) # "3天前"

# ISO 时间戳
DateUtil.iso_timestamp()  # "2024-01-01T12:00:00.000Z"
```

### 判断

```python
from datetime import date

# 是否月末最后一天
DateUtil.is_last_day_of_month(date(2024, 2, 29))  # True（闰年）
DateUtil.is_last_day_of_month(date(2024, 3, 15))  # False

# 是否在有效期外
DateUtil.is_expired(date(2025, 1, 1), date(2024, 1, 1), date(2024, 12, 31))  # True

# 两个时间段是否重叠
DateUtil.is_overlap(date(2024, 1, 1), date(2024, 6, 30),
                    date(2024, 3, 1), date(2024, 12, 31))  # True

# 日期是否在范围内
DateUtil.is_between(date(2024, 3, 15), date(2024, 1, 1), date(2024, 12, 31))  # True
```

### 日期属性

```python
from datetime import date

# 年内第几天
DateUtil.day_of_year(date(2024, 3, 1))   # 61

# 当月天数
DateUtil.length_of_month(date(2024, 2, 1))  # 29（闰年）
DateUtil.length_of_month(date(2023, 2, 1))  # 28

# 当年天数
DateUtil.length_of_year(date(2024, 1, 1))   # 366（闰年）

# 毫秒部分
DateUtil.millisecond(DateUtil.parse("2024-01-01 12:00:00.123"))  # 123

# 星座
DateUtil.get_zodiac(3, 21)   # "白羊座"

# 生肖
DateUtil.get_chinese_zodiac(2024)  # "龙"
```

### 日期比较与时区

```python
from datetime import date

# null-safe 日期比较
DateUtil.compare(date(2024, 1, 1), date(2024, 1, 2))   # -1
DateUtil.compare(date(2024, 1, 2), date(2024, 1, 1))   #  1
DateUtil.compare(None, date(2024, 1, 1))                # -1

# 时区转换
dt = DateUtil.parse("2024-03-15 12:00:00")
DateUtil.convert_timezone(dt, "Asia/Shanghai", "America/New_York")

# 中文日期格式
DateUtil.format_chinese_date(date(2024, 3, 15))  # "2024年03月15日"
```
