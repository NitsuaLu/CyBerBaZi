"""报告生成主入口 (Report Generator).

generate_report(chart) -> Report
"""

from __future__ import annotations

from bazi.types import BaziChart
from bazi.analysis.shishen import analyze_shishen
from bazi.analysis.shensha import analyze_shensha
from bazi.analysis.geju import analyze_geju
from bazi.analysis.wangshuai import analyze_wang_shuai
from bazi.analysis.yongshen import analyze_yongshen

from bazi.report.template import Report
from bazi.report.sections import (
    section_basic_info,
    section_shishen,
    section_shensha,
    section_geju,
    section_wangshuai,
    section_yongshen,
    section_dayun,
    section_summary,
)


def generate_report(chart: BaziChart) -> Report:
    """Generate a complete BaZi analysis report from a chart.

    Args:
        chart: A fully built BaziChart from build_chart().

    Returns:
        A Report object with all analysis sections.
    """
    # Run all analyses
    shishen_analysis = analyze_shishen(chart)
    shensha_analysis = analyze_shensha(chart)
    ws = analyze_wang_shuai(chart)
    gj = analyze_geju(chart, ws.level)
    ys = analyze_yongshen(chart, ws)

    # Build report
    report = Report()

    report.add_section("基本信息", section_basic_info(chart))
    report.add_section("十神分析", section_shishen(shishen_analysis))
    report.add_section("旺衰判断", section_wangshuai(ws))
    report.add_section("格局判定", section_geju(gj))
    report.add_section("用神分析", section_yongshen(ys, chart))
    report.add_section("神煞分析", section_shensha(shensha_analysis))
    report.add_section("大运走势", section_dayun(chart))
    report.add_section("命局总评", section_summary(chart, ws, gj, ys))

    return report
