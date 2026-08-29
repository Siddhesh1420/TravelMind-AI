from pydantic import BaseModel,Field
from typing import Optional,List

class TripInput(BaseModel):
    from_city: str=Field(...,description="Departure city")
    destination: str=Field(...,description="Place to visit")
    start_date: str=Field(...,description="Start date of the trip in YYYY-MM-DD format")
    end_date: str=Field(...,description="End date of the trip in YYYY-MM-DD format")
    budget: int=Field(...,description="Total budget for the trip in INR")
    group_size: int=Field(...,description="Number of people in a group")
    travel_mode: str=Field(...,description="Mode of travel (e.g., flight, train, bus, car)")
    preferences: Optional[List[str]]=Field([],description="List of preferences like . eg.['vegetarian','adventure','budget-friendly']")
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
    airline: str=Field(...,description="Airline Name")
    flight_number: str=Field(...,description="Flight number")
    departure_time: str=Field(...,description="Departure time in HH::MM format")
    arrival_time: str=Field(...,description="Arrival time in HH::MM format")
    duration: str=Field(...,description="Duration in HH::MM format")
    price: str=Field(...,description="Price")
    travel_class: str=Field(...,description="Travel class")
    
class TrainInfo(BaseModel):
    train_name: str=Field(...,description="Train Name")
    train_number: str=Field(...,description="Train numer number")
    departure_time: str=Field(...,description="Departure time in HH:MM format")
    arrival_time: str=Field(...,description="Arrival time in HH::MM format")
    duration: str=Field(...,description="Duration in HH::MM format")
    classes: List[str]=Field(...,description="List of classes")
    days: str=Field(...,description="Days on which train run . eg: Daily or 'MTWTFSS' ")
    
class HotelInfo(BaseModel):
    name: str=Field(...,description="Name of hotel")
    rating: float=Field(...,description="Give rating out of 5")
    price_per_night: str=Field(...,description="Price_per_night")
    total_price: str=Field(...,description="Total price")
    amenities: List[str]=Field(...,description="List of amenities")
    check_in_time: str=Field(...,description="Check in time")
    check_out_time: str=Field(...,description="Check out time")
    
class DayPlan(BaseModel):
    day_number: int=Field(...,description="Day number")
    date: str=Field(...,description="Date in YYYY-MM-DD format")
    morning: str=Field(...,description="Morning Plan")
    afternoon: str=Field(...,description="Afternoon Plan")
    evening: str=Field(...,description="Evening plan")
    weather: WeatherInfo=Field(...,description="Weather info")
    estimated_cost: str=Field(...,description="Estimated cost")
