import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # Look for a file in previous directory too

from tools.weather import get_weather
from tools.flight import search_flights
from tools.trains import search_trains
from tools.hotels import search_hotels
from tools.search import search
from tools.attractions import search_attractions

load_dotenv()
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
    weather=get_weather(destination)
    if not weather:
        weather={"message":"Weather forecast unavilable . Only available for next 5 days from today"}
    
    # Travel mode
        
    flights=[]
    trains=[]
    if travel_mode =='flight':      
        flights=search_flights(from_city,destination,start_date,type=2,travel_class=travel_class,stops=0,max_price=budget,sort_by=1,adults=group_size,children=0)
        trains=[]
    elif travel_mode=='train':
        trains=search_trains(from_city,destination,start_date,departure_time=state.get('departure_time',"06:00"),arrival_time=state.get('arrival_time',"23:00"))
        flights=[]
    elif travel_mode in ['car','bus','road']:
        trains=[]
        flights=[]
        
    # Hotels    
    hotels=search_hotels(destination,start_date,end_date,rating=hotel_rating,currency="INR",sort_by=3,adults=group_size,children=0,max_price=budget)
    
    # Attractions
    attractions=search_attractions(destination)
    
    # Travel tips
    tips=search(f"Travel tips for visiting {destination} things to know")
    return{
        **state,
        "weather_data":weather,
        "flights":flights,
        "trains":trains,
        "hotels":hotels,
        "attractions":attractions,
        "travel_tips":tips,
        "research_complete":True
    }
    
        
