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
