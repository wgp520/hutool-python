# 树结构工具 - TreeUtil

## 由来

在菜单管理、组织架构、分类目录等场景中，树形结构是常见的数据组织方式。`TreeUtil` 提供了从扁平数据构建树结构的方法。

## TreeNode

树节点的数据结构：

```python
from hutool import TreeUtil

# 从扁平数据构建树
data = [
    {"id": 1, "parentId": 0, "name": "根节点"},
    {"id": 2, "parentId": 1, "name": "子节点1"},
    {"id": 3, "parentId": 1, "name": "子节点2"},
    {"id": 4, "parentId": 2, "name": "孙节点1"},
]

tree = TreeUtil.build(data)
# 返回树结构的根节点列表
```

## 方法

### 构建树

```python
# 默认使用 id/parentId 字段
tree = TreeUtil.build(data)

# 自定义字段名
tree = TreeUtil.build(data, id_field="nodeId", parent_field="pid")

# 指定根节点 ID
tree = TreeUtil.build(data, root_id=0)
```

### 遍历

```python
# 广度优先遍历
TreeUtil.foreach(tree, lambda node: print(node.name))

# 深度优先遍历
TreeUtil.foreach_df(tree, lambda node: print(node.name))
```

### 转换

```python
# 树转扁平列表
flat_list = TreeUtil.to_list(tree)

# 树转字典
tree_map = TreeUtil.to_map(tree)
```

### 查找

```python
# 根据 ID 查找节点
node = TreeUtil.get_node_id(tree, 4)
```

### 其他

```python
# 构建单根树
root = TreeUtil.build_single(data, root_id=0)

# 获取节点完整路径名称
path = TreeUtil.get_parents_name(tree, 4, separator="/")  # "根/父/子"

# 获取祖先 ID 列表
ids = TreeUtil.get_parents_id(tree, 4)  # [1, 2, 4]

# 创建空节点
node = TreeUtil.create_empty_node(99, "new_node", parent_id=1)
```
