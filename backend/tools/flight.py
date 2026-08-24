from serpapi import GoogleSearch
from dotenv import load_dotenv
import airportsdata
import os

load_dotenv()
airports = airportsdata.load('IATA')

def get_airport_code(city):
    """
    Get the IATA airport code for a given city"""
    for code, data in airports.items():
        if data['city'].lower() == city.lower():
            return code
    return None

def search_flights(from_city,to_city,date,type,travel_class,stops,max_price,sort_by=1,adults=1,children=0):
    """
    Find flights between two cities on a specific date"""
    params={
        "engine":"google_flights",
        "departure_id": get_airport_code(from_city),
        "arrival_id": get_airport_code(to_city),
        "outbound_date": date,
        "currency":"INR",
        "type": type,
        "travel_class": travel_class,
        "stops": stops,
        "max_price": max_price,
        "adults": adults,
        "children": children,
        "api_key": os.getenv("SERPAPI_KEY")
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    best_flights = results.get("best_flights",[])
    
    if not best_flights:
        best_flights = results.get("other_flights",[])
    if not best_flights:
        print("No flights found for the given criteria.")
    if sort_by == 1:
        best_flights.sort(key=lambda x: x.get("price", float('inf')),reverse=True)
    elif sort_by == 2:
        best_flights.sort(key=lambda x: x.get("duration", float('inf')))
    elif sort_by == 3:
        best_flights.sort(key=lambda x: x.get("departure_time", float('inf')))
    else:
        print("Invalid sort option. Sorting by price.")
        best_flights.sort(key=lambda x: x.get("price", float('inf')))
    return best_flights[:3]  # Return top 3 flights

if __name__ == "__main__":
    from_city = input("Enter departure city: ")
    to_city = input("Enter arrival city: ")

    from_code= get_airport_code(from_city)
    to_code= get_airport_code(to_city)
    if from_code is None or to_code is None:
        print("Airport code not found for one or both cities.")
        exit()

    date = input("Enter date (YYYY-MM-DD): ")
    type = int(input("Enter type (one-way/round-trip): "))
    travel_class = int(input("Enter travel class (economy/business/first): "))
    stops = int(input("Enter number of stops (0/1/2): "))
    max_price = int(input("Enter maximum price: "))
    adults = int(input("Enter number of adults: "))
    children = int(input("Enter number of children: "))
    sort_by = int(input("Enter sort by (1: Price, 2: Duration, 3: Departure Time): "))
    flights = search_flights(from_city, to_city, date, type, travel_class, stops, max_price, sort_by,  adults, children)
    print(flights)
