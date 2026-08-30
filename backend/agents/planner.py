from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

groq_api=os.getenv('GROQ_API_KEY')
model=Groq(api_key=groq_api)

def plan_node(state):
    """
    Plans the trip
    """
    from_city=state['from_city']
    destination=state['destination']
    budget=state['budget']
    travel_mode=state['travel_mode']
    group_size=state['group_size']
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
        
    prompt=f'''You are an expert travel planner.

    Create a detailed {num_days}-day itinerary for a trip to {destination}.

    Trip details:
    - From: {from_city}
    - Travel mode: {travel_mode}
    - Budget: ₹{budget}
    - Group size: {group_size} people
    - Preferences: {preferences}

    Available data:
    - Weather: {weather_data}
    - Flights found: {flights}
    - Trains found: {trains}
    - Hotels found: {hotels}
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
    
    response = model.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.1
    )
    
    
    