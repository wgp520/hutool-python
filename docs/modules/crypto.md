# 加密解密工具

## 概述

加密分为三种：

1. **对称加密**（symmetric）：AES、DES 等
2. **非对称加密**（asymmetric）：RSA 等
3. **摘要加密**（digest）：MD5、SHA、HMAC 等

Hutool-Python 基于 `cryptography` 库封装了这三种加密类型。

## DigestUtil - 摘要加密

```python
from hutool import DigestUtil

# MD5
DigestUtil.md5_hex("hello")           # "5d41402abc4b2a76b9719d911017c592"
DigestUtil.md5_hex16("hello")         # 16位 MD5

# SHA
DigestUtil.sha1_hex("hello")
DigestUtil.sha256_hex("hello")
DigestUtil.sha384_hex("hello")
DigestUtil.sha512_hex("hello")

# HMAC
DigestUtil.hmac_md5_hex("hello", "secret_key")
DigestUtil.hmac_sha1_hex("hello", "secret_key")
DigestUtil.hmac_sha256_hex("hello", "secret_key")

# BCrypt
hashed = DigestUtil.bcrypt("password")
DigestUtil.bcrypt_check("password", hashed)  # True
```

## SecureUtil - 对称/非对称加密

### AES 加密

```python
from hutool import SecureUtil

# 生成密钥
key = SecureUtil.generate_aes_key(128)  # 128/192/256 位

# 加密解密
encrypted = SecureUtil.encrypt_aes(b"hello world", key, "CBC")
decrypted = SecureUtil.decrypt_aes(encrypted, key, "CBC")
assert decrypted == b"hello world"
```

### DES 加密

```python
key = SecureUtil.generate_des_key()

encrypted = SecureUtil.encrypt_des(b"hello", key, "ECB")
decrypted = SecureUtil.decrypt_des(encrypted, key, "ECB")
```

### RSA 加密

```python
# 生成密钥对
key_pair = SecureUtil.generate_rsa_key_pair(2048)

# 加密
encrypted = SecureUtil.encrypt_rsa(b"hello", key_pair.public_key)

# 解密
decrypted = SecureUtil.decrypt_rsa(encrypted, key_pair.private_key)

# 签名
signature = SecureUtil.sign_with_rsa(b"data", key_pair.private_key)

# 验签
SecureUtil.verify_with_rsa(b"data", signature, key_pair.public_key)  # True
```

## SignUtil - 签名工具

```python
from hutool import SignUtil

# 参数签名（常用于 API 签名）
params = {"name": "test", "timestamp": "1234567890"}
sign = SignUtil.sign_params(params, "secret_key")
sign = SignUtil.sort_sign(params, "secret_key")  # 按 key 排序后签名
```

## 凯撒密码

简单的字母位移加密，常用于教学和轻量级混淆：

```python
# 加密
SecureUtil.caesar_encode("Hello", 3)   # "Khoor"

# 解密
SecureUtil.caesar_decode("Khoor", 3)   # "Hello"
```

## 支持的算法

| 类型 | 算法 |
| ---- | ---- |
| 对称加密 | AES, DES, 3DES |
| 非对称加密 | RSA |
| 摘要 | MD5, SHA-1, SHA-256, SHA-384, SHA-512 |
| 消息认证码 | HMAC-MD5, HMAC-SHA1, HMAC-SHA256 |
| 密码哈希 | BCrypt |

## 其他

### 加密器工厂

```python
from hutool import SecureUtil

# AES 加密器
enc = SecureUtil.aes_encryptor(key)
encrypted = enc.encrypt(b"hello")
decrypted = enc.decrypt(encrypted)

# DES 加密器
enc = SecureUtil.des_encryptor(key)

# RC4 加密器
enc = SecureUtil.rc4_encryptor(key)

# RSA 加密器
enc = SecureUtil.rsa_encryptor(private_key, public_key)
```

### HMAC 创建器

```python
# hmacCreator — 创建 HMAC 实例
hmac = SecureUtil.hmac_creator("HmacSHA256", b"secret_key")
result = hmac.digest(b"hello")
```

### 签名

```python
# signData — 数字签名
signature = SecureUtil.sign_data(b"data", "SHA256withRSA", private_key)
```

### 密钥生成

```python
# generateKeyPair — 生成密钥对
private_key, public_key = SecureUtil.generate_key_pair("RSA", 2048)

# generateKey — 生成对称密钥
key = SecureUtil.generate_key("AES", 128)
```

### PBKDF2

```python
# pbkdf2 — 密码派生函数
derived = SecureUtil.pbkdf2("password", b"salt", iterations=10000, key_length=32)
```
