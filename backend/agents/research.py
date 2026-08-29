import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tools.weather import get_weather
from tools.flight import search_flights
from tools.trains import search_trains
from tools.hotels import search_hotels
from tools.search import search
from tools.attractions import search_attractions

load_dotenv()
def research_node(state):
    weather=get_weather(state['destination'])
    if not weather:
        print("Weather forecast unavilable . Only available for next 5 days from today")
    flights=[]
    traons=[]
    if state['travel_mode']=='flight':
        flights=search_flights(state['from_city'],state['destination'])
        trains=[]
    elif state['travel_mode']=='train':
        trains=search_trains(state['from_city'],state['destination'],state['start_date'])
        flights=[]
    hotels=search_hotels(state['destination'],state['start_date'])
    attractions=search_attractions(state['destination'])
    tips=search(f"Travel tips for visiting {state['destination']} things to know")
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
    
        
