import xml.etree.ElementTree as ET

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

    def test_clean_comment(self):
        xml = "<root><!-- comment --><child>text</child></root>"
        result = XmlUtil.clean_comment(xml)
        assert "<!--" not in result
        assert "<child>text</child>" in result

    def test_element_text(self):
        root = ET.fromstring("<root><child>hello</child></root>")
        assert XmlUtil.element_text(root, "child") == "hello"
        assert XmlUtil.element_text(root, "missing") is None

    def test_append_child(self):
        root = ET.Element("root")
        child = XmlUtil.append_child(root, "child", "text")
        assert child.tag == "child"
        assert child.text == "text"

    def test_append_child_no_text(self):
        root = ET.Element("root")
        child = XmlUtil.append_child(root, "child")
        assert child.text is None

    def test_append_text(self):
        root = ET.Element("root")
        root.text = "hello"
        XmlUtil.append_text(root, " world")
        assert root.text == "hello world"

    def test_append_text_empty(self):
        root = ET.Element("root")
        XmlUtil.append_text(root, "hello")
        assert root.text == "hello"

    def test_is_element(self):
        root = ET.Element("root")
        assert XmlUtil.is_element(root) is True
        assert XmlUtil.is_element("string") is False
        assert XmlUtil.is_element(None) is False

    def test_to_str(self):
        root = ET.Element("root")
        ET.SubElement(root, "child").text = "text"
        result = XmlUtil.to_str(root)
        assert "root" in result
        assert "child" in result

    def test_to_str_pretty(self):
        root = ET.Element("root")
        ET.SubElement(root, "child").text = "text"
        result = XmlUtil.to_str(root, pretty=True)
        assert "\n" in result

    def test_create_document(self):
        doc = XmlUtil.create_document()
        assert doc.tag == "root"
