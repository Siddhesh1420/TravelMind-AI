from fastapi import FastAPI,Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter,_rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from schemas import TripInput,TripResponse
from agents.graph import travel_mind_graph
from fastapi.responses import StreamingResponse
from integrations.whatsapp import send_whatsapp_message
from integrations.calendar import get_auth_url,exchange_code_for_token,create_calendar_events
import asyncio
import json
import uvicorn
from datetime import datetime

app=FastAPI(
    title="TravelMind-AI",
    description="An agent that takes input regarding inputs from user and agent returns complete plan",
    version="1.0.0",
    debug=True
)

limiter=Limiter(key_func=get_remote_address)
app.state.limiter=limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def build_initial_state(trip_input: TripInput):
    return {
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
        "flights_return": [],
        "trains_return": [],
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
        "report_complete": False,
        "transit_note": ""
    }
@app.post("/plan")
@limiter.limit("3/minute")
async def plan_trip(request:Request,trip_input: TripInput):
    
    # Validation of input
    valid_modes = ['flight', 'train', 'car', 'bus', 'road']
    if trip_input.travel_mode not in valid_modes:
        raise HTTPException(status_code=400, detail=f"Invalid travel mode. Choose from {valid_modes}")
    
    start = datetime.strptime(trip_input.start_date, "%Y-%m-%d")
    end = datetime.strptime(trip_input.end_date, "%Y-%m-%d")
    
    if end <= start:
        raise HTTPException(status_code=400, detail="End date must be after start date")
    
    if (end - start).days > 14:
        raise HTTPException(status_code=400, detail="Trip cannot exceed 14 days")
    
    if trip_input.budget < 2000:
        raise HTTPException(status_code=400, detail="Minimum budget is ₹2000")

    initial_state = build_initial_state(trip_input)
    return travel_mind_graph.invoke(initial_state)

@app.get("/health")
def get_health():
    return {"status": "ok"}

@app.post("/send-whatsapp")
async def send_whatsapp(request: Request, data: dict):
    phone_number = data.get("phone_number")
    message = data.get("message")
    
    if not phone_number:
        raise HTTPException(status_code=400, detail="Phone number required")
    if not message:
        raise HTTPException(status_code=400, detail="Message required")
    
    success = send_whatsapp_message(phone_number, message)
    
    if success:
        return {"status": "sent", "message": "WhatsApp message sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send WhatsApp message")
    
@app.get("/auth/google")
async def google_auth(user_id: str = "default"):
    auth_url, state = get_auth_url()
    return {"auth_url": auth_url, "state": state}

@app.get("/auth/callback")
async def google_callback(code: str, state: str = None):
    try:
        exchange_code_for_token(code,state, "default")
        return {"message": "Google Calendar connected successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/calendar/create")
async def create_events(request: Request, data: dict):
    user_id = data.get("user_id", "default")
    calendar_events = data.get("calendar_events", [])
    
    if not calendar_events:
        raise HTTPException(status_code=400, detail="No calendar events provided")
    
    success = create_calendar_events(user_id, calendar_events)
    
    if success:
        return {"status": "success", "message": f"Created {len(calendar_events)} calendar events"}
    else:
        raise HTTPException(status_code=400, detail="Failed to create events — please connect Google Calendar first")