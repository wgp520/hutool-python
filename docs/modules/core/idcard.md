# 身份证工具 - IdcardUtil

## 由来

中国身份证号码包含丰富的信息（地区、出生日期、性别），并且有严格的校验规则。`IdcardUtil` 提供身份证号码的校验和信息提取。

## 方法

```python
from hutool import IdcardUtil

idcard = "110101199001011234"

# 校验
IdcardUtil.is_valid_idcard(idcard)    # True/False
IdcardUtil.is_valid_card18(idcard)    # 18位身份证校验
IdcardUtil.is_valid_card15(idcard)    # 15位身份证校验

# 提取信息
IdcardUtil.get_birth(idcard)          # "19900101"
IdcardUtil.get_age(idcard)            # 34（当前年份 - 出生年份）
IdcardUtil.get_gender(idcard)         # "M" 或 "F"
IdcardUtil.get_province(idcard)       # "北京"

# 转换
IdcardUtil.convert15to18("110101900101123")  # 转为18位

# 脱敏
IdcardUtil.hide(idcard)               # "110101****1234"

# 提取出生年/月/日
IdcardUtil.get_year_by_id_card(idcard)   # 1990
IdcardUtil.get_month_by_id_card(idcard)  # 1
IdcardUtil.get_day_by_id_card(idcard)    # 1
```

### 身份证号码结构

18位身份证号码结构：

| 位置 | 含义 |
| ---- | ---- |
| 1-6 | 地区码 |
| 7-14 | 出生日期（yyyyMMdd） |
| 15-17 | 顺序码（奇数为男性，偶数为女性） |
| 18 | 校验码 |
