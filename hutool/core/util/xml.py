import html
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

    @staticmethod
    def create_xml(root_name: str) -> ET.Element:
        """创建空 XML 根元素。

        :param root_name: 根元素名称
        :return: XML 根元素
        """
        return ET.Element(root_name)

    @staticmethod
    def get_root_element(xml_str: str) -> ET.Element:
        """获取 XML 的根元素。

        :param xml_str: XML 字符串
        :return: 根元素
        """
        return ET.fromstring(xml_str)

    @staticmethod
    def get_elements(element: ET.Element, tag: str) -> list:
        """获取所有匹配 tag 的子元素列表。

        :param element: XML 元素
        :param tag: 子元素标签名
        :return: 匹配的元素列表
        """
        return list(element.iter(tag))

    @staticmethod
    def get_element(element: ET.Element, tag: str) -> Optional[ET.Element]:
        """获取第一个匹配 tag 的子元素。

        :param element: XML 元素
        :param tag: 子元素标签名
        :return: 匹配的元素，未找到返回 None
        """
        return element.find(tag)

    @staticmethod
    def element_text(element: ET.Element, tag: str) -> Optional[str]:
        """获取子元素的文本内容。

        :param element: 父元素
        :param tag: 子元素标签名
        :return: 子元素文本，未找到返回 None
        """
        child = element.find(tag)
        if child is None:
            return None
        return child.text

    @staticmethod
    def clean_comment(xml_str: str) -> str:
        """清除 XML 注释。

        :param xml_str: XML 字符串
        :return: 清除注释后的 XML 字符串
        """
        return re.sub(r"<!--.*?-->", "", xml_str, flags=re.DOTALL)

    @staticmethod
    def append_child(parent: ET.Element, tag: str, text: Optional[str] = None) -> ET.Element:
        """为父元素添加子元素。

        :param parent: 父元素
        :param tag: 子元素标签名
        :param text: 子元素文本内容，可选
        :return: 新创建的子元素
        """
        child = ET.SubElement(parent, tag)
        if text is not None:
            child.text = text
        return child

    @staticmethod
    def append_text(element: ET.Element, text: str) -> None:
        """为元素添加/追加文本内容。

        :param element: XML 元素
        :param text: 文本内容
        """
        if element.text:
            element.text += text
        else:
            element.text = text

    @staticmethod
    def is_element(obj: Any) -> bool:
        """判断对象是否为 XML Element。

        :param obj: 对象
        :return: 是否为 Element
        """
        return isinstance(obj, ET.Element)

    @staticmethod
    def to_str(element: ET.Element, pretty: bool = False, charset: str = "utf-8") -> str:
        """将 XML 元素序列化为字符串。

        :param element: XML 元素
        :param pretty: 是否格式化输出
        :param charset: 字符集
        :return: XML 字符串
        """
        xml_bytes = ET.tostring(element, encoding=charset, xml_declaration=True)
        result = xml_bytes.decode(charset)
        if pretty:
            result = XmlUtil.format_xml(result)
        return result

    @staticmethod
    def to_file(element: ET.Element, file_path: str, charset: str = "utf-8") -> None:
        """将 XML 元素写入文件。

        :param element: XML 元素
        :param file_path: 文件路径
        :param charset: 字符集
        """
        tree = ET.ElementTree(element)
        tree.write(file_path, encoding=charset, xml_declaration=True)

    @staticmethod
    def write(element: ET.Element, stream, charset: str = "utf-8") -> None:
        """将 XML 元素写入流。

        :param element: XML 元素
        :param stream: 可写流
        :param charset: 字符集
        """
        xml_bytes = ET.tostring(element, encoding=charset, xml_declaration=True)
        if hasattr(stream, "mode") and "b" in getattr(stream, "mode", ""):
            stream.write(xml_bytes)
        else:
            stream.write(xml_bytes.decode(charset))

    @staticmethod
    def create_document() -> ET.Element:
        """创建一个空的 XML 文档根元素。

        :return: 根为 ``<root/>`` 的 Element
        """
        return ET.Element("root")

    @staticmethod
    def bean_to_xml(obj: Any, root_tag: str = "root") -> str:
        """将字典或数据类对象转换为XML字符串。

        支持字典和带 ``__dict__`` 属性的数据类对象，递归处理嵌套结构。

        :param obj: 字典或数据类对象
        :param root_tag: 根元素标签名，默认为 ``"root"``
        :return: XML字符串
        """
        if hasattr(obj, "__dict__") and not isinstance(obj, dict):
            obj = obj.__dict__
        if not isinstance(obj, dict):
            raise TypeError("参数必须为字典或数据类对象")
        root = ET.Element(root_tag)
        XmlUtil._build_xml(root, obj)
        return ET.tostring(root, encoding="unicode")

    @staticmethod
    def xml_to_bean(xml_str: str, target_class: Any = None) -> Any:
        """将XML字符串转换为数据类对象或字典。

        若指定 ``target_class``，则将解析后的字典作为关键字参数传入构造函数；
        否则直接返回嵌套字典。

        :param xml_str: XML字符串
        :param target_class: 目标数据类，为 ``None`` 时返回字典
        :return: 数据类实例或字典
        """
        result = XmlUtil.parse_to_map(xml_str)
        if target_class is not None:
            # 取根元素下包裹的字典
            root_key = next(iter(result))
            data = result[root_key]
            if isinstance(data, dict):
                return target_class(**data)
            return target_class(data)
        return result

    @staticmethod
    def xml_to_map(xml_str: str) -> dict:
        """XML转字典（parse_to_map 的别名）。

        :param xml_str: XML字符串
        :return: 转换后的字典
        """
        return XmlUtil.parse_to_map(xml_str)

    @staticmethod
    def map_to_xml_str(map_data: dict, root_tag: str = "root") -> str:
        """字典转XML字符串（map_to_xml 的别名）。

        :param map_data: 待转换的字典数据
        :param root_tag: 根元素标签名，默认为 ``"root"``
        :return: XML字符串
        """
        return XmlUtil.map_to_xml(map_data, root_tag)

    @staticmethod
    def get_by_xpath(element: ET.Element, xpath: str) -> Optional[str]:
        """通过XPath查询获取元素文本。

        使用 ``element.find`` 查找第一个匹配元素并返回其文本内容。

        :param element: XML元素
        :param xpath: XPath表达式
        :return: 元素文本内容，未找到则返回 ``None``
        """
        target = element.find(xpath)
        if target is not None:
            return target.text
        return None

    @staticmethod
    def get_node_by_xpath(element: ET.Element, xpath: str) -> Optional[ET.Element]:
        """通过XPath查询获取单个节点。

        :param element: XML元素
        :param xpath: XPath表达式
        :return: 匹配的元素节点，未找到则返回 ``None``
        """
        return element.find(xpath)

    @staticmethod
    def get_node_list_by_xpath(element: ET.Element, xpath: str) -> list:
        """通过XPath查询获取节点列表。

        :param element: XML元素
        :param xpath: XPath表达式
        :return: 匹配的元素节点列表
        """
        return list(element.findall(xpath))

    @staticmethod
    def parse_xml(xml_str: str) -> ET.Element:
        """解析XML字符串并返回根元素。

        :param xml_str: XML字符串
        :return: 解析后的XML根元素
        """
        return ET.fromstring(xml_str)

    @staticmethod
    def read_xml_file(file_path: str) -> ET.Element:
        """读取XML文件并返回根元素。

        :param file_path: XML文件路径
        :return: 解析后的XML根元素
        """
        tree = ET.parse(file_path)
        return tree.getroot()

    @staticmethod
    def transform_xml(xml_str: str, xslt_str: str) -> str:
        """使用XSLT对XML进行基本转换。

        基于 ``ElementTree`` 实现的简易转换，仅支持 ``<xsl:value-of select="..."/>``
        标签的文本替换。复杂XSLT场景建议使用 ``lxml`` 等专业库。

        :param xml_str: XML字符串
        :param xslt_str: XSLT样式表字符串
        :return: 转换后的XML字符串
        """
        root = ET.fromstring(xml_str)
        xslt_root = ET.fromstring(xslt_str)

        # 查找所有 xsl:value-of 指令并做文本替换
        for value_of in xslt_root.iter("{http://www.w3.org/1999/XSL/Transform}value-of"):
            select = value_of.get("select", "")
            if select:
                found = root.find(select)
                if found is not None and found.text:
                    value_of.text = found.text
                    value_of.tag = "span"
                    for attr in list(value_of.attrib):
                        del value_of.attrib[attr]

        return ET.tostring(xslt_root, encoding="unicode")

    @staticmethod
    def escape_xml(text: str) -> str:
        """转义XML特殊字符。

        将 ``&``、``<``、``>``、``"``、``'`` 转义为对应的XML实体。

        :param text: 原始文本
        :return: 转义后的文本
        """
        return html.escape(text, quote=True)

    @staticmethod
    def unescape_xml(text: str) -> str:
        """反转义XML特殊字符。

        将XML实体还原为原始字符。

        :param text: 包含XML实体的文本
        :return: 还原后的文本
        """
        return html.unescape(text)

    @staticmethod
    def format_xml_pretty(xml_str: str, indent: int = 2) -> str:
        """使用自定义缩进格式化XML。

        :param xml_str: 待格式化的XML字符串
        :param indent: 缩进空格数，默认为 ``2``
        :return: 格式化后的XML字符串
        """
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent=" " * indent, encoding=None)
        lines = [line for line in pretty_xml.split("\n") if line.strip()]
        return "\n".join(lines)

    @staticmethod
    def write_object_as_xml(obj: Any, file_path: str, root_tag: str = "root") -> None:
        """将字典或数据类对象以XML格式写入文件。

        :param obj: 字典或数据类对象
        :param file_path: 目标文件路径
        :param root_tag: 根元素标签名，默认为 ``"root"``
        """
        xml_str = XmlUtil.bean_to_xml(obj, root_tag)
        tree = ET.ElementTree(ET.fromstring(xml_str))
        tree.write(file_path, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def dict_to_element(data: dict, tag: str = "item") -> ET.Element:
        """将 dict 转换为 XML Element。

        :param data: 字典数据
        :param tag: 根元素标签名，默认 ``"item"``
        :return: XML Element 对象

        ::

            elem = XmlUtil.dict_to_element({"name": "test", "age": 20})
            assert elem.tag == "item"
            assert elem.find("name").text == "test"
        """
        root = ET.Element(tag)
        XmlUtil._build_xml(root, data)
        return root

    @staticmethod
    def list_to_element(data: list, tag: str = "root", item_tag: str = "item") -> ET.Element:
        """将 list 转换为 XML Element。

        :param data: 列表数据
        :param tag: 根元素标签名，默认 ``"root"``
        :param item_tag: 子项标签名，默认 ``"item"``
        :return: XML Element 对象

        ::

            elem = XmlUtil.list_to_element([{"id": 1}, {"id": 2}])
            assert elem.tag == "root"
            assert len(list(elem)) == 2
        """
        root = ET.Element(tag)
        for item in data:
            child = ET.SubElement(root, item_tag)
            if isinstance(item, dict):
                XmlUtil._build_xml(child, item)
            elif isinstance(item, (list, tuple)):
                XmlUtil._build_xml(child, {"value": str(item)})
            else:
                child.text = str(item) if item is not None else ""
        return root

    @staticmethod
    def dict_to_xml(data: dict, tag: str = "item", encoding: str = "utf-8") -> str:
        """将 dict 转换为 XML 字符串。

        :param data: 字典数据
        :param tag: 根元素标签名
        :param encoding: 编码格式，默认 ``"utf-8"``
        :return: XML 字符串
        """
        elem = XmlUtil.dict_to_element(data, tag)
        return XmlUtil.to_str(elem, charset=encoding)

    @staticmethod
    def list_to_xml(data: list, tag: str = "root", item_tag: str = "item", encoding: str = "utf-8") -> str:
        """将 list 转换为 XML 字符串。

        :param data: 列表数据
        :param tag: 根元素标签名
        :param item_tag: 子项标签名
        :param encoding: 编码格式
        :return: XML 字符串
        """
        elem = XmlUtil.list_to_element(data, tag, item_tag)
        return XmlUtil.to_str(elem, charset=encoding)

    @staticmethod
    def indent_element(element: ET.Element, level: int = 0, indent: str = "  ") -> None:
        """对 XML Element 递归添加缩进（美化输出）。

        :param element: XML Element 对象
        :param level: 当前缩进层级
        :param indent: 每层缩进字符，默认两个空格
        """
        i = "\n" + level * indent
        if len(element):
            if not element.text or not element.text.strip():
                element.text = i + indent
            if not element.tail or not element.tail.strip():
                element.tail = i
            for idx, child in enumerate(element):
                XmlUtil.indent_element(child, level + 1, indent)
                if idx == len(element) - 1:
                    if not child.tail or not child.tail.strip():
                        child.tail = i
        else:
            if level and (not element.tail or not element.tail.strip()):
                element.tail = i
