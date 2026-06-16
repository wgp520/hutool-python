# 社会信用代码工具 - CreditCodeUtil

## 由来

统一社会信用代码是中国企业的唯一标识码，共 18 位，有严格的编码规则和校验算法。`CreditCodeUtil` 提供信用代码的校验功能。

## 统一社会信用代码结构

| 位置 | 长度 | 含义 |
| ---- | ---- | ---- |
| 1 | 1 | 登记管理部门代码 |
| 2 | 1 | 机构类别代码 |
| 3-8 | 6 | 登记管理机关行政区划码 |
| 9-17 | 9 | 主体标识码（组织机构代码） |
| 18 | 1 | 校验码 |

## 方法

```python
from hutool import CreditCodeUtil

# 校验统一社会信用代码
CreditCodeUtil.is_valid_credit_code("91110108MA004GHJ0K")  # True
CreditCodeUtil.is_valid_credit_code("invalid")               # False
```

```{note}
校验算法基于 GB 32100-2015 标准。
```
