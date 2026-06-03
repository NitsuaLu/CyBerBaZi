"""Integration tests for the BaZi REST API."""

import pytest
from fastapi.testclient import TestClient

from bazi_api.main import app

client = TestClient(app)

PAYLOAD = {
    "birth_date": "2000-06-15",
    "birth_time": "12:00:00",
    "sex": "male",
    "longitude": 120.0,
}


class TestHealth:
    def test_health_ok(self):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestCalculate:
    def test_calculate_200(self):
        response = client.post("/api/v1/bazi/calculate", json=PAYLOAD)
        assert response.status_code == 200
        data = response.json()
        assert data["day_master"]
        assert data["year_pillar"]["heavenly_stem"]
        assert data["month_pillar"]["heavenly_stem"]
        assert data["day_pillar"]["heavenly_stem"]
        assert data["hour_pillar"]["heavenly_stem"]
        assert len(data["fortune_cycles"]) >= 8

    def test_calculate_hidden_stems(self):
        response = client.post("/api/v1/bazi/calculate", json=PAYLOAD)
        data = response.json()
        for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar"):
            assert len(data[key]["hidden_stems"]) >= 1

    def test_calculate_nayin(self):
        response = client.post("/api/v1/bazi/calculate", json=PAYLOAD)
        data = response.json()
        for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar"):
            assert data[key]["nayin"]

    def test_calculate_female(self):
        payload = {**PAYLOAD, "sex": "female"}
        response = client.post("/api/v1/bazi/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["sex"] == "女"

    def test_calculate_bad_sex(self):
        payload = {**PAYLOAD, "sex": "other"}
        response = client.post("/api/v1/bazi/calculate", json=payload)
        assert response.status_code == 422  # validation error


class TestAnalyze:
    def test_analyze_200(self):
        response = client.post("/api/v1/bazi/analyze", json=PAYLOAD)
        assert response.status_code == 200
        data = response.json()
        assert len(data["shishen"]) > 0
        assert data["wang_shuai_level"]
        assert data["method"]

    def test_analyze_shensha(self):
        response = client.post("/api/v1/bazi/analyze", json=PAYLOAD)
        data = response.json()
        assert len(data["shensha"]) >= 0

    def test_analyze_suggestions(self):
        response = client.post("/api/v1/bazi/analyze", json=PAYLOAD)
        data = response.json()
        assert len(data["suggestions"]) > 0


class TestReport:
    def test_report_200(self):
        response = client.post("/api/v1/bazi/report", json=PAYLOAD)
        assert response.status_code == 200
        data = response.json()
        assert len(data["sections"]) >= 7
        assert len(data["markdown"]) > 0
        assert len(data["plain_text"]) > 0

    def test_report_markdown_has_title(self):
        response = client.post("/api/v1/bazi/report", json=PAYLOAD)
        data = response.json()
        assert data["markdown"].startswith("# ")

    def test_report_female(self):
        payload = {**PAYLOAD, "sex": "female"}
        response = client.post("/api/v1/bazi/report", json=payload)
        assert response.status_code == 200
