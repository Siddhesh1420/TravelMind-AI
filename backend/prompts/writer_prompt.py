def get_report_prompt(
    destination, from_city, start_date, end_date,
    group_size, travel_mode, budget, recommended_hotel,
    recommended_flight_or_train, itinerary,
    budget_breakdown, weather_data, travel_tips, transit_note
):
    return f"""You are a professional travel report writer.

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
    - Transit Note: {transit_note}
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

    CRITICAL: Use ONLY the itinerary provided below. 
    Do NOT invent any hotel names, activities or restaurants.
    Actual itinerary: {itinerary}
    
    Use emojis appropriately to make it visually appealing.
    Return the complete markdown report only. No extra text.
    """
    
def get_whatsapp_prompt(
    destination, start_date, end_date, group_size,
    recommended_hotel, recommended_flight_or_train,
    total_estimated_cost, itinerary
):
    return f"""Create a concise WhatsApp message summarizing this trip plan.

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