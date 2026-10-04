import requests
import urllib3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Patch requests to disable SSL verification
original_request = requests.Session.request
def patched_request(self, *args, **kwargs):
    kwargs['verify'] = False
    return original_request(self, *args, **kwargs)
requests.Session.request = patched_request

from tavily import TavilyClient
from config.settings import TAVILY_API_KEY

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def search_attractions(destination):
    """Find top attractions, activities and local food in a given destination"""
    
    query1 = f"Top tourist attractions to visit in {destination} with brief description and timings."
    query2 = f"Best restaurants and local food to try in {destination} with brief description and timings."
    query3 = f"Adventure activities and things to do in {destination} with brief description and timings."
    
    res_act = tavily_client.search(query1, max_results=3)
    res_restaurant = tavily_client.search(query2, max_results=3)
    res_activities = tavily_client.search(query3, max_results=3)
    
    return {
        "attractions": [r['content'] for r in res_act['results']],
        "restaurants": [r['content'] for r in res_restaurant['results']],
        "activities": [r['content'] for r in res_activities['results']]
    }

if __name__ == "__main__":
    destination = input("Enter destination: ")
    results = search_attractions(destination)
    print(results)