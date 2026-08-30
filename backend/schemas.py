from pydantic import BaseModel,Field
from typing import Optional,List

class TripInput(BaseModel):
    from_city: str=Field(...,description="Departure city")
    destination: str=Field(...,description="Place to visit")
    start_date: str=Field(...,description="Start date of the trip in YYYY-MM-DD format")
    end_date: str=Field(...,description="End date of the trip in YYYY-MM-DD format")
    budget: int=Field(...,description="Total budget for the trip in INR")
    departure_time: Optional[str] = Field("06:00", description="Preferred departure time HH:MM")
    arrival_time: Optional[str] = Field("23:00", description="Latest acceptable arrival time HH:MM")
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
    weather: Optional[WeatherInfo]=Field(None,description="Weather info")
    estimated_cost: int=Field(...,description="Estimated cost in INR")
    
class BudgetBreakdown(BaseModel):
    transport: int = Field(..., description="Transport cost")
    hotel: int = Field(..., description="Hotel cost")
    food: int = Field(..., description="Food cost")
    activities: int = Field(..., description="Activities cost")
    total: int = Field(..., description="Total cost")

class PlannerOutput(BaseModel):
    itinerary: List[DayPlan]
    recommended_hotel: str
    recommended_flight_or_train: str
    budget_breakdown: BudgetBreakdown
    total_estimated_cost: int
    replan_needed: bool
    replan_reason: str

class TripResponse(BaseModel):
    destination: str=Field(...,description="Place to visit")
    start_date: str=Field(...,description="Start date of the trip in YYYY-MM-DD format")
    end_date: str=Field(...,description="End date of the trip in YYYY-MM-DD format")
    total_days: int=Field(...,description="No. of days of trip")
    itinerary: List[DayPlan]=Field(...,description="Complete details day-wise")
    flights: List[FlightInfo]=Field(...,description="Flight Info")
    trains: List[TrainInfo]=Field(...,description="train Info")
    hotels: List[HotelInfo]=Field(...,description="Hotel Info")
    budget_breakdown: dict=Field(...,description="Breakdown of budget")
    total_estimated_cost: int=Field(...,description="Total estimated cost")
    formatted_report: str=Field(...,description="Report of all detials")
    recommendations: Optional[List[str]]=Field([],description="List of recommendations ")

class WhatsAppInput(BaseModel):
    phone_number: str=Field(...,description="Phone number of the user")
    message: str=Field(...,description="Message you want to sent")
    user_id: Optional[str]=Field(None,description="Email or unique identifier of the user")
    
    
