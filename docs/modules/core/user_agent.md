# UserAgent 生成器 - UserAgentUtil

## 由来

在爬虫开发和接口测试中，需要模拟不同浏览器的 User-Agent。`UserAgentUtil` 提供主流浏览器 UA 字符串的随机生成，纯标准库实现。

## 方法

### 随机生成

```python
from hutool import UserAgentUtil

# 随机选择任一浏览器
ua = UserAgentUtil.user_agent()
# "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/534.0 ..."
```

### 指定浏览器

```python
# Chrome
UserAgentUtil.chrome()
# "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.5 (KHTML, like Gecko) Chrome/98.0.845.0 Safari/534.5"

# Firefox
UserAgentUtil.firefox()
# "Mozilla/5.0 (Windows NT 5.1; en-US; rv:1.9.1.20) Gecko/20100101 Firefox/72.0"

# Safari
UserAgentUtil.safari()
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/533.21.1 ..."

# Opera
UserAgentUtil.opera()
# "Opera/9.15.45.678 (Linux; en-US) Presto/2.9.168 Version/12.00"

# Internet Explorer
UserAgentUtil.internet_explorer()
# "Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.1)"

# Edge
UserAgentUtil.edge()
# "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/534.5 ... Chrome/95.0.0.0 Safari/534.5 Edg/95.0.0.0"
```

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
