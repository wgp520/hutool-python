from collections import deque
from typing import Any, Callable, Dict, List, Optional


class TreeNode:
    """树节点

    用于表示树结构中的单个节点，包含节点标识、父节点标识、
    名称、权重、子节点列表以及扩展属性。
    """

    def __init__(
        self,
        id: Any = None,
        parent_id: Any = None,
        name: str = "",
        weight: int = 0,
    ):
        """初始化树节点

        :param id: 节点唯一标识
        :param parent_id: 父节点标识，根节点通常为 None 或特定根标识
        :param name: 节点名称
        :param weight: 节点权重，用于排序
        """
        self.id = id
        self.parent_id = parent_id
        self.name = name
        self.weight = weight
        self.children: List[TreeNode] = []
        self.extra: Dict[str, Any] = {}

    def __repr__(self) -> str:
        return (
            f"TreeNode(id={self.id!r}, parent_id={self.parent_id!r}, "
            f"name={self.name!r}, weight={self.weight}, "
            f"children_count={len(self.children)})"
        )

    def to_dict(self) -> dict:
        """将节点及其子树转为字典

        :return: 包含节点信息和子节点列表的字典
        """
        result = {
            "id": self.id,
            "parentId": self.parent_id,
            "name": self.name,
            "weight": self.weight,
            "children": [child.to_dict() for child in self.children],
        }
        if self.extra:
            result.update(self.extra)
        return result


class TreeUtil:
    """树工具类

    提供从平铺列表构建树、遍历、查找、统计等常用操作。
    """

    @staticmethod
    def build(
        list_data: List[dict],
        root_id: Any = None,
        id_field: str = "id",
        parent_field: str = "parentId",
        children_field: str = "children",
        name_field: str = "name",
        weight_field: str = "weight",
    ) -> List[TreeNode]:
        """从平铺列表构建树

        将包含 id 和 parentId 的平铺字典列表转换为树形结构。

        :param list_data: 平铺的字典列表
        :param root_id: 根节点的 parent_id 值，默认为 None
        :param id_field: 节点ID字段名，默认 "id"
        :param parent_field: 父节点ID字段名，默认 "parentId"
        :param children_field: 子节点列表字段名，默认 "children"
        :param name_field: 节点名称字段名，默认 "name"
        :param weight_field: 权重字段名，默认 "weight"
        :return: 根节点列表（可能有多个顶级节点）
        """
        # 构建 id -> TreeNode 的映射
        node_map: Dict[Any, TreeNode] = {}
        for item in list_data:
            node_id = item.get(id_field)
            node = TreeNode(
                id=node_id,
                parent_id=item.get(parent_field),
                name=str(item.get(name_field, "")),
                weight=int(item.get(weight_field, 0)),
            )
            # 将未识别的字段存入 extra
            known_fields = {id_field, parent_field, children_field, name_field, weight_field}
            for key, value in item.items():
                if key not in known_fields:
                    node.extra[key] = value
            node_map[node_id] = node

        # 组装父子关系
        roots: List[TreeNode] = []
        for item in list_data:
            node_id = item.get(id_field)
            parent_id = item.get(parent_field)
            node = node_map[node_id]
            if parent_id == root_id or parent_id not in node_map:
                roots.append(node)
            else:
                parent = node_map.get(parent_id)
                if parent is not None:
                    parent.children.append(node)

        # 按权重排序子节点
        def _sort_children(nodes: List[TreeNode]) -> None:
            nodes.sort(key=lambda n: n.weight)
            for child in nodes:
                _sort_children(child.children)

        _sort_children(roots)
        return roots

    @staticmethod
    def get_node_id(tree_nodes: List[TreeNode], node_id: Any) -> Optional[TreeNode]:
        """根据ID查找节点

        :param tree_nodes: 树节点列表
        :param node_id: 要查找的节点ID
        :return: 匹配的节点，未找到返回 None
        """
        queue = deque(tree_nodes)
        while queue:
            node = queue.popleft()
            if node.id == node_id:
                return node
            queue.extend(node.children)
        return None

    @staticmethod
    def to_list(tree_nodes: List[TreeNode]) -> List[dict]:
        """树转平铺列表

        将树形结构展平为字典列表，广度优先遍历。

        :param tree_nodes: 根节点列表
        :return: 平铺的字典列表
        """
        result: List[dict] = []
        queue = deque(tree_nodes)
        while queue:
            node = queue.popleft()
            result.append(node.to_dict())
            queue.extend(node.children)
        return result

    @staticmethod
    def foreach(
        tree_nodes: List[TreeNode],
        consumer: Callable[[TreeNode], None],
    ) -> None:
        """广度优先遍历（BFS）

        对树中每个节点执行 consumer 回调。

        :param tree_nodes: 根节点列表
        :param consumer: 遍历回调函数
        """
        queue = deque(tree_nodes)
        while queue:
            node = queue.popleft()
            consumer(node)
            queue.extend(node.children)

    @staticmethod
    def foreach_df(
        tree_nodes: List[TreeNode],
        consumer: Callable[[TreeNode], None],
    ) -> None:
        """深度优先遍历（DFS）

        对树中每个节点执行 consumer 回调，使用栈实现非递归遍历。

        :param tree_nodes: 根节点列表
        :param consumer: 遍历回调函数
        """
        stack = list(reversed(tree_nodes))
        while stack:
            node = stack.pop()
            consumer(node)
            # 反向压栈以保证从左到右的遍历顺序
            stack.extend(reversed(node.children))

    @staticmethod
    def to_map(tree_nodes: List[TreeNode]) -> Dict[Any, TreeNode]:
        """树转ID到节点的映射

        :param tree_nodes: 根节点列表
        :return: 以节点ID为键、节点对象为值的字典
        """
        result: Dict[Any, TreeNode] = {}
        queue = deque(tree_nodes)
        while queue:
            node = queue.popleft()
            result[node.id] = node
            queue.extend(node.children)
        return result

    @staticmethod
    def count(tree_nodes: List[TreeNode]) -> int:
        """统计节点总数

        :param tree_nodes: 根节点列表
        :return: 树中所有节点的数量
        """
        total = 0
        queue = deque(tree_nodes)
        while queue:
            node = queue.popleft()
            total += 1
            queue.extend(node.children)
        return total

    @staticmethod
    def get_leaf_nodes(tree_nodes: List[TreeNode]) -> List[TreeNode]:
        """获取所有叶子节点

        叶子节点是指没有子节点的节点。

        :param tree_nodes: 根节点列表
        :return: 叶子节点列表
        """
        leaves: List[TreeNode] = []
        queue = deque(tree_nodes)
        while queue:
            node = queue.popleft()
            if not node.children:
                leaves.append(node)
            else:
                queue.extend(node.children)
        return leaves

    @staticmethod
    def build_single(
        list_data: List[dict],
        root_id: Any = None,
        id_field: str = "id",
        parent_field: str = "parentId",
    ) -> Optional[TreeNode]:
        """从平铺列表构建单根树，返回唯一的根节点。

        :param list_data: 平铺的字典列表
        :param root_id: 根节点的 parent_id 值
        :param id_field: 节点 ID 字段名
        :param parent_field: 父节点 ID 字段名
        :return: 根节点，如果没有节点则返回 None
        :raises ValueError: 存在多个根节点时
        """
        roots = TreeUtil.build(list_data, root_id, id_field=id_field, parent_field=parent_field)
        if not roots:
            return None
        if len(roots) > 1:
            raise ValueError(f"存在 {len(roots)} 个根节点，无法构建单根树")
        return roots[0]

    @staticmethod
    def get_parents_name(tree_nodes: List[TreeNode], node_id: Any, separator: str = "/") -> str:
        """获取指定节点的完整路径名称。

        从根节点到目标节点的名称用 separator 连接。

        :param tree_nodes: 根节点列表
        :param node_id: 目标节点 ID
        :param separator: 路径分隔符，默认 ``"/"``
        :return: 完整路径名称，如 ``"根/父/子"``
        """
        node_map = TreeUtil.to_map(tree_nodes)
        node = node_map.get(node_id)
        if node is None:
            return ""
        names = []
        current = node
        while current is not None:
            names.append(current.name)
            parent_id = current.parent_id
            current = node_map.get(parent_id) if parent_id is not None else None
        names.reverse()
        return separator.join(names)

    @staticmethod
    def get_parents_id(tree_nodes: List[TreeNode], node_id: Any) -> list:
        """获取指定节点的所有祖先节点 ID（从根到当前节点）。

        :param tree_nodes: 根节点列表
        :param node_id: 目标节点 ID
        :return: 祖先 ID 列表
        """
        node_map = TreeUtil.to_map(tree_nodes)
        node = node_map.get(node_id)
        if node is None:
            return []
        ids = []
        current = node
        while current is not None:
            ids.append(current.id)
            parent_id = current.parent_id
            current = node_map.get(parent_id) if parent_id is not None else None
        ids.reverse()
        return ids

    @staticmethod
    def create_empty_node(node_id: Any, name: str = "", parent_id: Any = None) -> TreeNode:
        """创建一个空的树节点。

        :param node_id: 节点 ID
        :param name: 节点名称
        :param parent_id: 父节点 ID
        :return: 新的 TreeNode 实例
        """
        return TreeNode(id=node_id, parent_id=parent_id, name=name)
