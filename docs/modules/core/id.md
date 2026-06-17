# 唯一 ID 工具 - IdUtil

## 由来

在分布式系统中，唯一 ID 的生成是常见需求。`IdUtil` 提供了 UUID、NanoId、雪花 ID 等多种 ID 生成方案。

## 方法

### UUID

```python
from hutool import IdUtil

# 标准 UUID（带横线）
IdUtil.random_uuid()       # "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

# 简单 UUID（无横线）
IdUtil.simple_uuid()       # "a1b2c3d4e5f67890abcdef1234567890"

# 快速 UUID（使用 uuid4）
IdUtil.fast_uuid()         # 同 random_uuid
IdUtil.fast_simple_uuid()  # 同 simple_uuid
```

### NanoId

NanoId 是一种更短、更安全的 ID 生成算法：

```python
IdUtil.nano_id()           # "V1StGXR8_Z5jdHi6B-myT"（默认21位）
IdUtil.nano_id(10)         # "V1StGXR8_Z5"（自定义长度）
```

### 雪花 ID

雪花算法生成的 64 位整数 ID，适用于分布式系统：

```python
IdUtil.snowflake_id()      # 1234567890123456789
```

雪花 ID 结构：

- 1 位符号位
- 41 位时间戳（毫秒）
- 10 位工作机器 ID
- 12 位序列号

```python
# 创建雪花 ID 生成器
worker = IdUtil.create_snowflake(worker_id=1, datacenter_id=1)
id_val = worker.next_id()

# 获取全局单例雪花生成器
snowflake = IdUtil.get_snowflake(1, 1)

# 获取下一个雪花 ID
IdUtil.get_snowflake_next_id(1, 1)       # int
IdUtil.get_snowflake_next_id_str(1, 1)   # str
```

### 选择建议

| 方案 | 长度 | 有序性 | 适用场景 |
| ---- | ---- | ------ | ------- |
| UUID | 32 | 无 | 通用场景 |
| NanoId | 21（可配置） | 无 | 短 ID、URL 安全 |
| 雪花 ID | 18-19 位数字 | 有（时间有序） | 数据库主键、分布式系统 |

### 机器唯一 ID

基于 PID + 主机名哈希 + 时间戳 + 计数器组合生成的唯一 ID，适合分布式环境下的节点标识：

```python
from hutool import IdUtil

# 32 位机器唯一 ID（毫秒时间戳 12 位 + PID 8 位 + 计数器 12 位）
id32 = IdUtil.unique_machine32()    # 例如 287454212

# 64 位机器唯一 ID（含主机名哈希，跨机器唯一）
id64 = IdUtil.unique_machine64()    # 例如 1382741234567890

# 基于主机名的全局唯一 ID（适合 NFS 文件命名）
IdUtil.luid()                       # "A1B2C3D4-PID1234-60A1B2C3-0001"
IdUtil.luid(separator=":")          # "A1B2C3D4:PID1234:60A1B2C3:0001"
```

### Verhoeff 校验位 ID

使用 Verhoeff 算法生成带校验位的业务 ID（位于 `CheckUtil`）：

```python
from hutool import CheckUtil

# 带前缀的 ID（数字部分补零到 6 位，末位为校验位）
CheckUtil.build_verhoeff_id("INV", 42, length=6)    # "INV000042X"（X 为校验位）
CheckUtil.build_verhoeff_id("ORD", 7, length=1)     # "ORD7X"
CheckUtil.build_verhoeff_id("T", 0, length=1)        # "T0X"
```

### GUID128

生成 26 字符的全局唯一 ID，使用 Crockford Base32 编码：

```python
from hutool import IdUtil

IdUtil.guid128()                    # "0DGHJKMNPQRSTVWXYZ0123456"
IdUtil.guid128(salt="my-salt")      # 带盐值的唯一 ID
```

### 全局单例管理器

```python
from hutool.core.util.id import MachineIdGenerator

gen = MachineIdGenerator()
gen.generate32()    # 32 位 ID
gen.generate64()    # 64 位 ID
```
