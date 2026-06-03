"""Tests for EarthlyBranch (地支) module."""

import pytest
from bazi.core import EarthlyBranch, YinYang, WuXing


class TestEarthlyBranch:
    def test_all_branches_count(self):
        assert len(list(EarthlyBranch)) == 12

    def test_orders(self):
        assert EarthlyBranch.ZI.order == 1
        assert EarthlyBranch.HAI.order == 12

    @pytest.mark.parametrize(
        "branch, expected_yy",
        [
            (EarthlyBranch.ZI, YinYang.YANG),
            (EarthlyBranch.CHOU, YinYang.YIN),
            (EarthlyBranch.YIN, YinYang.YANG),
            (EarthlyBranch.MAO, YinYang.YIN),
            (EarthlyBranch.CHEN, YinYang.YANG),
            (EarthlyBranch.SI, YinYang.YIN),
            (EarthlyBranch.WU, YinYang.YANG),
            (EarthlyBranch.WEI, YinYang.YIN),
            (EarthlyBranch.SHEN, YinYang.YANG),
            (EarthlyBranch.YOU, YinYang.YIN),
            (EarthlyBranch.XU, YinYang.YANG),
            (EarthlyBranch.HAI, YinYang.YIN),
        ],
    )
    def test_yin_yang(self, branch, expected_yy):
        assert branch.yin_yang == expected_yy

    @pytest.mark.parametrize(
        "branch, expected_wx",
        [
            (EarthlyBranch.YIN, WuXing.WOOD),
            (EarthlyBranch.MAO, WuXing.WOOD),
            (EarthlyBranch.SI, WuXing.FIRE),
            (EarthlyBranch.WU, WuXing.FIRE),
            (EarthlyBranch.SHEN, WuXing.METAL),
            (EarthlyBranch.YOU, WuXing.METAL),
            (EarthlyBranch.HAI, WuXing.WATER),
            (EarthlyBranch.ZI, WuXing.WATER),
            (EarthlyBranch.CHEN, WuXing.EARTH),
            (EarthlyBranch.XU, WuXing.EARTH),
            (EarthlyBranch.CHOU, WuXing.EARTH),
            (EarthlyBranch.WEI, WuXing.EARTH),
        ],
    )
    def test_wuxing(self, branch, expected_wx):
        assert branch.wuxing == expected_wx

    @pytest.mark.parametrize(
        "branch, expected_zodiac",
        [
            (EarthlyBranch.ZI, "鼠"),
            (EarthlyBranch.CHOU, "牛"),
            (EarthlyBranch.YIN, "虎"),
            (EarthlyBranch.MAO, "兔"),
            (EarthlyBranch.CHEN, "龙"),
            (EarthlyBranch.SI, "蛇"),
            (EarthlyBranch.WU, "马"),
            (EarthlyBranch.WEI, "羊"),
            (EarthlyBranch.SHEN, "猴"),
            (EarthlyBranch.YOU, "鸡"),
            (EarthlyBranch.XU, "狗"),
            (EarthlyBranch.HAI, "猪"),
        ],
    )
    def test_zodiac(self, branch, expected_zodiac):
        assert branch.zodiac == expected_zodiac

    def test_from_order(self):
        assert EarthlyBranch.from_order(1) == EarthlyBranch.ZI
        assert EarthlyBranch.from_order(12) == EarthlyBranch.HAI

    def test_from_order_wraps(self):
        assert EarthlyBranch.from_order(13) == EarthlyBranch.ZI
        assert EarthlyBranch.from_order(0) == EarthlyBranch.HAI

    @pytest.mark.parametrize(
        "hour, expected",
        [
            (0, EarthlyBranch.ZI),
            (1, EarthlyBranch.CHOU),
            (3, EarthlyBranch.YIN),
            (5, EarthlyBranch.MAO),
            (7, EarthlyBranch.CHEN),
            (9, EarthlyBranch.SI),
            (11, EarthlyBranch.WU),
            (13, EarthlyBranch.WEI),
            (15, EarthlyBranch.SHEN),
            (17, EarthlyBranch.YOU),
            (19, EarthlyBranch.XU),
            (21, EarthlyBranch.HAI),
            (23.5, EarthlyBranch.ZI),
            (12.5, EarthlyBranch.WU),
        ],
    )
    def test_from_hour(self, hour, expected):
        assert EarthlyBranch.from_hour(hour) == expected

    def test_shichen_hours(self):
        start, end = EarthlyBranch.shichen_hours(EarthlyBranch.ZI)
        assert start == 23
        assert end == 1
        start, end = EarthlyBranch.shichen_hours(EarthlyBranch.WU)
        assert start == 11
        assert end == 13
