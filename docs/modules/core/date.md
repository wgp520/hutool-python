# 日期时间工具 - DateUtil / DateTime

## 由来

Java 中的日期操作一直为人诟病，Hutool 的 `DateUtil` 极大简化了日期操作。Python 版基于 `pendulum` 库实现，保留了 Hutool 的 API 风格。

## DateTime

`DateTime` 是对 `pendulum.DateTime` 的封装，支持所有 pendulum 的日期操作：

```python
from hutool import DateUtil, DateTime

dt = DateUtil.date()  # 获取当前 DateTime
```

### 工厂方法

```python
from hutool import DateTime

# 从年月日创建
dt = DateTime.of_date(2024, 6, 15)

# 从年月日时分秒创建
dt = DateTime.of_datetime(2024, 6, 15, 14, 30, 45)

# 从格式字符串解析
dt = DateTime.of_pattern("2024-06-15 14:30:45", "yyyy-MM-dd HH:mm:ss")

# UTC 当前时间
dt = DateTime.now_utc()

# 从时间戳创建
dt = DateTime.of_epoch(1700000000000)       # 毫秒
dt = DateTime.of_epoch(1700000000, False)   # 秒
```

### 查询方法

```python
dt = DateTime.of_date(2024, 1, 13)

dt.is_weekend()          # True（周六）
dt.is_am()               # True（hour < 12）
dt.is_pm()               # False
dt.is_past()             # True（已过去）
dt.is_future()           # False
dt.is_leap_year()        # True（2024 闰年）
dt.is_last_day_of_month() # False

# 比较
dt1 = DateTime.of_date(2024, 1, 1)
dt2 = DateTime.of_date(2024, 6, 1)
dt1.is_before(dt2)       # True
dt2.is_after(dt1)        # True
dt1.is_between(dt1, dt2) # True

# 属性
dt = DateTime.of_date(2024, 2, 1)
dt.length_of_month()     # 29
dt.length_of_year()      # 366
```

### 偏移方法

```python
dt = DateTime.of_date(2024, 1, 15)

dt.offset_day(1)       # 2024-01-16
dt.offset_week(2)      # 2024-01-29
dt.offset_month(-1)    # 2023-12-15
dt.offset_year(1)      # 2025-01-15
```

### 开始/结束时间（实例方法）

```python
dt = DateTime.of_datetime(2024, 6, 15, 14, 30, 45)

dt.begin_of_hour()     # 14:00:00
dt.end_of_hour()       # 14:59:59
dt.begin_of_minute()   # 14:30:00
dt.end_of_minute()     # 14:30:59
dt.begin_of_second()   # 14:30:45
dt.end_of_second()     # 14:30:45.999999
```

### 格式化与时区

```python
dt = DateTime.of_datetime(2024, 6, 15, 14, 30, 45)

dt.format("YYYY-MM-DD")         # "2024-06-15"
dt.to_local_datetime_str()      # "2024-06-15 14:30:45"

# 时区转换
dt_utc = DateTime.now_utc()
dt_sh = dt_utc.with_timezone("Asia/Shanghai")
dt_sh.timezone_name()           # "Asia/Shanghai"
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

# getDaySpan — 日跨度
DateUtil.get_day_span(date(2024, 1, 1), date(2024, 1, 31))  # 30

# getMonthSpan — 月跨度
DateUtil.get_month_span(date(2024, 1, 1), date(2024, 6, 1))  # 5
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

### 当前时间快捷方法

```python
DateUtil.this_year()            # 2024
DateUtil.this_month()           # 3
DateUtil.this_week_of_year()    # 12
DateUtil.this_week_of_month()   # 3
DateUtil.this_day_of_month()    # 15
DateUtil.this_day_of_week()     # 5（周五）
DateUtil.this_hour()            # 14
DateUtil.this_minute()          # 30
DateUtil.this_second()          # 45
DateUtil.this_millisecond()     # 123
```

### 时间转换

```python
# "HH:mm:ss" → 秒数
DateUtil.time_to_second("01:00:00")  # 3600
DateUtil.time_to_second("00:01:30")  # 90

# 秒数 → "HH:mm:ss"
DateUtil.second_to_time(3600)   # "01:00:00"
DateUtil.second_to_time(90)     # "00:01:30"
```

### 年龄计算

```python
# 计算到当前时间的年龄
DateUtil.age_of_now("1990-01-01")  # 34

# 计算两个日期间的年龄
from datetime import date
DateUtil.age(date(1990, 6, 15), date(2024, 6, 14))  # 33
DateUtil.age(date(1990, 6, 15), date(2024, 6, 15))  # 34
```

### 截断与舍入

```python
from datetime import datetime

dt = datetime(2024, 6, 15, 14, 30, 45)

# 截断（向下取整）
DateUtil.truncate(dt, "year")    # 2024-01-01 00:00:00
DateUtil.truncate(dt, "month")   # 2024-06-01 00:00:00
DateUtil.truncate(dt, "day")     # 2024-06-15 00:00:00
DateUtil.truncate(dt, "hour")    # 2024-06-15 14:00:00
DateUtil.truncate(dt, "minute")  # 2024-06-15 14:30:00
DateUtil.truncate(dt, "second")  # 2024-06-15 14:30:45

# 四舍五入
DateUtil.round(datetime(2024, 6, 15, 12, 0, 0), "day")  # 2024-06-16（>= 12:00 进位）
DateUtil.round(datetime(2024, 6, 15, 11, 59, 0), "day") # 2024-06-15（< 12:00 截断）

# 天花板舍入（向上取整）
DateUtil.ceiling(dt, "day")    # 2024-06-16 00:00:00
DateUtil.ceiling(dt, "hour")   # 2024-06-15 15:00:00
```

### 小时/分钟/秒 开始与结束

```python
dt = DateUtil.parse("2024-06-15 14:30:45")

DateUtil.begin_of_hour(dt)    # 2024-06-15 14:00:00
DateUtil.end_of_hour(dt)      # 2024-06-15 14:59:59
DateUtil.begin_of_minute(dt)  # 2024-06-15 14:30:00
DateUtil.end_of_minute(dt)    # 2024-06-15 14:30:59
DateUtil.begin_of_second(dt)  # 2024-06-15 14:30:45
DateUtil.end_of_second(dt)    # 2024-06-15 14:30:45.999999
```

### 通用偏移

```python
from datetime import datetime

dt = datetime(2024, 1, 31)

DateUtil.offset(dt, "day", 5)      # 2024-02-05
DateUtil.offset(dt, "month", 1)    # 2024-02-29（月末溢出自动处理）
DateUtil.offset(dt, "year", -1)    # 2023-01-31
DateUtil.offset(dt, "hour", 3)     # 加3小时
DateUtil.offset(dt, "week", 2)     # 加2周
```

### 日期范围

```python
from datetime import datetime

# 生成日期范围（不含结束日期）
DateUtil.range(datetime(2024, 1, 1), datetime(2024, 1, 4))
# [datetime(2024,1,1), datetime(2024,1,2), datetime(2024,1,3)]

# 生成日期范围（含结束日期）
DateUtil.range_to_list(datetime(2024, 1, 1), datetime(2024, 1, 3))
# [datetime(2024,1,1), datetime(2024,1,2), datetime(2024,1,3)]

# 按周步进
DateUtil.range(datetime(2024, 1, 1), datetime(2024, 1, 22), "week")
```

### 格式化间隔

```python
DateUtil.format_between_ms(3661001)
# "1小时1分1秒1毫秒"

DateUtil.format_between_ms(90000000, level="day")
# "1天"

DateUtil.format_between_ms(7200000, level="hour")
# "2小时"

DateUtil.format_between_ms(5000, level="second")
# "5秒"
```

### 本地格式化与解析

```python
from datetime import datetime

# 格式化为 "YYYY-MM-DD HH:mm:ss"
DateUtil.format_local_datetime(datetime(2024, 6, 15, 14, 30, 45))
# "2024-06-15 14:30:45"

# 解析 "YYYY-MM-DD HH:mm:ss"
DateUtil.parse_local_datetime("2024-06-15 14:30:45")

# 解析 UTC 时间
DateUtil.parse_utc("2024-01-15T10:30:00Z")

# 解析 RFC 2822 日期
DateUtil.parse_rfc2822("Mon, 15 Jan 2024 10:30:00 +0000")
```

### 纳秒转换

```python
DateUtil.nanos_to_millis(1_000_000)     # 1.0
DateUtil.nanos_to_seconds(1_000_000_000) # 1.0
```

### 秒表计时器

```python
sw = DateUtil.create_stop_watch("性能测试")

sw.start("步骤1")
# ... 执行操作 ...
sw.stop()

sw.start("步骤2")
# ... 执行操作 ...
sw.stop()

print(sw.pretty_print())
# StopWatch '性能测试': running time = 1234.56 ms
# ---------------------------------------------
# ms         %     Task name
# ---------------------------------------------
#     1000.00  81.0%  步骤1
#      234.56  19.0%  步骤2
```

### 范围判断

```python
from datetime import datetime

# 判断日期是否在范围内（含边界）
DateUtil.range_contains(
    datetime(2024, 1, 1), datetime(2024, 12, 31),
    datetime(2024, 6, 15)
)  # True

# 年份+季度
DateUtil.year_and_quarter(datetime(2024, 3, 15))  # "20241"
DateUtil.year_and_quarter(datetime(2024, 9, 15))  # "20243"
```

### AM/PM 判断

```python
from datetime import datetime

DateUtil.is_am(datetime(2024, 6, 15, 10, 0))  # True
DateUtil.is_pm(datetime(2024, 6, 15, 14, 0))  # True
```

### 月内周次与月末日

```python
from datetime import date

# weekOfMonth — 月内第几周
DateUtil.week_of_month(date(2024, 6, 15))  # 3

# getLastDayOfMonth — 月末日
DateUtil.get_last_day_of_month(date(2024, 2, 1))   # 29（闰年）
DateUtil.get_last_day_of_month(date(2023, 2, 1))   # 28
DateUtil.get_last_day_of_month(date(2024, 1, 15))  # 31
```

### 毫秒偏移

```python
from datetime import datetime

dt = datetime(2024, 6, 15, 12, 0, 0)
DateUtil.offset_millisecond(dt, 1500)  # 12:00:01.500
```

### 解析扩展

```python
# 解析 CST 格式
DateUtil.parse_cst("Mon Jun 16 12:00:00 CST 2026")

# 解析 UTC 格式
DateUtil.parse_utc("2024-01-15T10:30:00Z")

# 解析 RFC 2822 格式
DateUtil.parse_rfc2822("Mon, 15 Jan 2024 10:30:00 +0000")

# 解析今日时间字符串
DateUtil.parse_time_today("12:30:00")  # 今天 12:30:00
```

### 日期范围遍历

```python
from datetime import date

# 日期范围遍历（生成器）
for d in DateUtil.range_func(date(2024, 1, 1), date(2024, 1, 4)):
    print(d)
# 2024-01-01, 2024-01-02, 2024-01-03

# 日期范围消费（回调）
DateUtil.range_consume(date(2024, 1, 1), date(2024, 1, 4), lambda d: print(d))
```

### 计时与转换

```python
import time

# 计时（返回毫秒）
start = time.time()
# ... 执行操作 ...
ms = DateUtil.spend_nt(start)  # 消耗毫秒数

# 转为秒级时间戳
DateUtil.to_int_second(date(2024, 1, 1))  # 1704067200
```

### HTTP 日期格式

```python
from datetime import datetime

DateUtil.format_http_date(datetime(2024, 3, 15, 14, 30, 0))
# "Fri, 15 Mar 2024 14:30:00 GMT"
```

### 分组聚合

```python
from datetime import date
from hutool import DateUtil

# 按年分组
dates = [date(2023, 1, 1), date(2023, 6, 15), date(2024, 3, 1)]
DateUtil.group_by_year(dates)
# {2023: [date(2023, 1, 1), date(2023, 6, 15)], 2024: [date(2024, 3, 1)]}

# 按月分组
DateUtil.group_by_month(dates)

# 按季度分组
DateUtil.group_by_quarter(dates)

# 按周分组
DateUtil.group_by_week(dates)

# 按日分组
DateUtil.group_by_day(dates)

# 按小时分组
DateUtil.group_by_hour([datetime(2024, 1, 1, 10, 0), datetime(2024, 1, 1, 10, 30)])
```

### 季度操作

```python
from datetime import date

# getTertial — 获取半年（上/下半年）
DateUtil.get_tertial(date(2024, 3, 15))  # 1（上半年）
DateUtil.get_tertial(date(2024, 9, 15))  # 2（下半年）

# tertialAdd — 半年加减
DateUtil.tertial_add(date(2024, 3, 15), 1)  # 2024-09-15
```

### 便捷方法

```python
from datetime import date

# 今天/昨天/明天
DateUtil.today_str()       # "2024-06-15"
DateUtil.yesterday_str()   # "2024-06-14"
DateUtil.tomorrow_str()    # "2024-06-16"

# 周首末日
DateUtil.week_start(date(2024, 6, 15))  # date(2024, 6, 10)（周一）
DateUtil.week_end(date(2024, 6, 15))    # date(2024, 6, 16)（周日）

# 日首末时间
DateUtil.day_start(date(2024, 6, 15))   # datetime(2024, 6, 15, 0, 0, 0)
DateUtil.day_end(date(2024, 6, 15))     # datetime(2024, 6, 15, 23, 59, 59)

# 月首末日
DateUtil.month_start(date(2024, 6, 15)) # date(2024, 6, 1)
DateUtil.month_end(date(2024, 6, 15))   # date(2024, 6, 30)
```

### 格式化便捷方法

```python
from datetime import datetime, date

# format_date — 仅日期
DateUtil.format_date(date(2024, 6, 15))        # "2024-06-15"

# format_datetime — 日期时间
DateUtil.format_datetime(datetime(2024, 6, 15, 14, 30, 0))
# "2024-06-15 14:30:00"

# format_time — 仅时间
DateUtil.format_time(datetime(2024, 6, 15, 14, 30, 45))
# "14:30:45"
```

### SimpleFormat 工厂

```python
# newSimpleFormat — 创建格式化函数
fmt = DateUtil.new_simple_format("yyyy/MM/dd")
from datetime import date
fmt(date(2024, 6, 15))  # "2024/06/15"
```
