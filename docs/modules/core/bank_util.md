# 银行工具 - BankUtil

## 由来

IBAN（International Bank Account Number）是国际银行账号标准，校验算法基于 ISO 7064 mod 97-10。`BankUtil` 提供 IBAN 的计算和验证功能。

## 方法

### 计算 IBAN

```python
from hutool import BankUtil

# 根据账号和银行代码计算 IBAN
iban = BankUtil.calculate_iban('1234567890', '37040044')
# 'DE89370400441234567890'

# 指定国家代码
iban = BankUtil.calculate_iban('1234567890', '37040044', country='DE')
```

### 验证 IBAN

```python
BankUtil.check_iban('DE89370400441234567890')  # True
BankUtil.check_iban('DE00370400441234567890')  # False
```

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
