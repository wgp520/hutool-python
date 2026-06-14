# 发布指南

本章介绍如何将 Hutool-Python 发布到 PyPI，供全球开发者 `pip install` 使用。

## 前置准备

### 1. 注册 PyPI 账号

- 正式站：<https://pypi.org/account/register/>
- 测试站：<https://test.pypi.org/account/register/>

### 2. 安装构建工具

```bash
pip install build twine
```

| 工具 | 用途 |
|------|------|
| `build` | 按 PEP 517 标准构建 sdist 和 wheel |
| `twine` | 上传分发包到 PyPI |

### 3. 配置 API Token（推荐）

相比用户名+密码，API Token 更安全且可按项目隔离。

**正式站**：<https://pypi.org/manage/account/token/> 创建 token，scope 选"Hutool-Python"项目。

创建 `~/.pypirc`（Windows 为 `%USERPROFILE%\.pypirc`）：

```ini
[pypi]
username = __token__
password = pypi-AgEI...your-token...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEI...your-test-token...
```

---

## 发布流程

### 第一步：更新版本号

版本号需同步修改以下两处：

```bash
# pyproject.toml
version = "1.0.1"

# setup.py
version="1.0.1"
```

```{tip}
遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范：
- `MAJOR.MINOR.PATCH`（如 1.0.1）
- MAJOR：不兼容的 API 变更
- MINOR：向后兼容的功能新增
- PATCH：向后兼容的问题修正
```

### 第二步：更新 changelog

编辑 `docs/changelog.md`，记录本次版本变更内容。

### 第三步：确认仓库状态

```bash
# 确保测试通过
pytest tests/ -v

# 确保代码风格检查通过
ruff check .

# 确认 git 工作区干净
git status
```

### 第四步：构建分发包

```bash
# 清理旧构建
rm -rf dist/ build/ *.egg-info

# 构建 sdist + wheel
python -m build
```

构建完成后 `dist/` 目录下应有 4 个文件：

```
dist/
├── hutool_python-1.0.0-py3-none-any.whl    # wheel（推荐安装格式）
├── hutool_python-1.0.0.tar.gz              # sdist（源码包）
```

### 第五步：上传到 TestPyPI（可选）

先上传到测试站验证：

```bash
twine upload --repository testpypi dist/*
```

验证安装：

```bash
pip install --index-url https://test.pypi.org/simple/ hutool-python
```

### 第六步：上传到 PyPI

```bash
twine upload dist/*
```

上传成功后可在 <https://pypi.org/project/hutool-python/> 查看。

### 第七步：打 Git Tag 并推送

```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## GitHub Actions 自动发布

在 GitHub 仓库页面创建 Release 后，可手动触发以下 workflow 自动发布到 PyPI。

在 `.github/workflows/` 下添加 `publish.yml`：

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write          # 用于 Trusted Publishing（可选）
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.8"

      - name: Install build tools
        run: pip install build twine

      - name: Build
        run: python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

在仓库 Settings → Secrets and variables → Actions 中添加 `PYPI_API_TOKEN`。

```{note}
也可以使用 PyPI 的 [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) 功能，无需配置 token，直接通过 OpenID Connect 认证。
```

---

## 用户安装

发布后，用户即可通过 pip 安装：

```bash
# 安装最新版
pip install hutool-python

# 安装指定版本
pip install hutool-python==1.0.0

# 升级到最新版
pip install --upgrade hutool-python
```

```python
from hutool import StrUtil, DateUtil, IdUtil

StrUtil.is_blank("")     # True
DateUtil.today()         # "2026-06-14"
IdUtil.random_uuid()     # "550e8400-e29b-41d4-a716-446655440000"
```
