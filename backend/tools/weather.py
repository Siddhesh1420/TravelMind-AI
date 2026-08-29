import requests,os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
def get_weather(city:str):
    """
    Fetch the weather data for a given city between the dates specified in the form of 
    dictionary"""
    
    api=os.getenv("OPENWEATHERMAP_API_KEY")
    response=requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api}&units=metric')
    res=response.json()
    l=res['list']
    d={}
    for i in l:
        date=i['dt_txt'].split(" ")[0]
        time=i['dt_txt'].split(" ")[1]
        description=i['weather'][0]['description']
        temp=i['main']['temp']
        temp_feel=i['main']['feels_like']
        min_temp=i['main']['temp_min']
        max_temp=i['main']['temp_max']
        if date not in d:
            d[date]={}
        d[date][time]=[description,temp,temp_feel,min_temp,max_temp]
    daily_summary={}
    for date,time in d.items():
        if "12:00:00" in time:
            entry=time['12:00:00']
        else:
            entry=list(time.values())[0]
        daily_summary[date]={
            'condition':entry[0],
            'temp':entry[1],
            'feels_like':entry[2],
            'min_temp':entry[3],
            'max_temp':entry[4]
        }
    return daily_summary    
if __name__=="__main__":    
    city=input("")
    res=get_weather(city)
    print(res)

