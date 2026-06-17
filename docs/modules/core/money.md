# 货币工具 - MoneyUtil

## 由来

货币计算中浮点精度问题会导致金额错误（如 `0.1 + 0.2 != 0.3`）。`MoneyUtil` 使用 `Decimal` 精确运算，提供元/分转换和含税/不含税价格计算。

## 方法

### 元/分转换

```python
from hutool import MoneyUtil

MoneyUtil.fen_to_yuan(100)      # Decimal('1.00')
MoneyUtil.fen_to_yuan(1)        # Decimal('0.01')
MoneyUtil.fen_to_yuan('50')     # Decimal('0.50')

MoneyUtil.yuan_to_fen(1)        # 100
MoneyUtil.yuan_to_fen('0.5')    # 50
MoneyUtil.yuan_to_fen('0.01')   # 1
```

### 税价计算

默认增值税率为 13%（中国标准增值税率），可通过参数自定义：

```python
from decimal import Decimal

# 不含税价 → 含税价
MoneyUtil.gross_price(Decimal('100'))            # Decimal('113.00')
MoneyUtil.gross_price(Decimal('100'), tax_rate=8)  # Decimal('108.00')

# 含税价 → 不含税价
MoneyUtil.net_price(Decimal('113'))              # Decimal('100.00')
MoneyUtil.net_price(Decimal('108'), tax_rate=8)  # Decimal('100.00')

# 计算税额
MoneyUtil.tax_amount(Decimal('113'))             # Decimal('13.00')
```

### 利润率计算

```python
from decimal import Decimal

# netto — 不含税金额
MoneyUtil.netto(Decimal('100'), Decimal('0.13'))  # Decimal('88.50')

# brutto — 含税金额
MoneyUtil.brutto(Decimal('100'), Decimal('0.13'))  # Decimal('113.00')

# profitMargin — 利润率
MoneyUtil.profit_margin(Decimal('100'), Decimal('80'))  # Decimal('25.00')
```

### 元/分互转（增强）

```python
# centToYuan / yuanToCent — 与 fen_to_yuan / yuan_to_fen 相同
MoneyUtil.cent_to_yuan(100)    # Decimal('1.00')
MoneyUtil.yuan_to_cent(1.00)   # 100
```

### 税额计算（增强）

```python
# taxAmount — 精确税额计算
MoneyUtil.tax_amount(Decimal('100'), Decimal('0.13'))  # Decimal('13.00')
```

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
