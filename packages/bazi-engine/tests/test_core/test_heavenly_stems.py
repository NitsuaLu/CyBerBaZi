"""Tests for HeavenlyStem (天干) module."""

import pytest
from bazi.core import HeavenlyStem, YinYang, WuXing


class TestHeavenlyStem:
    def test_all_stems_count(self):
        assert len(list(HeavenlyStem)) == 10

    def test_orders(self):
        assert HeavenlyStem.JIA.order == 1
        assert HeavenlyStem.YI.order == 2
        assert HeavenlyStem.BING.order == 3
        assert HeavenlyStem.DING.order == 4
        assert HeavenlyStem.WU.order == 5
        assert HeavenlyStem.JI.order == 6
        assert HeavenlyStem.GENG.order == 7
        assert HeavenlyStem.XIN.order == 8
        assert HeavenlyStem.REN.order == 9
        assert HeavenlyStem.GUI.order == 10

    @pytest.mark.parametrize(
        "stem, expected_yy",
        [
            (HeavenlyStem.JIA, YinYang.YANG),
            (HeavenlyStem.YI, YinYang.YIN),
            (HeavenlyStem.BING, YinYang.YANG),
            (HeavenlyStem.DING, YinYang.YIN),
            (HeavenlyStem.WU, YinYang.YANG),
            (HeavenlyStem.JI, YinYang.YIN),
            (HeavenlyStem.GENG, YinYang.YANG),
            (HeavenlyStem.XIN, YinYang.YIN),
            (HeavenlyStem.REN, YinYang.YANG),
            (HeavenlyStem.GUI, YinYang.YIN),
        ],
    )
    def test_yin_yang(self, stem, expected_yy):
        assert stem.yin_yang == expected_yy

    @pytest.mark.parametrize(
        "stem, expected_wx",
        [
            (HeavenlyStem.JIA, WuXing.WOOD),
            (HeavenlyStem.YI, WuXing.WOOD),
            (HeavenlyStem.BING, WuXing.FIRE),
            (HeavenlyStem.DING, WuXing.FIRE),
            (HeavenlyStem.WU, WuXing.EARTH),
            (HeavenlyStem.JI, WuXing.EARTH),
            (HeavenlyStem.GENG, WuXing.METAL),
            (HeavenlyStem.XIN, WuXing.METAL),
            (HeavenlyStem.REN, WuXing.WATER),
            (HeavenlyStem.GUI, WuXing.WATER),
        ],
    )
    def test_wuxing(self, stem, expected_wx):
        assert stem.wuxing == expected_wx

    def test_from_order(self):
        assert HeavenlyStem.from_order(1) == HeavenlyStem.JIA
        assert HeavenlyStem.from_order(10) == HeavenlyStem.GUI

    def test_from_order_wraps(self):
        assert HeavenlyStem.from_order(11) == HeavenlyStem.JIA
        assert HeavenlyStem.from_order(0) == HeavenlyStem.GUI
        assert HeavenlyStem.from_order(21) == HeavenlyStem.JIA
