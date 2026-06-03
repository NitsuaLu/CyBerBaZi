"""公历<->农历互转模块 (Gregorian <-> Lunar Calendar Conversion).

For the initial version, implements a simplified lunar calendar conversion
using pre-computed lunar month data.

The Chinese lunar calendar is lunisolar:
- Each month begins on a new moon day
- Leap months (闰月) occur approx. every 3 years to align with solar terms
- The month containing 冬至 (winter solstice) is always month 11 (十一月)

Data format (lunar_calendar_1900_2100.json):
    {
      "1900": {
        "months": [29, 30, 30, 29, ...],  // 12 or 13 month lengths (days)
        "leap_month": 0,                   // 0 = no leap, N = which month is leap
        "new_year_date": "1900-01-31"      // Chinese New Year date
      },
      ...
    }
"""

from __future__ import annotations

import json
import os
from datetime import date, timedelta
from typing import NamedTuple


class LunarDate(NamedTuple):
    """Represents a date in the Chinese lunar calendar."""

    year: int
    month: int       # 1-12
    day: int         # 1-30
    is_leap: bool = False

    def __str__(self) -> str:
        leap = "闰" if self.is_leap else ""
        return f"{self.year}年{leap}{self.month}月{self.day}日"


_DATA: dict[int, dict] = {}
_LOADED = False


def _load_data():
    global _LOADED
    if _LOADED:
        return
    path = os.path.join(os.path.dirname(__file__), "data", "lunar_calendar_1900_2100.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for year_str, entry in raw.items():
            _DATA[int(year_str)] = entry
        _LOADED = True
    else:
        raise FileNotFoundError(
            f"Lunar calendar data not found at {path}. "
            "Run tools/generate_lunar_data.py first."
        )


def lunar_to_solar(lunar_date: LunarDate) -> date:
    """Convert a lunar date to a Gregorian date."""
    raise NotImplementedError("Lunar-to-solar conversion not yet implemented")


def solar_to_lunar(d: date) -> LunarDate:
    """Convert a Gregorian date to a lunar date."""
    raise NotImplementedError("Solar-to-lunar conversion not yet implemented")
