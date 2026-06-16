import math
from typing import NamedTuple


class Coordinate(NamedTuple):
    """坐标点"""

    longitude: float
    latitude: float


class CoordinateUtil:
    """坐标工具类，提供WGS84/GCJ02/BD09坐标系转换

    WGS84: GPS全球定位系统使用的坐标系
    GCJ02: 国测局坐标系（火星坐标系），国内地图服务使用
    BD09: 百度坐标系，在GCJ02基础上进一步加密
    """

    # 常量
    _PI = math.pi
    _A = 6378245.0  # 克拉索夫斯基椭球长半轴（米）
    _EE = 0.00669342162296594  # 偏心率平方

    @staticmethod
    def out_of_china(lng: float, lat: float) -> bool:
        """判断是否在中国范围外（公开方法）

        :param lng: 经度
        :param lat: 纬度
        :return: 是否在中国范围外
        """
        return not (72.004 <= lng <= 137.8347 and 0.8293 <= lat <= 55.8271)

    @staticmethod
    def wgs84_to_mercator(lng: float, lat: float) -> Coordinate:
        """WGS84 转 Web Mercator 投影坐标

        :param lng: WGS84 经度
        :param lat: WGS84 纬度
        :return: Web Mercator 坐标 (x, y)，单位为米
        """
        x = lng * 20037508.34 / 180.0
        y = math.log(math.tan((90.0 + lat) * math.pi / 360.0)) / (math.pi / 180.0)
        y = y * 20037508.34 / 180.0
        return Coordinate(x, y)

    @staticmethod
    def mercator_to_wgs84(x: float, y: float) -> Coordinate:
        """Web Mercator 投影坐标转 WGS84

        :param x: Mercator X 坐标（米）
        :param y: Mercator Y 坐标（米）
        :return: WGS84 坐标 (经度, 纬度)
        """
        lng = x / 20037508.34 * 180.0
        lat = y / 20037508.34 * 180.0
        lat = 180.0 / math.pi * (2.0 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
        return Coordinate(lng, lat)

    @staticmethod
    def _out_of_china(lng: float, lat: float) -> bool:
        """判断是否在中国范围外

        :param lng: 经度
        :param lat: 纬度
        :return: 是否在中国范围外
        """
        return not (72.004 <= lng <= 137.8347 and 0.8293 <= lat <= 55.8271)

    @staticmethod
    def _transform_lat(lng: float, lat: float) -> float:
        """纬度转换偏移量计算

        :param lng: 经度
        :param lat: 纬度
        :return: 纬度偏移量
        """
        pi = CoordinateUtil._PI
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
        ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * pi) + 320.0 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
        return ret

    @staticmethod
    def _transform_lng(lng: float, lat: float) -> float:
        """经度转换偏移量计算

        :param lng: 经度
        :param lat: 纬度
        :return: 经度偏移量
        """
        pi = CoordinateUtil._PI
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
        ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
        return ret

    @staticmethod
    def _delta(lng: float, lat: float) -> tuple:
        """计算GCJ-02偏移量

        :param lng: WGS84经度
        :param lat: WGS84纬度
        :return: (经度偏移, 纬度偏移)
        """
        pi = CoordinateUtil._PI
        a = CoordinateUtil._A
        ee = CoordinateUtil._EE
        dlat = CoordinateUtil._transform_lat(lng - 105.0, lat - 35.0)
        dlng = CoordinateUtil._transform_lng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * pi
        magic = math.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
        dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
        return dlng, dlat

    @staticmethod
    def wgs84_to_gcj02(lng: float, lat: float) -> Coordinate:
        """WGS84转GCJ02（GPS转国测局坐标）

        :param lng: WGS84经度
        :param lat: WGS84纬度
        :return: GCJ02坐标
        """
        if CoordinateUtil._out_of_china(lng, lat):
            return Coordinate(lng, lat)
        dlng, dlat = CoordinateUtil._delta(lng, lat)
        return Coordinate(lng + dlng, lat + dlat)

    @staticmethod
    def gcj02_to_wgs84(lng: float, lat: float) -> Coordinate:
        """GCJ02转WGS84

        :param lng: GCJ02经度
        :param lat: GCJ02纬度
        :return: WGS84坐标
        """
        if CoordinateUtil._out_of_china(lng, lat):
            return Coordinate(lng, lat)
        dlng, dlat = CoordinateUtil._delta(lng, lat)
        return Coordinate(lng - dlng, lat - dlat)

    @staticmethod
    def gcj02_to_bd09(lng: float, lat: float) -> Coordinate:
        """GCJ02转BD09（转百度坐标）

        :param lng: GCJ02经度
        :param lat: GCJ02纬度
        :return: BD09坐标
        """
        pi = CoordinateUtil._PI
        z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * pi * 3000.0 / 180.0)
        theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * pi * 3000.0 / 180.0)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return Coordinate(bd_lng, bd_lat)

    @staticmethod
    def bd09_to_gcj02(lng: float, lat: float) -> Coordinate:
        """BD09转GCJ02

        :param lng: BD09经度
        :param lat: BD09纬度
        :return: GCJ02坐标
        """
        pi = CoordinateUtil._PI
        x = lng - 0.0065
        y = lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * pi * 3000.0 / 180.0)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * pi * 3000.0 / 180.0)
        gcj_lng = z * math.cos(theta)
        gcj_lat = z * math.sin(theta)
        return Coordinate(gcj_lng, gcj_lat)

    @staticmethod
    def wgs84_to_bd09(lng: float, lat: float) -> Coordinate:
        """WGS84转BD09

        :param lng: WGS84经度
        :param lat: WGS84纬度
        :return: BD09坐标
        """
        gcj = CoordinateUtil.wgs84_to_gcj02(lng, lat)
        return CoordinateUtil.gcj02_to_bd09(gcj.longitude, gcj.latitude)

    @staticmethod
    def bd09_to_wgs84(lng: float, lat: float) -> Coordinate:
        """BD09转WGS84

        :param lng: BD09经度
        :param lat: BD09纬度
        :return: WGS84坐标
        """
        gcj = CoordinateUtil.bd09_to_gcj02(lng, lat)
        return CoordinateUtil.gcj02_to_wgs84(gcj.longitude, gcj.latitude)

    @staticmethod
    def distance(lng1: float, lat1: float, lng2: float, lat2: float) -> float:
        """计算两点间距离（米），使用Haversine公式

        :param lng1: 第一个点的经度
        :param lat1: 第一个点的纬度
        :param lng2: 第二个点的经度
        :param lat2: 第二个点的纬度
        :return: 两点间的距离（米）
        """
        earth_radius = 6371000.0  # 地球平均半径（米）

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return earth_radius * c
