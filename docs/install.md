# 安装指南

## 环境要求

- Python >= 3.8
- 操作系统：Windows / macOS / Linux

## 使用 pip 安装

```bash
pip install hutool-python
```

## 从源码安装

```bash
git clone https://github.com/user/hutool-python.git
cd hutool-python
pip install -e .
```

## 依赖说明

Hutool-Python 依赖以下第三方库，安装时会自动处理：

| 依赖 | 用途 |
| --- | --- |
| `pendulum>=3.0` | 日期时间处理（`DateUtil`） |
| `httpx>=0.27` | HTTP 客户端（`HttpUtil`） |
| `cryptography>=42.0` | 加密解密（`SecureUtil`、`DigestUtil`） |
| `qrcode[pil]>=7.0` | 二维码生成（`QrCodeUtil`） |
| `Pillow>=10.0` | 图像处理（`CaptchaUtil`） |
| `pypinyin>=0.50` | 中文拼音（`PinyinUtil`） |
| `emoji>=2.0` | Emoji 处理（`EmojiUtil`） |
| `jinja2>=3.0` | 模板引擎（`TemplateUtil`） |
| `pyjwt>=2.8` | JWT 令牌（`JWTUtil`） |
| `pyyaml>=6.0` | YAML 解析（`YamlUtil`） |
| `watchdog>=4.0` | 文件监听 |
| `sortedcontainers>=2.0` | 有序容器 |

## 开发依赖

```bash
pip install hutool-python[dev]
```

额外安装：

| 依赖 | 用途 |
| --- | --- |
| `pytest>=8.0` | 测试框架 |
| `ruff>=0.4.0` | 代码格式化和检查 |

## 验证安装

```python
import hutool
print(hutool.__version__)  # 1.0.0

from hutool import StrUtil
print(StrUtil.is_blank(""))  # True
```
