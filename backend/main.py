from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import TripInput,TripResponse
from agents.graph import travel_mind_graph
import uvicorn

app=FastAPI(
    title="TravelMind-AI",
    description="An agent that takes input regarding inputs from user and agent returns complete plan",
    version="1.0.0",
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/plan")
def trip_plan(trip_input : TripInput):
    initial_state = {
    "destination": trip_input.destination,
    "from_city": trip_input.from_city,
    "start_date": trip_input.start_date,
    "end_date": trip_input.end_date,
    "budget": trip_input.budget,
    "group_size": trip_input.group_size,
    "travel_mode": trip_input.travel_mode,
    "preferences": trip_input.preferences or [],
    "phone_number": trip_input.phone_number or "",
    "user_id": trip_input.user_id or "",
    "departure_time": trip_input.departure_time or "06:00",
    "arrival_time": trip_input.arrival_time or "23:00",
    "weather_data": {},
    "flights": [],
    "trains": [],
    "hotels": [],
    "attractions": {},
    "travel_tips": [],
    "research_complete": False,
    "itinerary": [],
    "budget_breakdown": {},
    "replan_needed": False,
    "replan_reason": "",
    "plan_complete": False,
    "recommended_hotel": "",
    "recommended_flight_or_train": "",
    "total_estimated_cost": 0,
    "next_agent": "",
    "orchestrator_feedback": "",
    "retry_counts": {},
    "formatted_report": "",
    "whatsapp_message": "",
    "calendar_events": [],
    "booking_links": {},
    "report_complete": False
    }
    return travel_mind_graph.invoke(initial_state)

@app.get("/health")
def get_health():
    return {"status": "ok"}