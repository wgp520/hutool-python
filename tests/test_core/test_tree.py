from hutool import TreeUtil


class TestTreeUtil:
    def test_build(self):
        data = [
            {"id": 1, "parentId": 0, "name": "root"},
            {"id": 2, "parentId": 1, "name": "child1"},
            {"id": 3, "parentId": 1, "name": "child2"},
            {"id": 4, "parentId": 2, "name": "grandchild1"},
        ]
        result = TreeUtil.build(data)
        assert len(result) == 1  # One root
        assert result[0].name == "root"
        assert len(result[0].children) == 2

    def test_build_custom_fields(self):
        data = [
            {"id": 1, "pid": 0, "name": "root"},
            {"id": 2, "pid": 1, "name": "child"},
        ]
        result = TreeUtil.build(data, id_field="id", parent_field="pid")
        assert len(result) == 1
        assert len(result[0].children) == 1

    def test_build_multiple_roots(self):
        data = [
            {"id": 1, "parentId": 0, "name": "root1"},
            {"id": 2, "parentId": 0, "name": "root2"},
        ]
        result = TreeUtil.build(data)
        assert len(result) == 2

    def test_to_list(self):
        data = [
            {"id": 1, "parentId": 0, "name": "root"},
            {"id": 2, "parentId": 1, "name": "child"},
        ]
        tree = TreeUtil.build(data)
        result = TreeUtil.to_list(tree)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_get_node_by_id(self):
        data = [
            {"id": 1, "parentId": 0, "name": "root"},
            {"id": 2, "parentId": 1, "name": "child"},
        ]
        tree = TreeUtil.build(data)
        node = TreeUtil.get_node_id(tree, 2)
        assert node is not None
        assert node.name == "child"

    def test_build_single(self):
        data = [
            {"id": 1, "parentId": 0, "name": "root"},
            {"id": 2, "parentId": 1, "name": "child"},
        ]
        root = TreeUtil.build_single(data, root_id=0)
        assert root is not None
        assert root.name == "root"
        assert len(root.children) == 1

    def test_build_single_empty(self):
        root = TreeUtil.build_single([], root_id=0)
        assert root is None

    def test_get_parents_name(self):
        data = [
            {"id": 1, "parentId": 0, "name": "root"},
            {"id": 2, "parentId": 1, "name": "child"},
            {"id": 3, "parentId": 2, "name": "leaf"},
        ]
        tree = TreeUtil.build(data, root_id=0)
        path = TreeUtil.get_parents_name(tree, 3, separator="/")
        assert path == "root/child/leaf"

    def test_get_parents_id(self):
        data = [
            {"id": 1, "parentId": 0, "name": "root"},
            {"id": 2, "parentId": 1, "name": "child"},
            {"id": 3, "parentId": 2, "name": "leaf"},
        ]
        tree = TreeUtil.build(data, root_id=0)
        ids = TreeUtil.get_parents_id(tree, 3)
        assert ids == [1, 2, 3]

    def test_create_empty_node(self):
        node = TreeUtil.create_empty_node(1, "test", 0)
        assert node.id == 1
        assert node.name == "test"
        assert node.parent_id == 0
