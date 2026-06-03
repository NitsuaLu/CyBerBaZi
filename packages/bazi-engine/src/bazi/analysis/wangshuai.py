"""旺衰判断 (Day Master Strength / Wang Shuai Analysis).

Assesses the strength of the day master based on four factors:
1. 得令 (month command): day master's wuxing vs month branch season
2. 得地 (grounding): day master's root in earthly branches
3. 得生 (nourishment): supporting elements from other stems
4. 得助 (assistance): same-element stems aiding the day master

Output: 极旺 / 偏旺 / 中和 / 偏弱 / 极弱
"""

from __future__ import annotations

from dataclasses import dataclass, field

from bazi.core.wuxing import WuXing
from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.core.relationships import ShiShen, get_shishen
from bazi.types import BaziChart


# 旺相休囚死: each wuxing's seasonal strength for each month branch
# Values: 旺=5, 相=4, 休=3, 囚=2, 死=1
# Season mapping: 寅卯(春-木旺), 巳午(夏-火旺), 申酉(秋-金旺), 亥子(冬-水旺)
# 辰戌丑未 = 土旺 (季末)
_SEASONAL_STRENGTH: dict[EarthlyBranch, dict[WuXing, int]] = {
    # 春: 木旺 火相 土死 金囚 水休
    EarthlyBranch.YIN:  {WuXing.WOOD: 5, WuXing.FIRE: 4, WuXing.EARTH: 1, WuXing.METAL: 2, WuXing.WATER: 3},
    EarthlyBranch.MAO:  {WuXing.WOOD: 5, WuXing.FIRE: 4, WuXing.EARTH: 1, WuXing.METAL: 2, WuXing.WATER: 3},
    # 夏: 火旺 土相 金死 水囚 木休
    EarthlyBranch.SI:   {WuXing.WOOD: 3, WuXing.FIRE: 5, WuXing.EARTH: 4, WuXing.METAL: 1, WuXing.WATER: 2},
    EarthlyBranch.WU:   {WuXing.WOOD: 3, WuXing.FIRE: 5, WuXing.EARTH: 4, WuXing.METAL: 1, WuXing.WATER: 2},
    # 秋: 金旺 水相 木死 火囚 土休
    EarthlyBranch.SHEN: {WuXing.WOOD: 1, WuXing.FIRE: 2, WuXing.EARTH: 3, WuXing.METAL: 5, WuXing.WATER: 4},
    EarthlyBranch.YOU:  {WuXing.WOOD: 1, WuXing.FIRE: 2, WuXing.EARTH: 3, WuXing.METAL: 5, WuXing.WATER: 4},
    # 冬: 水旺 木相 火死 土囚 金休
    EarthlyBranch.HAI:  {WuXing.WOOD: 4, WuXing.FIRE: 1, WuXing.EARTH: 2, WuXing.METAL: 3, WuXing.WATER: 5},
    EarthlyBranch.ZI:   {WuXing.WOOD: 4, WuXing.FIRE: 1, WuXing.EARTH: 2, WuXing.METAL: 3, WuXing.WATER: 5},
    # 四季末: 土旺 (辰戌丑未)
    EarthlyBranch.CHEN: {WuXing.WOOD: 2, WuXing.FIRE: 3, WuXing.EARTH: 5, WuXing.METAL: 4, WuXing.WATER: 1},
    EarthlyBranch.XU:   {WuXing.WOOD: 2, WuXing.FIRE: 3, WuXing.EARTH: 5, WuXing.METAL: 4, WuXing.WATER: 1},
    EarthlyBranch.CHOU: {WuXing.WOOD: 2, WuXing.FIRE: 3, WuXing.EARTH: 5, WuXing.METAL: 4, WuXing.WATER: 1},
    EarthlyBranch.WEI:  {WuXing.WOOD: 2, WuXing.FIRE: 3, WuXing.EARTH: 5, WuXing.METAL: 4, WuXing.WATER: 1},
}


@dataclass
class WangShuaiResult:
    """Day master strength assessment."""

    level: str  # "极旺" / "偏旺" / "中和" / "偏弱" / "极弱"

    de_ling: float = 0   # 得令 score (0-5)
    de_di: float = 0     # 得地 score
    de_sheng: float = 0  # 得生 score
    de_zhu: float = 0    # 得助 score

    total: float = 0
    details: list[str] = field(default_factory=list)

    @property
    def is_weak(self) -> bool:
        return self.level in ("偏弱", "极弱")

    @property
    def is_strong(self) -> bool:
        return self.level in ("偏旺", "极旺")

    @property
    def is_neutral(self) -> bool:
        return self.level == "中和"


def analyze_wang_shuai(chart: BaziChart) -> WangShuaiResult:
    """Assess the day master's strength (旺衰)."""
    dm = chart.day_master
    dm_wx = dm.wuxing

    result = WangShuaiResult(level="中和")

    # ---- 1. 得令 (Month command) ----
    month_branch = chart.month_pillar.earthly_branch
    seasonal = _SEASONAL_STRENGTH.get(month_branch, {})
    de_ling = float(seasonal.get(dm_wx, 3))  # default 3 if not found
    result.de_ling = de_ling
    result.details.append(f"得令: 月支{month_branch.value}, {dm_wx.value}得{_seasonal_label(de_ling)}")

    # ---- 2. 得地 (Root in branches) ----
    de_di = 0.0
    for pillar in chart.four_pillars:
        branch = pillar.earthly_branch
        for h in pillar.hidden_stems:
            if h.stem.wuxing == dm_wx:
                qi_weight = {"本气": 3.0, "中气": 2.0, "余气": 1.0}.get(h.qi_level, 1.0)
                de_di += qi_weight
    result.de_di = de_di
    result.details.append(f"得地: 地支通根强度 {de_di:.1f}")

    # ---- 3. 得生 (Nourishment from 印星) ----
    de_sheng = 0.0
    # 印星 = those that generate the day master
    nourishing = dm_wx.generated_by()
    for pillar in chart.four_pillars:
        if pillar.heavenly_stem.wuxing == nourishing:
            de_sheng += 2.0
        for h in pillar.hidden_stems:
            if h.stem.wuxing == nourishing:
                qi_weight = {"本气": 1.5, "中气": 1.0, "余气": 0.5}.get(h.qi_level, 0.5)
                de_sheng += qi_weight
    result.de_sheng = de_sheng
    result.details.append(f"得生: 印星({nourishing.value})生扶 {de_sheng:.1f}")

    # ---- 4. 得助 (Same-element support from 比劫) ----
    de_zhu = 0.0
    for pillar in chart.four_pillars:
        if pillar.heavenly_stem != dm and pillar.heavenly_stem.wuxing == dm_wx:
            de_zhu += 2.0
        for h in pillar.hidden_stems:
            if h.stem != dm and h.stem.wuxing == dm_wx:
                qi_weight = {"本气": 1.5, "中气": 1.0, "余气": 0.5}.get(h.qi_level, 0.5)
                de_zhu += qi_weight
    result.de_zhu = de_zhu
    result.details.append(f"得助: 比劫({dm_wx.value})帮扶 {de_zhu:.1f}")

    # ---- 5. Total score and level ----
    total = de_ling * 3 + de_di * 2 + de_sheng + de_zhu
    result.total = total

    # Thresholds (calibrated for 0-40 range)
    if total <= 10:
        result.level = "极弱"
    elif total <= 18:
        result.level = "偏弱"
    elif total <= 28:
        result.level = "中和"
    elif total <= 36:
        result.level = "偏旺"
    else:
        result.level = "极旺"

    result.details.append(f"总分: {total:.1f} → {result.level}")
    return result


def _seasonal_label(score: float) -> str:
    if score >= 5:
        return "旺"
    elif score >= 4:
        return "相"
    elif score >= 3:
        return "休"
    elif score >= 2:
        return "囚"
    else:
        return "死"
