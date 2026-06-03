"""节气查询模块 (Solar Terms Query).

Loads pre-computed solar term data and provides lookup functions.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, date
from typing import NamedTuple


class SolarTermEvent(NamedTuple):
    """A solar term with its name and precise datetime."""

    name: str
    datetime: datetime

    @property
    def date(self) -> date:
        return self.datetime.date()


_DATA: dict[int, list[SolarTermEvent]] = {}
_LOADED = False


def _load_data():
    global _LOADED
    if _LOADED:
        return
    path = os.path.join(os.path.dirname(__file__), "data", "solar_terms_1900_2100.json")
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    for year_str, terms in raw.items():
        year = int(year_str)
        _DATA[year] = [
            SolarTermEvent(name=t["name"], datetime=datetime.fromisoformat(t["datetime"]))
            for t in terms
        ]
    _LOADED = True


# All 24 solar term names in calendar-year order (starting from 立春)
SOLAR_TERM_NAMES = [
    "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
    "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
    "立冬", "小雪", "大雪", "冬至", "小寒", "大寒",
]

# Month-branch assignment: which solar term starts each month-branch
# 寅月 from 立春, 卯月 from 惊蛰, ..., 丑月 from 小寒
MONTH_BRANCH_SOLAR_TERM: dict[str, str] = {
    "立春": "寅", "惊蛰": "卯", "清明": "辰", "立夏": "巳",
    "芒种": "午", "小暑": "未", "立秋": "申", "白露": "酉",
    "寒露": "戌", "立冬": "亥", "大雪": "子", "小寒": "丑",
}

# Order index for each solar term name (0 = 立春, ..., 23 = 大寒)
SOLAR_TERM_ORDER: dict[str, int] = {n: i for i, n in enumerate(SOLAR_TERM_NAMES)}


def get_solar_terms_for_year(year: int) -> list[SolarTermEvent]:
    """Return all 24 solar term events for a given year, sorted by datetime."""
    _load_data()
    terms = _DATA.get(year, [])
    return sorted(terms, key=lambda t: t.datetime)


def get_next_solar_term(dt: datetime) -> SolarTermEvent:
    """Find the next solar term after the given datetime."""
    _load_data()
    year = dt.year
    best = None
    for y in (year, year + 1):
        if y not in _DATA:
            continue
        for term in _DATA[y]:
            if term.datetime > dt:
                if best is None or term.datetime < best.datetime:
                    best = term
    if best is None:
        raise ValueError(f"No solar term found after {dt}")
    return best


def get_prev_solar_term(dt: datetime) -> SolarTermEvent:
    """Find the most recent solar term on or before the given datetime."""
    _load_data()
    year = dt.year
    best = None
    for y in (year - 1, year, year + 1):
        if y not in _DATA:
            continue
        for term in _DATA[y]:
            if term.datetime <= dt:
                if best is None or term.datetime > best.datetime:
                    best = term
    if best is None:
        raise ValueError(f"No solar term found before {dt}")
    return best


def get_solar_term_by_name(year: int, name: str) -> SolarTermEvent | None:
    """Return a specific solar term event for a given year."""
    _load_data()
    for term in _DATA.get(year, []):
        if term.name == name:
            return term
    return None
