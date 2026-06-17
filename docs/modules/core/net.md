# 网络工具 - NetUtil / Ipv4Util

## 由来

网络编程中经常需要判断 IP 地址、端口、内网/外网等。`NetUtil` 提供了常用的网络工具方法。

## NetUtil

### IP 地址

```python
from hutool import NetUtil

NetUtil.get_local_ip()       # "192.168.1.100"（本机 IP）
NetUtil.get_localhost()      # "127.0.0.1"
NetUtil.get_mac_address()    # "AA:BB:CC:DD:EE:FF"

# 判断内网 IP
NetUtil.is_inner("192.168.1.1")   # True
NetUtil.is_inner("10.0.0.1")      # True
NetUtil.is_inner("8.8.8.8")       # False
```

### 端口

```python
NetUtil.is_valid_port(8080)             # True
NetUtil.is_valid_port(0)                # False
NetUtil.is_usable_port(8080)            # True（端口是否可用）
NetUtil.get_usable_port()               # 获取一个可用端口
```

### IP 转换

```python
# IPv4 与长整型互转
NetUtil.ipv4_to_long("192.168.1.1")    # 3232235777
NetUtil.long_to_ipv4(3232235777)       # "192.168.1.1"
```

### 连通性

```python
NetUtil.ping("baidu.com")              # True/False
NetUtil.is_open("baidu.com", 80)       # True（端口是否开放）
```

### 新增方法

```python
# 判断内网 IP（别名）
NetUtil.is_inner_ip("192.168.1.1")   # True
NetUtil.is_inner_ip("8.8.8.8")       # False

# IP 是否在 CIDR 范围内
NetUtil.is_in_range("192.168.1.100", "192.168.1.0/24")  # True
NetUtil.is_in_range("10.0.0.1", "192.168.1.0/24")       # False

# 遮蔽 IP 地址
NetUtil.hide_ip_part("192.168.1.100")   # "192.168.1.*"

# 获取本机 IPv4 列表
NetUtil.local_ipv4s()   # ["192.168.1.100", ...]

# 获取本机主机名
NetUtil.get_local_host_name()   # "my-computer"

# 解析主机名
NetUtil.get_ip_by_host("localhost")   # "127.0.0.1"

# 补全相对 URL
NetUtil.to_absolute_url("http://example.com/a/b", "../c")
# "http://example.com/c"
```

## Ipv4Util

IPv4 地址的高级操作：

```python
from hutool import Ipv4Util, MaskBit

# 掩码操作
MaskBit.get_mask(24)         # "255.255.255.0"
MaskBit.get_mask_bit("255.255.255.0")  # 24
```

### 主机信息

```python
from hutool import NetUtil

# 获取本机主机名（与 get_localhost 相同）
NetUtil.get_host_name()       # "DESKTOP-ABC123"

# 获取本机 IP 地址（通过 UDP 探测）
NetUtil.get_host_address()    # "192.168.1.100"
```
