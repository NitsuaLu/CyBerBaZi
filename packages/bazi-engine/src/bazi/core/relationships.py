"""十神关系推导引擎 (Ten Gods / Shi Shen).

Given a Day-Master stem and a target stem, derive the Ten-God relationship.

Ten Gods:
- 比肩 (Bi Jian / Peer)     — same wuxing, same yinyang
- 劫财 (Jie Cai / Rob Wealth) — same wuxing, opposite yinyang
- 食神 (Shi Shen / Eating God)   — I generate, same yinyang
- 伤官 (Shang Guan / Hurting Officer)  — I generate, opposite yinyang
- 偏财 (Pian Cai / Indirect Wealth)  — I overcome, same yinyang
- 正财 (Zheng Cai / Direct Wealth)   — I overcome, opposite yinyang
- 七杀 (Qi Sha / Seven Killings)     — overcomes me, same yinyang
- 正官 (Zheng Guan / Direct Officer) — overcomes me, opposite yinyang
- 偏印 (Pian Yin / Indirect Resource) — generates me, same yinyang
- 正印 (Zheng Yin / Direct Resource)  — generates me, opposite yinyang
"""

from __future__ import annotations

from enum import Enum

from bazi.core.heavenly_stems import HeavenlyStem, YinYang
from bazi.core.wuxing import WuXing


class ShiShen(Enum):
    """十神枚举."""

    BI_JIAN = "比肩"           # Peer
    JIE_CAI = "劫财"           # Rob Wealth
    SHI_SHEN = "食神"          # Eating God
    SHANG_GUAN = "伤官"        # Hurting Officer
    PIAN_CAI = "偏财"          # Indirect Wealth
    ZHENG_CAI = "正财"         # Direct Wealth
    QI_SHA = "七杀"            # Seven Killings
    ZHENG_GUAN = "正官"        # Direct Officer
    PIAN_YIN = "偏印"          # Indirect Resource
    ZHENG_YIN = "正印"         # Direct Resource

    def __repr__(self) -> str:
        return f"ShiShen.{self.name}"

    @property
    def is_good(self) -> bool:
        """Rough classification: traditionally auspicious or neutral."""
        return self in (
            ShiShen.ZHENG_YIN, ShiShen.ZHENG_GUAN, ShiShen.ZHENG_CAI,
            ShiShen.SHI_SHEN, ShiShen.BI_JIAN,
        )

    @property
    def is_evil(self) -> bool:
        """Rough classification: traditionally inauspicious."""
        return self in (
            ShiShen.QI_SHA, ShiShen.SHANG_GUAN, ShiShen.JIE_CAI,
            ShiShen.PIAN_YIN, ShiShen.PIAN_CAI,
        )


def get_shishen(day_master: HeavenlyStem, target: HeavenlyStem) -> ShiShen:
    """Derive the Ten-God relationship of `target` relative to `day_master`.

    Args:
        day_master: The 日主 (Day Master) stem.
        target: Any other heavenly stem.

    Returns:
        The ShiShen relationship.

    Examples:
        >>> dm = HeavenlyStem.JIA  # 甲木阳
        >>> get_shishen(dm, HeavenlyStem.JIA)  # 甲 vs 甲 = same, 比肩
        ShiShen.BI_JIAN
        >>> get_shishen(dm, HeavenlyStem.YI)   # 甲 vs 乙 = same wx diff yy, 劫财
        ShiShen.JIE_CAI
        >>> get_shishen(dm, HeavenlyStem.BING) # 甲(木)生火, 甲阳丙阳 = same yy, 食神
        ShiShen.SHI_SHEN
        >>> get_shishen(dm, HeavenlyStem.DING) # 甲(木)生火, 甲阳丁阴 = diff yy, 伤官
        ShiShen.SHANG_GUAN
        >>> get_shishen(dm, HeavenlyStem.WU)   # 甲(木)克土, 甲阳戊阳 = same yy, 偏财
        ShiShen.PIAN_CAI
        >>> get_shishen(dm, HeavenlyStem.JI)   # 甲(木)克土, 甲阳己阴 = diff yy, 正财
        ShiShen.ZHENG_CAI
        >>> get_shishen(dm, HeavenlyStem.GENG) # 金克木, 庚阳甲阳 = same yy, 七杀
        ShiShen.QI_SHA
        >>> get_shishen(dm, HeavenlyStem.XIN)  # 金克木, 辛阴甲阳 = diff yy, 正官
        ShiShen.ZHENG_GUAN
        >>> get_shishen(dm, HeavenlyStem.REN)  # 水生木, 壬阳甲阳 = same yy, 偏印
        ShiShen.PIAN_YIN
        >>> get_shishen(dm, HeavenlyStem.GUI)  # 水生木, 癸阴甲阳 = diff yy, 正印
        ShiShen.ZHENG_YIN
    """
    if target == day_master:
        return ShiShen.BI_JIAN

    dm_wx = day_master.wuxing
    target_wx = target.wuxing
    dm_yy = day_master.yin_yang
    target_yy = target.yin_yang
    same_yy = (dm_yy == target_yy)

    if target_wx == dm_wx:
        # Same element
        return ShiShen.BI_JIAN if same_yy else ShiShen.JIE_CAI

    if dm_wx.generates() == target_wx:
        # Day master generates target (我生)
        return ShiShen.SHI_SHEN if same_yy else ShiShen.SHANG_GUAN

    if dm_wx.overcomes() == target_wx:
        # Day master overcomes target (我克)
        return ShiShen.PIAN_CAI if same_yy else ShiShen.ZHENG_CAI

    if target_wx.overcomes() == dm_wx:
        # Target overcomes day master (克我)
        return ShiShen.QI_SHA if same_yy else ShiShen.ZHENG_GUAN

    if target_wx.generates() == dm_wx:
        # Target generates day master (生我)
        return ShiShen.PIAN_YIN if same_yy else ShiShen.ZHENG_YIN

    raise ValueError(
        f"Cannot determine shishen for day_master={dm_wx} target={target_wx}"
    )
