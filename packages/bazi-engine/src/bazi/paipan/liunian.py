"""流年流月推算 (Current Year / Current Month Flow).

流年 (Liu Nian): year Gan-Zhi for a given year.
流月 (Liu Yue): month Gan-Zhi for a given year-month, using 五虎遁.
"""

from __future__ import annotations

from datetime import date

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.calendar.day_cycle import sexagenary_index_for_year
from bazi.paipan.month_pillar import WU_HU_DUN

# Month branches in order: 寅卯辰巳午未申酉戌亥子丑
MONTH_BRANCHES: list[EarthlyBranch] = [
    EarthlyBranch.YIN, EarthlyBranch.MAO, EarthlyBranch.CHEN,
    EarthlyBranch.SI, EarthlyBranch.WU, EarthlyBranch.WEI,
    EarthlyBranch.SHEN, EarthlyBranch.YOU, EarthlyBranch.XU,
    EarthlyBranch.HAI, EarthlyBranch.ZI, EarthlyBranch.CHOU,
]


def get_liunian(year: int) -> tuple[HeavenlyStem, EarthlyBranch]:
    """Return the Gan-Zhi for a given Gregorian year (流年)."""
    index = sexagenary_index_for_year(year)
    stem_order = ((index - 1) % 10) + 1
    branch_order = ((index - 1) % 12) + 1
    return (
        HeavenlyStem.from_order(stem_order),
        EarthlyBranch.from_order(branch_order),
    )


def get_liuyue(year_stem: HeavenlyStem, month_num: int) -> tuple[HeavenlyStem, EarthlyBranch]:
    """Return the Gan-Zhi for a given month in a given year (流月).

    Month numbers use the Chinese calendar system:
    1 = 寅月 (Feb), 2 = 卯月 (Mar), ..., 12 = 丑月 (Jan of next year).

    Args:
        year_stem: the heavenly stem of the current year (for 五虎遁).
        month_num: month number 1-12, where 1 = 寅月.
    """
    if month_num < 1 or month_num > 12:
        raise ValueError(f"Month number must be 1-12, got {month_num}")

    month_branch = MONTH_BRANCHES[month_num - 1]

    yin_stem = WU_HU_DUN[year_stem]
    month_stem = HeavenlyStem.from_order(yin_stem.order + month_num - 1)

    return month_stem, month_branch
