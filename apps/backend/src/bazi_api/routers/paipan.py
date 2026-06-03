"""排盘路由 — /api/v1/bazi/calculate"""

from datetime import datetime

from fastapi import APIRouter, HTTPException

from bazi.types import Sex
from bazi.paipan import build_chart

from bazi_api.schemas.requests import CalculateRequest
from bazi_api.schemas.responses import (
    CalculateResponse,
    PillarResponse,
    HiddenStemResponse,
    FortuneCycleResponse,
)

router = APIRouter(prefix="/api/v1/bazi", tags=["排盘"])


def _pillar_to_response(pillar) -> PillarResponse:
    return PillarResponse(
        heavenly_stem=pillar.heavenly_stem.value,
        earthly_branch=pillar.earthly_branch.value,
        hidden_stems=[
            HiddenStemResponse(
                stem=h.stem.value,
                qi_level=h.qi_level,
                shishen=h.shishen.value if h.shishen else None,
            )
            for h in pillar.hidden_stems
        ],
        nayin=pillar.nayin,
        stem_shishen=pillar.stem_shishen.value if pillar.stem_shishen else None,
    )


@router.post("/calculate", response_model=CalculateResponse)
def calculate(request: CalculateRequest):
    """计算八字命盘."""
    try:
        birth_dt = datetime.combine(request.birth_date, request.birth_time)
        sex = Sex.MALE if request.sex == "male" else Sex.FEMALE
        chart = build_chart(birth_dt, sex, request.longitude)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"排盘失败: {e}")

    return CalculateResponse(
        sex=chart.sex.value,
        birth_datetime=chart.birth_datetime.isoformat(),
        true_solar_datetime=chart.true_solar_datetime.isoformat() if chart.true_solar_datetime else None,
        year_pillar=_pillar_to_response(chart.year_pillar),
        month_pillar=_pillar_to_response(chart.month_pillar),
        day_pillar=_pillar_to_response(chart.day_pillar),
        hour_pillar=_pillar_to_response(chart.hour_pillar),
        day_master=chart.day_master.value,
        day_master_wuxing=chart.day_master.wuxing.value if chart.day_master else "",
        fortune_cycles=[
            FortuneCycleResponse(
                stem=fc.stem.value,
                branch=fc.branch.value,
                start_age=fc.start_age,
                start_year=fc.start_year,
                end_year=fc.end_year,
                nayin=fc.nayin,
            )
            for fc in chart.fortune_cycles
        ],
        qi_yun_age=chart.qi_yun_age,
    )
