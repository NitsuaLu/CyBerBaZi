"""月柱排盘 (Month Pillar).

The month pillar is determined by:
1. The month branch: fixed by the nearest solar term before the birth date.
   立春→寅月, 惊蛰→卯月, 清明→辰月, 立夏→巳月, 芒种→午月,
   小暑→未月, 立秋→申月, 白露→酉月, 寒露→戌月, 立冬→亥月,
   大雪→子月, 小寒→丑月.

2. The month stem: determined by the year stem via 五虎遁 (Five Tiger Push).
   Year stem → first month (寅月) stem:
     甲己 → 丙寅, 乙庚 → 戊寅, 丙辛 → 庚寅,
     丁壬 → 壬寅, 戊癸 → 甲寅
"""

from __future__ import annotations

from datetime import datetime

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.calendar.solar_terms import get_prev_solar_term, MONTH_BRANCH_SOLAR_TERM

# 五虎遁: year_stem -> stem of 寅月 (first month of the Chinese year)
WU_HU_DUN: dict[HeavenlyStem, HeavenlyStem] = {
    HeavenlyStem.JIA: HeavenlyStem.BING,
    HeavenlyStem.YI: HeavenlyStem.BING,
    HeavenlyStem.JI: HeavenlyStem.BING,
    HeavenlyStem.GENG: HeavenlyStem.WU,
    HeavenlyStem.XIN: HeavenlyStem.GENG,
    HeavenlyStem.BING: HeavenlyStem.GENG,
    HeavenlyStem.DING: HeavenlyStem.REN,
    HeavenlyStem.REN: HeavenlyStem.REN,
    HeavenlyStem.WU: HeavenlyStem.JIA,
    HeavenlyStem.GUI: HeavenlyStem.JIA,
}

# Month branch order starting from 寅 (index 3)
MONTH_BRANCHES: list[EarthlyBranch] = [
    EarthlyBranch.YIN,   # 寅月 (Feb)
    EarthlyBranch.MAO,   # 卯月 (Mar)
    EarthlyBranch.CHEN,  # 辰月 (Apr)
    EarthlyBranch.SI,    # 巳月 (May)
    EarthlyBranch.WU,    # 午月 (Jun)
    EarthlyBranch.WEI,   # 未月 (Jul)
    EarthlyBranch.SHEN,  # 申月 (Aug)
    EarthlyBranch.YOU,   # 酉月 (Sep)
    EarthlyBranch.XU,    # 戌月 (Oct)
    EarthlyBranch.HAI,   # 亥月 (Nov)
    EarthlyBranch.ZI,    # 子月 (Dec)
    EarthlyBranch.CHOU,  # 丑月 (Jan)
]


def get_month_pillar(
    birth_dt: datetime,
    year_stem: HeavenlyStem,
) -> tuple[HeavenlyStem, EarthlyBranch]:
    """Return the (stem, branch) for the month pillar.

    Args:
        birth_dt: birth datetime.
        year_stem: the heavenly stem of the year pillar (for 五虎遁).
    """
    # 1. Find the month branch from the previous solar term
    prev_term = get_prev_solar_term(birth_dt)
    month_branch_name = MONTH_BRANCH_SOLAR_TERM.get(prev_term.name)

    if month_branch_name is None:
        raise ValueError(f"Cannot determine month branch from solar term: {prev_term.name}")

    # Convert branch name to EarthlyBranch
    month_branch = _branch_from_name(month_branch_name)

    # 2. Determine the month stem using 五虎遁
    # Find the index of 寅月 in MONTH_BRANCHES
    yin_index = MONTH_BRANCHES.index(EarthlyBranch.YIN)
    target_index = MONTH_BRANCHES.index(month_branch)
    offset = target_index - yin_index  # how many months after 寅月

    # Stem of 寅月 determined by year stem
    yin_stem = WU_HU_DUN.get(year_stem)
    if yin_stem is None:
        raise ValueError(f"No 五虎遁 entry for year stem {year_stem}")

    month_stem = HeavenlyStem.from_order(yin_stem.order + offset)

    return month_stem, month_branch


def _branch_from_name(name: str) -> EarthlyBranch:
    """Convert a Chinese branch name to EarthlyBranch enum."""
    for b in EarthlyBranch:
        if b.value == name:
            return b
    raise ValueError(f"Unknown branch name: {name}")
