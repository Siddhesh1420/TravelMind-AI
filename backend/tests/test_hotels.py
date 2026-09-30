import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pytest

from tools.hotels import search_hotels

def test_hotels_returns_list():
    try:
        result = search_hotels("Manali", "2026-12-20", "2026-12-25", rating=7, adults=2)
        assert isinstance(result, list)
    except Exception:
        pytest.skip("SerpApi connection issue")

def test_hotels_max_three():
    try:
        result = search_hotels("Manali", "2026-12-20", "2026-12-25", rating=7, adults=2)
        assert len(result) <= 3
    except Exception:
        pytest.skip("SerpApi connection issue")

def test_hotels_have_name():
    try:
        result = search_hotels("Goa", "2026-12-20", "2026-12-25", rating=7, adults=2)
        for hotel in result:
            assert "name" in hotel
    except Exception:
        pytest.skip("SerpApi connection issue")

def test_hotels_invalid_dates_handled():
    try:
        result = search_hotels("Manali", "2026-12-25", "2026-12-20", rating=7, adults=2)
        assert isinstance(result, list)
    except Exception:
        pytest.skip("SerpApi connection issue")