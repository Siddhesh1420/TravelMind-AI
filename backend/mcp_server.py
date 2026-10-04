from fastmcp import FastMCP
import os
import sys
import ssl
import certifi
sys.path.append(os.path.dirname(__file__))

from tools.weather import get_weather as _get_weather
from tools.flight import search_flights as _search_flights
from tools.hotels import search_hotels as _search_hotels
from tools.trains import search_trains as _search_trains
from tools.attractions import search_attractions as _search_attractions

ssl._create_default_https_context = ssl._create_unverified_context
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''

mcp = FastMCP(name="TravelMind AI")
@mcp.tool()
async def get_weather(city: str):
    """Get weather forecast for a city in India"""
    return _get_weather(city)

@mcp.tool()
async def search_flights(from_city: str, to_city: str, date: str, adults: int = 1):
    """Search available flights between two Indian cities"""
    return _search_flights(from_city, to_city, date, adults=adults)

@mcp.tool()
async def search_hotels(destination: str, checkin: str, checkout: str, adults: int = 2,rating: int=7):
    """Search hotels at a destination"""
    return _search_hotels(destination, checkin, checkout, adults=adults,rating=rating)

@mcp.tool()
async def search_trains(from_city: str, to_city: str, date: str,departure_time: str = "06:00", arrival_time: str = "22:00"):
    """Search trains between two Indian cities"""
    return _search_trains(from_city, to_city, date,departure_time=departure_time, arrival_time=arrival_time)

@mcp.tool()
async def search_attractions(destination: str):
    """Search tourist attractions, restaurants and activities at a destination"""
    return _search_attractions(destination)

@mcp.tool()
async def plan_trip(
    destination: str,
    from_city: str,
    start_date: str,
    end_date: str,
    budget: int,
    group_size: int = 2,
    travel_mode: str = "train",
    preferences: str = "budget"
):
    """
    Plan a complete trip with full day-by-day itinerary, hotel recommendation,
    transport options and budget breakdown.
    
    Args:
        destination: City to travel to (e.g. 'Goa', 'Manali', 'Jaipur')
        from_city: Departure city (e.g. 'Delhi', 'Mumbai')
        start_date: Trip start date in YYYY-MM-DD format
        end_date: Trip end date in YYYY-MM-DD format
        budget: Total budget in INR (e.g. 15000)
        group_size: Number of travellers (default 2)
        travel_mode: 'train', 'flight', 'car', or 'bus'
        preferences: Comma-separated preferences e.g. 'budget,adventure'
    """
    import requests
    
    response = requests.post(
        "http://localhost:8000/plan",
        json={
            "destination": destination,
            "from_city": from_city,
            "start_date": start_date,
            "end_date": end_date,
            "budget": budget,
            "group_size": group_size,
            "travel_mode": travel_mode,
            "preferences": preferences.split(','),
            "departure_time": "06:00",
            "arrival_time": "22:00",
            "phone_number": "",
            "user_id": "mcp_user"
        },
        headers={"Authorization": "Bearer mcp-internal-token"},
        timeout=600
    )
    
    if response.ok:
        data = response.json()
        return {
            "itinerary": data.get("itinerary", []),
            "recommended_hotel": data.get("recommended_hotel", ""),
            "recommended_transport": data.get("recommended_flight_or_train", ""),
            "budget_breakdown": data.get("budget_breakdown", {}),
            "total_cost": data.get("total_estimated_cost", 0),
            "whatsapp_message": data.get("whatsapp_message", ""),
            "formatted_report": data.get("formatted_report", "")
        }
    else:
        return {"error": f"Planning failed: {response.text}"}

if __name__ == "__main__":
    mcp.run()





