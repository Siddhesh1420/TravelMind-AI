import requests
import urllib3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

original_request = requests.Session.request
def patched_request(self, *args, **kwargs):
    kwargs['verify'] = False
    return original_request(self, *args, **kwargs)
requests.Session.request = patched_request

from serpapi import GoogleSearch
import airportsdata
from config.settings import SERPAPI_KEY

airports = airportsdata.load('IATA')

CITY_ALIASES = {
    "goa": "GOI",
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "bombay": "BOM",
    "calcutta": "CCU",
    "madras": "MAA",
    "trivandrum": "TRV",
    "kochi": "COK",
    "cochin": "COK",
    "varanasi": "VNS",
    "banaras": "VNS",
    "shimla": "SLV",
    "manali": "KUL",
    "dehradun": "DED",
    "mussoorie": "DED",
    "leh": "IXL",
    "srinagar": "SXR",
    "jammu": "IXJ",
    "amritsar": "ATQ",
    "chandigarh": "IXC",
    "nagpur": "NAG",
    "bhopal": "BHO",
    "indore": "IDR",
    "raipur": "RPR",
    "patna": "PAT",
    "ranchi": "IXR",
    "bhubaneswar": "BBI",
    "visakhapatnam": "VTZ",
    "vizag": "VTZ",
    "coimbatore": "CJB",
    "madurai": "IXM",
    "agra": "AGR",
    "jaipur": "JAI",
    "udaipur": "UDR",
    "jodhpur": "JDH",
    "new delhi": "DEL",
    "delhi": "DEL",
    "bhilai": "RPR",
    "durg": "RPR",
}

def get_airport_code(city):
    """Get the IATA airport code for a given city"""
    city_lower = city.lower().strip()
    if city_lower in CITY_ALIASES:
        return CITY_ALIASES[city_lower]
    for code, data in airports.items():
        if data['city'].lower() == city.lower():
            return code
    return None

def search_flights(from_city, to_city, date, type=2, travel_class=1, stops=0,
                   max_price=50000, sort_by=1, adults=1, children=0):
    """Find flights between two cities on a specific date"""
    params = {
        "engine": "google_flights",
        "departure_id": get_airport_code(from_city),
        "arrival_id": get_airport_code(to_city),
        "outbound_date": date,
        "currency": "INR",
        "type": type,
        "travel_class": travel_class,
        "stops": stops,
        "max_price": max_price,
        "adults": adults,
        "children": children,
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    best_flights = results.get("best_flights", [])

    if not best_flights:
        best_flights = results.get("other_flights", [])
    if not best_flights:
        print("No flights found for the given criteria.")

    if sort_by == 1:
        best_flights.sort(key=lambda x: x.get("price", float('inf')), reverse=True)
    elif sort_by == 2:
        best_flights.sort(key=lambda x: x.get("duration", float('inf')))
    elif sort_by == 3:
        best_flights.sort(key=lambda x: x.get("departure_time", float('inf')))
    else:
        best_flights.sort(key=lambda x: x.get("price", float('inf')))

    return best_flights[:3]

if __name__ == "__main__":
    from_city = input("Enter departure city: ")
    to_city = input("Enter arrival city: ")
    from_code = get_airport_code(from_city)
    to_code = get_airport_code(to_city)
    if from_code is None or to_code is None:
        print("Airport code not found.")
        exit()
    date = input("Enter date (YYYY-MM-DD): ")
    flights = search_flights(from_city, to_city, date)
    print(flights)