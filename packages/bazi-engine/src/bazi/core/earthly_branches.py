from __future__ import annotations

from enum import Enum

from bazi.core.wuxing import WuXing
from bazi.core.heavenly_stems import YinYang


class EarthlyBranch(Enum):
    """地支 (Earthly Branches)."""

    ZI = "子"
    CHOU = "丑"
    YIN = "寅"
    MAO = "卯"
    CHEN = "辰"
    SI = "巳"
    WU = "午"
    WEI = "未"
    SHEN = "申"
    YOU = "酉"
    XU = "戌"
    HAI = "亥"

    def __repr__(self) -> str:
        return f"EarthlyBranch.{self.name}"

    @property
    def order(self) -> int:
        return BRANCH_ORDER[self]

    @property
    def yin_yang(self) -> YinYang:
        return YinYang.YANG if self.order % 2 == 1 else YinYang.YIN

    @property
    def wuxing(self) -> WuXing:
        return BRANCH_WUXING[self]

    @property
    def zodiac(self) -> str:
        return BRANCH_ZODIAC[self]

    @property
    def season(self) -> str:
        return BRANCH_SEASON[self]

    @classmethod
    def from_order(cls, n: int) -> "EarthlyBranch":
        n = ((n - 1) % 12) + 1
        return BRANCH_BY_ORDER[n]

    @classmethod
    def shichen_hours(cls, branch: "EarthlyBranch") -> tuple[int, int]:
        return SHICHEN_HOURS[branch]

    @classmethod
    def from_hour(cls, hour: float) -> "EarthlyBranch":
        h = hour % 24
        if h >= 23 or h < 1:
            return cls.ZI
        return cls.from_order(int((h - 1) // 2) + 2)


BRANCH_ORDER: dict[EarthlyBranch, int] = {
    EarthlyBranch.ZI: 1, EarthlyBranch.CHOU: 2, EarthlyBranch.YIN: 3,
    EarthlyBranch.MAO: 4, EarthlyBranch.CHEN: 5, EarthlyBranch.SI: 6,
    EarthlyBranch.WU: 7, EarthlyBranch.WEI: 8, EarthlyBranch.SHEN: 9,
    EarthlyBranch.YOU: 10, EarthlyBranch.XU: 11, EarthlyBranch.HAI: 12,
}

BRANCH_BY_ORDER: dict[int, EarthlyBranch] = {v: k for k, v in BRANCH_ORDER.items()}

BRANCH_WUXING: dict[EarthlyBranch, WuXing] = {
    EarthlyBranch.YIN: WuXing.WOOD, EarthlyBranch.MAO: WuXing.WOOD,
    EarthlyBranch.SI: WuXing.FIRE, EarthlyBranch.WU: WuXing.FIRE,
    EarthlyBranch.SHEN: WuXing.METAL, EarthlyBranch.YOU: WuXing.METAL,
    EarthlyBranch.HAI: WuXing.WATER, EarthlyBranch.ZI: WuXing.WATER,
    EarthlyBranch.CHEN: WuXing.EARTH, EarthlyBranch.XU: WuXing.EARTH,
    EarthlyBranch.CHOU: WuXing.EARTH, EarthlyBranch.WEI: WuXing.EARTH,
}

BRANCH_ZODIAC: dict[EarthlyBranch, str] = {
    EarthlyBranch.ZI: "鼠", EarthlyBranch.CHOU: "牛", EarthlyBranch.YIN: "虎",
    EarthlyBranch.MAO: "兔", EarthlyBranch.CHEN: "龙", EarthlyBranch.SI: "蛇",
    EarthlyBranch.WU: "马", EarthlyBranch.WEI: "羊", EarthlyBranch.SHEN: "猴",
    EarthlyBranch.YOU: "鸡", EarthlyBranch.XU: "狗", EarthlyBranch.HAI: "猪",
}

BRANCH_SEASON: dict[EarthlyBranch, str] = {
    EarthlyBranch.YIN: "春", EarthlyBranch.MAO: "春", EarthlyBranch.CHEN: "春",
    EarthlyBranch.SI: "夏", EarthlyBranch.WU: "夏", EarthlyBranch.WEI: "夏",
    EarthlyBranch.SHEN: "秋", EarthlyBranch.YOU: "秋", EarthlyBranch.XU: "秋",
    EarthlyBranch.HAI: "冬", EarthlyBranch.ZI: "冬", EarthlyBranch.CHOU: "冬",
}

SHICHEN_HOURS: dict[EarthlyBranch, tuple[int, int]] = {
    EarthlyBranch.ZI: (23, 1), EarthlyBranch.CHOU: (1, 3),
    EarthlyBranch.YIN: (3, 5), EarthlyBranch.MAO: (5, 7),
    EarthlyBranch.CHEN: (7, 9), EarthlyBranch.SI: (9, 11),
    EarthlyBranch.WU: (11, 13), EarthlyBranch.WEI: (13, 15),
    EarthlyBranch.SHEN: (15, 17), EarthlyBranch.YOU: (17, 19),
    EarthlyBranch.XU: (19, 21), EarthlyBranch.HAI: (21, 23),
}
