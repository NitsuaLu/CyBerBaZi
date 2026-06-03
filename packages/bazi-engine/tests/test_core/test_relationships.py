"""Tests for Ten Gods (十神) relationship derivation."""

from bazi.core import HeavenlyStem, ShiShen, get_shishen


class TestShiShen:
    """Test that get_shishen returns correct Ten-God relationships.

    Day Master = 甲 (Jia, Yang Wood).
    """

    DM = HeavenlyStem.JIA  # 甲木阳

    def test_bi_jian(self):
        # 甲 vs 甲 = same wx, same yy
        assert get_shishen(self.DM, HeavenlyStem.JIA) == ShiShen.BI_JIAN

    def test_jie_cai(self):
        # 甲 vs 乙 = same wx (木), diff yy (甲阳乙阴)
        assert get_shishen(self.DM, HeavenlyStem.YI) == ShiShen.JIE_CAI

    def test_shi_shen(self):
        # 甲木生火, 丙火阳 = same yy
        assert get_shishen(self.DM, HeavenlyStem.BING) == ShiShen.SHI_SHEN

    def test_shang_guan(self):
        # 甲木生火, 丁火阴 = diff yy
        assert get_shishen(self.DM, HeavenlyStem.DING) == ShiShen.SHANG_GUAN

    def test_pian_cai(self):
        # 甲木克土, 戊土阳 = same yy
        assert get_shishen(self.DM, HeavenlyStem.WU) == ShiShen.PIAN_CAI

    def test_zheng_cai(self):
        # 甲木克土, 己土阴 = diff yy
        assert get_shishen(self.DM, HeavenlyStem.JI) == ShiShen.ZHENG_CAI

    def test_qi_sha(self):
        # 金克木, 庚金阳 = same yy
        assert get_shishen(self.DM, HeavenlyStem.GENG) == ShiShen.QI_SHA

    def test_zheng_guan(self):
        # 金克木, 辛金阴 = diff yy
        assert get_shishen(self.DM, HeavenlyStem.XIN) == ShiShen.ZHENG_GUAN

    def test_pian_yin(self):
        # 水生木, 壬水阳 = same yy
        assert get_shishen(self.DM, HeavenlyStem.REN) == ShiShen.PIAN_YIN

    def test_zheng_yin(self):
        # 水生木, 癸水阴 = diff yy
        assert get_shishen(self.DM, HeavenlyStem.GUI) == ShiShen.ZHENG_YIN


class TestShiShenDayMasterDing:
    """Test with 丁 (Ding, Yin Fire) as Day Master."""

    DM = HeavenlyStem.DING  # 丁火阴

    def test_ding_vs_bing(self):
        # 丁 vs 丙 = same wx (火), diff yy (丁阴丙阳) = 劫财
        assert get_shishen(self.DM, HeavenlyStem.BING) == ShiShen.JIE_CAI

    def test_ding_vs_ding(self):
        assert get_shishen(self.DM, HeavenlyStem.DING) == ShiShen.BI_JIAN

    def test_ding_vs_ren(self):
        # 水克火, 壬阳 vs 丁阴 = diff yy = 正官
        assert get_shishen(self.DM, HeavenlyStem.REN) == ShiShen.ZHENG_GUAN

    def test_ding_vs_gui(self):
        # 水克火, 癸阴 vs 丁阴 = same yy = 七杀
        assert get_shishen(self.DM, HeavenlyStem.GUI) == ShiShen.QI_SHA

    def test_ding_vs_jia(self):
        # 木生火, 甲阳 vs 丁阴 = diff yy = 正印
        assert get_shishen(self.DM, HeavenlyStem.JIA) == ShiShen.ZHENG_YIN

    def test_ding_vs_yi(self):
        # 木生火, 乙阴 vs 丁阴 = same yy = 偏印
        assert get_shishen(self.DM, HeavenlyStem.YI) == ShiShen.PIAN_YIN


class TestShiShenProperties:
    def test_is_good(self):
        assert ShiShen.ZHENG_YIN.is_good
        assert ShiShen.ZHENG_GUAN.is_good
        assert ShiShen.SHI_SHEN.is_good
        assert not ShiShen.QI_SHA.is_good
        assert not ShiShen.SHANG_GUAN.is_good

    def test_is_evil(self):
        assert ShiShen.QI_SHA.is_evil
        assert ShiShen.SHANG_GUAN.is_evil
        assert ShiShen.JIE_CAI.is_evil
        assert not ShiShen.ZHENG_YIN.is_evil
