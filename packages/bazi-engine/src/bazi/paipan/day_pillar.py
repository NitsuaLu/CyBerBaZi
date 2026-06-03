"""日柱排盘 (Day Pillar).

The day pillar uses the continuous Gan-Zhi day cycle.
Simply delegates to the calendar.day_cycle module.
"""

from __future__ import annotations

from datetime import datetime, date

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.calendar.day_cycle import gan_zhi_for_date


def get_day_pillar(birth_dt: datetime) -> tuple[HeavenlyStem, EarthlyBranch]:
    """Return the (stem, branch) for the day pillar.

    The day pillar is based on the continuous sexagenary day cycle,
    using the birth date (date only, no time adjustment needed).
    """
    d: date = birth_dt.date()
    return gan_zhi_for_date(d)
