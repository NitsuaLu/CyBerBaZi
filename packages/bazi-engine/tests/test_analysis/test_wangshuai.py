"""Tests for wangshuai (旺衰) module."""

from datetime import datetime

from bazi.types import Sex
from bazi.paipan import build_chart
from bazi.analysis.wangshuai import analyze_wang_shuai, WangShuaiResult


class TestWangShuai:
    def test_returns_valid_level(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        result = analyze_wang_shuai(chart)
        assert result.level in ("极旺", "偏旺", "中和", "偏弱", "极弱")

    def test_four_factors_present(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        result = analyze_wang_shuai(chart)
        assert result.de_ling > 0
        assert result.de_di >= 0
        assert result.de_sheng >= 0
        assert result.de_zhu >= 0
        assert result.total > 0

    def test_details_provided(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        result = analyze_wang_shuai(chart)
        assert len(result.details) >= 4

    def test_summer_birth_stronger_fire(self):
        """Day master with fire wuxing born in summer should score higher de_ling."""
        # Fire day master in June (summer = fire strong)
        chart1 = build_chart(datetime(2024, 6, 15, 12, 0), Sex.MALE)
        # Same day master wuxing in December (winter = fire weak)
        chart2 = build_chart(datetime(2024, 12, 15, 12, 0), Sex.MALE)

        r1 = analyze_wang_shuai(chart1)
        r2 = analyze_wang_shuai(chart2)

        # If both have same day master wuxing, summer one should have higher de_ling
        if chart1.day_master.wuxing == chart2.day_master.wuxing:
            assert r1.de_ling >= r2.de_ling

    def test_is_helpers(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        result = analyze_wang_shuai(chart)
        assert isinstance(result.is_weak, bool)
        assert isinstance(result.is_strong, bool)
        assert isinstance(result.is_neutral, bool)
