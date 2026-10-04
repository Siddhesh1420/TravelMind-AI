import requests
import urllib3
import os
import sys
import json as _json
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

original_request = requests.Session.request
def patched_request(self, *args, **kwargs):
    kwargs['verify'] = False
    return original_request(self, *args, **kwargs)
requests.Session.request = patched_request

from tavily import TavilyClient
from model import get_model, invoke_model
from config.settings import TAVILY_API_KEY

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
model = get_model()

def search_trains(from_city, to_city, date, departure_time="06:00", arrival_time="22:00"):
    """Search trains between the cities"""
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    day = date_obj.strftime("%A")

    query = f"Direct trains from {from_city} to {to_city} IRCTC train number timings fare 2026. Trains departing after {departure_time} arriving before {arrival_time} on {day} {date}"
    res = tavily_client.search(query, max_results=10)

    search_text = "\n".join([r['content'][:200] for r in res['results'][:5]])

    prompt = f'''
Return ONLY a valid JSON array. No explanation. No markdown. No thinking.

Extract train information for trains running from {from_city} to {to_city} on {date} on {day}.
Date is given in YYYY-MM-DD format.
Include only trains whose operating days include that day.

For each train return these exact keys:
- train_name (full train name)
- train_number (numeric train number)
- departure_time (HH:MM format, use "N/A" if not found)
- arrival_time (HH:MM format, use "N/A" if not found)
- duration (XhYm format, use "N/A" if not found)
- fare (numeric INR fare value only, look for ₹ symbol or "fare" or "price" keywords, use "N/A" if not found)
- classes (list of available classes, empty list if not found)

IMPORTANT: Never return null for any field. Always use "N/A" if data is missing.

Search results to extract from:
{search_text}

Return top 3 trains as a JSON array only. Sort by fare first, then duration, then closest to departure time {departure_time}. Nothing else.
'''
    ans = invoke_model(model, prompt)
    try:
        ans = ans.strip()
        if ans.startswith("```json"):
            ans = ans[7:].strip()
        if ans.startswith("```"):
            ans = ans[3:].strip()
        if ans.endswith("```"):
            ans = ans[:-3].strip()
        return _json.loads(ans)
    except:
        return []

if __name__ == "__main__":
    from_city = input("Enter departure city: ")
    to_city = input("Enter arrival city: ")
    date = input("Enter date (YYYY-MM-DD): ")
    departure_time = input("Enter departure time (HH:MM): ")
    arrival_time = input("Enter arrival time (HH:MM): ")
    res = search_trains(from_city, to_city, date, departure_time, arrival_time)
    print(res)