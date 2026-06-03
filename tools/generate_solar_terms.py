"""Generate solar terms data for 1900-2100 using ephem.

Run: python tools/generate_solar_terms.py

Chinese solar terms correspond to 15-degree increments of the Sun's
geocentric ecliptic longitude (J2000.0 mean equinox).
"""

import json
import math
import os
from datetime import datetime, timezone, timedelta

import ephem

CST = timezone(timedelta(hours=8))
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data")

SOLAR_TERM_NAMES = [
    "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
    "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
    "立冬", "小雪", "大雪", "冬至", "小寒", "大寒",
]

# Solar term angles: index 0 = 立春 at 315 degrees
SOLAR_TERM_DEGREES = [(i * 15 + 315) % 360 for i in range(24)]


def sun_lon_deg(sun: ephem.Sun, t: ephem.Date) -> float:
    """Return the Sun's geocentric ecliptic longitude in degrees (0-360) at time t."""
    sun.compute(t)
    lon = float(ephem.Ecliptic(sun).lon)
    return math.degrees(lon) % 360


def find_solar_term(year: int, target_deg: float) -> datetime:
    """Find the date and time when the Sun reaches the target ecliptic longitude.

    Uses a two-pass approach:
    1. Scan day-by-day to find the day of the crossing
    2. Use linear interpolation to pinpoint the exact time
    """
    sun = ephem.Sun()

    # 立春 for a given year can fall between Feb 3-5
    # For other terms, estimate based on angle difference from 立春
    # But for robustness, scan from Jan 1 forward

    t = ephem.Date(f"{year}/01/01 00:00:00")
    prev_lon = sun_lon_deg(sun, t)
    prev_t = float(t)

    # Scan day by day
    for day in range(1, 368):
        t = ephem.Date(f"{year}/01/01 00:00:00") + day
        lon = sun_lon_deg(sun, t)

        # Check if target was crossed
        # Handle both normal crossing and 0/360 wrap
        crossed = False
        if prev_lon <= lon:
            crossed = prev_lon <= target_deg <= lon
        else:
            # Wrap at 360
            crossed = target_deg <= lon or target_deg >= prev_lon

        if crossed:
            # Linear interpolation to find exact moment
            if prev_lon <= lon:
                fraction = (target_deg - prev_lon) / (lon - prev_lon) if lon != prev_lon else 0
            else:
                # Handle wrap
                if target_deg >= prev_lon:
                    fraction = (target_deg - prev_lon) / (lon + 360 - prev_lon)
                else:
                    fraction = (target_deg + 360 - prev_lon) / (lon + 360 - prev_lon)

            exact_day = float(t - 1) + fraction
            result = ephem.Date(exact_day).datetime()
            dt_cst = result.replace(tzinfo=timezone.utc).astimezone(CST)
            return dt_cst.replace(tzinfo=None)

        prev_lon = lon
        prev_t = float(t)

    # Fallback: if not found within the year, return the last computed position
    return datetime(year, 12, 31, 23, 59, 59)


def generate_solar_terms_json(start_year: int = 1900, end_year: int = 2100):
    """Generate the solar terms JSON file."""
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    data: dict[str, list[dict]] = {}

    for year in range(start_year, end_year + 1):
        year_terms = []
        for deg, name in zip(SOLAR_TERM_DEGREES, SOLAR_TERM_NAMES):
            dt = find_solar_term(year, deg)
            year_terms.append({
                "name": name,
                "datetime": dt.strftime("%Y-%m-%dT%H:%M:%S"),
            })
            if (year == 2000 or year == start_year) and name in ("立春", "冬至", "夏至"):
                print(f"  {year} {name}: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        data[str(year)] = year_terms

    output_file = os.path.join(OUTPUT_PATH, "solar_terms_1900_2100.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nGenerated {sum(len(v) for v in data.values())} entries -> {output_file}")


if __name__ == "__main__":
    generate_solar_terms_json()
