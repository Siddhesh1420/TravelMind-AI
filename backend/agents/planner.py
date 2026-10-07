import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from schemas import PlannerOutput
from model import get_model, invoke_model
from config.settings import (
    MAX_HOTELS, MAX_FLIGHTS, MAX_TRAINS,
    MAX_ATTRACTIONS, MAX_TIPS,
    ATTRACTION_CONTENT_LENGTH, TIP_CONTENT_LENGTH
)
import json
from prompts.planner_prompt import get_itinerary_prompt,get_budget_prompt
from memory.store import get_last_trip
from datetime import datetime,timedelta # for date validation
import time
import re

model=get_model()

def summarize_hotels(hotels):
    return [
        {
            "name": h.get("name"),
            "price_per_night": h.get("rate_per_night", {}).get("lowest"),
            "rating": h.get("overall_rating"),
        }
        for h in hotels
    ]

time.sleep(10)
def plan_node(state):
    """
    Plans the trip
    """
    
    print("Calling agent planner")
    
    from_city=state['from_city']
    destination=state['destination']
    budget=state['budget']
    travel_mode=state['travel_mode']
    group_size=state['group_size']
    preferences=state.get('preferences',[])
    weather_data = state.get('weather_data', {})
    flights = state.get('flights', [])
    trains = state.get('trains', [])
    flights_return = state.get('flights_return', [])
    trains_return = state.get('trains_return', [])
    hotels = state.get('hotels', [])
    attractions = state.get('attractions', {})
    travel_tips = state.get('travel_tips', [])
    orchestrator_feedback = state.get('orchestrator_feedback', '')
    start_date=state['start_date']
    end_date=state['end_date']
    user_id = state.get('user_id', 'default')
    last_trip = get_last_trip(user_id)
    
    if isinstance(trains, str):
        try:
            import json as _json
            trains = _json.loads(trains)
        except:
            trains = []
    
    start=datetime.strptime(start_date,"%Y-%m-%d")
    end=datetime.strptime(end_date,"%Y-%m-%d")
    num_days=(end-start).days+1
    
    if num_days<=0:
        return{
            **state,
            "replan_needed":True,
            "replan_reason": "End date must be after start date"
        }
        
    hotels_summary = summarize_hotels(hotels[:MAX_HOTELS])
    
    # Trim flights
    flights_slim = [
    {
        "fare_inr": f.get("price", 0),  # rename to fare_inr
        "duration_mins": f.get("total_duration", 0),
        "airline": f.get("flights", [{}])[0].get("airline", ""),
        "flight_number": f.get("flights", [{}])[0].get("flight_number", ""),
        "departure_time": f.get("flights", [{}])[0].get("departure_airport", {}).get("time", "")
    }
    for f in flights[:MAX_FLIGHTS]
]

    # Trim trains
    trains_slim = trains[:MAX_TRAINS]
    
    print(f"Trains slim passed to budget: {trains_slim}")
    
    flights_return_slim = [
    {
        "fare_inr": f.get("price", 0),  # rename to fare_inr
        "duration_mins": f.get("total_duration", 0),
        "airline": f.get("flights", [{}])[0].get("airline", ""),
        "flight_number": f.get("flights", [{}])[0].get("flight_number", ""),
        "departure_time": f.get("flights", [{}])[0].get("departure_airport", {}).get("time", "")
    }
    for f in flights_return[:MAX_FLIGHTS]
]

    trains_return_slim = trains_return[:MAX_TRAINS]
        
    transit_note=state.get('transit_note','')
    if not flights and not trains and travel_mode in ['flight', 'train']:
        transit_note = f"No direct {travel_mode} found from {from_city} to {destination}. Consider nearby transit hubs."
    
        # Trim attractions to first 3 per category
    if attractions:
        attractions_slim = {
            "attractions": [a[:ATTRACTION_CONTENT_LENGTH] for a in attractions.get("attractions", [])[:MAX_ATTRACTIONS]],
            "restaurants": [r[:ATTRACTION_CONTENT_LENGTH] for r in attractions.get("restaurants", [])[:MAX_ATTRACTIONS]],
            "activities": [a[:ATTRACTION_CONTENT_LENGTH] for a in attractions.get("activities", [])[:MAX_ATTRACTIONS]]
        }
    else:
        attractions_slim = {}

    tips_slim = [t.get("content", "")[:TIP_CONTENT_LENGTH] for t in travel_tips[:MAX_TIPS]]
    
    itinerary_prompt = get_itinerary_prompt(
        num_days=num_days,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        preferences=preferences,
        weather_data=weather_data,
        attractions_slim=attractions_slim,
        transit_note=transit_note,
        orchestrator_feedback=orchestrator_feedback,
        travel_mode=travel_mode,
        departure_time=state.get('departure_time', '06:00'),
        arrival_time=state.get('arrival_time', '23:00')
    )

    print(f"Itinerary prompt tokens: {len(itinerary_prompt) // 4}")
    itinerary_output = invoke_model(model, itinerary_prompt)
    print(f"Itinerary output length: {len(itinerary_output) if itinerary_output else 0}")
    print(f"Itinerary preview: {itinerary_output[:200] if itinerary_output else 'EMPTY'}")

    if not itinerary_output or itinerary_output.strip() == "":
        return {
            **state,
            "replan_needed": True,
            "replan_reason": "LLM returned empty itinerary",
            "plan_complete": False
        }
    
    print(f"flights_slim before budget: {flights_slim}")
    print(f"flights_return_slim before budget: {flights_return_slim}")
    
    # Call 2 — Generate budget and recommendations
    budget_prompt = get_budget_prompt(
    destination=destination,
    num_days=num_days,
    budget=budget,
    group_size=group_size,
    hotels_summary=hotels_summary,
    flights_slim=flights_slim,
    trains_slim=trains_slim,
    flights_return_slim=flights_return_slim,
    trains_return_slim=trains_return_slim,
    travel_mode=travel_mode,
    departure_time=state.get('departure_time', '06:00'),
    arrival_time=state.get('arrival_time', '23:00'),
    last_trip=last_trip
)

    print(f"Budget prompt tokens: {len(budget_prompt) // 4}")
    budget_output = invoke_model(model, budget_prompt)
    print(f"Budget output length: {len(budget_output) if budget_output else 0}")
    print(f"Budget preview: {budget_output[:200] if budget_output else 'EMPTY'}")

    if not budget_output or budget_output.strip() == "":
        return {
            **state,
            "replan_needed": True,
            "replan_reason": "LLM returned empty budget",
            "plan_complete": False
        }

    try:
        # Clean and parse itinerary
        itinerary_raw = itinerary_output.strip()
        if itinerary_raw.startswith("```json"):
            itinerary_raw = itinerary_raw[7:].strip()
        if itinerary_raw.startswith("```"):
            itinerary_raw = itinerary_raw[3:].strip()
        if itinerary_raw.endswith("```"):
            itinerary_raw = itinerary_raw[:-3].strip()

        json_match = re.search(r'\[.*\]', itinerary_raw, re.DOTALL)
        if json_match:
            itinerary_raw = json_match.group(0)

        itinerary_data = json.loads(itinerary_raw)

        # Fix dates regardless of what LLM returned
        start = datetime.strptime(start_date, "%Y-%m-%d")
        for i, day in enumerate(itinerary_data):
            expected_date = (start + timedelta(days=i)).strftime("%Y-%m-%d")
            day['date'] = expected_date
            day['day_number'] = i + 1

        # Clean and parse budget
        budget_raw = budget_output.strip()
        if budget_raw.startswith("```json"):
            budget_raw = budget_raw[7:].strip()
        if budget_raw.startswith("```"):
            budget_raw = budget_raw[3:].strip()
        if budget_raw.endswith("```"):
            budget_raw = budget_raw[:-3].strip()

        json_match = re.search(r'\{.*\}', budget_raw, re.DOTALL)
        if json_match:
            budget_raw = json_match.group(0)

        budget_raw = budget_raw.replace('₹', 'Rs')
        budget_data = json.loads(budget_raw)

        # Check budget exceeded
        if budget_data.get('total_estimated_cost', 0) > budget:
            budget_data['replan_needed'] = True
            budget_data['replan_reason'] = "Total estimated cost exceeds budget"

        # Validate itinerary length
        if len(itinerary_data) != num_days:
            return {
                **state,
                "replan_needed": True,
                "replan_reason": f"Expected {num_days} days but got {len(itinerary_data)}",
                "plan_complete": False
            }

        return {
            **state,
            "itinerary": itinerary_data,
            "budget_breakdown": budget_data.get('budget_breakdown', {}),
            "recommended_hotel": budget_data.get('recommended_hotel', ''),
            "recommended_flight_or_train": budget_data.get('recommended_flight_or_train', ''),
            "total_estimated_cost": budget_data.get('total_estimated_cost', 0),
            "replan_needed": budget_data.get('replan_needed', False),
            "replan_reason": budget_data.get('replan_reason', ''),
            "plan_complete": True
        }

    except Exception as e:
        print(f"Parse error: {e}")
        print(f"Itinerary raw: {itinerary_output[:200] if itinerary_output else 'EMPTY'}")
        print(f"Budget raw: {budget_output[:200] if budget_output else 'EMPTY'}")
        return {
            **state,
            "replan_needed": True,
            "replan_reason": f"Failed to parse outputs: {str(e)}",
            "plan_complete": False
        }