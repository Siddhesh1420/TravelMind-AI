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

from tavily import TavilyClient
from config.settings import TAVILY_API_KEY

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def search(query):
    """Search for a query using the Tavily API and return the results"""
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