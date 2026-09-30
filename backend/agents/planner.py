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
from prompts.planner_prompt import get_planner_prompt
from datetime import datetime,timedelta # for date validation

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
    hotels = state.get('hotels', [])
    attractions = state.get('attractions', {})
    travel_tips = state.get('travel_tips', [])
    orchestrator_feedback = state.get('orchestrator_feedback', '')
    start_date=state['start_date']
    end_date=state['end_date']
    
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
            "price": f.get("price", ""),
            "duration": f.get("total_duration", ""),
            "airline": f.get("flights", [{}])[0].get("airline", "")
        }
        for f in flights[:MAX_FLIGHTS]
    ]

    # Trim trains
    trains_slim = trains[:MAX_TRAINS]
        
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
    
    prompt = get_planner_prompt(
    num_days=num_days,
    destination=destination,
    from_city=from_city,
    start_date=start_date,
    end_date=end_date,
    travel_mode=travel_mode,
    budget=budget,
    group_size=group_size,
    preferences=preferences,
    weather_data=weather_data,
    flights_slim=flights_slim,
    trains_slim=trains_slim,
    hotels_summary=hotels_summary,
    attractions_slim=attractions_slim,
    tips_slim=tips_slim,
    transit_note=transit_note,
    orchestrator_feedback=orchestrator_feedback
)
       
    output=invoke_model(model,prompt)
    
    if not output or output.strip() == "":
        print("Empty output — rate limited")
        return {
            **state,
            "replan_needed": True,
            "replan_reason": "LLM returned empty response — rate limit hit",
            "plan_complete": False
        }
    
    # In case of malformed JSON
    try:
        output=output.strip()
        if output.startswith("```json"):
            output = output[len("```json"):].strip()

        if output.endswith("```"):
            output = output[:-3].strip()
        data=json.loads(output) # loads read from string while load reads from object
        
        # Adding date validation to ensure the itinerary dates are within the start and end date range
        start = datetime.strptime(start_date, "%Y-%m-%d")
        for i, day in enumerate(data['itinerary']):
            expected_date = (start + timedelta(days=i)).strftime("%Y-%m-%d")
            if day.get('date') != expected_date:
                print(f"Date mismatch day {i+1}: got {day.get('date')}, fixing to {expected_date}")
                day['date'] = expected_date
            if day.get('day_number') != i+1:
                day['day_number'] = i+1  
                
        if data.get("total_estimated_cost",0)> budget :
            data['replan_needed']=True
            data['replan_reason']="Total estiamted cost exceeds the budget"
        
            
        # Validating data
        plan=PlannerOutput(**data)
        
        return{
                    **state,
                    "itinerary":[day.dict() for day in plan.itinerary],
                    "budget_breakdown": plan.budget_breakdown.dict(),
                    "recommended_hotel": plan.recommended_hotel,
                    "recommended_flight_or_train": plan.recommended_flight_or_train,
                    "total_estimated_cost":plan.total_estimated_cost,
                    "replan_needed": plan.replan_needed,
                    "replan_reason":plan.replan_reason,
                    "plan_complete": plan.plan_complete
                }
        
    except (json.JSONDecodeError, Exception) as e:
        print("Planner JSON error:", e)
        print("Raw output:", output)
        
        return{
            **state,
            "replan_needed": True,
            "replan_reason":f"Failed to parse planner output {str(e)}",
            "plan_complete": False
        }