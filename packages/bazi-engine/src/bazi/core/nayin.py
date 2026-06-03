"""六十甲子纳音表 (Na Yin / Melodious Sounds of the Sexagenary Cycle).

Each adjacent pair of heavenly-stem + earthly-branch combinations shares a nayin name.
For example: 甲子+乙丑 = 海中金, 丙寅+丁卯 = 炉中火, ...
"""

from __future__ import annotations

from bazi.core.heavenly_stems import HeavenlyStem
from bazi.core.earthly_branches import EarthlyBranch
from bazi.core.wuxing import WuXing


# (stem_order, branch_order) -> nayin_name
# Mapping follows the standard 60-Jiazi table
_NAYIN_TABLE: dict[tuple[int, int], tuple[str, WuXing]] = {
    # 甲子 乙丑 -> 海中金
    (1, 1): ("海中金", WuXing.METAL),
    (2, 2): ("海中金", WuXing.METAL),
    # 丙寅 丁卯 -> 炉中火
    (3, 3): ("炉中火", WuXing.FIRE),
    (4, 4): ("炉中火", WuXing.FIRE),
    # 戊辰 己巳 -> 大林木
    (5, 5): ("大林木", WuXing.WOOD),
    (6, 6): ("大林木", WuXing.WOOD),
    # 庚午 辛未 -> 路旁土
    (7, 7): ("路旁土", WuXing.EARTH),
    (8, 8): ("路旁土", WuXing.EARTH),
    # 壬申 癸酉 -> 剑锋金
    (9, 9): ("剑锋金", WuXing.METAL),
    (10, 10): ("剑锋金", WuXing.METAL),
    # 甲戌 乙亥 -> 山头火
    (1, 11): ("山头火", WuXing.FIRE),
    (2, 12): ("山头火", WuXing.FIRE),
    # 丙子 丁丑 -> 涧下水
    (3, 1): ("涧下水", WuXing.WATER),
    (4, 2): ("涧下水", WuXing.WATER),
    # 戊寅 己卯 -> 城头土
    (5, 3): ("城头土", WuXing.EARTH),
    (6, 4): ("城头土", WuXing.EARTH),
    # 庚辰 辛巳 -> 白蜡金
    (7, 5): ("白蜡金", WuXing.METAL),
    (8, 6): ("白蜡金", WuXing.METAL),
    # 壬午 癸未 -> 杨柳木
    (9, 7): ("杨柳木", WuXing.WOOD),
    (10, 8): ("杨柳木", WuXing.WOOD),
    # 甲申 乙酉 -> 泉中水
    (1, 9): ("泉中水", WuXing.WATER),
    (2, 10): ("泉中水", WuXing.WATER),
    # 丙戌 丁亥 -> 屋上土
    (3, 11): ("屋上土", WuXing.EARTH),
    (4, 12): ("屋上土", WuXing.EARTH),
    # 戊子 己丑 -> 霹雳火
    (5, 1): ("霹雳火", WuXing.FIRE),
    (6, 2): ("霹雳火", WuXing.FIRE),
    # 庚寅 辛卯 -> 松柏木
    (7, 3): ("松柏木", WuXing.WOOD),
    (8, 4): ("松柏木", WuXing.WOOD),
    # 壬辰 癸巳 -> 长流水
    (9, 5): ("长流水", WuXing.WATER),
    (10, 6): ("长流水", WuXing.WATER),
    # 甲午 乙未 -> 沙中金
    (1, 7): ("沙中金", WuXing.METAL),
    (2, 8): ("沙中金", WuXing.METAL),
    # 丙申 丁酉 -> 山下火
    (3, 9): ("山下火", WuXing.FIRE),
    (4, 10): ("山下火", WuXing.FIRE),
    # 戊戌 己亥 -> 平地木
    (5, 11): ("平地木", WuXing.WOOD),
    (6, 12): ("平地木", WuXing.WOOD),
    # 庚子 辛丑 -> 壁上土
    (7, 1): ("壁上土", WuXing.EARTH),
    (8, 2): ("壁上土", WuXing.EARTH),
    # 壬寅 癸卯 -> 金箔金
    (9, 3): ("金箔金", WuXing.METAL),
    (10, 4): ("金箔金", WuXing.METAL),
    # 甲辰 乙巳 -> 覆灯火
    (1, 5): ("覆灯火", WuXing.FIRE),
    (2, 6): ("覆灯火", WuXing.FIRE),
    # 丙午 丁未 -> 天河水
    (3, 7): ("天河水", WuXing.WATER),
    (4, 8): ("天河水", WuXing.WATER),
    # 戊申 己酉 -> 大驿土
    (5, 9): ("大驿土", WuXing.EARTH),
    (6, 10): ("大驿土", WuXing.EARTH),
    # 庚戌 辛亥 -> 钗钏金
    (7, 11): ("钗钏金", WuXing.METAL),
    (8, 12): ("钗钏金", WuXing.METAL),
    # 壬子 癸丑 -> 桑柘木
    (9, 1): ("桑柘木", WuXing.WOOD),
    (10, 2): ("桑柘木", WuXing.WOOD),
    # 甲寅 乙卯 -> 大溪水
    (1, 3): ("大溪水", WuXing.WATER),
    (2, 4): ("大溪水", WuXing.WATER),
    # 丙辰 丁巳 -> 沙中土
    (3, 5): ("沙中土", WuXing.EARTH),
    (4, 6): ("沙中土", WuXing.EARTH),
    # 戊午 己未 -> 天上火
    (5, 7): ("天上火", WuXing.FIRE),
    (6, 8): ("天上火", WuXing.FIRE),
    # 庚申 辛酉 -> 石榴木
    (7, 9): ("石榴木", WuXing.WOOD),
    (8, 10): ("石榴木", WuXing.WOOD),
    # 壬戌 癸亥 -> 大海水
    (9, 11): ("大海水", WuXing.WATER),
    (10, 12): ("大海水", WuXing.WATER),
}


def get_nayin(stem: HeavenlyStem, branch: EarthlyBranch) -> tuple[str, WuXing]:
    """Return (nayin_name, nayin_wuxing) for a given stem-branch pair.

    >>> from bazi.core.heavenly_stems import HeavenlyStem
    >>> from bazi.core.earthly_branches import EarthlyBranch
    >>> name, wx = get_nayin(HeavenlyStem.JIA, EarthlyBranch.ZI)
    >>> name
    '海中金'
    >>> wx
    WuXing.METAL
    """
    key = (stem.order, branch.order)
    if key not in _NAYIN_TABLE:
        raise ValueError(f"No nayin entry for {stem.value}{branch.value}")
    return _NAYIN_TABLE[key]


def get_nayin_by_sexagenary_index(index: int) -> tuple[str, WuXing]:
    """Return nayin for a 1-indexed position in the 60-Jiazi cycle."""
    stem_order = ((index - 1) % 10) + 1
    branch_order = ((index - 1) % 12) + 1
    return get_nayin(
        HeavenlyStem.from_order(stem_order),
        EarthlyBranch.from_order(branch_order),
    )
