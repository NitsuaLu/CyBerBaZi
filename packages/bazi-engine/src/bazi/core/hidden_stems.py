"""地支藏干表 (Hidden Heavenly Stems within Earthly Branches).

Each earthly branch contains 1-3 hidden heavenly stems, classified as:
- 本气 (main qi) — the dominant stem
- 中气 (middle qi) — secondary
- 余气 (residual qi) — the weakest
"""

from __future__ import annotations

from bazi.core.earthly_branches import EarthlyBranch
from bazi.core.heavenly_stems import HeavenlyStem


class HiddenStemEntry:
    """A single hidden stem entry with its qi level."""

    def __init__(self, stem: HeavenlyStem, qi_level: str):
        self.stem = stem
        self.qi_level = qi_level  # "本气" / "中气" / "余气"

    def __repr__(self) -> str:
        return f"HiddenStemEntry({self.stem.value}, {self.qi_level})"


# Standard hidden stems table
_HIDDEN_STEMS: dict[EarthlyBranch, list[HiddenStemEntry]] = {
    EarthlyBranch.ZI: [
        HiddenStemEntry(HeavenlyStem.GUI, "本气"),
    ],
    EarthlyBranch.CHOU: [
        HiddenStemEntry(HeavenlyStem.JI, "本气"),
        HiddenStemEntry(HeavenlyStem.GUI, "中气"),
        HiddenStemEntry(HeavenlyStem.XIN, "余气"),
    ],
    EarthlyBranch.YIN: [
        HiddenStemEntry(HeavenlyStem.JIA, "本气"),
        HiddenStemEntry(HeavenlyStem.BING, "中气"),
        HiddenStemEntry(HeavenlyStem.WU, "余气"),
    ],
    EarthlyBranch.MAO: [
        HiddenStemEntry(HeavenlyStem.YI, "本气"),
    ],
    EarthlyBranch.CHEN: [
        HiddenStemEntry(HeavenlyStem.WU, "本气"),
        HiddenStemEntry(HeavenlyStem.YI, "中气"),
        HiddenStemEntry(HeavenlyStem.GUI, "余气"),
    ],
    EarthlyBranch.SI: [
        HiddenStemEntry(HeavenlyStem.BING, "本气"),
        HiddenStemEntry(HeavenlyStem.GENG, "中气"),
        HiddenStemEntry(HeavenlyStem.WU, "余气"),
    ],
    EarthlyBranch.WU: [
        HiddenStemEntry(HeavenlyStem.DING, "本气"),
        HiddenStemEntry(HeavenlyStem.JI, "中气"),
    ],
    EarthlyBranch.WEI: [
        HiddenStemEntry(HeavenlyStem.JI, "本气"),
        HiddenStemEntry(HeavenlyStem.DING, "中气"),
        HiddenStemEntry(HeavenlyStem.YI, "余气"),
    ],
    EarthlyBranch.SHEN: [
        HiddenStemEntry(HeavenlyStem.GENG, "本气"),
        HiddenStemEntry(HeavenlyStem.REN, "中气"),
        HiddenStemEntry(HeavenlyStem.WU, "余气"),
    ],
    EarthlyBranch.YOU: [
        HiddenStemEntry(HeavenlyStem.XIN, "本气"),
    ],
    EarthlyBranch.XU: [
        HiddenStemEntry(HeavenlyStem.WU, "本气"),
        HiddenStemEntry(HeavenlyStem.XIN, "中气"),
        HiddenStemEntry(HeavenlyStem.DING, "余气"),
    ],
    EarthlyBranch.HAI: [
        HiddenStemEntry(HeavenlyStem.REN, "本气"),
        HiddenStemEntry(HeavenlyStem.JIA, "中气"),
    ],
}


def get_hidden_stems(branch: EarthlyBranch) -> list[HiddenStemEntry]:
    """Return all hidden stems within an earthly branch."""
    return _HIDDEN_STEMS[branch]


def get_main_qi(branch: EarthlyBranch) -> HeavenlyStem:
    """Return the main-qi (本气) heavenly stem for an earthly branch."""
    return _HIDDEN_STEMS[branch][0].stem
