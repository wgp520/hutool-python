# 贡献指南

感谢你对 Hutool-Python 的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题

如果你发现了 Bug 或有功能建议，请在 GitHub Issues 中提交。

### 提交代码

1. Fork 项目仓库
2. 创建你的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 开发环境

```bash
# 克隆项目
git clone https://github.com/user/hutool-python.git
cd hutool-python

# 创建虚拟环境
conda create -n hutool python=3.8
conda activate hutool

# 安装开发依赖
pip install -e ".[dev]"
```

## 代码规范

- 使用 `ruff` 进行代码格式化和检查：

```bash
ruff format hutool/ tests/
ruff check hutool/ tests/ --fix
```

- 类名保持 Hutool 的 PascalCase 风格（如 `StrUtil`）
- 方法名使用 Python 的 snake_case（如 `is_blank`）
- 所有文档注释使用中文，采用 Sphinx 风格（`:param:` / `:return:` / `:raises:`）
- 兼容 Python >= 3.8

## 运行测试

```bash
pytest tests/ -v
```

## 文档构建

```bash
cd docs
pip install -r requirements.txt
make html
# 打开 _build/html/index.html 查看
```
