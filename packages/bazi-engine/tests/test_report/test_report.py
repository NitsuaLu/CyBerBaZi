"""Tests for report generation module."""

from datetime import datetime

from bazi.types import Sex
from bazi.paipan import build_chart
from bazi.report import generate_report, Report
from bazi.report.sections import (
    section_basic_info,
    section_dayun,
)


class TestReportGeneration:
    def test_generates_all_sections(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        report = generate_report(chart)
        assert len(report.sections) >= 7

    def test_basic_info_contains_pillars(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        text = section_basic_info(chart)
        assert "年柱" in text
        assert "月柱" in text
        assert "日柱" in text
        assert "时柱" in text
        assert "日主" in text

    def test_dayun_section(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        text = section_dayun(chart)
        assert "起运年龄" in text
        assert str(chart.qi_yun_age) in text

    def test_report_render(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        report = generate_report(chart)
        # Both render modes
        md = report.render()
        plain = report.render_plain()
        assert len(md) > 0
        assert len(plain) > 0
        # Markdown has headers
        assert md.startswith("# ")
        # Plain has different header style
        assert "═══" in plain or "【" in plain

    def test_female_chart(self):
        chart = build_chart(datetime(1990, 5, 20, 8, 0), Sex.FEMALE)
        report = generate_report(chart)
        assert len(report.sections) >= 7

    def test_report_type(self):
        chart = build_chart(datetime(2000, 6, 15, 12, 0), Sex.MALE)
        report = generate_report(chart)
        assert isinstance(report, Report)
        for heading, content in report.sections:
            assert isinstance(heading, str)
            assert isinstance(content, str)
            assert len(heading) > 0
            assert len(content) > 0
