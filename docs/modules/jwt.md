# JWT 工具 - JWTUtil

## 由来

JWT（JSON Web Token）是一种网络身份认证和信息交换格式。`JWTUtil` 基于 PyJWT 封装，提供简洁的 JWT 操作接口。

## JWT 结构

- **Header**：头部信息，声明签名算法
- **Payload**：载荷信息，承载声明和数据
- **Signature**：签名，用于校验数据

整体结构：`header.payload.signature`

## 使用

### 生成 Token

```python
from hutool import JWTUtil

# 生成 Token（默认 HS256 算法）
token = JWTUtil.create_token(
    {"sub": "1234567890", "name": "张三", "admin": True},
    secret="my-secret-key"
)
# "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# 使用其他算法
token = JWTUtil.create_token(
    {"sub": "1234567890"},
    secret="my-secret-key",
    algorithm="HS512"
)
```

### 解析 Token

```python
# 解析并验证签名
payload = JWTUtil.parse_token(token, secret="my-secret-key")
# {"sub": "1234567890", "name": "张三", "admin": True}
```

### 验证 Token

```python
# 验证签名是否有效
JWTUtil.verify(token, secret="my-secret-key")   # True
JWTUtil.verify(token, secret="wrong-key")        # False
```

### 获取 Payload（不验证签名）

```python
# 不验证签名，仅解码
payload = JWTUtil.get_payload(token)
# {"sub": "1234567890", "name": "张三", "admin": True}
```

## 支持的算法

| 算法 | 说明 |
| ---- | ---- |
| HS256 | HMAC-SHA256（默认） |
| HS384 | HMAC-SHA384 |
| HS512 | HMAC-SHA512 |
| RS256 | RSA-SHA256 |
| RS384 | RSA-SHA384 |
| RS512 | RSA-SHA512 |
