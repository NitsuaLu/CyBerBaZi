"""Tests for Gan-Zhi day cycle module."""

from datetime import date

from bazi.core import HeavenlyStem, EarthlyBranch
from bazi.calendar.day_cycle import (
    sexagenary_index_for_date,
    gan_zhi_for_date,
    stem_for_date,
    branch_for_date,
    sexagenary_index_for_year,
    gan_zhi_for_year,
)


class TestDayCycle:
    def test_reference_date(self):
        # 1900-01-01 = 甲戌日, index 11
        assert sexagenary_index_for_date(date(1900, 1, 1)) == 11
        stem, branch = gan_zhi_for_date(date(1900, 1, 1))
        assert stem == HeavenlyStem.JIA
        assert branch == EarthlyBranch.XU

    def test_next_day(self):
        # 1900-01-02 = 乙亥日, index 12
        stem, branch = gan_zhi_for_date(date(1900, 1, 2))
        assert stem == HeavenlyStem.YI
        assert branch == EarthlyBranch.HAI
        assert sexagenary_index_for_date(date(1900, 1, 2)) == 12

    def test_60_days_cycle(self):
        # 1900-01-01 = 甲戌 (11), +60 days = 1900-03-02 = 甲戌 again
        idx1 = sexagenary_index_for_date(date(1900, 1, 1))
        idx2 = sexagenary_index_for_date(date(1900, 3, 2))
        assert idx1 == idx2 == 11

    def test_known_date_2024_spring_festival(self):
        # 2024-02-10 = 甲辰日
        stem, branch = gan_zhi_for_date(date(2024, 2, 10))
        assert stem == HeavenlyStem.JIA
        assert branch == EarthlyBranch.CHEN

    def test_known_date_2024_12_31(self):
        # 2024-12-31 = 己巳日
        stem, branch = gan_zhi_for_date(date(2024, 12, 31))
        assert stem == HeavenlyStem.JI
        assert branch == EarthlyBranch.SI

    def test_stem_for_date(self):
        assert stem_for_date(date(1900, 1, 1)) == HeavenlyStem.JIA

    def test_branch_for_date(self):
        assert branch_for_date(date(1900, 1, 1)) == EarthlyBranch.XU


class TestYearGanZhi:
    def test_2024_year(self):
        # 2024 = 甲辰年 (index 41)
        idx = sexagenary_index_for_year(2024)
        assert idx == 41
        stem, branch = gan_zhi_for_year(2024)
        assert stem == HeavenlyStem.JIA
        assert branch == EarthlyBranch.CHEN

    def test_2025_year(self):
        # 2025 = 乙巳年 (index 42)
        stem, branch = gan_zhi_for_year(2025)
        assert stem == HeavenlyStem.YI
        assert branch == EarthlyBranch.SI

    def test_1984_year(self):
        # 1984 = 甲子年 (index 1)
        assert sexagenary_index_for_year(1984) == 1
        stem, branch = gan_zhi_for_year(1984)
        assert stem == HeavenlyStem.JIA
        assert branch == EarthlyBranch.ZI
