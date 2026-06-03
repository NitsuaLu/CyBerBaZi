"""Shared types for the BaZi engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.core.wuxing import WuXing
from bazi.core.relationships import ShiShen


class Sex(Enum):
    MALE = "男"
    FEMALE = "女"


@dataclass
class HiddenStemInfo:
    """A hidden stem within an earthly branch, with its qi level and shishen."""
    stem: HeavenlyStem
    qi_level: str  # "本气" / "中气" / "余气"
    shishen: ShiShen | None = None  # relative to day master


@dataclass
class Pillar:
    """A single pillar (柱) in the BaZi chart."""
    heavenly_stem: HeavenlyStem
    earthly_branch: EarthlyBranch
    hidden_stems: list[HiddenStemInfo] = field(default_factory=list)
    nayin: str = ""
    stem_shishen: ShiShen | None = None  # shishen of the heavenly stem relative to day master


@dataclass
class FortuneCycle:
    """A single 大运 (10-year fortune cycle)."""
    stem: HeavenlyStem
    branch: EarthlyBranch
    start_age: int
    start_year: int
    end_year: int
    nayin: str = ""


@dataclass
class BaziChart:
    """Complete BaZi chart (八字命盘)."""

    sex: Sex
    birth_datetime: datetime
    true_solar_datetime: datetime | None = None  # 真太阳时校正后的时间

    year_pillar: Pillar | None = None
    month_pillar: Pillar | None = None
    day_pillar: Pillar | None = None
    hour_pillar: Pillar | None = None

    day_master: HeavenlyStem | None = None

    fortune_cycles: list[FortuneCycle] = field(default_factory=list)
    qi_yun_age: int = 0  # 起运年龄

    @property
    def four_pillars(self) -> list[Pillar]:
        """Return the four pillars in order: year, month, day, hour."""
        return [
            self.year_pillar,
            self.month_pillar,
            self.day_pillar,
            self.hour_pillar,
        ]

    @property
    def day_master_wuxing(self) -> WuXing | None:
        """Return the WuXing of the day master."""
        if self.day_master is None:
            return None
        return self.day_master.wuxing
