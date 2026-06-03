"""分析/报告路由 — /api/v1/bazi/analyze, /api/v1/bazi/report"""

from datetime import datetime

from fastapi import APIRouter, HTTPException

from bazi.types import Sex
from bazi.paipan import build_chart
from bazi.analysis import (
    analyze_shishen,
    analyze_shensha,
    analyze_geju,
    analyze_wang_shuai,
    analyze_yongshen,
)
from bazi.report import generate_report

from bazi_api.schemas.requests import CalculateRequest
from bazi_api.schemas.responses import (
    AnalyzeResponse,
    ReportResponse,
    ShiShenCountResponse,
    ShenShaResultResponse,
)

router = APIRouter(prefix="/api/v1/bazi", tags=["分析"])


def _build_full_chart(request: CalculateRequest):
    birth_dt = datetime.combine(request.birth_date, request.birth_time)
    sex = Sex.MALE if request.sex == "male" else Sex.FEMALE
    return build_chart(birth_dt, sex, request.longitude)


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: CalculateRequest):
    """全面分析八字命盘."""
    try:
        chart = _build_full_chart(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"排盘失败: {e}")

    sa = analyze_shishen(chart)
    ss = analyze_shensha(chart)
    ws = analyze_wang_shuai(chart)
    gj = analyze_geju(chart, ws.level)
    ys = analyze_yongshen(chart, ws)

    return AnalyzeResponse(
        sex=chart.sex.value,
        birth_datetime=chart.birth_datetime.isoformat(),
        day_master=chart.day_master.value,
        shishen=[
            ShiShenCountResponse(
                shishen=s.value,
                stem_count=c.stem_count,
                hidden_count=c.hidden_count,
                total=c.total,
            )
            for s, c in sorted(sa.counts.items(), key=lambda x: x[1].total, reverse=True)
        ],
        shensha=[
            ShenShaResultResponse(
                name=r.name,
                category=r.category,
                location=r.location,
                description=r.description,
            )
            for r in ss.results
        ],
        wang_shuai_level=ws.level,
        wang_shuai_score=ws.total,
        wang_shuai_details=ws.details,
        geju=gj.primary.pattern_name if gj.primary else "未定",
        geju_category=gj.primary.category if gj.primary else "未定",
        yong_shen=[w.value for w in ys.yong_shen],
        ji_shen=[w.value for w in ys.ji_shen],
        method=ys.method,
        suggestions=ys.suggestions,
    )


@router.post("/report", response_model=ReportResponse)
def report(request: CalculateRequest):
    """生成命理分析报告."""
    try:
        chart = _build_full_chart(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"排盘失败: {e}")

    report_obj = generate_report(chart)

    return ReportResponse(
        title=report_obj.title,
        sections=[
            {"heading": h, "content": c}
            for h, c in report_obj.sections
        ],
        plain_text=report_obj.render_plain(),
        markdown=report_obj.render(),
    )
