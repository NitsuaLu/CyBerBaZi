"""Integration tests for build_chart() with known BaZi references."""

from datetime import datetime

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.types import Sex
from bazi.paipan import build_chart


class TestBuildChart:
    """Integration tests for the full chart builder."""

    def test_chart_has_four_pillars(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        assert chart.year_pillar is not None
        assert chart.month_pillar is not None
        assert chart.day_pillar is not None
        assert chart.hour_pillar is not None

    def test_day_master_set(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        assert chart.day_master is not None
        assert isinstance(chart.day_master, HeavenlyStem)

    def test_hidden_stems_annotated(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        # Every pillar should have hidden stems with shishen annotated
        for pillar in chart.four_pillars:
            assert len(pillar.hidden_stems) >= 1
            for h in pillar.hidden_stems:
                assert h.shishen is not None

    def test_shishen_on_stems(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        for pillar in chart.four_pillars:
            assert pillar.stem_shishen is not None

    def test_nayin_on_all_pillars(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        for pillar in chart.four_pillars:
            assert pillar.nayin, f"Missing nayin for {pillar.heavenly_stem.value}{pillar.earthly_branch.value}"

    def test_fortune_cycles_generated(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        assert len(chart.fortune_cycles) >= 8
        assert chart.qi_yun_age >= 1

    def test_fortune_cycles_have_nayin(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        for fc in chart.fortune_cycles:
            assert fc.nayin, f"Missing nayin for {fc.stem.value}{fc.branch.value}"

    def test_true_solar_time_applied(self):
        # Longitude 105°E (3 hours west of Beijing line at 120°E = 15° offset)
        # Should correct birth time by -60 minutes
        chart = build_chart(datetime(2000, 6, 15, 8, 0), Sex.MALE, longitude=105.0)
        assert chart.true_solar_datetime is not None
        assert chart.true_solar_datetime.hour < 8  # Should be ~7:00


class TestKnownChart:
    """Verify known BaZi charts against reference data."""

    def test_2024_03_15_noon_male(self):
        """2024-03-15 12:00, Male.
        Year: 2024 = 甲辰
        Month: after 惊蛰 (Mar 5) -> 卯月, year stem=甲 -> 丙寅? No:
        Wait, 甲年 寅月 stem = 丙. 卯月 = 寅月 + 1 offset = 丁卯.
        Day: Mar 15 2024, self-verifying
        Hour: 午时, day stem determines hour stem via 五鼠遁.
        """
        chart = build_chart(datetime(2024, 3, 15, 12, 0), Sex.MALE)

        # Year pillar
        assert chart.year_pillar.heavenly_stem == HeavenlyStem.JIA  # 甲
        assert chart.year_pillar.earthly_branch == EarthlyBranch.CHEN  # 辰

        # Day master should exist
        assert chart.day_master is not None

    def test_male_vs_female_fortune_direction(self):
        """2024 = 甲辰 (Yang year).
        Male -> forward (顺排), Female -> backward (逆排).
        Forward means the first fortune cycle's stem/branch comes AFTER
        the month pillar in the sexagenary order.
        """
        dt = datetime(2024, 6, 15, 12, 0)  # After 芒种, 午月

        chart_m = build_chart(dt, Sex.MALE)
        chart_f = build_chart(dt, Sex.FEMALE)

        month_stem = chart_m.month_pillar.heavenly_stem
        month_branch = chart_m.month_pillar.earthly_branch

        # Male (forward): first cycle stem should be month_stem + 1
        first_cycle_m = chart_m.fortune_cycles[0]
        assert HeavenlyStem.from_order(month_stem.order + 1) == first_cycle_m.stem

        # Female (backward): first cycle stem should be month_stem - 1
        first_cycle_f = chart_f.fortune_cycles[0]
        assert HeavenlyStem.from_order(month_stem.order - 1) == first_cycle_f.stem

    def test_different_longitude_same_day_pillar(self):
        """Day pillar is based on date, not time — same day, same pillar."""
        c1 = build_chart(datetime(2024, 6, 15, 3, 0), Sex.MALE, longitude=75.0)
        c2 = build_chart(datetime(2024, 6, 15, 23, 0), Sex.MALE, longitude=135.0)
        assert c1.day_pillar.heavenly_stem == c2.day_pillar.heavenly_stem
        assert c1.day_pillar.earthly_branch == c2.day_pillar.earthly_branch

    def test_hour_changes_with_longitude(self):
        """True solar time correction affects hour pillar."""
        # Birth at 23:15 at 75°E (shifted 3 hours west = -180 min)
        # True solar time = 23:15 - 3:00 = 20:15 -> 戌时
        chart = build_chart(datetime(2024, 6, 15, 23, 15), Sex.MALE, longitude=75.0)
        assert chart.hour_pillar.earthly_branch == EarthlyBranch.XU  # 戌时 (19-21)
        assert chart.true_solar_datetime.hour < 23
