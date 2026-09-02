from datetime import datetime
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # looks for a file evn in previous directory
from schemas import PlannerOutput
from model import get_model,invoke_model
import json

load_dotenv()

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

# def summarize_attractions(attractions):
#     if isinstance(attractions, dict):
#         summarized = {}
#         for k, v in attractions.items():
#             if isinstance(v, list):
#                 summarized[k] = [
#                     {
#                         "name": item.get("name") or item.get("title"),
#                         "rating": item.get("rating"),
#                         "description": (item.get("description") or "")[:150]
#                     }
#                     for item in v[:5]
#                 ]
#             else:
#                 summarized[k] = v
#         return summarized
#     elif isinstance(attractions, list):
#         return [
#             {
#                 "name": a.get("name") or a.get("title"),
#                 "rating": a.get("rating"),
#                 "description": (a.get("description") or "")[:150]
#             }
#             for a in attractions[:5]
#         ]
#     return attractions

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
    num_days=(end-start).days
    
    if num_days<=0:
        return{
            **state,
            "replan_needed":True,
            "replan_reason": "End date must be after start date"
        }
        
    hotels_summary = summarize_hotels(hotels)
    # attractions_summary = summarize_attractions(attractions)
    prompt=f'''You are an expert travel planner.

    Create a detailed {num_days}-day itinerary for a trip to {destination}.

    Trip details:
    - From: {from_city}
    - Travel mode: {travel_mode}
    - Budget: ₹{budget}
    - Group size: {group_size}
    - Preferences: {preferences}

    Available data:
    - Weather: {weather_data}
    - Flights found: {flights}
    - Trains found: {trains}
    - Hotels found: {hotels_summary}
    - Attractions: {attractions}
    - Travel tips: {travel_tips}
    - Orchestrator feedback: {orchestrator_feedback}

    Rules:
    1. Day 1 morning should account for travel time from {from_city}
    2. If weather shows rain on a day — plan indoor activities for that day
    3. Recommend the best hotel from the hotels list based on budget and rating
    4. Recommend the best flight/train option
    5. Include local food recommendations from restaurants data
    6. Keep total cost within ₹{budget}
    7. Apply preferences: {preferences}

    Return ONLY a valid JSON with this structure:
    {{
    "itinerary": [
        {{
        "day_number": 1,
        "date": "YYYY-MM-DD",
        "morning": "activity description",
        "afternoon": "activity description", 
        "evening": "activity description",
        "estimated_cost": 2000
        }}
    ],
    "recommended_hotel": "hotel name and why",
    "recommended_flight_or_train": "option name and why",
    "budget_breakdown": {{
        "transport": 5000,
        "hotel": 10000,
        "food": 3000,
        "activities": 2000,
        "total": 20000
    }},
    "total_estimated_cost": 20000,
    "replan_needed": false,
    "replan_reason": ""
    }}" '''
       
    raw=invoke_model(model,prompt)
    
    # In case of malformed JSON
    try:
        data=json.loads(raw) # loads read from string while load reads from object
          
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
                    "plan_complete": True
                }
        
    except (json.JSONDecodeError, Exception) as e:
        return{
            **state,
            "replan_needed": True,
            "replan_reason":f"Failed to parse planner output {str(e)}",
            "plan_complete": False
        }