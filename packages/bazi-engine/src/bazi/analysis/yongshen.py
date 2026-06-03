"""用神忌神分析 (Useful God / Unfavorable God Analysis).

Determines the most beneficial elements (用神) for a BaZi chart.

Methods:
1. 扶抑法: strengthen weak, weaken strong
2. 调候法: temperature adjustment based on day stem and birth month
3. 通关法: mediator when two elements clash
4. 病药法: identify the "illness" and the "medicine"
"""

from __future__ import annotations

from dataclasses import dataclass, field

from bazi.core.wuxing import WuXing
from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.core.relationships import ShiShen
from bazi.types import BaziChart
from bazi.analysis.wangshuai import WangShuaiResult


# 调候用神 reference table (simplified)
# Key: (day_stem_value, month_branch_value) -> suggested wuxing
# "甲木生于..." pattern
_TIAOHOU_TABLE: dict[str, dict[str, str]] = {
    # 甲木
    "甲": {
        "寅": "丙癸", "卯": "丙癸", "辰": "丙癸",
        "巳": "癸庚", "午": "癸庚", "未": "癸庚",
        "申": "庚丁", "酉": "庚丁", "戌": "庚丁",
        "亥": "庚丁", "子": "庚丁", "丑": "庚丁",
    },
    # 乙木
    "乙": {
        "寅": "丙癸", "卯": "丙癸", "辰": "丙癸",
        "巳": "癸", "午": "癸", "未": "癸",
        "申": "丙癸", "酉": "丙癸", "戌": "丙癸",
        "亥": "丙火", "子": "丙火", "丑": "丙火",
    },
    # 丙火
    "丙": {
        "寅": "壬庚", "卯": "壬庚", "辰": "壬庚",
        "巳": "壬庚", "午": "壬庚", "未": "壬庚",
        "申": "壬甲", "酉": "壬甲", "戌": "壬甲",
        "亥": "甲", "子": "甲", "丑": "甲",
    },
    # 丁火
    "丁": {
        "寅": "甲庚", "卯": "甲庚", "辰": "甲庚",
        "巳": "甲庚", "午": "甲庚", "未": "甲庚",
        "申": "甲庚", "酉": "甲庚", "戌": "甲庚",
        "亥": "甲庚", "子": "甲庚", "丑": "甲庚",
    },
    # 戊土
    "戊": {
        "寅": "丙癸甲", "卯": "丙癸甲", "辰": "丙癸甲",
        "巳": "癸丙", "午": "癸丙", "未": "癸丙",
        "申": "丙癸甲", "酉": "丙癸甲", "戌": "丙癸甲",
        "亥": "丙甲", "子": "丙甲", "丑": "丙甲",
    },
    # 己土
    "己": {
        "寅": "丙癸甲", "卯": "丙癸甲", "辰": "丙癸甲",
        "巳": "癸丙", "午": "癸丙", "未": "癸丙",
        "申": "丙癸", "酉": "丙癸", "戌": "丙癸",
        "亥": "丙甲", "子": "丙甲", "丑": "丙甲",
    },
    # 庚金
    "庚": {
        "寅": "丙甲", "卯": "丙甲", "辰": "丙甲",
        "巳": "壬丙", "午": "壬丙", "未": "壬丙",
        "申": "丁甲", "酉": "丁甲", "戌": "丁甲",
        "亥": "丙丁", "子": "丙丁", "丑": "丙丁",
    },
    # 辛金
    "辛": {
        "寅": "壬甲", "卯": "壬甲", "辰": "壬甲",
        "巳": "壬甲", "午": "壬甲", "未": "壬甲",
        "申": "壬甲", "酉": "壬甲", "戌": "壬甲",
        "亥": "丙壬", "子": "丙壬", "丑": "丙壬",
    },
    # 壬水
    "壬": {
        "寅": "庚戊", "卯": "庚戊", "辰": "庚戊",
        "巳": "壬辛", "午": "壬辛", "未": "壬辛",
        "申": "戊丁", "酉": "戊丁", "戌": "戊丁",
        "亥": "戊丙", "子": "戊丙", "丑": "戊丙",
    },
    # 癸水
    "癸": {
        "寅": "庚戊", "卯": "庚戊", "辰": "庚戊",
        "巳": "辛", "午": "辛", "未": "辛",
        "申": "庚戊", "酉": "庚戊", "戌": "庚戊",
        "亥": "丙", "子": "丙", "丑": "丙",
    },
}

# Chinese wuxing character to WuXing enum
_WX_CHAR: dict[str, WuXing] = {
    "木": WuXing.WOOD, "火": WuXing.FIRE, "土": WuXing.EARTH,
    "金": WuXing.METAL, "水": WuXing.WATER,
}

# Heavenly stem character to its WuXing (for 调候 parsing)
from bazi.core.heavenly_stems import HeavenlyStem as _HS
_STEM_TO_WUXING: dict[str, WuXing] = {
    "甲": WuXing.WOOD, "乙": WuXing.WOOD,
    "丙": WuXing.FIRE, "丁": WuXing.FIRE,
    "戊": WuXing.EARTH, "己": WuXing.EARTH,
    "庚": WuXing.METAL, "辛": WuXing.METAL,
    "壬": WuXing.WATER, "癸": WuXing.WATER,
}

# Combined: character -> WuXing (tries stem first, then wuxing)
_CHAR_TO_WUXING = {**_WX_CHAR, **_STEM_TO_WUXING}


@dataclass
class YongShenResult:
    """用神分析结果."""

    yong_shen: list[WuXing] = field(default_factory=list)   # 用神
    xi_shen: list[WuXing] = field(default_factory=list)     # 喜神
    ji_shen: list[WuXing] = field(default_factory=list)     # 忌神
    chou_shen: list[WuXing] = field(default_factory=list)   # 仇神

    method: str = ""           # 主要分析方法
    suggestions: list[str] = field(default_factory=list)

    @property
    def yong_shen_names(self) -> list[str]:
        return [w.value for w in self.yong_shen]

    @property
    def ji_shen_names(self) -> list[str]:
        return [w.value for w in self.ji_shen]


def analyze_yongshen(
    chart: BaziChart,
    wang_shuai: WangShuaiResult,
) -> YongShenResult:
    """Determine the useful gods (用神) for a BaZi chart.

    Priority: 调候 > 扶抑 > 通关 > 病药
    """
    dm = chart.day_master
    dm_wx = dm.wuxing
    result = YongShenResult()

    # ---- 1. 调候 (Temperature Adjustment) ----
    month_branch = chart.month_pillar.earthly_branch
    tiaohou_str = _TIAOHOU_TABLE.get(dm.value, {}).get(month_branch.value, "")
    tiaohou_wuxing = [_CHAR_TO_WUXING[c] for c in tiaohou_str if c in _CHAR_TO_WUXING]

    if tiaohou_wuxing:
        result.yong_shen = list(set(tiaohou_wuxing))
        result.method = "调候法"
        result.suggestions.append(
            f"日主{dm.value}生于{month_branch.value}月, 调候用神: {', '.join(w.value for w in tiaohou_wuxing)}"
        )

    # ---- 2. 扶抑 (Support / Suppress) ----
    if wang_shuai.is_weak:
        # Weak: use 印 (nourishing) and 比 (same element)
        nourishing = dm_wx.generated_by()
        support = [nourishing, dm_wx]
        if not result.yong_shen:
            result.yong_shen = support
            result.method = "扶抑法(扶)"
        result.suggestions.append(
            f"日主{wang_shuai.level}, 宜扶: 用{nourishing.value}(印), {dm_wx.value}(比)"
        )
    elif wang_shuai.is_strong:
        # Strong: 克 (overcome), 泄 (drain), 耗 (consume)
        overcomer = dm_wx.overcome_by()
        drain = dm_wx.generates()
        consume = dm_wx.overcomes()
        suppress = [overcomer, drain, consume]
        if not result.yong_shen:
            result.yong_shen = suppress
            result.method = "扶抑法(抑)"
        result.suggestions.append(
            f"日主{wang_shuai.level}, 宜抑: 用{overcomer.value}(官杀), {drain.value}(食伤), {consume.value}(财)"
        )
    else:
        # 中和: balanced, minor adjustment
        if not result.yong_shen:
            result.yong_shen = [dm_wx]
            result.method = "中和(顺势)"
        result.suggestions.append("日主中和，命局平衡，顺势而为即可。")

    # ---- 3. 通关 (Mediator) ----
    # Check for two elements in conflict; suggest the mediator
    # Simplified: check if 财破印 or 伤官见官 patterns exist
    # If found, suggest the mediating element

    # ---- 4. Calculate 喜神, 忌神, 仇神 ----
    all_wx = list(WuXing)

    # 喜神: aids the 用神
    if result.yong_shen:
        xi_set = set()
        for y in result.yong_shen:
            xi_set.add(y.generated_by())
        xi_set -= set(result.yong_shen)
        result.xi_shen = list(xi_set)

    # 忌神: opposes the 用神
    if result.yong_shen:
        ji_set = set()
        for y in result.yong_shen:
            ji_set.add(y.generates())  # 用神所生
            ji_set.add(y.overcomes())  # 用神所克
        ji_set -= set(result.yong_shen)
        result.ji_shen = list(ji_set)

    # 仇神: aids the 忌神
    if result.ji_shen:
        chou_set = set()
        for j in result.ji_shen:
            chou_set.add(j.generated_by())
        chou_set -= set(result.ji_shen)
        chou_set -= set(result.yong_shen)
        result.chou_shen = list(chou_set)

    return result
