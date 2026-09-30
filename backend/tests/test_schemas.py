import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pytest
from pydantic import ValidationError
from schemas import TripInput, DayPlan, BudgetBreakdown, PlannerOutput

def test_trip_input_valid():
    trip = TripInput(
        from_city="Delhi",
        destination="Manali",
        start_date="2026-12-20",
        end_date="2026-12-25",
        budget=30000,
        group_size=2,
        travel_mode="train",
        preferences=["budget", "adventure"]
    )
    assert trip.destination == "Manali"
    assert trip.budget == 30000

def test_trip_input_missing_required_field():
    with pytest.raises(ValidationError):
        TripInput(
            destination="Manali",
            # missing from_city, dates, budget etc
        )

def test_budget_breakdown_valid():
    bd = BudgetBreakdown(
        transport=3000,
        hotel=10000,
        food=5000,
        activities=2000,
        total=20000
    )
    assert bd.total == 20000

def test_day_plan_valid():
    day = DayPlan(
        day_number=1,
        date="2026-12-20",
        morning="Visit temple",
        afternoon="Explore market",
        evening="Dinner",
        estimated_cost=2000
    )
    assert day.day_number == 1
    assert day.estimated_cost == 2000