"""报告段落生成 (Report Section Generators).

Each function takes analysis results and returns formatted text for that section.
"""

from __future__ import annotations

from bazi.core.relationships import ShiShen
from bazi.types import BaziChart
from bazi.analysis.shishen import ShiShenAnalysis
from bazi.analysis.shensha import ShenShaAnalysis
from bazi.analysis.geju import GeJuAnalysis
from bazi.analysis.wangshuai import WangShuaiResult
from bazi.analysis.yongshen import YongShenResult


def section_basic_info(chart: BaziChart) -> str:
    """Generate the basic chart information section."""
    lines = []

    sex_label = "乾造" if chart.sex.value == "男" else "坤造"
    lines.append(f"性别: {chart.sex.value} ({sex_label})")
    lines.append(f"出生时间: {chart.birth_datetime.strftime('%Y年%m月%d日 %H:%M')}")

    if chart.true_solar_datetime:
        diff = chart.true_solar_datetime - chart.birth_datetime
        minutes = int(diff.total_seconds() / 60)
        if minutes != 0:
            sign = "+" if minutes > 0 else ""
            lines.append(f"真太阳时: {chart.true_solar_datetime.strftime('%Y年%m月%d日 %H:%M')} (校正{sign}{minutes}分钟)")

    lines.append("")
    lines.append("## 四柱命盘")
    lines.append("")
    lines.append("|  | 年柱 | 月柱 | 日柱 | 时柱 |")
    lines.append("|------|------|------|------|------|")

    pillars = chart.four_pillars
    labels = ["年柱", "月柱", "日柱", "时柱"]

    # 天干 row
    stems = "| 天干 |"
    for p in pillars:
        stems += f" **{p.heavenly_stem.value}** |"
    lines.append(stems)

    # 地支 row
    branches = "| 地支 |"
    for p in pillars:
        branches += f" {p.earthly_branch.value} |"
    lines.append(branches)

    # 藏干 row
    hidden = "| 藏干 |"
    for p in pillars:
        h_str = " ".join(h.stem.value for h in p.hidden_stems)
        hidden += f" {h_str} |"
    lines.append(hidden)

    # 十神 row
    shishen_row = "| 十神 |"
    for p in pillars:
        shishen_row += f" {p.stem_shishen.value if p.stem_shishen else '-'} |"
    lines.append(shishen_row)

    # 纳音 row
    nayin_row = "| 纳音 |"
    for p in pillars:
        nayin_row += f" {p.nayin} |"
    lines.append(nayin_row)

    lines.append("")

    # Day master info
    dm = chart.day_master
    lines.append(f"**日主**: {dm.value} ({dm.yin_yang.value}{dm.wuxing.value})")
    lines.append(f"**纳音**: {chart.day_pillar.nayin}")

    return "\n".join(lines)


def section_shishen(analysis: ShiShenAnalysis) -> str:
    """Generate the ShiShen analysis section."""
    lines = []

    lines.append(f"日主 **{analysis.day_master_stem}** 的十神分布如下：")
    lines.append("")

    for ss, count in sorted(analysis.counts.items(), key=lambda x: x[1].total, reverse=True):
        label = "吉" if ss.is_good else "凶"
        lines.append(
            f"- **{ss.value}**({label}): "
            f"天干透出 {count.stem_count} 位, "
            f"地支藏干 {count.hidden_count} 位, "
            f"共 {count.total} 位"
        )

    # Dominant shishen interpretation
    dominant = analysis.dominant_shishen
    if dominant:
        lines.append("")
        lines.append(f"命局中以 **{dominant.value}** 最为显著。")
        lines.append(_shishen_interpretation(dominant))

    return "\n".join(lines)


def _shishen_interpretation(ss: ShiShen) -> str:
    """Provide a short interpretation of a shishen."""
    interpretations = {
        ShiShen.ZHENG_GUAN: "正官代表事业、纪律、责任感。正官旺盛者行事端正，有管理才能。",
        ShiShen.QI_SHA: "七杀代表权威、竞争、魄力。七杀得力者处事果断，适合军警、管理岗位。",
        ShiShen.ZHENG_YIN: "正印代表学识、仁慈、贵人。正印有力者学业有成，得长辈庇荫。",
        ShiShen.PIAN_YIN: "偏印代表偏门学识、独特思维。偏印旺者善于钻研，适合技术、研究类工作。",
        ShiShen.ZHENG_CAI: "正财代表正当收入、稳定财源。正财有力者勤俭持家，财运稳定。",
        ShiShen.PIAN_CAI: "偏财代表意外之财、投资运气。偏财旺者善于经营，有商业头脑。",
        ShiShen.SHI_SHEN: "食神代表才华、享受、口福。食神旺盛者多才多艺，生活安逸。",
        ShiShen.SHANG_GUAN: "伤官代表创造力、表现欲、不拘一格。伤官得力者才华横溢，适合艺术创作。",
        ShiShen.BI_JIAN: "比肩代表兄弟朋友、竞争、自主。比肩多者独立性强，朋友多助。",
        ShiShen.JIE_CAI: "劫财代表合作、竞争、消耗。劫财多者社交能力强，但需注意财务规划。",
    }
    return interpretations.get(ss, "")


def section_shensha(analysis: ShenShaAnalysis) -> str:
    """Generate the ShenSha analysis section."""
    if not analysis.results:
        return "命局中未检出明显神煞。"

    lines = []
    ji_shen = [r for r in analysis.results if r.category == "吉神"]
    xiong_shen = [r for r in analysis.results if r.category == "凶神"]
    zhong_xing = [r for r in analysis.results if r.category == "中性"]

    if ji_shen:
        lines.append("### 吉神")
        for r in ji_shen:
            lines.append(f"- **{r.name}** ({r.location}): {r.description}")

    if xiong_shen:
        lines.append("")
        lines.append("### 凶神")
        for r in xiong_shen:
            lines.append(f"- **{r.name}** ({r.location}): {r.description}")

    if zhong_xing:
        lines.append("")
        lines.append("### 中性神煞")
        for r in zhong_xing:
            lines.append(f"- **{r.name}** ({r.location}): {r.description}")

    return "\n".join(lines)


def section_geju(analysis: GeJuAnalysis) -> str:
    """Generate the GeJu analysis section."""
    lines = []

    if analysis.primary:
        lines.append(f"**主格**: {analysis.primary.pattern_name} ({analysis.primary.category})")
        lines.append(f"{analysis.primary.description}")
    else:
        lines.append("格局未定。")

    if analysis.alternatives:
        others = [a for a in analysis.alternatives if a != analysis.primary]
        if others:
            lines.append("")
            lines.append("**其他可能格局**:")
            for a in others:
                lines.append(f"- {a.pattern_name}: {a.description}")

    return "\n".join(lines)


def section_wangshuai(result: WangShuaiResult) -> str:
    """Generate the WangShuai analysis section."""
    lines = []

    lines.append(f"**旺衰等级**: {result.level}")
    lines.append(f"**综合得分**: {result.total:.1f}")
    lines.append("")

    level_desc = {
        "极旺": "日主极旺，命局气势磅礴，宜顺势而为，不宜强行克制。",
        "偏旺": "日主偏旺，自身力量充实，有担当能力，但需适当平衡。",
        "中和": "日主中和，命局平衡协调，适应能力强，运势起伏较小。",
        "偏弱": "日主偏弱，需借助印星和比劫之力，适合合作发展。",
        "极弱": "日主极弱，宜从格而论，顺势而行，不宜强行独立支撑。",
    }
    lines.append(level_desc.get(result.level, ""))

    lines.append("")
    lines.append("**各维度分析**:")
    for detail in result.details:
        lines.append(f"- {detail}")

    return "\n".join(lines)


def section_yongshen(result: YongShenResult, chart: BaziChart) -> str:
    """Generate the YongShen analysis section."""
    lines = []

    lines.append(f"**分析方法**: {result.method}")
    lines.append("")

    if result.yong_shen:
        lines.append(f"**用神**: {', '.join(w.value for w in result.yong_shen)}")
        lines.append(f"**喜神**: {', '.join(w.value for w in result.xi_shen) if result.xi_shen else '无'}")
        lines.append(f"**忌神**: {', '.join(w.value for w in result.ji_shen) if result.ji_shen else '无'}")
        lines.append(f"**仇神**: {', '.join(w.value for w in result.chou_shen) if result.chou_shen else '无'}")

    if result.suggestions:
        lines.append("")
        lines.append("**命理建议**:")
        for s in result.suggestions:
            lines.append(f"- {s}")

    # Add element-specific advice
    lines.append("")
    lines.append(_element_advice(result, chart))

    return "\n".join(lines)


def _element_advice(result: YongShenResult, chart: BaziChart) -> str:
    """Generate element-based life advice."""
    lines = []

    if not result.yong_shen:
        return ""

    yong = result.yong_shen[0]

    advice = {
        "木": [
            "宜从事教育、文化、医疗、环保等行业",
            "宜居住东方或靠近园林绿地之处",
            "宜多穿戴绿色、青色衣物",
        ],
        "火": [
            "宜从事能源、餐饮、娱乐、传媒等行业",
            "宜居住南方或阳光充足之处",
            "宜多穿戴红色、紫色衣物",
        ],
        "土": [
            "宜从事房地产、建筑、农业、金融等行业",
            "宜居住中部或地势平坦之处",
            "宜多穿戴黄色、棕色衣物",
        ],
        "金": [
            "宜从事金融、法律、机械、IT等行业",
            "宜居住西方或靠近金属建筑之处",
            "宜多穿戴白色、金色衣物",
        ],
        "水": [
            "宜从事物流、贸易、旅游、水产等行业",
            "宜居住北方或靠近水源之处",
            "宜多穿戴黑色、蓝色衣物",
        ],
    }

    ad = advice.get(yong.value, ["五行调和，各业皆宜。"])

    lines.append(f"**用神为{yong.value}，命理建议**:")
    for a in ad:
        lines.append(f"- {a}")

    return "\n".join(lines)


def section_dayun(chart: BaziChart) -> str:
    """Generate the Fortune Cycles section."""
    lines = []

    lines.append(f"**起运年龄**: {chart.qi_yun_age} 岁")
    lines.append("")
    lines.append("**大运走势**:")
    lines.append("")

    for fc in chart.fortune_cycles:
        current_marker = " ← 当前" if _is_current_cycle(fc, chart) else ""
        lines.append(
            f"- **{fc.start_age}岁**: {fc.stem.value}{fc.branch.value} "
            f"({fc.start_year}年-{fc.end_year}年) 纳音{fc.nayin}{current_marker}"
        )

    return "\n".join(lines)


def _is_current_cycle(fc, chart: BaziChart) -> bool:
    """Check if a fortune cycle is the current one."""
    from datetime import datetime
    current_year = datetime.now().year
    return fc.start_year <= current_year <= fc.end_year


def section_summary(
    chart: BaziChart,
    ws: WangShuaiResult,
    gj: GeJuAnalysis,
    ys: YongShenResult,
) -> str:
    """Generate an overall summary of the chart."""
    lines = []

    dm = chart.day_master
    sex_label = "先生" if chart.sex.value == "男" else "女士"

    lines.append(
        f"此命为{chart.year_pillar.heavenly_stem.value}{chart.year_pillar.earthly_branch.value}年"
        f"出生之{sex_label}，"
        f"日主为 **{dm.value}** ({dm.yin_yang.value}{dm.wuxing.value})。"
    )

    if gj.primary:
        lines.append(f"命局为 **{gj.primary.pattern_name}**，")

    lines.append(f"日主{ws.level}（得分 {ws.total:.1f}）。")

    if ys.yong_shen:
        lines.append(
            f"以 **{'、'.join(w.value for w in ys.yong_shen)}** 为用神，"
            f"宜{'、'.join(w.value for w in ys.xi_shen) if ys.xi_shen else ''}为喜。"
        )

    lines.append("")
    lines.append("*此分析基于传统命理学方法，仅供参考。命理虽可揭示先天趋势，但后天努力与选择同样重要。*")

    return "\n".join(lines)
