# 坐标转换工具 - CoordinateUtil

## 由来

中国地图存在多个坐标系（WGS84、GCJ02、BD09），它们之间需要相互转换。`CoordinateUtil` 提供了常用的坐标转换方法。

## 坐标系说明

| 坐标系 | 说明 | 使用场景 |
|--------|------|---------|
| WGS84 | GPS 全球定位系统坐标 | 国际标准、GPS 设备 |
| GCJ02 | 国测局坐标（火星坐标） | 高德地图、腾讯地图 |
| BD09 | 百度坐标 | 百度地图 |

## 方法

```python
from hutool import CoordinateUtil

# WGS84 <-> GCJ02（GPS <-> 火星坐标）
coord = CoordinateUtil.wgs84_to_gcj02(116.397128, 39.916527)
print(coord.longitude, coord.latitude)

coord = CoordinateUtil.gcj02_to_wgs84(116.407128, 39.926527)

# GCJ02 <-> BD09（火星坐标 <-> 百度坐标）
coord = CoordinateUtil.gcj02_to_bd09(116.407128, 39.926527)
coord = CoordinateUtil.bd09_to_gcj02(116.417128, 39.936527)

# WGS84 <-> BD09（一步到位）
coord = CoordinateUtil.wgs84_to_bd09(116.397128, 39.916527)
coord = CoordinateUtil.bd09_to_wgs84(116.417128, 39.936527)
```

### Coordinate 对象

```python
coord = CoordinateUtil.wgs84_to_gcj02(116.397128, 39.916527)
print(coord.longitude)  # 经度
print(coord.latitude)   # 纬度
```
