import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, Optional
from xml.dom import minidom


class XmlUtil:
    """XML工具类"""

    @staticmethod
    def read_xml(xml_str_or_path: str) -> ET.Element:
        """读取XML（字符串或文件路径）

        支持传入XML字符串或文件路径，自动判断并解析。

        :param xml_str_or_path: XML字符串或文件路径
        :return: 解析后的XML根元素
        """
        xml_str_or_path = xml_str_or_path.strip()
        if xml_str_or_path.startswith("<"):
            return ET.fromstring(xml_str_or_path)
        else:
            tree = ET.parse(xml_str_or_path)
            return tree.getroot()

    @staticmethod
    def parse_to_map(xml_str: str) -> dict:
        """XML转字典

        将XML字符串递归转换为嵌套字典结构。如果同名子元素出现多次，值为列表。

        :param xml_str: XML字符串
        :return: 转换后的字典
        """
        root = ET.fromstring(xml_str) if xml_str.strip().startswith("<") else ET.parse(xml_str).getroot()

        def _element_to_dict(element: ET.Element) -> Any:
            children = list(element)
            if not children:
                text = element.text
                if text is not None:
                    text = text.strip()
                return text if text else ""

            result: Dict[str, Any] = {}
            for child in children:
                child_data = _element_to_dict(child)
                if child.tag in result:
                    existing = result[child.tag]
                    if isinstance(existing, list):
                        existing.append(child_data)
                    else:
                        result[child.tag] = [existing, child_data]
                else:
                    result[child.tag] = child_data

            # 添加属性
            if element.attrib:
                for key, value in element.attrib.items():
                    result[f"@{key}"] = value

            return result

        tag = root.tag
        return {tag: _element_to_dict(root)}

    @staticmethod
    def to_xml_str(root_name: str, data: dict) -> str:
        """字典转XML字符串

        :param root_name: 根元素名称
        :param data: 待转换的字典数据
        :return: XML字符串
        """
        return XmlUtil.map_to_xml(data, root_name)

    @staticmethod
    def map_to_xml(data: dict, root_name: str = "root") -> str:
        """字典转XML

        将字典递归转换为XML字符串。

        :param data: 待转换的字典数据
        :param root_name: 根元素名称，默认为"root"
        :return: XML字符串
        """
        root = ET.Element(root_name)
        XmlUtil._build_xml(root, data)
        return ET.tostring(root, encoding="unicode")

    @staticmethod
    def _build_xml(parent: ET.Element, data: Any) -> None:
        """递归构建XML元素

        :param parent: 父元素
        :param data: 当前数据（字典或值）
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if key.startswith("@"):
                    # XML属性
                    parent.set(key[1:], str(value))
                elif isinstance(value, list):
                    for item in value:
                        child = ET.SubElement(parent, key)
                        XmlUtil._build_xml(child, item)
                else:
                    child = ET.SubElement(parent, key)
                    XmlUtil._build_xml(child, value)
        else:
            parent.text = str(data) if data is not None else ""

    @staticmethod
    def format_xml(xml_str: str) -> str:
        """格式化XML

        将XML字符串格式化为带缩进的可读格式。

        :param xml_str: 待格式化的XML字符串
        :return: 格式化后的XML字符串
        """
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="  ", encoding=None)
        # 去除minidom添加的多余空行
        lines = [line for line in pretty_xml.split("\n") if line.strip()]
        return "\n".join(lines)

    @staticmethod
    def get_element_text(element: ET.Element, xpath: str) -> Optional[str]:
        """获取元素文本

        通过xpath查找子元素并返回其文本内容。

        :param element: XML元素
        :param xpath: 子元素的标签路径，如 "child/subchild"
        :return: 元素文本内容，未找到则返回None
        """
        target = element.find(xpath)
        if target is not None:
            return target.text
        return None

    @staticmethod
    def clean_invalid(xml_str: str) -> str:
        """清理XML中的非法字符

        移除XML规范中不允许的控制字符（除了制表符、换行符、回车符）。

        :param xml_str: 原始XML字符串
        :return: 清理后的XML字符串
        """
        # 移除非法字符：XML合法字符为 #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]
        valid_xml_chars = re.compile(
            r"[^\x09\x0A\x0D\x20-\x7E\x80-\xFF"
            r"Ā-퟿-�"
            r"\U00010000-\U0010FFFF]"
        )
        return valid_xml_chars.sub("", xml_str)
