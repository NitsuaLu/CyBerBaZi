"""格局判定 (Pattern / Ge Ju Analysis).

Determines the pattern/格局 of a BaZi chart.

正格 (8 Standard Patterns):
- Based on the month branch's hidden stem that "透出" (appears) in heavenly stems.
  正官格, 七杀格, 正印格, 偏印格, 正财格, 偏财格, 食神格, 伤官格

变格 (Special Patterns):
- 从格: 从杀格, 从财格, 从儿格, 从强格 (day master extremely weak or strong)
- 化气格: day stem combines with month/hour stem and transforms
"""

from __future__ import annotations

from dataclasses import dataclass, field

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.core.relationships import ShiShen, get_shishen
from bazi.core.hidden_stems import get_hidden_stems
from bazi.types import BaziChart, Sex


@dataclass
class GeJuResult:
    pattern_name: str
    category: str    # "正格" / "变格" / "特殊"
    shishen: ShiShen | None = None
    description: str = ""


@dataclass
class GeJuAnalysis:
    primary: GeJuResult | None = None
    alternatives: list[GeJuResult] = field(default_factory=list)


def analyze_geju(chart: BaziChart, wang_shuai: str = "中和") -> GeJuAnalysis:
    """Determine the 格局 of a BaZi chart.

    Args:
        chart: the BaZi chart.
        wang_shuai: day master strength assessment ("极旺", "偏旺", "中和", "偏弱", "极弱").

    Returns:
        GeJuAnalysis with primary pattern and alternatives.
    """
    day_master = chart.day_master
    month_branch = chart.month_pillar.earthly_branch
    month_hidden = get_hidden_stems(month_branch)

    analysis = GeJuAnalysis()

    # ---- Check 正格: which hidden stem in month branch appears in heavenly stems ----
    heavenly_stems: list[HeavenlyStem] = [
        chart.year_pillar.heavenly_stem,
        chart.month_pillar.heavenly_stem,
        chart.day_pillar.heavenly_stem,
        chart.hour_pillar.heavenly_stem,
    ]

    for entry in month_hidden:
        if entry.stem in heavenly_stems and entry.stem != day_master:
            ss = get_shishen(day_master, entry.stem)
            pattern_name = f"{ss.value}格"
            analysis.alternatives.append(GeJuResult(
                pattern_name=pattern_name,
                category="正格",
                shishen=ss,
                description=f"月支{month_branch.value}藏{entry.stem.value}({entry.qi_level})透干, 取{pattern_name}",
            ))

    # Check 建禄格 / 月刃格 (special patterns based on month branch)
    month_branch_order = month_branch.order
    dm_lu = _find_lu_shen(day_master)

    if dm_lu is not None and month_branch_order == dm_lu.order:
        analysis.alternatives.append(GeJuResult(
            pattern_name="建禄格",
            category="特殊",
            description=f"月支{month_branch.value}为日主{day_master.value}之禄位",
        ))

    # Check 羊刃格
    dm_ren = _find_yang_ren(day_master)
    if dm_ren is not None and month_branch_order == dm_ren.order:
        analysis.alternatives.append(GeJuResult(
            pattern_name="月刃格",
            category="特殊",
            description=f"月支{month_branch.value}为日主{day_master.value}之羊刃",
        ))

    # ---- Check 变格 (special patterns) ----
    # 从格: day master extremely weak or strong
    if wang_shuai == "极弱":
        analysis.alternatives.append(GeJuResult(
            pattern_name="从格(待定)",
            category="变格",
            description="日主极弱, 可能从财/从杀/从儿",
        ))
    elif wang_shuai == "极旺":
        analysis.alternatives.append(GeJuResult(
            pattern_name="从强格(待定)",
            category="变格",
            description="日主极旺, 可能从强/从旺",
        ))

    # Pick the first valid 正格 as primary
    for alt in analysis.alternatives:
        if alt.category == "正格":
            analysis.primary = alt
            break

    if analysis.primary is None and analysis.alternatives:
        analysis.primary = analysis.alternatives[0]

    return analysis


def _find_lu_shen(stem: HeavenlyStem) -> EarthlyBranch | None:
    """Return the 禄 position for a heavenly stem."""
    from bazi.analysis.shensha import LU_SHEN_BY_STEM
    return LU_SHEN_BY_STEM.get(stem)


def _find_yang_ren(stem: HeavenlyStem) -> EarthlyBranch | None:
    """Return the 羊刃 position for a heavenly stem."""
    from bazi.analysis.shensha import YANG_REN_BY_STEM
    return YANG_REN_BY_STEM.get(stem)
