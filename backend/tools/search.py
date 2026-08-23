from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()
api=os.getenv('TAVILY_API_KEY')

tavily_client = TavilyClient(api_key=api)

def search(query):
    """
    Search for a query using the Tavily API and return the results"""
    response = tavily_client.search(query)
    return response['results']

if __name__ == "__main__":
    query = input("Enter your search query: ")
    results = search(query)
    for result in results:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Content: {result['content']}")
        print("-" * 50)
