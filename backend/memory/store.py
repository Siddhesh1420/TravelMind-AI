import json
import os

TRIPS_FILE = "trip_history.json"

def load_trip_history():
    try:
        with open(TRIPS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_trip(user_id: str, state: dict):
    history = load_trip_history()
    if user_id not in history:
        history[user_id] = []
    
    history[user_id].append({
        "destination": state.get('destination'),
        "from_city": state.get('from_city'),
        "start_date": state.get('start_date'),
        "end_date": state.get('end_date'),
        "budget": state.get('budget'),
        "travel_mode": state.get('travel_mode'),
        "total_cost": state.get('total_estimated_cost'),
        "itinerary": state.get('itinerary', []),
        "recommended_hotel": state.get('recommended_hotel', ''),
        "recommended_flight_or_train": state.get('recommended_flight_or_train', ''),
        "budget_breakdown": state.get('budget_breakdown', {}),
        "total_estimated_cost": state.get('total_estimated_cost', 0),
        "formatted_report": state.get('formatted_report', ''),
        "whatsapp_message": state.get('whatsapp_message', ''),
        "calendar_events": state.get('calendar_events', []),
        "booking_links": state.get('booking_links', {}),
        "weather_data": state.get('weather_data', {}),
        "transit_note": state.get('transit_note', ''),
    })
    
    with open(TRIPS_FILE, 'w') as f:
        json.dump(history, f)
    
def get_last_trip(user_id: str) -> dict:
    history = load_trip_history()
    user_trips = history.get(user_id, [])
    return user_trips[-1] if len(user_trips) > 1 else None