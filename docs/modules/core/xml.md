# XML 工具 - XmlUtil

## 由来

XML 在配置文件、数据交换等场景中仍然广泛使用。`XmlUtil` 基于 Python 内置的 `xml.etree.ElementTree` 封装了常用的 XML 操作。

## 方法

### 解析

```python
from hutool import XmlUtil

xml_str = "<root><name>test</name><value>123</value></root>"

# 解析为 Element
element = XmlUtil.read_xml(xml_str)

# 解析为字典
data = XmlUtil.parse_to_map(xml_str)
# {"name": "test", "value": "123"}
```

### 生成

```python
# 字典转 XML
xml = XmlUtil.map_to_xml({"name": "test", "value": "123"}, "root")
# '<?xml version="1.0" ?><root><name>test</name><value>123</value></root>'

# 自定义根节点
xml = XmlUtil.to_xml_str("config", {"key": "value"})
```

### 格式化

```python
# 格式化输出
formatted = XmlUtil.format(xml_str)
pretty = XmlUtil.pretty_print(xml_str)

# formatXml — 美化缩进
xml = '<root><name>test</name><value>123</value></root>'
XmlUtil.format_xml(xml, indent=2)
# <root>
#   <name>test</name>
#   <value>123</value>
# </root>
```

### XPath

```python
# XPath 查询
elements = XmlUtil.get_element_by_xpath(element, "./name")
text = XmlUtil.get_element_text(element, "./name")  # "test"
```

### 工具

```python
# 清理无效 XML 字符
clean = XmlUtil.clean_invalid(xml_str)

# 创建空 XML 根元素
root = XmlUtil.create_xml("root")

# 获取根元素
root = XmlUtil.get_root_element("<root><child/></root>")

# 获取所有匹配标签的元素
items = XmlUtil.get_elements(root, "item")

# 获取第一个匹配标签的元素
child = XmlUtil.get_element(root, "child")
```

### Bean/XML 互转

```python
# dict/Bean 转 XML
data = {"name": "test", "value": 123}
xml = XmlUtil.bean_to_xml(data, root_tag="config")

# XML 转 dataclass
from dataclasses import dataclass
@dataclass
class Config:
    name: str = ""
    value: int = 0

obj = XmlUtil.xml_to_bean('<config><name>test</name><value>123</value></config>', Config)
# Config(name="test", value=123)

# XML 转字典
data = XmlUtil.xml_to_map('<root><a>1</a><b>2</b></root>')
# {"a": "1", "b": "2"}

# 字典转 XML 字符串
xml_str = XmlUtil.map_to_xml_str({"name": "test"}, root_tag="root")
```

### XPath 查询（增强）

```python
from hutool import XmlUtil

element = XmlUtil.parse_xml('<root><item id="1">A</item><item id="2">B</item></root>')

# 获取文本
text = XmlUtil.get_by_xpath(element, "./item[@id='1']")  # "A"

# 获取节点
node = XmlUtil.get_node_by_xpath(element, "./item")

# 获取节点列表
nodes = XmlUtil.get_node_list_by_xpath(element, "./item")
```

### XML 解析与读取

```python
# 解析 XML 字符串
element = XmlUtil.parse_xml('<root><child/></root>')

# 读取 XML 文件
element = XmlUtil.read_xml("/path/to/config.xml")
```

### XML 转义

```python
# XML 特殊字符转义
XmlUtil.escape_xml('Tom & Jerry <"friends">')
# "Tom &amp; Jerry &lt;&quot;friends&quot;&gt;"

# XML 反转义
XmlUtil.unescape_xml("Tom &amp; Jerry")
# "Tom & Jerry"
```

### XSLT 转换

```python
# XSLT 转换（需 lxml）
xslt_str = '<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"><xsl:template match="root"><output><xsl:value-of select="name"/></output></xsl:template></xsl:stylesheet>'
result = XmlUtil.transform_xml('<root><name>test</name></root>', xslt_str)
```

### 写入文件

```python
# writeObjectAsXml — 将对象写为 XML 文件
data = {"host": "localhost", "port": 8080}
XmlUtil.write_object_as_xml(data, "/path/to/config.xml", root_tag="server")
```
