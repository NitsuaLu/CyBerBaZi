"""时柱排盘 (Hour Pillar).

The hour pillar is determined by:
1. The hour branch: fixed by the 时辰 (two-hour period).
   子 23-1, 丑 1-3, 寅 3-5, 卯 5-7, 辰 7-9, 巳 9-11,
   午 11-13, 未 13-15, 申 15-17, 酉 17-19, 戌 19-21, 亥 21-23.

2. The hour stem: determined by the day stem via 五鼠遁 (Five Rat Push).
   Day stem → 子时 stem:
     甲己 → 甲子, 乙庚 → 丙子, 丙辛 → 戊子,
     丁壬 → 庚子, 戊癸 → 壬子
"""

from __future__ import annotations

from datetime import datetime

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch

# 五鼠遁: day_stem -> stem of 子时 (23:00-01:00)
WU_SHU_DUN: dict[HeavenlyStem, HeavenlyStem] = {
    HeavenlyStem.JIA: HeavenlyStem.JIA,
    HeavenlyStem.YI: HeavenlyStem.JIA,
    HeavenlyStem.JI: HeavenlyStem.JIA,
    HeavenlyStem.GENG: HeavenlyStem.BING,
    HeavenlyStem.XIN: HeavenlyStem.WU,
    HeavenlyStem.BING: HeavenlyStem.WU,
    HeavenlyStem.DING: HeavenlyStem.GENG,
    HeavenlyStem.REN: HeavenlyStem.GENG,
    HeavenlyStem.WU: HeavenlyStem.REN,
    HeavenlyStem.GUI: HeavenlyStem.REN,
}


def get_hour_pillar(
    birth_dt: datetime,
    day_stem: HeavenlyStem,
    longitude: float = 120.0,
) -> tuple[HeavenlyStem, EarthlyBranch]:
    """Return the (stem, branch) for the hour pillar.

    Args:
        birth_dt: birth datetime (wall clock time at birth location).
        day_stem: the heavenly stem of the day pillar (for 五鼠遁).
        longitude: birth location longitude in degrees east (default 120 = Beijing).
                   Used for true solar time correction.

    True solar time correction:
        Beijing time (CST) is based on 120°E longitude.
        For each degree west of 120°E, subtract 4 minutes.
        For each degree east of 120°E, add 4 minutes.
    """
    # True solar time correction
    hour = birth_dt.hour + birth_dt.minute / 60.0 + birth_dt.second / 3600.0

    # Adjust for longitude: 1 degree = 4 minutes = 4/60 hours
    hour += (longitude - 120.0) * 4.0 / 60.0

    # Normalize to [0, 24)
    hour = hour % 24.0

    # Get the hour branch from the corrected time
    hour_branch = EarthlyBranch.from_hour(hour)

    # Determine the hour stem using 五鼠遁
    # 子时 is the first shichen (index 0 in the 12-branch cycle)
    zi_stem = WU_SHU_DUN.get(day_stem)
    if zi_stem is None:
        raise ValueError(f"No 五鼠遁 entry for day stem {day_stem}")

    # Offset from 子时 (branch order 1) to the target branch
    zi_order = 1  # 子 = order 1
    target_order = hour_branch.order
    offset = (target_order - zi_order) % 12

    hour_stem = HeavenlyStem.from_order(zi_stem.order + offset)

    return hour_stem, hour_branch
