import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

GEOCODING_PATH = "https://geocoding-api.open-meteo.com/v1/search?"
ARCHIVE_PATH = "https://archive-api.open-meteo.com/v1/archive"



def setup_client():
    cache_session = requests_cache.CachedSession(".cache", expire_after=  3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor=0.2)
    client = openmeteo_requests.Client(session = retry_session)
    return client


def search_data_city(name, session):
    params = {
        "name": name,
        "count": 10,
        "format": "json",
        "language": "en"
    }
    
    try:
        response = session.get(GEOCODING_PATH, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "results" in data and data["results"]:
            city = data["results"][0]
            lat,lon = city["latitude"], city["longitude"]
            print(f"City found: {city['name']} ({city['country']})")
            return city, lat, lon
        else:
            print("City not found.")
            
    except Exception as e:
        print(f"error: {e}")
        
        
def get_hourly_weater(client, session, name, start_date, end_date):
    
    _, lat, lon = search_data_city(name, session )
    
    params_hourly = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m","precipitation"],
        "start_date": start_date,
        "end_date": end_date
    }
    
    responses = client.weather_api(ARCHIVE_PATH, params = params_hourly)
    response = responses[0]
    hourly = response.Hourly()
    time = pd.to_datetime(hourly.Time(), unit = "s", utc=True)
    temp = hourly.Variables(0).ValuesAsNumpy()
    precip = hourly.Variables(1).ValuesAsNumpy()
    
    
    hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
    )}
    
    hourly_data["temperature (°C)"] = temp
    hourly_data["rain (mm)"] = precip
    hourly_dataframe = pd.DataFrame(data = hourly_data)

    
    return hourly_dataframe