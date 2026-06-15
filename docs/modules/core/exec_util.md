# 并发执行工具 - ExecUtil

## 由来

批量任务并发执行是常见的性能优化手段。`ExecUtil` 基于 `concurrent.futures` 标准库，提供线程池和进程池的批量任务提交接口。

## 方法

### 线程池

适用于 I/O 密集型任务（网络请求、文件读写等）：

```python
from hutool import ExecUtil
import time

def fetch(url):
    time.sleep(0.1)  # 模拟 I/O
    return f"data from {url}"

urls = ["url1", "url2", "url3", "url4"]
results = ExecUtil.multi_thread_submit(fetch, urls, max_workers=4)
# results 包含所有结果（顺序可能不同）
```

### 进程池

适用于 CPU 密集型任务（数值计算、数据处理等）：

```python
def compute(n):
    return n ** 2

results = ExecUtil.multi_process_submit(compute, [1, 2, 3, 4, 5])
# [1, 4, 9, 16, 25]
```

```{note}
进程池要求 `func` 和参数必须可 pickle 序列化。对于 I/O 密集型任务，建议使用线程池。
```

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
