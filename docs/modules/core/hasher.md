# Hash 算法 - HashUtil

## 由来

提供多种经典哈希算法的实现，包括 FNV、BKDR、DJB 等。这些算法在哈希表、布隆过滤器等场景中有广泛应用。

## 方法

```python
from hutool import HashUtil

# FNV 哈希
HashUtil.fnv1(b"hello")       # FNV1 哈希值
HashUtil.fnv1a(b"hello")      # FNV1a 哈希值

# 字符串哈希
HashUtil.bkdr_hash("hello")   # BKDR 哈希
HashUtil.ap_hash("hello")     # AP 哈希
HashUtil.djb_hash("hello")    # DJB 哈希
HashUtil.js_hash("hello")     # JS 哈希
HashUtil.rs_hash("hello")     # RS 哈希
HashUtil.sdbm_hash("hello")   # SDBM 哈希
HashUtil.elf_hash("hello")    # ELF 哈希
HashUtil.dek_hash("hello")    # DEK 哈希

# Java hashCode 兼容
HashUtil.java_hash_code("hello")  # 与 Java 的 "hello".hashCode() 一致
```

### 算法对比

| 算法 | 特点 | 适用场景 |
|------|------|---------|
| FNV1/FNV1a | 快速、分布均匀 | 通用哈希 |
| BKDR | 简单、高效 | 字符串哈希 |
| DJB | 分布好 | 字符串哈希 |
| Java hashCode | 与 Java 兼容 | 跨语言场景 |
