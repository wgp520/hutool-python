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

    def test_escape_xml(self):
        assert XmlUtil.escape_xml('a&b<c>"e') == "a&amp;b&lt;c&gt;&quot;e"

    def test_unescape_xml(self):
        assert XmlUtil.unescape_xml("a&amp;b&lt;c&gt;") == "a&b<c>"

    def test_xml_to_map(self):
        xml = "<root><name>test</name><value>123</value></root>"
        result = XmlUtil.xml_to_map(xml)
        assert "root" in result

    def test_map_to_xml_str(self):
        data = {"name": "test", "value": "123"}
        result = XmlUtil.map_to_xml_str(data)
        assert "<name>" in result
        assert "<value>" in result

    def test_bean_to_xml(self):
        data = {"name": "test", "value": "123"}
        result = XmlUtil.bean_to_xml(data, "item")
        assert "<item>" in result

    def test_parse_xml(self):
        xml = "<root><a>1</a></root>"
        elem = XmlUtil.parse_xml(xml)
        assert elem.tag == "root"

    def test_read_xml_file(self, tmp_path):
        p = tmp_path / "test.xml"
        p.write_text("<root><a>1</a></root>", encoding="utf-8")
        elem = XmlUtil.read_xml_file(str(p))
        assert elem.tag == "root"

    def test_format_xml_pretty(self):
        xml = "<root><a>1</a></root>"
        result = XmlUtil.format_xml_pretty(xml, indent=2)
        assert "\n" in result

    def test_get_by_xpath(self):
        from xml.etree.ElementTree import fromstring

        elem = fromstring("<root><child>text</child></root>")
        result = XmlUtil.get_by_xpath(elem, "child")
        assert result == "text"

    def test_get_node_by_xpath(self):
        from xml.etree.ElementTree import fromstring

        elem = fromstring("<root><child>text</child></root>")
        node = XmlUtil.get_node_by_xpath(elem, "child")
        assert node is not None
        assert node.text == "text"

    def test_write_object_as_xml(self, tmp_path):
        data = {"name": "test"}
        p = tmp_path / "out.xml"
        XmlUtil.write_object_as_xml(data, str(p), "root")
        assert p.exists()

    def test_dict_to_element(self):
        data = {"name": "test", "age": "20"}
        elem = XmlUtil.dict_to_element(data)
        assert elem.tag == "item"
        assert elem.find("name").text == "test"
        assert elem.find("age").text == "20"

    def test_dict_to_element_custom_tag(self):
        data = {"x": 1}
        elem = XmlUtil.dict_to_element(data, tag="record")
        assert elem.tag == "record"

    def test_list_to_element(self):
        data = [{"id": "1"}, {"id": "2"}]
        elem = XmlUtil.list_to_element(data)
        assert elem.tag == "root"
        assert len(list(elem)) == 2
        assert next(iter(elem)).tag == "item"

    def test_list_to_element_custom_tags(self):
        data = [{"id": "1"}]
        elem = XmlUtil.list_to_element(data, tag="items", item_tag="entry")
        assert elem.tag == "items"
        assert next(iter(elem)).tag == "entry"

    def test_list_to_element_scalars(self):
        data = ["a", "b", "c"]
        elem = XmlUtil.list_to_element(data)
        assert len(list(elem)) == 3
        assert next(iter(elem)).text == "a"

    def test_dict_to_xml(self):
        data = {"name": "test"}
        xml_str = XmlUtil.dict_to_xml(data)
        assert "<name>test</name>" in xml_str

    def test_list_to_xml(self):
        data = [{"id": "1"}, {"id": "2"}]
        xml_str = XmlUtil.list_to_xml(data)
        assert "<root>" in xml_str
        assert xml_str.count("<item>") == 2

    def test_indent_element(self):
        root = ET.Element("root")
        child = ET.SubElement(root, "child")
        child.text = "text"
        XmlUtil.indent_element(root)
        xml_str = ET.tostring(root, encoding="unicode")
        assert "\n" in xml_str
