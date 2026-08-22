import requests,os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
def get_weather(city:str):
    """
    Fetch the weather data for a given city between the dates specified in the form of 
    dictionary"""
    
    api=os.getenv("OPENWEATHERMAP_API_KEY")
    response=requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api}&units=metric')
    # group response by date . in dictionary date as key with time as value and then temp,max temp,mintemp and description
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
    
city=input("")
res=get_weather(city)
print(res)

# {'2026-08-02': {'15:00:00': ['light rain', 28.3, 33.04, 28.16, 28.3], '18:00:00': ['scattered clouds', 28.3, 32.86, 28.27, 28.3], '21:00:00': ['light rain', 28.26, 32.59, 28.26, 28.26]}, '2026-08-03': {'00:00:00': ['light rain', 28.16, 32.5, 28.16, 28.16], '03:00:00': ['light rain', 28.15, 32.64, 28.15, 28.15], '06:00:00': ['light rain', 27.95, 32.13, 27.95, 27.95], '09:00:00': ['moderate rain', 28.27, 32.78, 28.27, 28.27], '12:00:00': ['moderate rain', 27.92, 32.05, 27.92, 27.92], '15:00:00': ['light rain', 28.01, 32.12, 28.01, 28.01], '18:00:00': ['light rain', 28.01, 32.12, 28.01, 28.01], '21:00:00': ['moderate rain', 27.54, 31.23, 27.54, 27.54]}, '2026-08-04': {'00:00:00': ['light rain', 27.95, 31.97, 27.95, 27.95], '03:00:00': ['moderate rain', 27.61, 31.54, 27.61, 27.61], '06:00:00': ['moderate rain', 28.53, 33.1, 28.53, 28.53], '09:00:00': ['light rain', 28.84, 34.09, 28.84, 28.84], '12:00:00': ['light rain', 28.37, 33.22, 28.37, 28.37], '15:00:00': ['light rain', 28.18, 32.55, 28.18, 28.18], '18:00:00': ['light rain', 28.1, 32.51, 28.1, 28.1], '21:00:00': ['light rain', 28.07, 32.27, 28.07, 28.07]}, '2026-08-05': {'00:00:00': ['light rain', 28.29, 32.5, 28.29, 28.29], '03:00:00': ['light rain', 28.06, 32.41, 28.06, 28.06], '06:00:00': ['light rain', 28.38, 32.89, 28.38, 28.38], '09:00:00': ['light rain', 28.36, 32.84, 28.36, 28.36], '12:00:00': ['light rain', 28.22, 33, 28.22, 28.22], '15:00:00': ['light rain', 27.95, 32.13, 27.95, 27.95], '18:00:00': ['light rain', 28.06, 32.41, 28.06, 28.06], '21:00:00': ['light rain', 28.1, 32.35, 28.1, 28.1]}, '2026-08-06': {'00:00:00': ['light rain', 28.05, 32.22, 28.05, 28.05], '03:00:00': ['light rain', 28.17, 32.53, 28.17, 28.17], '06:00:00': ['light rain', 28.38, 33.07, 28.38, 28.38], '09:00:00': ['light rain', 28.56, 33.54, 28.56, 28.56], '12:00:00': ['light rain', 28.28, 33.16, 28.28, 28.28], '15:00:00': ['light rain', 28.04, 32.36, 28.04, 28.04], '18:00:00': ['light rain', 28.08, 32.46, 28.08, 28.08], '21:00:00': ['light rain', 28.03, 32.17, 28.03, 28.03]}, '2026-08-07': {'00:00:00': ['light rain', 27.78, 31.7, 27.78, 27.78], '03:00:00': ['light rain', 28.2, 32.6, 28.2, 28.2], '06:00:00': ['light rain', 28.08, 32.46, 28.08, 28.08], '09:00:00': ['light rain', 28.27, 32.78, 28.27, 28.27], '12:00:00': ['light rain', 28.22, 32.82, 28.22, 28.22]}}
