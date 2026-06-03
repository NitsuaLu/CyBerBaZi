from enum import Enum


class WuXing(Enum):
    """五行 (Five Elements / Five Phases)."""

    WOOD = "木"
    FIRE = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"

    def __repr__(self) -> str:
        return f"WuXing.{self.name}"

    def generates(self) -> "WuXing":
        """Return the element this one generates (相生)."""
        return WUXING_GENERATES[self]

    def generated_by(self) -> "WuXing":
        """Return the element that generates this one."""
        return WUXING_GENERATED_BY[self]

    def overcomes(self) -> "WuXing":
        """Return the element this one overcomes (相克)."""
        return WUXING_OVERCOMES[self]

    def overcome_by(self) -> "WuXing":
        """Return the element that overcomes this one."""
        return WUXING_OVERCOME_BY[self]


# 木生火 火生土 土生金 金生水 水生木
WUXING_GENERATES: dict[WuXing, WuXing] = {
    WuXing.WOOD: WuXing.FIRE,
    WuXing.FIRE: WuXing.EARTH,
    WuXing.EARTH: WuXing.METAL,
    WuXing.METAL: WuXing.WATER,
    WuXing.WATER: WuXing.WOOD,
}

WUXING_GENERATED_BY: dict[WuXing, WuXing] = {v: k for k, v in WUXING_GENERATES.items()}

# 木克土 土克水 水克火 火克金 金克木
WUXING_OVERCOMES: dict[WuXing, WuXing] = {
    WuXing.WOOD: WuXing.EARTH,
    WuXing.EARTH: WuXing.WATER,
    WuXing.WATER: WuXing.FIRE,
    WuXing.FIRE: WuXing.METAL,
    WuXing.METAL: WuXing.WOOD,
}

WUXING_OVERCOME_BY: dict[WuXing, WuXing] = {v: k for k, v in WUXING_OVERCOMES.items()}
