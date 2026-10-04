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
        "total_cost": state.get('total_estimated_cost')
    })
    
    with open(TRIPS_FILE, 'w') as f:
        json.dump(history, f)
    
    print(f"Trip saved for user: {user_id}")