from tavily import TavilyClient
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # To check a file in previous directory too
from model import get_model,invoke_model
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


api=os.getenv('TAVILY_API_KEY')

tavily_client = TavilyClient(api_key=api)
model=get_model()

def search_trains(from_city,to_city,date,departure_time,arrival_time):
    """
    Search trains between the cities"""
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    day = date_obj.strftime("%A")  # Get the day of the week
    
    query=f"Trains from {from_city} to {to_city} on {date} on {day} IRCTC schedule timings which departs at or after {departure_time} and reaches at or before {arrival_time} classes . Also find the fare for all the trains."
    res=tavily_client.search(query,max_results=10)
    
    search_text="\n".join([r['content'] for r in res['results']])
    
    prompt = f'''
    Return ONLY a valid JSON array. No explanation. No markdown. No thinking.

    Extract train information for trains running from {from_city} to {to_city} on {date} on {day}.
    Date is given in YYYY-MM-DD format.
    Include only trains whose operating days include that day.

    For each train return these exact keys:
    - train_name
    - train_number
    - departure_time
    - arrival_time
    - duration
    - fare
    - classes

    Search results to extract from:
    {search_text}

    Return top 3 trains as a JSON array only. Sort these trains first on fare then on duration and  then nearer to {departure_time}. Nothing else.
    '''
    ans=invoke_model(model,prompt)
    return ans


if __name__=="__main__":
    from_city=input("Enter departure city: ")
    to_city=input("Enter arrival city: ")
    date=input("Enter date (YYYY-MM-DD): ")
    departure_time=input("Enter departure time: in HH:MM format ")
    arrival_time=input("Enter arrival time: ")
    res=search_trains(from_city,to_city,date,departure_time,arrival_time)
    print(res)
    
    
    