"""年柱排盘 (Year Pillar).

The year pillar changes at 立春 (Start of Spring), NOT at Chinese New Year.
Formula: year_gan_zhi_index = (year - 4) % 60
If the birth date is before 立春, use the previous year.
"""

from __future__ import annotations

from datetime import datetime

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.calendar.solar_terms import get_solar_term_by_name


def get_year_pillar(birth_dt: datetime) -> tuple[HeavenlyStem, EarthlyBranch]:
    """Return the (stem, branch) for the year pillar.

    Adjusts for the 立春 boundary: if birth is before 立春 of the same year,
    the year pillar belongs to the previous year.
    """
    year = birth_dt.year

    # Check if birth is before 立春 of this year
    lichun = get_solar_term_by_name(year, "立春")
    if lichun is not None and birth_dt < lichun.datetime:
        year -= 1

    index = ((year - 4) % 60) + 1
    stem_order = ((index - 1) % 10) + 1
    branch_order = ((index - 1) % 12) + 1

    return (
        HeavenlyStem.from_order(stem_order),
        EarthlyBranch.from_order(branch_order),
    )
