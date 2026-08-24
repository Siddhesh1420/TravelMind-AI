from tavily import TavilyClient
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


api=os.getenv('TAVILY_API_KEY')
groq_api=os.getenv('GROQ_API_KEY')

tavily_client = TavilyClient(api_key=api)
model=Groq(api_key=groq_api)

def search_trains(from_city,to_city,date):
    """
    Search trains between the cities"""
    
    query=f"Trains from {from_city} to {to_city} on {date} IRCTC schedule timings classes"
    res=tavily_client.search(query)
    
    search_text="\n".join([r['content'] for r in res['results']])
    
    prompt = f'''
    Return ONLY a valid JSON array. No explanation. No markdown. No thinking.

    Extract train information for trains running from {from_city} to {to_city} on {date}.
    Check if train runs on that day of week.

    For each train return these exact keys:
    - train_name
    - train_number
    - departure_time
    - arrival_time
    - duration
    - classes
    - days

    Search results to extract from:
    {search_text}

    Return top 3 trains as a JSON array only. Nothing else.
    '''
    response = model.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1000,
    temperature=0.1
)
    ans=response.choices[0].message.content
    return ans

if __name__=="__main__":
    from_city=input("Enter departure city: ")
    to_city=input("Enter arrival city: ")
    date=input("Enter date (YYYY-MM-DD): ")
    res=search_trains(from_city,to_city,date)
    print(res)
    
    
    