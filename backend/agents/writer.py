import os
import sys
from groq import Groq
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tools.flight import get_airport_code

load_dotenv()
groq_api=os.getenv('GROQ_API_KEY')
model=Groq(api_key=groq_api)

def write_node(state):
    """
    Writer agent node:
    - Generates a comprehensive Markdown trip report.
    - Generates a concise WhatsApp summary message.
    - Constructs calendar events and direct booking links.
    """
    
    itinerary=state['itinerary']
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
    
    report_prompt = f"""You are a professional travel report writer.

    Create a beautiful, detailed travel itinerary report in markdown format.

    Trip Summary:
    - Destination: {destination}
    - From: {from_city}
    - Dates: {start_date} to {end_date}
    - Group Size: {group_size} people
    - Travel Mode: {travel_mode}
    - Total Budget: ₹{budget}
    - Recommended Hotel: {recommended_hotel}
    - Recommended Transport: {recommended_flight_or_train}

    Day by Day Itinerary:
    {itinerary}

    Budget Breakdown:
    {budget_breakdown}

    Weather Information:
    {weather_data}

    Travel Tips:
    {travel_tips}

    Format the report with:
    1. A header with trip title and dates
    2. A quick summary section (destination highlights, best time, weather)
    3. Day by day plan — each day clearly labeled with morning, afternoon, evening activities
    4. Hotel recommendation with reasons
    5. Transport recommendation with reasons  
    6. Budget breakdown as a markdown table
    7. Important travel tips section
    8. Packing suggestions based on weather and activities

    Use emojis appropriately to make it visually appealing.
    Return the complete markdown report only. No extra text."""
    
    response1 = model.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": report_prompt}],
            max_tokens=4000,
            temperature=0.1
        )
    report=response1.choices[0].message.content
    
    whatsapp_prompt = f"""Create a concise WhatsApp message summarizing this trip plan.

    Trip Details:
    - Destination: {destination}
    - Dates: {start_date} to {end_date}
    - Group Size: {group_size} people
    - Hotel: {recommended_hotel}
    - Transport: {recommended_flight_or_train}
    - Total Cost: ₹{total_estimated_cost}

    Day by Day Summary:
    {itinerary}

    Rules:
    1. Keep it under 500 characters
    2. Use WhatsApp friendly formatting — bold with *text*, new lines between days
    3. Include destination, dates, hotel name
    4. One line summary per day maximum
    5. End with total estimated cost
    6. Add relevant emojis

    Return the WhatsApp message only. Nothing else."""
    
    response2=model.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": whatsapp_prompt}],
        max_tokens=4000,
        temperature=0.1
    )
    whatsapp_msg=response2.choices[0].message.content
    
    calendar_event=[]
    
    for day in itinerary:
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
    
    return{
        **state,
        "formatted_report":report,
        "whatsapp_message":whatsapp_msg,
        "calendar_events": calendar_event,
        "booking_links": booking_links,
        "report_complete": True
    }