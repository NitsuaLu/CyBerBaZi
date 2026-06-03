"""八字排盘主入口 (Chart Builder).

build_chart(birth_datetime, sex, longitude) -> BaziChart
"""

from __future__ import annotations

from datetime import datetime, timedelta

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.core.nayin import get_nayin
from bazi.core.hidden_stems import get_hidden_stems
from bazi.core.relationships import get_shishen

from bazi.paipan.year_pillar import get_year_pillar
from bazi.paipan.month_pillar import get_month_pillar
from bazi.paipan.day_pillar import get_day_pillar
from bazi.paipan.hour_pillar import get_hour_pillar
from bazi.paipan.dayun import compute_fortune_cycles

from bazi.types import (
    Sex, Pillar, HiddenStemInfo, BaziChart, FortuneCycle,
)


def build_chart(
    birth_datetime: datetime,
    sex: Sex,
    longitude: float = 120.0,
) -> BaziChart:
    """Build a complete BaZi chart from birth information.

    Args:
        birth_datetime: birth date and time (wall clock time at birth location).
        sex: Sex.MALE or Sex.FEMALE.
        longitude: birth location longitude in degrees east (default 120° = Beijing).

    Returns:
        A complete BaziChart with four pillars, day master, fortune cycles, etc.
    """
    # True solar time correction
    offset_minutes = (longitude - 120.0) * 4.0
    true_solar_dt = birth_datetime + timedelta(minutes=offset_minutes)

    chart = BaziChart(
        sex=sex,
        birth_datetime=birth_datetime,
        true_solar_datetime=true_solar_dt,
    )

    # ---- Build pillars ----
    year_stem, year_branch = get_year_pillar(birth_datetime)
    month_stem, month_branch = get_month_pillar(birth_datetime, year_stem)
    day_stem, day_branch = get_day_pillar(birth_datetime)
    hour_stem, hour_branch = get_hour_pillar(birth_datetime, day_stem, longitude)

    chart.day_master = day_stem

    # Annotate pillars with hidden stems, shishen, nayin
    chart.year_pillar = _build_pillar(year_stem, year_branch, day_stem)
    chart.month_pillar = _build_pillar(month_stem, month_branch, day_stem)
    chart.day_pillar = _build_pillar(day_stem, day_branch, day_stem)
    chart.hour_pillar = _build_pillar(hour_stem, hour_branch, day_stem)

    # ---- Fortune cycles ----
    cycles, qi_yun_age = compute_fortune_cycles(
        birth_datetime, sex, year_stem, month_stem, month_branch,
    )
    chart.fortune_cycles = cycles
    chart.qi_yun_age = qi_yun_age

    return chart


def _build_pillar(
    stem: HeavenlyStem,
    branch: EarthlyBranch,
    day_master: HeavenlyStem,
) -> Pillar:
    """Build a single pillar with all annotations."""
    # Nayin
    nayin_name, _ = get_nayin(stem, branch)

    # Hidden stems with shishen
    hidden_stems = []
    for entry in get_hidden_stems(branch):
        hidden_stems.append(HiddenStemInfo(
            stem=entry.stem,
            qi_level=entry.qi_level,
            shishen=get_shishen(day_master, entry.stem),
        ))

    # Shishen of the heavenly stem
    stem_shishen = get_shishen(day_master, stem)

    return Pillar(
        heavenly_stem=stem,
        earthly_branch=branch,
        hidden_stems=hidden_stems,
        nayin=nayin_name,
        stem_shishen=stem_shishen,
    )
