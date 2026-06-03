"""Tests for WuXing (五行) module."""

from bazi.core import WuXing


class TestWuXingBasics:
    def test_all_elements_present(self):
        assert len(list(WuXing)) == 5
        assert WuXing.WOOD.value == "木"
        assert WuXing.FIRE.value == "火"
        assert WuXing.EARTH.value == "土"
        assert WuXing.METAL.value == "金"
        assert WuXing.WATER.value == "水"

    def test_generating_cycle(self):
        # 木生火 火生土 土生金 金生水 水生木
        assert WuXing.WOOD.generates() == WuXing.FIRE
        assert WuXing.FIRE.generates() == WuXing.EARTH
        assert WuXing.EARTH.generates() == WuXing.METAL
        assert WuXing.METAL.generates() == WuXing.WATER
        assert WuXing.WATER.generates() == WuXing.WOOD

    def test_generated_by(self):
        assert WuXing.FIRE.generated_by() == WuXing.WOOD
        assert WuXing.EARTH.generated_by() == WuXing.FIRE
        assert WuXing.METAL.generated_by() == WuXing.EARTH
        assert WuXing.WATER.generated_by() == WuXing.METAL
        assert WuXing.WOOD.generated_by() == WuXing.WATER

    def test_overcoming_cycle(self):
        # 木克土 土克水 水克火 火克金 金克木
        assert WuXing.WOOD.overcomes() == WuXing.EARTH
        assert WuXing.EARTH.overcomes() == WuXing.WATER
        assert WuXing.WATER.overcomes() == WuXing.FIRE
        assert WuXing.FIRE.overcomes() == WuXing.METAL
        assert WuXing.METAL.overcomes() == WuXing.WOOD

    def test_overcome_by(self):
        assert WuXing.EARTH.overcome_by() == WuXing.WOOD
        assert WuXing.WATER.overcome_by() == WuXing.EARTH
        assert WuXing.FIRE.overcome_by() == WuXing.WATER
        assert WuXing.METAL.overcome_by() == WuXing.FIRE
        assert WuXing.WOOD.overcome_by() == WuXing.METAL
