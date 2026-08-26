from pydantic import BaseModel,Field
from typing import Optional

class TripInput(BaseModel):
    from_city: str=Field(...,description="Departure city")
    destination: str=Field(...,description="Place to visit")
    start_date: str=Field(...,description="Start date of the trip in YYYY-MM-DD format")
    end_date: str=Field(...,description="End date of the trip in YYYY-MM-DD format")
    budget: int=Field(...,description="Total budget for the trip in INR")
    group_size: int=Field(...,description="Number of people in a group")
    travel_mode: str=Field(...,description="Mode of travel (e.g., flight, train, bus, car)")
    preferences: list[str]=Field(...,description="List of preferences like . eg.['vegetarian','adventure','budget-friendly']")
    phone_number: Optional[str]=Field(None,description="Phone number of the user")
    user_id: Optional[str]=Field(None,description="Email or unique identifier of the user")
    
class WeatherInfo(BaseModel):
    date: str=Field(...,description="Current date")
    condition: str=Field(...,description="Current weather condition")
    temp: float=Field(...,description="Current weather condition")
    feels_like: float=Field(...,description="Actually what is the temperature that feels like")
    min_temp: float=Field(...,description="Minimum temperature")
    max_temp: float=Field(...,description="Maximum temperature")
    
class FlightInfo(BaseModel):
    