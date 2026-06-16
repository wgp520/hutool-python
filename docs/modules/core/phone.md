# 手机号工具 - PhoneUtil

## 由来

提供中国大陆及港澳台手机号的校验和脱敏功能。

## 方法

```python
from hutool import PhoneUtil

# 校验
PhoneUtil.is_mobile("13812345678")      # True（大陆手机号）
PhoneUtil.is_mobile_hk("91234567")      # True（香港）
PhoneUtil.is_mobile_tw("0912345678")    # True（台湾）
PhoneUtil.is_mobile_mo("66123456")      # True（澳门）
PhoneUtil.is_phone("010-12345678")      # True（座机）

PhoneUtil.is_mobile_simple("10000000000") # True（宽松判断）

# 脱敏
PhoneUtil.hide_before("13812345678")    # "****5678"
PhoneUtil.hide_between("13812345678")   # "138****5678"
PhoneUtil.hide_after("13812345678")     # "1381****"

# 截取
PhoneUtil.sub_before("13812345678")     # "138"
PhoneUtil.sub_after("13812345678")      # "5678"

# 是否为座机号码
PhoneUtil.is_tel("010-12345678")        # True

# 是否为 400/800 号码
PhoneUtil.is_tel_400_800("4001234567")  # True

# 截取指定位
PhoneUtil.sub_between("13800138000", 3, 7)  # "0013"

# 座机区号/号码
PhoneUtil.sub_tel_before("010-12345678")    # "010"
PhoneUtil.sub_tel_after("010-12345678")     # "12345678"
```
