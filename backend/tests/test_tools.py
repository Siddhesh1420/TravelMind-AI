import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tools.weather import get_weather
from tools.attractions import search_attractions
from tools.search import search

# ── Weather Tests ─────────────────────────────────

def test_weather_returns_dict():
    result = get_weather("Mumbai")
    assert result is not None
    assert isinstance(result, dict)

def test_weather_has_correct_keys():
    result = get_weather("Delhi")
    if result and "message" not in result:
        first_day = list(result.values())[0]
        assert "condition" in first_day
        assert "temp" in first_day
        assert "min_temp" in first_day
        assert "max_temp" in first_day

def test_weather_invalid_city():
    result = get_weather("InvalidCityXYZ999")
    assert result is None or isinstance(result, dict)

# ── Attractions Tests ─────────────────────────────

def test_attractions_returns_dict():
    result = search_attractions("Goa")
    assert isinstance(result, dict)

def test_attractions_has_three_keys():
    result = search_attractions("Goa")
    assert "attractions" in result
    assert "restaurants" in result
    assert "activities" in result

def test_attractions_returns_lists():
    result = search_attractions("Goa")
    assert isinstance(result["attractions"], list)
    assert isinstance(result["restaurants"], list)
    assert isinstance(result["activities"], list)

def test_attractions_max_results():
    result = search_attractions("Goa")
    assert len(result["attractions"]) <= 10
    assert len(result["restaurants"]) <= 10
    assert len(result["activities"]) <= 10

# ── Search Tests ──────────────────────────────────

def test_search_returns_list():
    result = search("travel tips for Manali")
    assert isinstance(result, list)
    assert len(result) > 0

def test_search_results_have_content():
    result = search("best places in Goa")
    for r in result:
        assert "content" in r
        assert "title" in r
        assert "url" in r