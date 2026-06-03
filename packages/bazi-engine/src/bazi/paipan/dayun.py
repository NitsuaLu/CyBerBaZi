"""大运排盘 (Fortune Cycles / Da Yun).

Determines the 10-year fortune cycles (大运) for a BaZi chart.

Direction rules:
- 阳年 (Yang year-stem) + Male   → 顺排 (forward)
- 阳年 + Female                   → 逆排 (backward)
- 阴年 (Yin year-stem) + Male     → 逆排
- 阴年 + Female                   → 顺排

Starting age (起运):
- Forward: days from birth to next month-boundary solar term / 3
- Backward: days from previous month-boundary solar term to birth / 3
"""

from __future__ import annotations

from datetime import datetime

from bazi.core.heavenly_stems import HeavenlyStem, YinYang
from bazi.core.earthly_branches import EarthlyBranch
from bazi.core.nayin import get_nayin
from bazi.calendar.solar_terms import get_next_solar_term, get_prev_solar_term
from bazi.types import Sex, FortuneCycle


def compute_fortune_cycles(
    birth_dt: datetime,
    sex: Sex,
    year_stem: HeavenlyStem,
    month_stem: HeavenlyStem,
    month_branch: EarthlyBranch,
    num_cycles: int = 8,
) -> tuple[list[FortuneCycle], int]:
    """Compute the fortune cycles (大运) and starting age (起运年龄).

    Returns (cycles, qi_yun_age).
    """
    year_yin_yang = year_stem.yin_yang
    is_forward = _is_forward(year_yin_yang, sex)

    # Calculate starting age
    qi_yun_age = _calculate_qi_yun_age(birth_dt, is_forward)

    # Generate fortune cycles
    cycles = _generate_cycles(
        month_stem, month_branch, qi_yun_age, birth_dt.year, is_forward, num_cycles
    )

    return cycles, qi_yun_age


def _is_forward(year_yin_yang: YinYang, sex: Sex) -> bool:
    """Determine if fortune cycles go forward (顺排) or backward (逆排)."""
    if sex == Sex.MALE:
        return year_yin_yang == YinYang.YANG
    else:
        return year_yin_yang == YinYang.YIN


def _calculate_qi_yun_age(birth_dt: datetime, is_forward: bool) -> int:
    """Calculate the age at which fortune cycles begin.

    Forward: count days from birth to next month-boundary solar term.
    Backward: count days from previous month-boundary solar term to birth.
    3 days ≈ 1 year of fortune start age (rounded up).
    """
    if is_forward:
        # Find the next solar term after birth
        next_term = get_next_solar_term(birth_dt)
        days = (next_term.datetime - birth_dt).total_seconds() / 86400.0
    else:
        # Find the previous solar term before birth
        prev_term = get_prev_solar_term(birth_dt)
        days = (birth_dt - prev_term.datetime).total_seconds() / 86400.0

    # 3 days = 1 year, round up
    age = max(1, round(days / 3.0))

    return age


def _generate_cycles(
    month_stem: HeavenlyStem,
    month_branch: EarthlyBranch,
    qi_yun_age: int,
    birth_year: int,
    is_forward: bool,
    num_cycles: int,
) -> list[FortuneCycle]:
    """Generate fortune cycles starting from the month pillar."""
    cycles = []

    for i in range(num_cycles):
        if is_forward:
            stem = HeavenlyStem.from_order(month_stem.order + i + 1)
            branch = EarthlyBranch.from_order(month_branch.order + i + 1)
        else:
            stem = HeavenlyStem.from_order(month_stem.order - i - 1)
            branch = EarthlyBranch.from_order(month_branch.order - i - 1)

        start_age = qi_yun_age + i * 10
        start_year = birth_year + start_age
        end_year = start_year + 9

        nayin_name, _ = get_nayin(stem, branch)

        cycles.append(FortuneCycle(
            stem=stem,
            branch=branch,
            start_age=start_age,
            start_year=start_year,
            end_year=end_year,
            nayin=nayin_name,
        ))

    return cycles
