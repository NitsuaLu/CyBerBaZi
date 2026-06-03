"""合冲刑害关系 (Combinations, Clashes, Punishments, Harms).

- 天干五合 (5 Heavenly Stem combinations)
- 地支六合 (6 Earthly Branch 2-combinations)
- 地支三合 (4 Earthly Branch 3-combinations / San He)
- 地支三会 (4 Earthly Branch 3-meetings / San Hui)
- 地支六冲 (6 Earthly Branch clashes / Liu Chong)
- 地支六害 (6 Earthly Branch harms / Liu Hai)
- 地支三刑 (Earthly Branch punishments)
"""

from __future__ import annotations

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.core.wuxing import WuXing

# ============================================================
# 天干五合 (Heavenly Stem 5-combinations)
# ============================================================
# 甲己合土 乙庚合金 丙辛合水 丁壬合木 戊癸合火
_HE_STEM_COMBINATIONS: dict[HeavenlyStem, tuple[HeavenlyStem, WuXing]] = {
    HeavenlyStem.JIA: (HeavenlyStem.JI, WuXing.EARTH),
    HeavenlyStem.JI: (HeavenlyStem.JIA, WuXing.EARTH),
    HeavenlyStem.YI: (HeavenlyStem.GENG, WuXing.METAL),
    HeavenlyStem.GENG: (HeavenlyStem.YI, WuXing.METAL),
    HeavenlyStem.BING: (HeavenlyStem.XIN, WuXing.WATER),
    HeavenlyStem.XIN: (HeavenlyStem.BING, WuXing.WATER),
    HeavenlyStem.DING: (HeavenlyStem.REN, WuXing.WOOD),
    HeavenlyStem.REN: (HeavenlyStem.DING, WuXing.WOOD),
    HeavenlyStem.WU: (HeavenlyStem.GUI, WuXing.FIRE),
    HeavenlyStem.GUI: (HeavenlyStem.WU, WuXing.FIRE),
}


def stem_combination(stem: HeavenlyStem) -> tuple[HeavenlyStem, WuXing] | None:
    """Return (partner_stem, resulting_wuxing) if this stem has a combination partner."""
    return _HE_STEM_COMBINATIONS.get(stem)


def are_stems_combined(a: HeavenlyStem, b: HeavenlyStem) -> bool:
    """Check if two heavenly stems form a 五合 pair."""
    combo = _HE_STEM_COMBINATIONS.get(a)
    return combo is not None and combo[0] == b


# ============================================================
# 地支六合 (Earthly Branch 6-combinations)
# ============================================================
# 子丑合土 寅亥合木 卯戌合火 辰酉合金 巳申合水 午未合(日月/土)
_BRANCH_2_COMBINATIONS: dict[EarthlyBranch, tuple[EarthlyBranch, WuXing]] = {
    EarthlyBranch.ZI: (EarthlyBranch.CHOU, WuXing.EARTH),
    EarthlyBranch.CHOU: (EarthlyBranch.ZI, WuXing.EARTH),
    EarthlyBranch.YIN: (EarthlyBranch.HAI, WuXing.WOOD),
    EarthlyBranch.HAI: (EarthlyBranch.YIN, WuXing.WOOD),
    EarthlyBranch.MAO: (EarthlyBranch.XU, WuXing.FIRE),
    EarthlyBranch.XU: (EarthlyBranch.MAO, WuXing.FIRE),
    EarthlyBranch.CHEN: (EarthlyBranch.YOU, WuXing.METAL),
    EarthlyBranch.YOU: (EarthlyBranch.CHEN, WuXing.METAL),
    EarthlyBranch.SI: (EarthlyBranch.SHEN, WuXing.WATER),
    EarthlyBranch.SHEN: (EarthlyBranch.SI, WuXing.WATER),
    EarthlyBranch.WU: (EarthlyBranch.WEI, WuXing.EARTH),
    EarthlyBranch.WEI: (EarthlyBranch.WU, WuXing.EARTH),
}


def branch_2_combination(branch: EarthlyBranch) -> tuple[EarthlyBranch, WuXing] | None:
    """Return (partner_branch, resulting_wuxing) for 六合."""
    return _BRANCH_2_COMBINATIONS.get(branch)


# ============================================================
# 地支三合局 (San He / Three Harmony Combinations)
# ============================================================
# 申子辰合水 亥卯未合木 寅午戌合火 巳酉丑合金
_SAN_HE: dict[str, tuple[EarthlyBranch, EarthlyBranch, EarthlyBranch]] = {
    "water": (EarthlyBranch.SHEN, EarthlyBranch.ZI, EarthlyBranch.CHEN),
    "wood": (EarthlyBranch.HAI, EarthlyBranch.MAO, EarthlyBranch.WEI),
    "fire": (EarthlyBranch.YIN, EarthlyBranch.WU, EarthlyBranch.XU),
    "metal": (EarthlyBranch.SI, EarthlyBranch.YOU, EarthlyBranch.CHOU),
}

_SAN_HE_WUXING: dict[str, WuXing] = {
    "water": WuXing.WATER, "wood": WuXing.WOOD,
    "fire": WuXing.FIRE, "metal": WuXing.METAL,
}

# Reverse lookup: branch -> (wuxing, role)
_SAN_HE_REVERSE: dict[EarthlyBranch, tuple[WuXing, str]] = {}
for _wx_name, (p1, p2, p3) in _SAN_HE.items():
    wx = _SAN_HE_WUXING[_wx_name]
    _SAN_HE_REVERSE[p1] = (wx, "长生")
    _SAN_HE_REVERSE[p2] = (wx, "帝旺")
    _SAN_HE_REVERSE[p3] = (wx, "墓库")


def san_he_group(branch: EarthlyBranch) -> tuple[WuXing, str] | None:
    """Return (wuxing, role) if the branch belongs to a 三合 group."""
    return _SAN_HE_REVERSE.get(branch)


# ============================================================
# 地支三会方 (San Hui / Three Meetings)
# ============================================================
# 寅卯辰会木 巳午未会火 申酉戌会金 亥子丑会水
_SAN_HUI: dict[WuXing, tuple[EarthlyBranch, EarthlyBranch, EarthlyBranch]] = {
    WuXing.WOOD: (EarthlyBranch.YIN, EarthlyBranch.MAO, EarthlyBranch.CHEN),
    WuXing.FIRE: (EarthlyBranch.SI, EarthlyBranch.WU, EarthlyBranch.WEI),
    WuXing.METAL: (EarthlyBranch.SHEN, EarthlyBranch.YOU, EarthlyBranch.XU),
    WuXing.WATER: (EarthlyBranch.HAI, EarthlyBranch.ZI, EarthlyBranch.CHOU),
}

_SAN_HUI_REVERSE: dict[EarthlyBranch, WuXing] = {}
for wx, branches in _SAN_HUI.items():
    for b in branches:
        _SAN_HUI_REVERSE[b] = wx


def san_hui_wuxing(branch: EarthlyBranch) -> WuXing | None:
    """Return the wuxing if the branch belongs to a 三会 group."""
    return _SAN_HUI_REVERSE.get(branch)


# ============================================================
# 地支六冲 (Six Clashes / Liu Chong)
# ============================================================
# 子午冲 丑未冲 寅申冲 卯酉冲 辰戌冲 巳亥冲
_SIX_CLASHES: dict[EarthlyBranch, EarthlyBranch] = {
    EarthlyBranch.ZI: EarthlyBranch.WU,
    EarthlyBranch.WU: EarthlyBranch.ZI,
    EarthlyBranch.CHOU: EarthlyBranch.WEI,
    EarthlyBranch.WEI: EarthlyBranch.CHOU,
    EarthlyBranch.YIN: EarthlyBranch.SHEN,
    EarthlyBranch.SHEN: EarthlyBranch.YIN,
    EarthlyBranch.MAO: EarthlyBranch.YOU,
    EarthlyBranch.YOU: EarthlyBranch.MAO,
    EarthlyBranch.CHEN: EarthlyBranch.XU,
    EarthlyBranch.XU: EarthlyBranch.CHEN,
    EarthlyBranch.SI: EarthlyBranch.HAI,
    EarthlyBranch.HAI: EarthlyBranch.SI,
}


def clash_branch(branch: EarthlyBranch) -> EarthlyBranch:
    """Return the opposing branch in 六冲."""
    return _SIX_CLASHES.get(branch, None)


def are_branches_clashing(a: EarthlyBranch, b: EarthlyBranch) -> bool:
    """Check if two branches form a 六冲 pair."""
    return _SIX_CLASHES.get(a) == b


# ============================================================
# 地支六害 (Six Harms / Liu Hai)
# ============================================================
# 子未害 丑午害 寅巳害 卯辰害 申亥害 酉戌害
_SIX_HARMS: dict[EarthlyBranch, EarthlyBranch] = {
    EarthlyBranch.ZI: EarthlyBranch.WEI,
    EarthlyBranch.WEI: EarthlyBranch.ZI,
    EarthlyBranch.CHOU: EarthlyBranch.WU,
    EarthlyBranch.WU: EarthlyBranch.CHOU,
    EarthlyBranch.YIN: EarthlyBranch.SI,
    EarthlyBranch.SI: EarthlyBranch.YIN,
    EarthlyBranch.MAO: EarthlyBranch.CHEN,
    EarthlyBranch.CHEN: EarthlyBranch.MAO,
    EarthlyBranch.SHEN: EarthlyBranch.HAI,
    EarthlyBranch.HAI: EarthlyBranch.SHEN,
    EarthlyBranch.YOU: EarthlyBranch.XU,
    EarthlyBranch.XU: EarthlyBranch.YOU,
}


def harm_branch(branch: EarthlyBranch) -> EarthlyBranch | None:
    """Return the harming branch in 六害."""
    return _SIX_HARMS.get(branch)


# ============================================================
# 三刑 (Three Punishments)
# ============================================================
# 无礼之刑: 子卯
# 无恩之刑: 寅巳申
# 恃势之刑: 丑戌未
# 自刑: 辰辰 午午 酉酉 亥亥
_PUNISHMENT_GROUPS: list[set[EarthlyBranch]] = [
    {EarthlyBranch.ZI, EarthlyBranch.MAO},                      # 无礼之刑
    {EarthlyBranch.YIN, EarthlyBranch.SI, EarthlyBranch.SHEN},  # 无恩之刑
    {EarthlyBranch.CHOU, EarthlyBranch.XU, EarthlyBranch.WEI},  # 恃势之刑
]

_SELF_PUNISHMENT: set[EarthlyBranch] = {
    EarthlyBranch.CHEN, EarthlyBranch.WU, EarthlyBranch.YOU, EarthlyBranch.HAI,
}


def are_branches_punishing(a: EarthlyBranch, b: EarthlyBranch) -> bool:
    """Check if two branches form a 三刑 relationship (includes self-punishment)."""
    if a == b and a in _SELF_PUNISHMENT:
        return True
    for group in _PUNISHMENT_GROUPS:
        if a in group and b in group and a != b:
            return True
    return False


def get_punishment_branches(branch: EarthlyBranch) -> list[EarthlyBranch]:
    """Return all branches that form a punishment relationship with the given branch."""
    result = []
    if branch in _SELF_PUNISHMENT:
        result.append(branch)
    for group in _PUNISHMENT_GROUPS:
        if branch in group:
            result.extend(b for b in group if b != branch)
    return result
