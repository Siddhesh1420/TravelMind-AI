from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()
api=os.getenv('TAVILY_API_KEY')
tavily_client= TavilyClient(api_key=api)

def search_attractions(destination):
    """
    Find top attractions ,a ctivities and local food in a given destination"""
    
    query1=f"Top tourist attractions to visit in {destination} with brief description and timings."
    query2=f"Best restaurants and local food to try in {destination} with brief description and timings."
    query3=f"Adventure activities and things to do in {destination} with brief description and timings."
    
    res_act=tavily_client.search(query1,max_results=4)
    res_restaurant=tavily_client.search(query2,max_results=4)
    res_activities=tavily_client.search(query3,max_results=4)
    
    return{
        "attractions":[r['content'] for r in res_act['results']],
        "restaurants":[r['content'] for r in res_restaurant['results']],
        "activities":[r['content'] for r in res_activities['results']]
    }
    
if __name__=="__main__":
    destination=input("Enter destunation: ")
    results=search_attractions(destination)
    print(results)
        