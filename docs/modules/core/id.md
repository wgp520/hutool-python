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
