def get_itinerary_prompt(num_days, destination, start_date, end_date, 
                          preferences, weather_data, attractions_slim,
                          transit_note, orchestrator_feedback,departure_time,arrival_time):
    return f"""
You are planning a trip to {destination}.

ABSOLUTE REQUIREMENTS — DO NOT DEVIATE:
- Destination: {destination} ONLY. Do not mention any other city as the main destination.
- From city is the departure point only — traveller ARRIVES at {destination}.
- Start date: {start_date} — this is Day 1 date. Non-negotiable.
- End date: {end_date} — this is Day {num_days} date. Non-negotiable.
- Total days: EXACTLY {num_days}. Not more, not less.
- Preferred departure time from source city: {departure_time}
- Must arrive at {destination} considering travel time
- Last day departure should be around {arrival_time}

Trip context:
- Preferences: {preferences}
- Weather at {destination}: {weather_data}
- Things to do at {destination}: {attractions_slim}
- Transit note: {transit_note}

RULES:
1. ALL activities must be IN {destination} — not in any other city
2. Day 1 date MUST be exactly {start_date}
3. Day {num_days} date MUST be exactly {end_date}
4. Dates must be consecutive starting from {start_date}
5. Day 1 morning — traveller arrives at {destination}
6. Last day afternoon/evening — traveller departs {destination}
7. Use different restaurants each evening
8. If weather shows rain — suggest indoor activities
9. estimated_cost must be realistic — never 0
10. If weather_data is empty or has a "message" key — add this note 
    in Day 1 EVENING description only, at the end:
    " (Weather forecast unavailable — check closer to travel date)"
    Do NOT put this in morning or afternoon.
    Do NOT replace any activity with this note.
    Every morning and afternoon must have a real activity.

Return ONLY a JSON array — no other text, no markdown:
[
  {{
    "day_number": 1,
    "date": "{start_date}",
    "morning": "Arrive at {destination}...",
    "afternoon": "activity in {destination}",
    "evening": "dinner at specific restaurant in {destination}",
    "estimated_cost": 1500
  }}
]
"""

def get_budget_prompt(destination, num_days, budget, group_size,
                       hotels_summary, flights_slim, trains_slim,
                       flights_return_slim, trains_return_slim,
                       travel_mode, departure_time, arrival_time):
    return f"""
Given this trip to {destination} for {num_days} days:
- Total budget: ₹{budget}
- Group size: {group_size} people
- Travel mode: {travel_mode}
- Preferred departure time: {departure_time}
- Preferred arrival time: {arrival_time}

Available outbound transport:
- Flights: {flights_slim}
- Trains: {trains_slim}

Available return transport:
- Flights: {flights_return_slim}
- Trains: {trains_return_slim}

Available hotels: {hotels_summary}

RULES:
1. recommended_hotel MUST be from hotels list
2. recommended_flight_or_train MUST include specific train/flight name 
   and number for both outbound and return.
   Format exactly: 
   "Outbound: [Train Name] [Number] (₹[fare]). Return: [Train Name] [Number] (₹[fare])"
   If no specific data available — write "Check IRCTC for available trains"
3. Transport cost = (outbound fare + return fare) × {group_size} people
4. Hotel cost = price per night × {num_days} nights
5. Food cost = daily food estimate × {group_size} people × {num_days} days
6. budget_breakdown total MUST equal total_estimated_cost
7. CRITICAL: total_estimated_cost MUST be less than or equal to ₹{budget}.
   If transport alone exceeds the budget — set replan_needed: true and 
   replan_reason: "Transport cost exceeds total budget. Consider cheaper 
   options like train instead of flight, or reduce group size."
   If total exceeds budget — set replan_needed: true with specific reason.
   Never return a plan where total_estimated_cost > {budget}.
8. Select transport closest to departure time {departure_time}

Return ONLY this JSON:
{{
  "recommended_hotel": "hotel name and reason",
  "recommended_flight_or_train": "outbound: X, return: Y",
  "budget_breakdown": {{
    "transport": 0,
    "hotel": 0,
    "food": 0,
    "activities": 0,
    "total": 0
  }},
  "total_estimated_cost": 0,
  "replan_needed": false,
  "replan_reason": ""
}}
"""