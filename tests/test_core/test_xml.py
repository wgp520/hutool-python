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
