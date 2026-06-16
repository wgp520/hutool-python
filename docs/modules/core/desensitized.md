# 信息脱敏工具 - DesensitizedUtil

## 由来

在数据展示和日志记录中，经常需要对敏感信息进行脱敏处理。`DesensitizedUtil` 提供了针对各种敏感数据的脱敏方法。

## 方法

```python
from hutool import DesensitizedUtil

# 中文姓名：保留姓，其余用 * 替代
DesensitizedUtil.chinese_name("张三")       # "张*"
DesensitizedUtil.chinese_name("欧阳娜娜")   # "欧**"

# 身份证号
DesensitizedUtil.id_card("110101199001011234")  # "110101****1234"

# 手机号：中间4位用 * 替代
DesensitizedUtil.mobile_phone("13812345678")   # "138****5678"

# 座机号
DesensitizedUtil.fixed_phone("01012345678")    # "010****5678"

# 邮箱：@前保留首尾字符
DesensitizedUtil.email("test@example.com")     # "t***t@example.com"

# 地址
DesensitizedUtil.address("北京市海淀区中关村大街1号", 3)  # "北京市海淀区****"

# 银行卡
DesensitizedUtil.bank_card("6222021234567890123")  # "6222 **** **** 0123"

# 密码
DesensitizedUtil.password("my_password")  # "**********"

# 车牌号
DesensitizedUtil.car_license("京A12345")  # "京A****"

# IPv4
DesensitizedUtil.ipv4("192.168.1.100")  # "192.168.*.*"

# IPv6
DesensitizedUtil.ipv6("fe80::1")  # "fe80::*"

# 前 N 个字符脱敏
DesensitizedUtil.first_mask("13800138000", mask_len=4)  # "****0138000"

# 护照号脱敏
DesensitizedUtil.passport("E12345678")  # "E******8"

# 统一社会信用代码脱敏
DesensitizedUtil.credit_code("91350100M000100Y43")  # "913501***100Y43"
```
