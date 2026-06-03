"""Tests for solar terms query module."""

from datetime import datetime

from bazi.calendar.solar_terms import (
    get_solar_terms_for_year,
    get_next_solar_term,
    get_prev_solar_term,
    get_solar_term_by_name,
    SOLAR_TERM_NAMES,
    MONTH_BRANCH_SOLAR_TERM,
)


class TestSolarTerms:
    def test_all_24_terms_per_year(self):
        terms = get_solar_terms_for_year(2000)
        assert len(terms) == 24
        names = {t.name for t in terms}
        assert len(names) == 24

    def test_terms_sorted_by_time(self):
        terms = get_solar_terms_for_year(2000)
        for i in range(len(terms) - 1):
            assert terms[i].datetime < terms[i + 1].datetime

    def test_lichun_2000(self):
        term = get_solar_term_by_name(2000, "立春")
        assert term is not None
        assert term.datetime.year == 2000
        assert term.datetime.month == 2
        assert term.datetime.day == 4

    def test_dongzhi_2024(self):
        term = get_solar_term_by_name(2024, "冬至")
        assert term is not None
        assert term.datetime.month == 12
        assert 21 <= term.datetime.day <= 22  # 冬至 is Dec 21 or 22

    def test_xiazhi_2024(self):
        term = get_solar_term_by_name(2024, "夏至")
        assert term is not None
        assert term.datetime.month == 6
        assert 20 <= term.datetime.day <= 22

    def test_lichun_is_first_in_cycle(self):
        """立春 should be solar term index 0 (start of the term cycle)."""
        order = {n: i for i, n in enumerate(SOLAR_TERM_NAMES)}
        assert order["立春"] == 0
        assert order["惊蛰"] == 2
        assert order["冬至"] == 21

    def test_month_branch_mapping(self):
        """Test that each month-branch term is correctly mapped."""
        assert MONTH_BRANCH_SOLAR_TERM["立春"] == "寅"
        assert MONTH_BRANCH_SOLAR_TERM["惊蛰"] == "卯"
        assert MONTH_BRANCH_SOLAR_TERM["清明"] == "辰"
        assert MONTH_BRANCH_SOLAR_TERM["立夏"] == "巳"
        assert MONTH_BRANCH_SOLAR_TERM["芒种"] == "午"
        assert MONTH_BRANCH_SOLAR_TERM["小暑"] == "未"
        assert MONTH_BRANCH_SOLAR_TERM["立秋"] == "申"
        assert MONTH_BRANCH_SOLAR_TERM["白露"] == "酉"
        assert MONTH_BRANCH_SOLAR_TERM["寒露"] == "戌"
        assert MONTH_BRANCH_SOLAR_TERM["立冬"] == "亥"
        assert MONTH_BRANCH_SOLAR_TERM["大雪"] == "子"
        assert MONTH_BRANCH_SOLAR_TERM["小寒"] == "丑"


class TestSolarTermNavigation:
    def test_next_solar_term(self):
        dt = datetime(2024, 1, 1, 0, 0, 0)
        next_term = get_next_solar_term(dt)
        assert next_term.name == "小寒"  # 小寒 is around Jan 5-6

    def test_prev_solar_term(self):
        dt = datetime(2024, 1, 15, 0, 0, 0)
        prev = get_prev_solar_term(dt)
        assert prev.name == "小寒"  # Just after 小寒

    def test_prev_at_exact_boundary(self):
        """When datetime equals the solar term, get_prev should return that term."""
        lichun = get_solar_term_by_name(2024, "立春")
        dt = lichun.datetime
        prev = get_prev_solar_term(dt)
        assert prev.name == "立春"
        assert prev.datetime == dt
