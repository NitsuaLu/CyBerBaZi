"""Pydantic request schemas."""

from datetime import date, time

from pydantic import BaseModel, Field


class CalculateRequest(BaseModel):
    """Request for BaZi chart calculation."""

    birth_date: date = Field(description="公历出生日期")
    birth_time: time = Field(description="出生时间 (24小时制)")
    sex: str = Field(default="male", pattern="^(male|female)$", description="性别")
    longitude: float = Field(default=120.0, ge=0, le=360, description="出生地经度 (默认120=北京时间)")
