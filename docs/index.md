# Hutool-Python 文档

<p align="center">
<strong>让 Python 和 Java 一样"甜蜜"的工具库</strong>
</p>

---

## 简介

**Hutool-Python** 是 [Java Hutool](https://github.com/dromara/hutool) 的 Python 移植版本，旨在将 Hutool 丰富且易用的工具类生态带到 Python 世界。

Hutool 是一个功能丰富且易用的 Java 工具库，涵盖了字符串、数字、集合、编码、日期、文件、IO、加密、JSON、HTTP 客户端等一系列操作。Hutool-Python 将这些能力忠实移植到 Python，保留 Hutool 的命名风格和设计理念，让 Java 开发者无缝切换，也让 Python 开发者享受 Hutool 式的便捷体验。

## 设计理念

- **忠实移植**：类名保持 Hutool 的 PascalCase 风格（如 `StrUtil`、`DateUtil`），方法名转为 Python 的 snake_case
- **Python 化实现**：底层使用 Python 生态最佳实践（`pendulum`、`httpx`、`cryptography` 等）
- **中文注释**：所有文档注释均使用中文，采用 Sphinx 风格
- **零配置开箱即用**：`pip install` 后即可使用

## 快速开始

```python
from hutool import StrUtil, DateUtil, IdUtil

# 字符串工具
StrUtil.is_blank("")          # True
StrUtil.sub("abcdefgh", 2, 5) # "cde"

# 日期工具
DateUtil.now()                 # 当前时间字符串
DateUtil.format_date(DateUtil.date())  # "2024-01-01"

# ID 生成
IdUtil.random_uuid()           # UUID
IdUtil.simple_uuid()           # 无横线 UUID
```

---

## 模块总览

````{grid} 2
:gutter: 3

```{grid-item-card} 核心工具 (core)
:link: modules/core/overview
:link-type: doc

字符串、数字、数组、对象、集合、日期、IO、编解码、网络等 25+ 工具类
```

```{grid-item-card} HTTP 客户端
:link: modules/httpx_client
:link-type: doc

基于 httpx 的 HTTP 请求工具，支持链式调用、文件上传、Cookie 管理
```

```{grid-item-card} JSON 工具
:link: modules/json
:link-type: doc

JSON 解析、序列化、路径查询、XML 互转
```

```{grid-item-card} 加密解密
:link: modules/crypto
:link-type: doc

MD5、SHA、HMAC、AES、DES、RSA、签名验证
```

```{grid-item-card} 缓存
:link: modules/cache
:link-type: doc

FIFO、LFU、LRU、定时缓存等多种策略
```

```{grid-item-card} 验证码
:link: modules/captcha
:link-type: doc

文字验证码、算术验证码生成
```

```{grid-item-card} 敏感词过滤
:link: modules/dfa
:link-type: doc

基于 DFA 算法的高性能敏感词过滤
```

```{grid-item-card} 扩展工具
:link: modules/extra
:link-type: doc

拼音、Emoji、模板引擎、二维码
```

```{grid-item-card} 定时任务
:link: modules/cron
:link-type: doc

Cron 表达式定时任务调度
```

```{grid-item-card} JWT 工具
:link: modules/jwt
:link-type: doc

JWT 令牌生成、解析、验证
```

```{grid-item-card} 配置工具
:link: modules/setting
:link-type: doc

YAML、Properties 配置文件读写
```

````

---

## 与 Java Hutool 的对应关系

| Python 模块 | Java Hutool 模块 | 说明 |
|---|---|---|
| `hutool.core` | `cn.hutool.core` | 核心工具类 |
| `hutool.httpx_client` | `cn.hutool.http` | HTTP 客户端 |
| `hutool.json` | `cn.hutool.json` | JSON 工具 |
| `hutool.crypto` | `cn.hutool.crypto` | 加密解密 |
| `hutool.cache` | `cn.hutool.cache` | 缓存 |
| `hutool.captcha` | `cn.hutool.captcha` | 验证码 |
| `hutool.dfa` | `cn.hutool.dfa` | 敏感词过滤 |
| `hutool.extra` | `cn.hutool.extra` | 扩展工具 |
| `hutool.cron` | `cn.hutool.cron` | 定时任务 |
| `hutool.jwt` | `cn.hutool.jwt` | JWT |
| `hutool.setting` | `cn.hutool.setting` | 配置工具 |

---

```{toctree}
:hidden:
:maxdepth: 2
:caption: 使用指南

install
quickstart
publish
changelog
contributing
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: 模块文档

modules/core/overview
modules/httpx_client
modules/json
modules/crypto
modules/cache
modules/captcha
modules/dfa
modules/extra
modules/cron
modules/jwt
modules/setting
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: API 参考

apidocs/index
```
