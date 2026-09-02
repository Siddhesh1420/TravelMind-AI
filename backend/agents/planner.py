from datetime import datetime
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # looks for a file evn in previous directory
from schemas import PlannerOutput
from model import get_model,invoke_model
import json
from datetime import timedelta # for date validation

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
    
    transit_state=state.get('transit_state','')
    if not flights and not trains and travel_mode in ['flight', 'train']:
        transit_note = f"No direct {travel_mode} found from {from_city} to {destination}. Consider nearby transit hubs."

    prompt = f'''
    You are an expert travel planner.

    Create a detailed {num_days}-day itinerary for a trip to {destination}.

    TRIP DETAILS:
    - From: {from_city}
    - Start date: {start_date}
    - End date: {end_date}
    - Travel mode: {travel_mode}
    - Budget: ₹{budget}
    - Group size: {group_size}
    - Preferences: {preferences}

    AVAILABLE RESEARCH DATA:
    - Weather: {weather_data}
    - Flights: {flights}
    - Trains: {trains}
    - Hotels: {hotels_summary}
    - Attractions: {attractions}
    - Travel tips: {travel_tips}
    - transit state: {transit_state}

    ORCHESTRATOR FEEDBACK:
    {orchestrator_feedback}


    PLANNING RULES:

    1. Create EXACTLY {num_days} itinerary entries.

    2. The itinerary must contain one entry for EVERY day from
    {start_date} through {end_date}.

    3. Each itinerary entry MUST contain:
    - day_number
    - date
    - morning
    - afternoon
    - evening
    - estimated_cost

    4. The first itinerary date MUST be {start_date}.
    The last itinerary date MUST be {end_date}.

    5. Day numbers MUST be consecutive:
    1, 2, 3, ... {num_days}

    6. DO NOT skip any day.

    7. Account for travel time from {from_city} on the first day.

    8. IMPORTANT TRANSPORT RULE:
    Only recommend a flight or train that actually appears in the
    provided Flights or Trains research data.

    9. Do NOT assume that a train to a nearby city means the train
    directly reaches {destination}.

    10. If the provided transport data only reaches another city,
        describe the onward journey separately and do NOT claim that
        the train directly reaches {destination}.

    11. Recommend a hotel ONLY from the provided Hotels research data.

    12. Recommend restaurants or food ONLY from the provided research data.

    13. Do NOT invent:
        - hotel names
        - train names
        - flight names
        - restaurant names
        - prices
        - ratings
        - travel times
        - booking information
        - attractions that are not supported by the research data

    14. Use the provided attractions and research data when creating
        the itinerary.

    15. Apply the user's preferences:
        {preferences}

    16. If weather data is available for a particular itinerary day,
        take it into account when planning activities.

    17. Keep the total estimated cost within the budget of ₹{budget}.

    18. The budget_breakdown total MUST equal total_estimated_cost.

    19. If the planner cannot produce a complete and reliable itinerary
        using the provided research data, set:
        "replan_needed": true

    20. If the itinerary contains fewer than {num_days} days,
        "plan_complete" MUST be false.

    21. If any required recommendation is invented or cannot be supported
        by the research data, "plan_complete" MUST be false.

    22. "plan_complete" can be true ONLY when:
        - exactly {num_days} days are present
        - dates are complete and consecutive
        - day numbers are complete and consecutive
        - the recommendations are supported by the research data
        - the budget is valid
        - the itinerary is internally consistent

    23. Never set "plan_complete": true for a partial itinerary.
    
    24.If transit_note is not empty — Day 1 morning MUST explicitly
    mention the transit journey and connection point


    JSON OUTPUT REQUIREMENTS:

    Return EXACTLY ONE JSON OBJECT.

    Your response MUST:
    - Start with {{
    - End with }}
    - Contain NO text before the JSON
    - Contain NO text after the JSON
    - Contain NO Markdown
    - Contain NO ```json code fences
    - Contain NO explanations
    - Contain NO comments
    - Use double quotes for all JSON keys and string values
    - Use valid JSON syntax
    - Use no trailing commas
    - Be directly parseable using Python's json.loads()


    RETURN EXACTLY THIS STRUCTURE:

    {{
        "itinerary": [
            {{
                "day_number": 1,
                "date": "YYYY-MM-DD",
                "morning": "activity description",
                "afternoon": "activity description",
                "evening": "activity description",
                "estimated_cost": 0
            }}
        ],
        "recommended_hotel": "hotel name and reason",
        "recommended_flight_or_train": "option name and reason",
        "budget_breakdown": {{
            "transport": 0,
            "hotel": 0,
            "food": 0,
            "activities": 0,
            "total": 0
        }},
        "total_estimated_cost": 0,
        "replan_needed": false,
        "replan_reason": "",
        "plan_complete": true
    }}


    FINAL VALIDATION BEFORE RESPONDING:

    Before returning the JSON, verify internally:

    - Is the itinerary length exactly {num_days}?
    - Does it start on {start_date}?
    - Does it end on {end_date}?
    - Are all day numbers present from 1 to {num_days}?
    - Are all dates consecutive?
    - Is the recommended hotel present in the provided hotel data?
    - Is the recommended train/flight present in the provided transport data?
    - Were any facts, names, prices, or recommendations invented?
    - Is total_estimated_cost within ₹{budget}?
    - Does budget_breakdown.total equal total_estimated_cost?
    - If ANY answer is NO, set "plan_complete": false and
    "replan_needed": true.

    Return ONLY the JSON object.
    Nothing else.
    '''
       
    output=invoke_model(model,prompt)
    
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