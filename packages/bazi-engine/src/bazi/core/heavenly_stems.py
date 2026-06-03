from __future__ import annotations

from enum import Enum

from bazi.core.wuxing import WuXing


class YinYang(Enum):
    """阴阳."""
    YIN = "阴"
    YANG = "阳"

    def __repr__(self) -> str:
        return f"YinYang.{self.name}"


class HeavenlyStem(Enum):
    """天干 (Heavenly Stems / Celestial Stems).

    甲(jia) 乙(yi) 丙(bing) 丁(ding) 戊(wu)
    己(ji) 庚(geng) 辛(xin) 壬(ren) 癸(gui)
    """

    JIA = "甲"
    YI = "乙"
    BING = "丙"
    DING = "丁"
    WU = "戊"
    JI = "己"
    GENG = "庚"
    XIN = "辛"
    REN = "壬"
    GUI = "癸"

    def __repr__(self) -> str:
        return f"HeavenlyStem.{self.name}"

    @property
    def order(self) -> int:
        """Return 1-indexed order in the sexagenary cycle."""
        return STEM_ORDER[self]

    @property
    def yin_yang(self) -> YinYang:
        """阴阳属性: odd order = Yang, even = Yin."""
        return YinYang.YANG if self.order % 2 == 1 else YinYang.YIN

    @property
    def wuxing(self) -> WuXing:
        """五行归属."""
        return STEM_WUXING[self]

    @classmethod
    def from_order(cls, n: int) -> "HeavenlyStem":
        """Return the stem for a 1-indexed order (1-10). Values outside 1-10 wrap."""
        n = ((n - 1) % 10) + 1
        return STEM_BY_ORDER[n]


STEM_ORDER: dict[HeavenlyStem, int] = {
    HeavenlyStem.JIA: 1, HeavenlyStem.YI: 2, HeavenlyStem.BING: 3,
    HeavenlyStem.DING: 4, HeavenlyStem.WU: 5,
    HeavenlyStem.JI: 6, HeavenlyStem.GENG: 7, HeavenlyStem.XIN: 8,
    HeavenlyStem.REN: 9, HeavenlyStem.GUI: 10,
}

STEM_BY_ORDER: dict[int, HeavenlyStem] = {v: k for k, v in STEM_ORDER.items()}

# 甲乙木 丙丁火 戊己土 庚辛金 壬癸水
STEM_WUXING: dict[HeavenlyStem, WuXing] = {
    HeavenlyStem.JIA: WuXing.WOOD, HeavenlyStem.YI: WuXing.WOOD,
    HeavenlyStem.BING: WuXing.FIRE, HeavenlyStem.DING: WuXing.FIRE,
    HeavenlyStem.WU: WuXing.EARTH, HeavenlyStem.JI: WuXing.EARTH,
    HeavenlyStem.GENG: WuXing.METAL, HeavenlyStem.XIN: WuXing.METAL,
    HeavenlyStem.REN: WuXing.WATER, HeavenlyStem.GUI: WuXing.WATER,
}
