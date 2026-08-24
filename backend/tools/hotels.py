from serpapi import GoogleSearch
from dotenv import load_dotenv
import os 

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def search_hotels(destination,check_in,check_out,rating,free_cancellation,currency="INR",sort_by=3,adults=1,children=0,min_price=None,max_price=None):
    """ 
    Search for hotels based on above details  """
    
    params={
        "engine":"google_hotels",
        "q":f"Hotels in {destination}",
        "check_in_date":check_in,
        "check_out_date":check_out,
        "currency":currency,
        "min_price":min_price,
        "max_price":max_price,
        "rating":rating,
        "free_cancellation":free_cancellation,
        "adults":adults,
        "children":children,
        "sort_by":sort_by,
        "api_key": os.getenv("SERPAPI_KEY")
    }
    
    params={k:v for k,v in params.items() if v is not None}
    
    search=GoogleSearch(params)
    results=search.get_dict()
    hotels=results.get("properties",[])
    if not hotels:
        print("No hotels found for the given criteria.")
        return []
    return hotels[:3]  # Return top 3 hotels

if __name__=="__main__":
    destination=input("Enter destination: ")
    check_in=input("Enter check-in date (YYYY-MM-DD): ")
    check_out=input("Enter check-out date (YYYY-MM-DD): ")
    currency=input("Enter currency (default INR): ")
    min_price=int(input("Enter minimum price: "))
    max_price=int(input("Enter maximum price: "))
    rating=int(input("Enter minimum rating (7: 3.5+ , 8: 4.0+ , 9: 4.5+ ): "))
    free_cancellation=input("Require free cancellation? (yes/no): ").lower() == "yes"
    adults=int(input("Enter number of adults: "))
    children=int(input("Enter number of children: "))
    sort_by=int(input("Sort by (3=Price, 8=Rating, 13=Most Reviewed): "))

    hotels=search_hotels(destination,check_in,check_out,rating,free_cancellation,currency,sort_by,adults,children,min_price,max_price)
    print(hotels)
        
        
    
    