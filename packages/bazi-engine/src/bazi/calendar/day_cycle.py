"""干支纪日推算 (Gan-Zhi Day Cycle).

The sexagenary day cycle has been continuous since ancient times.
Given a reference point (known Gan-Zhi for a specific date), we can
compute the Gan-Zhi for any date by counting the day difference modulo 60.

Reference: 1900-01-01 = 甲戌日 (sexagenary index 11)
"""

from __future__ import annotations

from datetime import date, datetime

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch


# 1900-01-01 = 甲戌 (Jia-Xu)
# 甲 = stem 1, 戌 = branch 11, sexagenary index = 11
REFERENCE_DATE = date(1900, 1, 1)
REFERENCE_SEXAGENARY_INDEX = 11


def days_since_reference(d: date) -> int:
    """Return the number of days between the reference date and d."""
    return (d - REFERENCE_DATE).days


def sexagenary_index_for_date(d: date) -> int:
    """Return the 1-indexed sexagenary index (1-60) for a given date.

    The index 1 = 甲子, 2 = 乙丑, ..., 60 = 癸亥.
    """
    offset = days_since_reference(d)
    return ((REFERENCE_SEXAGENARY_INDEX - 1 + offset) % 60) + 1


def gan_zhi_for_date(d: date) -> tuple[HeavenlyStem, EarthlyBranch]:
    """Return the heavenly stem and earthly branch for a given date."""
    index = sexagenary_index_for_date(d)
    stem_order = ((index - 1) % 10) + 1
    branch_order = ((index - 1) % 12) + 1
    return (
        HeavenlyStem.from_order(stem_order),
        EarthlyBranch.from_order(branch_order),
    )


def stem_for_date(d: date) -> HeavenlyStem:
    """Return just the heavenly stem for a given date."""
    return gan_zhi_for_date(d)[0]


def branch_for_date(d: date) -> EarthlyBranch:
    """Return just the earthly branch for a given date."""
    return gan_zhi_for_date(d)[1]


def sexagenary_index_for_year(year: int) -> int:
    """Return the sexagenary index (1-60) for a given Gregorian year.

    Formula: (year - 4) % 60 = index (0-based), +1 for 1-based.
    Note: This uses the standard "立春" boundary rule — the year pillar
    changes at 立春, not at the Gregorian new year. This function returns
    the year's Gan-Zhi assuming the whole calendar year; the paipan module
    will handle the 立春 boundary correctly.
    """
    return ((year - 4) % 60) + 1


def gan_zhi_for_year(year: int) -> tuple[HeavenlyStem, EarthlyBranch]:
    """Return the Gan-Zhi for a given year (rough, without 立春 adjustment)."""
    index = sexagenary_index_for_year(year)
    stem_order = ((index - 1) % 10) + 1
    branch_order = ((index - 1) % 12) + 1
    return (
        HeavenlyStem.from_order(stem_order),
        EarthlyBranch.from_order(branch_order),
    )
