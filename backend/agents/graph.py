from typing import TypedDict,List,Optional,Any

class TravelState(TypedDict):
    # User input
    destination: str
    from_city: str
    start_date: str
    end_date: str
    budget: int
    group_size: int
    travel_mode: str
    preferences: list
    phone_number: str
    user_id: str
    departure_time: str
    arrival_time: str
    
    # Research output
    weather_data: dict
    flights: list
    trains: list
    hotels: list
    attractions: dict
    travel_tips: list
    research_complete: bool
    
    # Planner output
    itinerary: list
    budget_breakdown: dict
    replan_needed: bool
    replan_reason: str
    plan_complete: bool
    
    # Orchestrator control
    next_agent: str
    orchestrator_feedback: str
    retry_counts: dict
    
    # Writer output
    formatted_report: str
    whatsapp_message: str
    calendar_events: list
    booking_links: dict
    report_complete: bool