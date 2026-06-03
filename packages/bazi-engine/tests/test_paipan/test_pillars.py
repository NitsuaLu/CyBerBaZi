"""Tests for the four pillar modules."""

from datetime import datetime

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.paipan.year_pillar import get_year_pillar
from bazi.paipan.month_pillar import get_month_pillar
from bazi.paipan.day_pillar import get_day_pillar
from bazi.paipan.hour_pillar import get_hour_pillar


class TestYearPillar:
    def test_after_lichun(self):
        """Birth after 立春 should use current year."""
        # 2000-02-05 is after 立春 (Feb 4 ~20:30)
        stem, branch = get_year_pillar(datetime(2000, 2, 5, 8, 0))
        assert stem == HeavenlyStem.GENG  # 庚
        assert branch == EarthlyBranch.CHEN  # 辰

    def test_before_lichun(self):
        """Birth before 立春 should use previous year."""
        # 2000-02-03 is before 立春 (Feb 4)
        stem, branch = get_year_pillar(datetime(2000, 2, 3, 8, 0))
        assert stem == HeavenlyStem.JI  # 1999 is 己卯年
        assert branch == EarthlyBranch.MAO

    def test_2024_year(self):
        """2024 = 甲辰年."""
        stem, branch = get_year_pillar(datetime(2024, 6, 1, 12, 0))
        assert stem == HeavenlyStem.JIA
        assert branch == EarthlyBranch.CHEN

    def test_1984_jia_zi(self):
        """1984 = 甲子年 (after 立春)."""
        stem, branch = get_year_pillar(datetime(1984, 5, 15, 12, 0))
        assert stem == HeavenlyStem.JIA
        assert branch == EarthlyBranch.ZI


class TestMonthPillar:
    def test_january_after_xiaohan(self):
        """After 小寒 -> 丑月."""
        year_stem = HeavenlyStem.GENG  # 2000 = 庚辰
        stem, branch = get_month_pillar(datetime(2000, 1, 15, 12, 0), year_stem)
        assert branch == EarthlyBranch.CHOU  # 丑月

    def test_february_after_lichun(self):
        """After 立春 -> 寅月, 五虎遁: year=庚 -> 戊寅."""
        stem, branch = get_month_pillar(datetime(2000, 2, 5, 12, 0), HeavenlyStem.GENG)
        assert branch == EarthlyBranch.YIN
        assert stem == HeavenlyStem.WU  # 庚年 -> 戊寅

    def test_june_after_mangzhong(self):
        """After 芒种 -> 午月."""
        year_stem = HeavenlyStem.GENG
        stem, branch = get_month_pillar(datetime(2000, 6, 15, 12, 0), year_stem)
        assert branch == EarthlyBranch.WU

    def test_wu_hu_dun_all(self):
        """Test all 五虎遁 mappings."""
        from bazi.paipan.month_pillar import WU_HU_DUN
        assert WU_HU_DUN[HeavenlyStem.JIA] == HeavenlyStem.BING
        assert WU_HU_DUN[HeavenlyStem.YI] == HeavenlyStem.BING
        assert WU_HU_DUN[HeavenlyStem.BING] == HeavenlyStem.GENG
        assert WU_HU_DUN[HeavenlyStem.DING] == HeavenlyStem.REN
        assert WU_HU_DUN[HeavenlyStem.WU] == HeavenlyStem.JIA
        assert WU_HU_DUN[HeavenlyStem.JI] == HeavenlyStem.BING
        assert WU_HU_DUN[HeavenlyStem.GENG] == HeavenlyStem.WU
        assert WU_HU_DUN[HeavenlyStem.XIN] == HeavenlyStem.GENG
        assert WU_HU_DUN[HeavenlyStem.REN] == HeavenlyStem.REN
        assert WU_HU_DUN[HeavenlyStem.GUI] == HeavenlyStem.JIA


class TestDayPillar:
    def test_reference(self):
        """1900-01-01 = 甲戌."""
        stem, branch = get_day_pillar(datetime(1900, 1, 1, 0, 0))
        assert stem == HeavenlyStem.JIA
        assert branch == EarthlyBranch.XU

    def test_60_day_cycle(self):
        """60 days later, same Gan-Zhi."""
        s1, b1 = get_day_pillar(datetime(2024, 1, 1, 0, 0))
        s2, b2 = get_day_pillar(datetime(2024, 3, 1, 0, 0))
        # 2024 is a leap year: Jan (31) + Feb (29) = 60 days
        assert s1 == s2
        assert b1 == b2


class TestHourPillar:
    def test_zi_shi(self):
        """子时 (23:00-01:00)."""
        # 2000-01-01 day stem = 戊午, 五鼠遁: 戊 → 壬子
        day_stem = HeavenlyStem.WU  # 戊
        stem, branch = get_hour_pillar(
            datetime(2000, 1, 1, 0, 30), day_stem
        )
        assert branch == EarthlyBranch.ZI
        assert stem == HeavenlyStem.REN  # 戊日 → 壬子

    def test_wu_shi(self):
        """午时 (11:00-13:00)."""
        day_stem = HeavenlyStem.WU
        stem, branch = get_hour_pillar(
            datetime(2000, 1, 1, 12, 0), day_stem
        )
        assert branch == EarthlyBranch.WU
        # 戊日 子时=壬, so 午时 offset 6 from 子: stem = 壬+6 = 15 → 戊午

    def test_wu_shu_dun_all(self):
        """Test all 五鼠遁 mappings."""
        from bazi.paipan.hour_pillar import WU_SHU_DUN
        assert WU_SHU_DUN[HeavenlyStem.JIA] == HeavenlyStem.JIA
        assert WU_SHU_DUN[HeavenlyStem.JI] == HeavenlyStem.JIA
        assert WU_SHU_DUN[HeavenlyStem.YI] == HeavenlyStem.JIA
        assert WU_SHU_DUN[HeavenlyStem.GENG] == HeavenlyStem.BING
        assert WU_SHU_DUN[HeavenlyStem.XIN] == HeavenlyStem.WU
        assert WU_SHU_DUN[HeavenlyStem.BING] == HeavenlyStem.WU
        assert WU_SHU_DUN[HeavenlyStem.DING] == HeavenlyStem.GENG
        assert WU_SHU_DUN[HeavenlyStem.REN] == HeavenlyStem.GENG
        assert WU_SHU_DUN[HeavenlyStem.WU] == HeavenlyStem.REN
        assert WU_SHU_DUN[HeavenlyStem.GUI] == HeavenlyStem.REN
