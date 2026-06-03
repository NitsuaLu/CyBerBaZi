"""十神分析 (Shi Shen Analysis).

Analyzes the Ten God (十神) distribution across a BaZi chart:
- Count of each shishen type across heavenly stems and hidden stems
- 透干 (heavenly stem reveal) vs 藏支 (hidden in branch) analysis
- Location analysis: which pillar each shishen appears in
"""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import Counter

from bazi.core.relationships import ShiShen
from bazi.types import BaziChart, Pillar


@dataclass
class ShiShenCount:
    """Count of a specific shishen type in the chart."""
    shishen: ShiShen
    stem_count: int = 0       # count in heavenly stems (透干)
    hidden_count: int = 0     # count in hidden stems (藏支)
    total: int = 0

    @property
    def stems(self) -> int:
        return self.stem_count

    @property
    def hidden(self) -> int:
        return self.hidden_count


@dataclass
class ShiShenAnalysis:
    """Complete shishen analysis for a BaZi chart."""

    day_master_stem: str
    counts: dict[ShiShen, ShiShenCount] = field(default_factory=dict)
    stem_by_pillar: dict[str, ShiShen] = field(default_factory=dict)
    # pillar_name -> list of (hidden_stem_value, shishen)
    hidden_by_pillar: dict[str, list[tuple[str, ShiShen]]] = field(
        default_factory=lambda: {"年柱": [], "月柱": [], "日柱": [], "时柱": []}
    )

    @property
    def dominant_shishen(self) -> ShiShen | None:
        """Return the most frequent shishen (stems only)."""
        if not self.counts:
            return None
        return max(self.counts, key=lambda s: self.counts[s].stem_count)

    @property
    def all_stem_shishen(self) -> list[ShiShen]:
        """Return all shishen values for the four heavenly stems."""
        return list(self.stem_by_pillar.values())


def analyze_shishen(chart: BaziChart) -> ShiShenAnalysis:
    """Analyze the shishen distribution in a BaZi chart."""
    if chart.day_master is None:
        raise ValueError("Chart must have a day master")

    analysis = ShiShenAnalysis(
        day_master_stem=chart.day_master.value,
    )

    pillar_names = ["年柱", "月柱", "日柱", "时柱"]
    counts: dict[ShiShen, ShiShenCount] = {}

    for name, pillar in zip(pillar_names, chart.four_pillars):
        # Heavenly stem shishen
        ss = pillar.stem_shishen
        if ss is not None:
            if ss not in counts:
                counts[ss] = ShiShenCount(shishen=ss)
            counts[ss].stem_count += 1
            analysis.stem_by_pillar[name] = ss

        # Hidden stem shishen
        for h in pillar.hidden_stems:
            if h.shishen is not None:
                if h.shishen not in counts:
                    counts[h.shishen] = ShiShenCount(shishen=h.shishen)
                counts[h.shishen].hidden_count += 1
                analysis.hidden_by_pillar[name].append((h.stem.value, h.shishen))

    # Update totals
    for c in counts.values():
        c.total = c.stem_count + c.hidden_count

    analysis.counts = counts
    return analysis
