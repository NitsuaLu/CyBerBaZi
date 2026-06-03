"""Pydantic response schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HiddenStemResponse(BaseModel):
    stem: str
    qi_level: str
    shishen: str | None = None


class PillarResponse(BaseModel):
    heavenly_stem: str
    earthly_branch: str
    hidden_stems: list[HiddenStemResponse]
    nayin: str
    stem_shishen: str | None = None


class FortuneCycleResponse(BaseModel):
    stem: str
    branch: str
    start_age: int
    start_year: int
    end_year: int
    nayin: str


class ShiShenCountResponse(BaseModel):
    shishen: str
    stem_count: int
    hidden_count: int
    total: int


class ShenShaResultResponse(BaseModel):
    name: str
    category: str
    location: str
    description: str


class CalculateResponse(BaseModel):
    """Full BaZi chart response."""
    sex: str
    birth_datetime: str
    true_solar_datetime: str | None = None

    year_pillar: PillarResponse
    month_pillar: PillarResponse
    day_pillar: PillarResponse
    hour_pillar: PillarResponse

    day_master: str
    day_master_wuxing: str

    fortune_cycles: list[FortuneCycleResponse]
    qi_yun_age: int


class AnalyzeResponse(BaseModel):
    """Full analysis response."""
    sex: str
    birth_datetime: str
    day_master: str

    shishen: list[ShiShenCountResponse]
    shensha: list[ShenShaResultResponse]
    wang_shuai_level: str
    wang_shuai_score: float
    wang_shuai_details: list[str]
    geju: str
    geju_category: str
    yong_shen: list[str]
    ji_shen: list[str]
    method: str
    suggestions: list[str]


class ReportResponse(BaseModel):
    """Report response."""
    title: str
    sections: list[dict[str, str]]
    plain_text: str
    markdown: str
