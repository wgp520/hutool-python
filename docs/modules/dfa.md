# 敏感词过滤 - SensitiveUtil

## 由来

内容审核是很多业务系统的需求，需要对文本中的敏感词进行检测和过滤。`SensitiveUtil` 基于 DFA（确定性有限自动机）算法实现高性能的敏感词查找和替换。

## DFA 算法

DFA 全称为 Deterministic Finite Automaton（确定有穷自动机）。用所有关键字构造一棵树，然后用正文遍历这棵树，遍历到叶子节点即表示存在这个关键字。查找复杂度为 O(n)。

## 使用

### 初始化

```python
from hutool import SensitiveUtil

# 加载敏感词库
SensitiveUtil.init(["傻逼", "混蛋", "色情", "赌博"])
```

### 检测

```python
# 是否包含敏感词
SensitiveUtil.contains("这是一个傻逼的测试")     # True
SensitiveUtil.contains("这是一个正常的文本")     # False

# 查找第一个敏感词
SensitiveUtil.find_first("这是傻逼和混蛋的测试")  # "傻逼"

# 查找所有敏感词
SensitiveUtil.find_all("这是傻逼和混蛋的测试")    # ["傻逼", "混蛋"]
```

### 替换

```python
# 替换敏感词
SensitiveUtil.replace("这是一个傻逼的测试")
# "这是一个*的测试"

# 自定义替换字符
SensitiveUtil.replace("这是一个傻逼的测试", replace_char="#")
# "这是一个##的测试"
```

## 使用建议

1. 从文件加载敏感词库：每行一个关键词
2. 定期更新敏感词库
3. 对于大型词库，DFA 算法的性能远优于逐个关键词匹配
