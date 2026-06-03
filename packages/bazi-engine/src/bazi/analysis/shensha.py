"""神煞系统 (Shen Sha / Divine Spirits).

Implements the major Shen Sha (divine spirits) used in BaZi analysis.
Each shensha has lookup rules based on stems and branches in the chart.

Implemented shensha:
- 天乙贵人, 文昌贵人, 桃花(咸池), 驿马, 羊刃, 禄神
- 空亡, 华盖, 天德贵人, 月德贵人, 将星
"""

from __future__ import annotations

from dataclasses import dataclass, field

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.types import BaziChart, Pillar


@dataclass
class ShenShaResult:
    """A single shensha found in the chart."""
    name: str
    category: str           # "吉神" / "凶神" / "中性"
    location: str           # "年柱" / "月柱" / "日柱" / "时柱" / "命局"
    description: str = ""


@dataclass
class ShenShaAnalysis:
    """Complete shensha analysis for a BaZi chart."""
    results: list[ShenShaResult] = field(default_factory=list)
    stem_based: dict[str, list[ShenShaResult]] = field(default_factory=dict)
    branch_based: dict[str, list[ShenShaResult]] = field(default_factory=dict)


# ============================================================
# 天乙贵人 lookup tables
# ============================================================
TIANYI_BY_STEM: dict[HeavenlyStem, list[EarthlyBranch]] = {
    HeavenlyStem.JIA:  [EarthlyBranch.CHOU, EarthlyBranch.WEI],
    HeavenlyStem.WU:   [EarthlyBranch.CHOU, EarthlyBranch.WEI],
    HeavenlyStem.GENG: [EarthlyBranch.CHOU, EarthlyBranch.WEI],
    HeavenlyStem.YI:   [EarthlyBranch.ZI, EarthlyBranch.SHEN],
    HeavenlyStem.JI:   [EarthlyBranch.ZI, EarthlyBranch.SHEN],
    HeavenlyStem.BING: [EarthlyBranch.HAI, EarthlyBranch.YOU],
    HeavenlyStem.DING: [EarthlyBranch.HAI, EarthlyBranch.YOU],
    HeavenlyStem.XIN:  [EarthlyBranch.WU, EarthlyBranch.YIN],
    HeavenlyStem.REN:  [EarthlyBranch.MAO, EarthlyBranch.SI],
    HeavenlyStem.GUI:  [EarthlyBranch.MAO, EarthlyBranch.SI],
}

# ============================================================
# 文昌贵人 lookup
# ============================================================
WENCHANG_BY_STEM: dict[HeavenlyStem, EarthlyBranch] = {
    HeavenlyStem.JIA:  EarthlyBranch.SI,
    HeavenlyStem.YI:   EarthlyBranch.WU,
    HeavenlyStem.BING: EarthlyBranch.SHEN,
    HeavenlyStem.DING: EarthlyBranch.YOU,
    HeavenlyStem.WU:   EarthlyBranch.SHEN,
    HeavenlyStem.JI:   EarthlyBranch.YOU,
    HeavenlyStem.GENG: EarthlyBranch.HAI,
    HeavenlyStem.XIN:  EarthlyBranch.ZI,
    HeavenlyStem.REN:  EarthlyBranch.YIN,
    HeavenlyStem.GUI:  EarthlyBranch.MAO,
}

# ============================================================
# 禄神 lookup
# ============================================================
LU_SHEN_BY_STEM: dict[HeavenlyStem, EarthlyBranch] = {
    HeavenlyStem.JIA:  EarthlyBranch.YIN,
    HeavenlyStem.YI:   EarthlyBranch.MAO,
    HeavenlyStem.BING: EarthlyBranch.SI,
    HeavenlyStem.DING: EarthlyBranch.WU,
    HeavenlyStem.WU:   EarthlyBranch.SI,
    HeavenlyStem.JI:   EarthlyBranch.WU,
    HeavenlyStem.GENG: EarthlyBranch.SHEN,
    HeavenlyStem.XIN:  EarthlyBranch.YOU,
    HeavenlyStem.REN:  EarthlyBranch.HAI,
    HeavenlyStem.GUI:  EarthlyBranch.ZI,
}

# ============================================================
# 羊刃 lookup
# ============================================================
YANG_REN_BY_STEM: dict[HeavenlyStem, EarthlyBranch] = {
    HeavenlyStem.JIA:  EarthlyBranch.MAO,
    HeavenlyStem.BING: EarthlyBranch.WU,
    HeavenlyStem.WU:   EarthlyBranch.WU,
    HeavenlyStem.GENG: EarthlyBranch.YOU,
    HeavenlyStem.REN:  EarthlyBranch.ZI,
    HeavenlyStem.YI:   EarthlyBranch.YIN,
    HeavenlyStem.DING: EarthlyBranch.SI,
    HeavenlyStem.JI:   EarthlyBranch.SI,
    HeavenlyStem.XIN:  EarthlyBranch.SHEN,
    HeavenlyStem.GUI:  EarthlyBranch.HAI,
}

# ============================================================
# 桃花(咸池), 驿马, 华盖, 将星 — 基于三合局
# These use San He groups: 申子辰, 寅午戌, 巳酉丑, 亥卯未
# ============================================================
_SAN_HE_GROUPS = {
    "water": [EarthlyBranch.SHEN, EarthlyBranch.ZI, EarthlyBranch.CHEN],
    "fire":  [EarthlyBranch.YIN, EarthlyBranch.WU, EarthlyBranch.XU],
    "metal": [EarthlyBranch.SI, EarthlyBranch.YOU, EarthlyBranch.CHOU],
    "wood":  [EarthlyBranch.HAI, EarthlyBranch.MAO, EarthlyBranch.WEI],
}

TAOHUA_BY_GROUP = {
    "water": EarthlyBranch.YOU,
    "fire":  EarthlyBranch.MAO,
    "metal": EarthlyBranch.WU,
    "wood":  EarthlyBranch.ZI,
}

YIMA_BY_GROUP = {
    "water": EarthlyBranch.YIN,
    "fire":  EarthlyBranch.SHEN,
    "metal": EarthlyBranch.HAI,
    "wood":  EarthlyBranch.SI,
}

HUAGAI_BY_GROUP = {
    "water": EarthlyBranch.CHEN,
    "fire":  EarthlyBranch.XU,
    "metal": EarthlyBranch.CHOU,
    "wood":  EarthlyBranch.WEI,
}

JIANGXING_BY_GROUP = {
    "water": EarthlyBranch.ZI,
    "fire":  EarthlyBranch.WU,
    "metal": EarthlyBranch.YOU,
    "wood":  EarthlyBranch.MAO,
}


def _get_san_he_group(branch: EarthlyBranch) -> str | None:
    """Return the San He group name for an earthly branch."""
    for name, members in _SAN_HE_GROUPS.items():
        if branch in members:
            return name
    return None


# ============================================================
# 天德贵人 based on month branch
# ============================================================
# 天德贵人: month branch -> target heavenly stem
# Some months map to stems, some to branches — split into two tables
TIANDE_STEM_BY_MONTH: dict[EarthlyBranch, HeavenlyStem] = {
    EarthlyBranch.YIN:  HeavenlyStem.DING,   # 正月见丁
    EarthlyBranch.CHEN: HeavenlyStem.REN,    # 三月见壬
    EarthlyBranch.SI:   HeavenlyStem.XIN,    # 四月见辛
    EarthlyBranch.WEI:  HeavenlyStem.JIA,    # 六月见甲
    EarthlyBranch.SHEN: HeavenlyStem.GUI,    # 七月见癸
    EarthlyBranch.XU:   HeavenlyStem.BING,   # 九月见丙
    EarthlyBranch.HAI:  HeavenlyStem.YI,     # 十月见乙
    EarthlyBranch.CHOU: HeavenlyStem.GENG,   # 十二月见庚
}

# 天德贵人 (branch version): month branch -> target earthly branch
TIANDE_BRANCH_BY_MONTH: dict[EarthlyBranch, EarthlyBranch] = {
    EarthlyBranch.MAO: EarthlyBranch.SHEN,  # 二月见申
    EarthlyBranch.WU:  EarthlyBranch.HAI,   # 五月见亥
    EarthlyBranch.YOU: EarthlyBranch.YIN,   # 八月见寅
    EarthlyBranch.ZI:  EarthlyBranch.SI,    # 十一月见巳
}

# ============================================================
# 月德贵人 based on month branch
# ============================================================

# We need to check both stems and branches present in the chart.

# ============================================================
# 月德贵人 based on month branch
# ============================================================
YUEDE_BY_SANHE: dict[str, HeavenlyStem] = {
    "fire":  HeavenlyStem.BING,
    "wood":  HeavenlyStem.JIA,
    "water": HeavenlyStem.REN,
    "metal": HeavenlyStem.GENG,
}


def _find_tiande(chart: BaziChart) -> list[ShenShaResult]:
    """Find 天德贵人 in the chart."""
    month_branch = chart.month_pillar.earthly_branch
    pillar_names = ["年柱", "月柱", "日柱", "时柱"]
    results = []

    # Stem-based 天德
    if month_branch in TIANDE_STEM_BY_MONTH:
        target_stem = TIANDE_STEM_BY_MONTH[month_branch]
        for name, pillar in zip(pillar_names, chart.four_pillars):
            if pillar.heavenly_stem == target_stem:
                results.append(ShenShaResult(
                    name="天德贵人",
                    category="吉神",
                    location=name,
                    description=f"月支{month_branch.value}, 见{target_stem.value}在{name}",
                ))

    # Branch-based 天德 entries (申, 亥, 寅, 巳)
    if month_branch in TIANDE_BRANCH_BY_MONTH:
        target_branch = TIANDE_BRANCH_BY_MONTH[month_branch]
        for name, pillar in zip(pillar_names, chart.four_pillars):
            if pillar.earthly_branch == target_branch:
                results.append(ShenShaResult(
                    name="天德贵人",
                    category="吉神",
                    location=name,
                    description=f"月支{month_branch.value}, 见{target_branch.value}在{name}",
                ))

    return results


def _find_yuede(chart: BaziChart) -> list[ShenShaResult]:
    """Find 月德贵人 in the chart."""
    month_branch = chart.month_pillar.earthly_branch
    group = _get_san_he_group(month_branch)
    if group is None or group not in YUEDE_BY_SANHE:
        return []

    target_stem = YUEDE_BY_SANHE[group]
    results = []
    pillar_names = ["年柱", "月柱", "日柱", "时柱"]
    for name, pillar in zip(pillar_names, chart.four_pillars):
        if pillar.heavenly_stem == target_stem:
            results.append(ShenShaResult(
                name="月德贵人",
                category="吉神",
                location=name,
                description=f"月支{month_branch.value}属{group}局, 见{target_stem.value}在{name}",
            ))
    return results


def _find_taohua(chart: BaziChart, by: str = "日") -> list[ShenShaResult]:
    """Find 桃花(咸池). By default checks day branch, also checks year branch."""
    results = []
    pillar_names = ["年柱", "月柱", "日柱", "时柱"]
    ref_branches = []

    if by in ("日", "all"):
        ref_branches.append(("日支", chart.day_pillar.earthly_branch))
    if by in ("年", "all"):
        ref_branches.append(("年支", chart.year_pillar.earthly_branch))

    for ref_label, ref_branch in ref_branches:
        group = _get_san_he_group(ref_branch)
        if group is None:
            continue
        target = TAOHUA_BY_GROUP[group]
        for name, pillar in zip(pillar_names, chart.four_pillars):
            if pillar.earthly_branch == target:
                results.append(ShenShaResult(
                    name="桃花(咸池)",
                    category="中性",
                    location=name,
                    description=f"{ref_label}{ref_branch.value}属{group}局, 桃花在{target.value}",
                ))
    return results


def _find_yima(chart: BaziChart) -> list[ShenShaResult]:
    """Find 驿马 based on day branch."""
    results = []
    group = _get_san_he_group(chart.day_pillar.earthly_branch)
    if group is None:
        return results
    target = YIMA_BY_GROUP[group]
    pillar_names = ["年柱", "月柱", "日柱", "时柱"]
    for name, pillar in zip(pillar_names, chart.four_pillars):
        if pillar.earthly_branch == target:
            results.append(ShenShaResult(
                name="驿马",
                category="中性",
                location=name,
                description=f"日支{chart.day_pillar.earthly_branch.value}属{group}局, 驿马在{target.value}",
            ))
    return results


def _find_huagai(chart: BaziChart) -> list[ShenShaResult]:
    """Find 华盖 based on day branch."""
    results = []
    group = _get_san_he_group(chart.day_pillar.earthly_branch)
    if group is None:
        return results
    target = HUAGAI_BY_GROUP[group]
    pillar_names = ["年柱", "月柱", "日柱", "时柱"]
    for name, pillar in zip(pillar_names, chart.four_pillars):
        if pillar.earthly_branch == target:
            results.append(ShenShaResult(
                name="华盖",
                category="中性",
                location=name,
                description=f"日支{chart.day_pillar.earthly_branch.value}属{group}局, 华盖在{target.value}",
            ))
    return results


def _find_jiangxing(chart: BaziChart) -> list[ShenShaResult]:
    """Find 将星 based on day branch."""
    results = []
    group = _get_san_he_group(chart.day_pillar.earthly_branch)
    if group is None:
        return results
    target = JIANGXING_BY_GROUP[group]
    pillar_names = ["年柱", "月柱", "日柱", "时柱"]
    for name, pillar in zip(pillar_names, chart.four_pillars):
        if pillar.earthly_branch == target:
            results.append(ShenShaResult(
                name="将星",
                category="吉神",
                location=name,
                description=f"日支{chart.day_pillar.earthly_branch.value}属{group}局, 将星在{target.value}",
            ))
    return results


def _find_xun_kong(chart: BaziChart) -> list[ShenShaResult]:
    """Find 空亡 based on the day pillar's xun (旬空).

    The 60 sexagenary cycle is divided into 6 xun, each covering 10 days.
    Each xun has 2 empty branches.
    """
    day_stem_order = chart.day_pillar.heavenly_stem.order
    day_branch_order = chart.day_pillar.earthly_branch.order

    # Determine which xun the day pillar belongs to
    # Xun leader stem: the stem at the start of each xun
    # 甲子(1,1), 甲戌(1,11), 甲申(1,9), 甲午(1,7), 甲辰(1,5), 甲寅(1,3)
    # The two empty branches for each xun:
    XUN_KONG_MAP = {
        1:  [EarthlyBranch.XU, EarthlyBranch.HAI],   # 甲子旬 → 戌亥空
        11: [EarthlyBranch.SHEN, EarthlyBranch.YOU],  # 甲戌旬 → 申酉空
        9:  [EarthlyBranch.WU, EarthlyBranch.WEI],    # 甲申旬 → 午未空
        7:  [EarthlyBranch.CHEN, EarthlyBranch.SI],   # 甲午旬 → 辰巳空
        5:  [EarthlyBranch.YIN, EarthlyBranch.MAO],   # 甲辰旬 → 寅卯空
        3:  [EarthlyBranch.ZI, EarthlyBranch.CHOU],   # 甲寅旬 → 子丑空
    }

    # Find xun leader: the most recent branch with order = (day_branch_order - day_stem_order + 1) mod 12 ...
    # Actually, find when stem order = day_stem_order - offset gives 1 (甲),
    # and corresponding branch order = day_branch_order - offset
    # offset = day_stem_order - 1 (since 甲 = order 1)
    offset = day_stem_order - 1
    xun_leader_branch = ((day_branch_order - offset - 1) % 12) + 1

    if xun_leader_branch not in XUN_KONG_MAP:
        return []

    empty_branches = XUN_KONG_MAP[xun_leader_branch]

    results = []
    pillar_names = ["年柱", "月柱", "日柱", "时柱"]
    for name, pillar in zip(pillar_names, chart.four_pillars):
        if pillar.earthly_branch in empty_branches:
            results.append(ShenShaResult(
                name="空亡",
                category="凶神",
                location=name,
                description=f"日柱属{xun_leader_branch}旬, 空{empty_branches[0].value}{empty_branches[1].value}",
            ))
    return results


def analyze_shensha(chart: BaziChart) -> ShenShaAnalysis:
    """Analyze all shensha in a BaZi chart."""
    analysis = ShenShaAnalysis()

    # ---- Stem-based shensha (check which pillar has the target branch) ----
    day_stem = chart.day_master
    pillar_names = ["年柱", "月柱", "日柱", "时柱"]

    # 天乙贵人
    if day_stem in TIANYI_BY_STEM:
        targets = TIANYI_BY_STEM[day_stem]
        for name, pillar in zip(pillar_names, chart.four_pillars):
            if pillar.earthly_branch in targets:
                r = ShenShaResult(
                    name="天乙贵人",
                    category="吉神",
                    location=name,
                    description=f"日主{day_stem.value}, 贵人{targets[0].value}/{targets[1].value}",
                )
                analysis.results.append(r)

    # 文昌贵人
    if day_stem in WENCHANG_BY_STEM:
        target = WENCHANG_BY_STEM[day_stem]
        for name, pillar in zip(pillar_names, chart.four_pillars):
            if pillar.earthly_branch == target:
                analysis.results.append(ShenShaResult(
                    name="文昌贵人",
                    category="吉神",
                    location=name,
                    description=f"日主{day_stem.value}, 文昌在{target.value}",
                ))

    # 禄神
    if day_stem in LU_SHEN_BY_STEM:
        target = LU_SHEN_BY_STEM[day_stem]
        for name, pillar in zip(pillar_names, chart.four_pillars):
            if pillar.earthly_branch == target:
                analysis.results.append(ShenShaResult(
                    name="禄神",
                    category="吉神",
                    location=name,
                    description=f"日主{day_stem.value}, 禄在{target.value}",
                ))

    # 羊刃
    if day_stem in YANG_REN_BY_STEM:
        target = YANG_REN_BY_STEM[day_stem]
        for name, pillar in zip(pillar_names, chart.four_pillars):
            if pillar.earthly_branch == target:
                analysis.results.append(ShenShaResult(
                    name="羊刃",
                    category="凶神",
                    location=name,
                    description=f"日主{day_stem.value}, 刃在{target.value}",
                ))

    # ---- Branch-based shensha ----
    analysis.results.extend(_find_taohua(chart, by="all"))
    analysis.results.extend(_find_yima(chart))
    analysis.results.extend(_find_huagai(chart))
    analysis.results.extend(_find_jiangxing(chart))
    analysis.results.extend(_find_xun_kong(chart))
    analysis.results.extend(_find_tiande(chart))
    analysis.results.extend(_find_yuede(chart))

    return analysis
