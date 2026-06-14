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
```
