from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()
api=os.getenv('TAVILY_API_KEY')

tavily_client = TavilyClient(api_key=api)
query=input("")
response = tavily_client.search(query)
print(response['results'])
