# 工作日工具 - WorkdayUtil

## 由来

在业务系统中，工作日计算（如发货时效、审批周期）是常见需求。`WorkdayUtil` 提供工作日判断、工作日数计算、加减工作日等功能，默认使用中国法定节假日配置，支持自定义假日列表。

## 方法

### 配置假日

```python
from hutool import WorkdayUtil
from datetime import date

# 默认使用中国法定假日（2024/2025 年内置数据）
holidays = WorkdayUtil.holidays(2024)

# 自定义假日列表
WorkdayUtil.set_custom_holidays([
    date(2024, 1, 1),
    date(2024, 2, 10),
    date(2024, 2, 11),
])

# 恢复默认
WorkdayUtil.set_custom_holidays(None)
```

### 工作日判断

```python
from datetime import date

WorkdayUtil.is_workday(date(2024, 1, 2))   # True（周二，非假日）
WorkdayUtil.is_workday(date(2024, 1, 1))   # False（元旦）
WorkdayUtil.is_workday(date(2024, 1, 6))   # False（周六）
```

### 工作日导航

```python
# 下一个工作日
WorkdayUtil.next_workday(date(2024, 1, 5))   # date(2024, 1, 8)（跳过周末）

# 上一个工作日
WorkdayUtil.previous_workday(date(2024, 1, 8))  # date(2024, 1, 5)
```

### 工作日数计算

```python
# 两个日期之间的工作日数（含首末日）
WorkdayUtil.workdays(date(2024, 1, 1), date(2024, 1, 5))  # 3

# 日期加减 N 个工作日
WorkdayUtil.add_workdays(date(2024, 1, 1), 5)   # date(2024, 1, 8)
WorkdayUtil.add_workdays(date(2024, 1, 8), -3)  # date(2024, 1, 3)
```

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
