from hutool import CoordinateUtil


class TestCoordinateUtil:
    def test_wgs84_to_gcj02(self):
        result = CoordinateUtil.wgs84_to_gcj02(116.397128, 39.916527)
        assert result is not None
        assert abs(result.longitude - 116.397128) > 0.001  # Should be offset

    def test_gcj02_to_wgs84(self):
        result = CoordinateUtil.gcj02_to_wgs84(116.404, 39.915)
        assert result is not None

    def test_gcj02_to_bd09(self):
        result = CoordinateUtil.gcj02_to_bd09(116.404, 39.915)
        assert result is not None
        assert result.longitude > 116.404  # BD09 should be offset north-east

    def test_bd09_to_gcj02(self):
        result = CoordinateUtil.bd09_to_gcj02(116.404, 39.915)
        assert result is not None

    def test_roundtrip_gcj02_bd09(self):
        original_lng, original_lat = 116.404, 39.915
        gcj_to_bd = CoordinateUtil.gcj02_to_bd09(original_lng, original_lat)
        bd_to_gcj = CoordinateUtil.bd09_to_gcj02(gcj_to_bd.longitude, gcj_to_bd.latitude)
        assert abs(bd_to_gcj.longitude - original_lng) < 0.0001
        assert abs(bd_to_gcj.latitude - original_lat) < 0.0001

    def test_wgs84_to_bd09(self):
        result = CoordinateUtil.wgs84_to_bd09(116.397128, 39.916527)
        assert result is not None

    def test_bd09_to_wgs84(self):
        result = CoordinateUtil.bd09_to_wgs84(116.404, 39.915)
        assert result is not None
