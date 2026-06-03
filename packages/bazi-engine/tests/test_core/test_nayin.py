"""Tests for NaYin (纳音) module."""

import pytest
from bazi.core import HeavenlyStem, EarthlyBranch, WuXing, get_nayin, get_nayin_by_sexagenary_index


class TestNayin:
    @pytest.mark.parametrize(
        "stem, branch, expected_name, expected_wx",
        [
            (HeavenlyStem.JIA, EarthlyBranch.ZI, "海中金", WuXing.METAL),
            (HeavenlyStem.YI, EarthlyBranch.CHOU, "海中金", WuXing.METAL),
            (HeavenlyStem.BING, EarthlyBranch.YIN, "炉中火", WuXing.FIRE),
            (HeavenlyStem.DING, EarthlyBranch.MAO, "炉中火", WuXing.FIRE),
            (HeavenlyStem.WU, EarthlyBranch.CHEN, "大林木", WuXing.WOOD),
            (HeavenlyStem.JI, EarthlyBranch.SI, "大林木", WuXing.WOOD),
            (HeavenlyStem.GENG, EarthlyBranch.WU, "路旁土", WuXing.EARTH),
            (HeavenlyStem.XIN, EarthlyBranch.WEI, "路旁土", WuXing.EARTH),
            (HeavenlyStem.REN, EarthlyBranch.SHEN, "剑锋金", WuXing.METAL),
            (HeavenlyStem.GUI, EarthlyBranch.YOU, "剑锋金", WuXing.METAL),
            (HeavenlyStem.REN, EarthlyBranch.XU, "大海水", WuXing.WATER),
            (HeavenlyStem.GUI, EarthlyBranch.HAI, "大海水", WuXing.WATER),
        ],
    )
    def test_get_nayin(self, stem, branch, expected_name, expected_wx):
        name, wx = get_nayin(stem, branch)
        assert name == expected_name
        assert wx == expected_wx

    def test_get_nayin_by_index(self):
        # 甲子 = index 1
        name, wx = get_nayin_by_sexagenary_index(1)
        assert name == "海中金"
        assert wx == WuXing.METAL
        # 丙寅 = index 3
        name, wx = get_nayin_by_sexagenary_index(3)
        assert name == "炉中火"
        assert wx == WuXing.FIRE

    def test_all_60_entries_exist(self):
        """Verify all 60 sexagenary combinations have nayin entries.

        Valid pairs: stem_order and branch_order share the same parity
        (both odd or both even). This yields exactly 60 combinations.
        """
        count = 0
        for stem in HeavenlyStem:
            for branch in EarthlyBranch:
                if (stem.order % 2) == (branch.order % 2):
                    name, wx = get_nayin(stem, branch)
                    assert isinstance(name, str)
                    assert isinstance(wx, WuXing)
                    assert len(name) > 0
                    count += 1
        assert count == 60, f"Expected 60 nayin entries, got {count}"
