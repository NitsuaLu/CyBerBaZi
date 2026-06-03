"""Tests for shishen analysis module."""

from datetime import datetime

from bazi.types import Sex
from bazi.paipan import build_chart
from bazi.analysis.shishen import analyze_shishen


class TestShiShenAnalysis:
    def test_all_four_stems_annotated(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        analysis = analyze_shishen(chart)
        # Should have shishen for all 4 heavenly stems
        assert len(analysis.stem_by_pillar) == 4
        assert "年柱" in analysis.stem_by_pillar
        assert "月柱" in analysis.stem_by_pillar
        assert "日柱" in analysis.stem_by_pillar
        assert "时柱" in analysis.stem_by_pillar

    def test_counts_non_empty(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        analysis = analyze_shishen(chart)
        assert len(analysis.counts) > 0
        for count in analysis.counts.values():
            assert count.total >= 1

    def test_hidden_stems_analyzed(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        analysis = analyze_shishen(chart)
        # At least some hidden stems should be found
        total_hidden = sum(c.hidden_count for c in analysis.counts.values())
        assert total_hidden > 0
