# 分页工具 - PageUtil

## 由来

Web 开发中分页是常见需求，`PageUtil` 提供分页计算的便捷方法。

## 方法

```python
from hutool import PageUtil

# 计算总页数
PageUtil.total_page(100, 10)   # 10
PageUtil.total_page(101, 10)   # 11
PageUtil.total_page(0, 10)     # 0

# 页码彩虹（分页导航显示哪些页码）
PageUtil.rainbow(5, 10, 7)     # [2, 3, 4, 5, 6, 7, 8]

# 索引转页码
PageUtil.to_page(0, 10)        # 1（第1页）
PageUtil.to_page(15, 10)       # 2（第2页）

# 获取起始位置
PageUtil.get_start(1, 10)      # 0（第1页，每页10条）
PageUtil.get_start(3, 10)      # 20（第3页，每页10条）

# 第一页
PageUtil.first_page()          # 1

# 设置/获取首页页码
PageUtil.set_first_page_no(1)
PageUtil.get_first_page_no()       # 1

# 获取结束位置
PageUtil.get_end(2, 10)            # 20

# 转为 (start, end) 元组
start, end = PageUtil.trans_to_start_end(2, 10)  # (10, 20)

# 计算总页数
PageUtil.to_segment(100, 10)       # 10
PageUtil.to_segment(101, 10)       # 11
```
