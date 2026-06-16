# 版本比较工具 - VersionUtil

## 由来

在依赖管理和功能判断中，经常需要比较版本号大小。`VersionUtil` 提供了语义化版本号的比较功能。

## 方法

```python
from hutool import VersionUtil

# 比较版本号
VersionUtil.compare("1.0.0", "1.0.1")   # -1（前者小于后者）
VersionUtil.compare("1.0.1", "1.0.0")   # 1（前者大于后者）
VersionUtil.compare("1.0.0", "1.0.0")   # 0（相等）

# 判断版本大小
VersionUtil.is_greater("2.0.0", "1.9.9")  # True
VersionUtil.is_lower("1.9.9", "2.0.0")    # True

# 获取主版本号
VersionUtil.get_main_version("1.2.3")      # "1"

# 是否匹配候选版本
VersionUtil.any_match("1.0.0", "1.0.0", "2.0.0")  # True

# 大于等于 / 小于等于
VersionUtil.is_greater_or_equal("1.0.1", "1.0.0")  # True
VersionUtil.is_less_or_equal("0.9.0", "1.0.0")     # True
```
