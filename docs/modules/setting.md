# 配置工具 - setting

## 概述

配置文件读写是应用程序的基础需求。Hutool-Python 提供了 YAML 和 Properties 两种配置文件的读写工具。

## YamlUtil

基于 PyYAML 的 YAML 文件读写。

```python
from hutool import YamlUtil

# 读取 YAML 文件
config = YamlUtil.load("config.yaml")

# 从字符串加载
config = YamlUtil.load_by_string("""
server:
  host: localhost
  port: 8080
database:
  url: jdbc:mysql://localhost/db
""")

# 导出为 YAML 字符串
yaml_str = YamlUtil.dump({"server": {"host": "localhost", "port": 8080}})

# 写入文件
YamlUtil.dump({"key": "value"}, "output.yaml")
```

## PropsUtil

Properties 格式配置文件读写。

```python
from hutool import PropsUtil

# 读取 Properties 文件
props = PropsUtil.load("application.properties")
# {"server.port": "8080", "server.host": "localhost"}

# 获取值
port = PropsUtil.get(props, "server.port")           # "8080"
host = PropsUtil.get(props, "server.host", "0.0.0.0")  # "localhost"
```

## SettingUtil

通用配置加载工具。

```python
from hutool import SettingUtil

# 加载配置文件
config = SettingUtil.load("setting.txt")
```

## 文件格式示例

### YAML 格式

```yaml
server:
  host: localhost
  port: 8080
database:
  driver: com.mysql.cj.jdbc.Driver
  url: jdbc:mysql://localhost:3306/mydb
  username: root
  password: 123456
```

### Properties 格式

```properties
server.host=localhost
server.port=8080
database.driver=com.mysql.cj.jdbc.Driver
database.url=jdbc:mysql://localhost:3306/mydb
database.username=root
database.password=123456
```
