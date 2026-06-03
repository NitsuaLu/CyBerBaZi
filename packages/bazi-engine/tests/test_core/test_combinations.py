"""Tests for Combinations (合冲刑害) module."""

from bazi.core import HeavenlyStem, EarthlyBranch, WuXing
from bazi.core.combinations import (
    stem_combination, are_stems_combined,
    branch_2_combination,
    san_he_group, san_hui_wuxing,
    clash_branch, are_branches_clashing,
    harm_branch,
    are_branches_punishing, get_punishment_branches,
)


class TestStemCombinations:
    def test_jia_ji_he(self):
        partner, wx = stem_combination(HeavenlyStem.JIA)
        assert partner == HeavenlyStem.JI
        assert wx == WuXing.EARTH

    def test_ji_jia_he(self):
        partner, wx = stem_combination(HeavenlyStem.JI)
        assert partner == HeavenlyStem.JIA
        assert wx == WuXing.EARTH

    def test_yi_geng_he(self):
        partner, wx = stem_combination(HeavenlyStem.YI)
        assert partner == HeavenlyStem.GENG
        assert wx == WuXing.METAL

    def test_are_stems_combined(self):
        assert are_stems_combined(HeavenlyStem.JIA, HeavenlyStem.JI)
        assert are_stems_combined(HeavenlyStem.JI, HeavenlyStem.JIA)
        assert not are_stems_combined(HeavenlyStem.JIA, HeavenlyStem.YI)

    def test_all_five_pairs(self):
        pairs = [
            (HeavenlyStem.JIA, HeavenlyStem.JI),
            (HeavenlyStem.YI, HeavenlyStem.GENG),
            (HeavenlyStem.BING, HeavenlyStem.XIN),
            (HeavenlyStem.DING, HeavenlyStem.REN),
            (HeavenlyStem.WU, HeavenlyStem.GUI),
        ]
        for a, b in pairs:
            assert are_stems_combined(a, b)
            assert are_stems_combined(b, a)


class TestBranch2Combinations:
    def test_zi_chou_he(self):
        partner, wx = branch_2_combination(EarthlyBranch.ZI)
        assert partner == EarthlyBranch.CHOU
        assert wx == WuXing.EARTH

    def test_six_pairs(self):
        pairs = [
            (EarthlyBranch.ZI, EarthlyBranch.CHOU),
            (EarthlyBranch.YIN, EarthlyBranch.HAI),
            (EarthlyBranch.MAO, EarthlyBranch.XU),
            (EarthlyBranch.CHEN, EarthlyBranch.YOU),
            (EarthlyBranch.SI, EarthlyBranch.SHEN),
            (EarthlyBranch.WU, EarthlyBranch.WEI),
        ]
        for a, b in pairs:
            partner, _ = branch_2_combination(a)
            assert partner == b
            partner, _ = branch_2_combination(b)
            assert partner == a


class TestSanHe:
    def test_shen_zi_chen_water(self):
        assert san_he_group(EarthlyBranch.SHEN) == (WuXing.WATER, "长生")
        assert san_he_group(EarthlyBranch.ZI) == (WuXing.WATER, "帝旺")
        assert san_he_group(EarthlyBranch.CHEN) == (WuXing.WATER, "墓库")

    def test_yin_wu_xu_fire(self):
        assert san_he_group(EarthlyBranch.YIN) == (WuXing.FIRE, "长生")
        assert san_he_group(EarthlyBranch.WU) == (WuXing.FIRE, "帝旺")
        assert san_he_group(EarthlyBranch.XU) == (WuXing.FIRE, "墓库")


class TestSanHui:
    def test_yin_mao_chen_wood(self):
        assert san_hui_wuxing(EarthlyBranch.YIN) == WuXing.WOOD
        assert san_hui_wuxing(EarthlyBranch.MAO) == WuXing.WOOD
        assert san_hui_wuxing(EarthlyBranch.CHEN) == WuXing.WOOD

    def test_si_wu_wei_fire(self):
        assert san_hui_wuxing(EarthlyBranch.SI) == WuXing.FIRE
        assert san_hui_wuxing(EarthlyBranch.WU) == WuXing.FIRE
        assert san_hui_wuxing(EarthlyBranch.WEI) == WuXing.FIRE


class TestSixClashes:
    def test_zi_wu_chong(self):
        assert are_branches_clashing(EarthlyBranch.ZI, EarthlyBranch.WU)
        assert are_branches_clashing(EarthlyBranch.WU, EarthlyBranch.ZI)

    def test_all_six(self):
        pairs = [
            (EarthlyBranch.ZI, EarthlyBranch.WU),
            (EarthlyBranch.CHOU, EarthlyBranch.WEI),
            (EarthlyBranch.YIN, EarthlyBranch.SHEN),
            (EarthlyBranch.MAO, EarthlyBranch.YOU),
            (EarthlyBranch.CHEN, EarthlyBranch.XU),
            (EarthlyBranch.SI, EarthlyBranch.HAI),
        ]
        for a, b in pairs:
            assert are_branches_clashing(a, b)
            assert are_branches_clashing(b, a)
            assert clash_branch(a) == b

    def test_no_clash(self):
        assert not are_branches_clashing(EarthlyBranch.ZI, EarthlyBranch.CHOU)
        assert clash_branch(EarthlyBranch.ZI) != EarthlyBranch.CHOU


class TestSixHarms:
    def test_zi_wei_hai(self):
        assert harm_branch(EarthlyBranch.ZI) == EarthlyBranch.WEI
        assert harm_branch(EarthlyBranch.WEI) == EarthlyBranch.ZI

    def test_chou_wu_hai(self):
        assert harm_branch(EarthlyBranch.CHOU) == EarthlyBranch.WU
        assert harm_branch(EarthlyBranch.WU) == EarthlyBranch.CHOU


class TestPunishment:
    def test_zi_mao_wu_li(self):
        assert are_branches_punishing(EarthlyBranch.ZI, EarthlyBranch.MAO)
        assert are_branches_punishing(EarthlyBranch.MAO, EarthlyBranch.ZI)

    def test_self_punishment(self):
        assert are_branches_punishing(EarthlyBranch.CHEN, EarthlyBranch.CHEN)
        assert are_branches_punishing(EarthlyBranch.WU, EarthlyBranch.WU)
        assert not are_branches_punishing(EarthlyBranch.ZI, EarthlyBranch.ZI)

    def test_wu_en(self):
        assert are_branches_punishing(EarthlyBranch.YIN, EarthlyBranch.SI)
        assert are_branches_punishing(EarthlyBranch.SI, EarthlyBranch.SHEN)
        assert are_branches_punishing(EarthlyBranch.SHEN, EarthlyBranch.YIN)
