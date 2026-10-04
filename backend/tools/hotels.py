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
from config.settings import SERPAPI_KEY

def search_hotels(destination, check_in, check_out, rating=7, currency="INR",
                  sort_by=3, adults=1, children=0, max_price=None):
    """Search for hotels based on above details"""
    params = {
        "engine": "google_hotels",
        "q": f"Hotels in {destination}",
        "check_in_date": check_in,
        "check_out_date": check_out,
        "currency": currency,
        "max_price": max_price,
        "rating": rating,
        "adults": adults,
        "children": children,
        "sort_by": sort_by,
        "api_key": SERPAPI_KEY
    }

    params = {k: v for k, v in params.items() if v is not None}

    search = GoogleSearch(params)
    results = search.get_dict()
    hotels = results.get("properties", [])

    if not hotels:
        print("No hotels found for the given criteria.")
        return []

    return hotels[:3]

if __name__ == "__main__":
    destination = input("Enter destination: ")
    check_in = input("Enter check-in date (YYYY-MM-DD): ")
    check_out = input("Enter check-out date (YYYY-MM-DD): ")
    rating = int(input("Enter minimum rating (7/8/9): "))
    hotels = search_hotels(destination, check_in, check_out, rating)
    print(hotels)