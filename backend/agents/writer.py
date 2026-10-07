import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # Look for file in previous directory too
from tools.flight import get_airport_code
from model import get_model,invoke_model
from prompts.writer_prompt import get_report_prompt,get_whatsapp_prompt
from memory.store import save_trip
load_dotenv()

model=get_model()


def write_node(state):
    """
    Writer agent node:
    - Generates a comprehensive Markdown trip report.
    - Generates a concise WhatsApp summary message.
    - Constructs calendar events and direct booking links.
    """
    print("Calling agent writer")
    print(f"Writer called with itinerary length: {len(state.get('itinerary', []))}")
    budget_breakdown=state['budget_breakdown']
    recommended_hotel=state.get('recommended_hotel','')
    recommended_flight_or_train=state.get('recommended_flight_or_train','')
    group_size=state['group_size']
    destination=state['destination']
    budget=state['budget']
    weather_data=state.get('weather_data',{})
    flights=state.get('flights',[])
    trains=state.get('trains',[])
    hotels=state.get('hotels',[])
    travel_tips=state['travel_tips']
    start_date=state['start_date']
    end_date=state['end_date']
    from_city=state['from_city']
    total_estimated_cost=state['total_estimated_cost']
    travel_mode=state['travel_mode']
    phone_number=state.get('phone_number',"")
    transit_note=state.get('transit_note','')
    itinerary=state['itinerary']
    
    if not itinerary:
        return {
            **state,
            "formatted_report": "Trip planning failed — itinerary could not be generated.",
            "whatsapp_message": "",
            "calendar_events": [],
            "booking_links": {},
            "report_complete": True
        }
    
    itinerary_slim = [
    {
        "day_number": day.get("day_number"),
        "date": day.get("date"),
        "morning": day.get("morning", "")[:150],
        "afternoon": day.get("afternoon", "")[:150],
        "evening": day.get("evening", "")[:150],
        "estimated_cost": day.get("estimated_cost", 0)
    }
    for day in itinerary
]

# Trim travel tips
    travel_tips_slim = travel_tips[:2] if travel_tips else []
    
    report_prompt = get_report_prompt(
    destination=destination,
    from_city=from_city,
    start_date=start_date,
    end_date=end_date,
    group_size=group_size,
    travel_mode=travel_mode,
    budget=budget,
    recommended_hotel=recommended_hotel,
    recommended_flight_or_train=recommended_flight_or_train,
    itinerary=itinerary_slim,
    budget_breakdown=budget_breakdown,
    weather_data=weather_data,
    travel_tips=travel_tips_slim,
    transit_note=state.get('transit_note', '')
)
    
    report=invoke_model(model,report_prompt)
    
    whatsapp_prompt = get_whatsapp_prompt(
    destination=destination,
    start_date=start_date,
    end_date=end_date,
    group_size=group_size,
    recommended_hotel=recommended_hotel,
    recommended_flight_or_train=recommended_flight_or_train,
    total_estimated_cost=total_estimated_cost,
    itinerary=itinerary_slim
)
    
    whatsapp_msg=invoke_model(model,whatsapp_prompt)
    
    calendar_event=[]
    
    for day in itinerary_slim:
        calendar_event.append({
        "title": f"Day {day['day_number']} — {destination}",
        "date": day['date'],
        "description": f"Morning: {day['morning']}\nAfternoon: {day['afternoon']}\nEvening: {day['evening']}"
    })
    
    booking_links = {}

    # Flight booking link
    if flights:
        from_code = get_airport_code(from_city)
        to_code = get_airport_code(destination)
        booking_links['flight'] = f"https://www.makemytrip.com/flights/search?itinerary={from_code}-{to_code}-{start_date}&tripType=O&paxType=A-{group_size}_C-0_I-0&intl=false&cabinClass=E&lang=eng"

    # Train booking link
    if trains:
        booking_links['train'] = f"https://www.irctc.co.in/nget/train-search"

    # Hotel booking link
    booking_links['hotel'] = f"https://www.booking.com/search.html?ss={destination}&checkin={start_date}&checkout={end_date}&group_adults={group_size}"
    
    result={
        **state,
        "formatted_report":report,
        "whatsapp_message":whatsapp_msg,
        "calendar_events": calendar_event,
        "booking_links": booking_links,
        "report_complete": True
    }
    # Save trip history
    user_id = state.get('user_id', 'default')
    if user_id and user_id != 'default':
        save_trip(user_id, result)
        
    return result