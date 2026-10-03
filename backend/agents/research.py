import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # Look for a file in previous directory too

from tools.weather import get_weather
from tools.flight import search_flights
from tools.flight import get_airport_code
from tools.trains import search_trains
from tools.hotels import search_hotels
from tools.search import search
from tools.attractions import search_attractions
import time

load_dotenv()

def call_with_retry(func,*args,max_retries=3,**kwargs):
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Tool call failed (attempt {attempt+1}): {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Tool call failed after {max_retries} attempts: {e}")
                return None  # return None so research_node handles gracefully
            
            
def research_node(state):
    """
    Collects data required for the trip 
    """
    
    print("Calling agent research")
    
    destination = state['destination']
    from_city = state['from_city']
    start_date = state['start_date']
    end_date = state['end_date']
    group_size = state['group_size']
    budget = state['budget']
    travel_mode = state['travel_mode']
    preferences=state.get('preferences',[])
    
    # Determine settings from preferences
    if 'luxury' in preferences:
        travel_class = 3
        hotel_rating = 9
    elif 'budget' in preferences:
        travel_class = 1
        hotel_rating = 7
    else:
        travel_class = 1
        hotel_rating = 8
    
    # Weather
    weather=call_with_retry(get_weather,destination)
    if not weather:
        weather={"message":"Weather forecast unavilable . Only available for next 5 days from today"}
    
    # Travel mode
    
    print(f"From airport: {get_airport_code(from_city)}")
    print(f"To airport: {get_airport_code(destination)}")
    flights=[]
    trains=[]
    if travel_mode =='flight':      
        flights=call_with_retry(search_flights,from_city,destination,start_date,type=2,travel_class=travel_class,stops=0,max_price=budget,sort_by=1,adults=group_size,children=0) or []
        trains=[]
    elif travel_mode=='train':
        trains=call_with_retry(search_trains,from_city,destination,start_date,departure_time=state.get('departure_time',"06:00"),arrival_time=state.get('arrival_time',"23:00")) or []
        if isinstance(trains, str):
            try:
                import json as _json
                trains = _json.loads(trains)
            except:
                trains = []
        flights=[]
    elif travel_mode in ['car','bus','road']:
        trains=[]
        flights=[]
        
    # Return journey
    flights_return = []
    trains_return = []

    if travel_mode == 'flight':
        flights_return = call_with_retry(
            search_flights, destination, from_city, end_date,
            type=2, travel_class=travel_class, stops=0,
            max_price=budget, sort_by=1, adults=group_size, children=0
        ) or []
    elif travel_mode == 'train':
        trains_return = call_with_retry(
            search_trains, destination, from_city, end_date,
            departure_time=state.get('departure_time', '06:00'),
            arrival_time=state.get('arrival_time', '23:00')
        ) or []
        if isinstance(trains_return, str):
            try:
                trains_return = _json.loads(trains_return)
            except:
                trains_return = []
    
    # Used to check if no direct flights or train found
    transit_note = ""
    if not flights and not trains and travel_mode in ['flight', 'train']:
        transit_note = f"No direct {travel_mode} found from {from_city}. Consider travelling to nearest major city first, then take {travel_mode} to {destination}."
        
    # Hotels    
    hotels=call_with_retry(search_hotels,destination,start_date,end_date,rating=hotel_rating,currency="INR",sort_by=3,adults=group_size,children=0,max_price=budget) or []
    
    # Attractions
    attractions=call_with_retry(search_attractions,destination) or {}
    
    # Travel tips
    tips=call_with_retry(search, f"Travel tips for visiting {destination} things to know") or []
    if tips:
        tips[:2]
        
    print(f"Travel mode: {travel_mode}")
    print(f"Trains fetched: {trains}")
    print(f"Flights fetched: {flights}")
    print(f"Hotels fetched: {hotels}")
    return{
        **state,
        "weather_data":weather,
        "flights":flights,
        "trains":trains,
        "flights_return": flights_return,
        "trains_return": trains_return,
        "hotels":hotels,
        "attractions":attractions,
        "travel_tips":tips,
        "transit_note":transit_note,
        "research_complete":True
    }
    
        
