from hutool import XmlUtil


class TestXmlUtil:
    def test_read_xml(self):
        xml_str = "<root><name>test</name><value>123</value></root>"
        elem = XmlUtil.read_xml(xml_str)
        assert elem is not None

    def test_parse_to_map(self):
        xml_str = "<root><name>test</name><value>123</value></root>"
        result = XmlUtil.parse_to_map(xml_str)
        assert isinstance(result, dict)

    def test_format(self):
        xml_str = "<root><name>test</name></root>"
        result = XmlUtil.format_xml(xml_str)
        assert "\n" in result

    def test_map_to_xml(self):
        data = {"name": "test", "value": "123"}
        result = XmlUtil.map_to_xml(data, "root")
        assert "<root>" in result
        assert "<name>test</name>" in result

    def test_clean_invalid(self):
        result = XmlUtil.clean_invalid("abc\x00def")
        assert "\x00" not in result

    def test_create_xml(self):
        root = XmlUtil.create_xml("root")
        assert root.tag == "root"

    def test_get_root_element(self):
        xml_str = "<root><child>text</child></root>"
        root = XmlUtil.get_root_element(xml_str)
        assert root.tag == "root"

    def test_get_elements(self):
        xml_str = "<root><item>a</item><item>b</item></root>"
        root = XmlUtil.get_root_element(xml_str)
        items = XmlUtil.get_elements(root, "item")
        assert len(items) == 2

    def test_get_element(self):
        xml_str = "<root><child>text</child></root>"
        root = XmlUtil.get_root_element(xml_str)
        child = XmlUtil.get_element(root, "child")
        assert child is not None
        assert child.text == "text"
        assert XmlUtil.get_element(root, "missing") is None
