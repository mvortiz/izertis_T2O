import openmeteo_requests

import pandas as pd
import numpy
import json
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
            return "", float(0), float(0)
            
    except Exception as e:
        print(f"error: {e}")
        
        
def get_hourly_weater(client, session, name, start_date, end_date):
    
    _, lat, lon = search_data_city(name, session )
    if lat == lon == float(0) :
        return 0
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
    temp = hourly.Variables(0).ValuesAsNumpy()
    precip = hourly.Variables(1).ValuesAsNumpy()
    
    date = pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
    )
    hourly_data = {"date":date }
    
    hourly_data["city name"] = name
    hourly_data["latitude"] = lat
    hourly_data["longitude"] = lon
    hourly_data["temperature (°C)"] = temp
    hourly_data["precipitations (mm)"] = precip
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    
    date_list = date.strftime("%Y-%m-%dT%H:%M").tolist()
    weather_info = {}
    for key, tp, pp in zip(date_list, temp, precip):
        t = "{:.2f}".format(numpy.float64.item(tp))
        p = "{:.2f}".format(numpy.float64.item(pp))
        weather_info.setdefault(key, []).append(({"temperature":t, "precipitations": p}))
        
    data = {
        "city_name": name,
        "latitude": lat,
        "longitude": lon,
        "weather info": weather_info
    }
    json_data = json.dumps(data)
    json_object = json.loads(json_data)
    data_object = json.dumps(json_object, indent=4)   
    return data_object


def obtain_temp_statistics(client,session,bbdd, name, start_date, end_date, above_thr, below_thr):
   
    if not bbdd:
        _, lat, lon = search_data_city(name, session)
        if lat == lon == float(0) :
            return 0
    else:
        data = json.loads(bbdd)
        lat = data.get("latitude")
        lon = data.get("longitude")
    params_statistics = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_mean", "temperature_2m_max","temperature_2m_min"],
        "hourly": ["temperature_2m"]
    }
    responses = client.weather_api(ARCHIVE_PATH, params = params_statistics)
    response = responses[0]
    
    daily = response.Daily()
    mean = daily.Variables(0).ValuesAsNumpy().tolist()
    max = daily.Variables(1).ValuesAsNumpy()
    min = daily.Variables(2).ValuesAsNumpy()
    hourly = response.Hourly()
    temps = hourly.Variables(0).ValuesAsNumpy()
    
    average = numpy.mean(temps)
    
    date_daily_range = pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
    )
    date_hourly_range = pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
    )
    
    date_list = date_daily_range.strftime("%Y-%m-%d").tolist()
    datetime_list = date_hourly_range.strftime("%Y-%m-%dT%H:%M").tolist()
    date_max_dict = { d: m for d, m in zip(datetime_list, temps)}
    date_min_dict = { d: m for d, m in zip(datetime_list, min)}
    date_mean_dict = { d: m for d, m in zip(date_list, mean)}

    max_temp = numpy.max(temps)
    date_max_temp = [k for k, v in date_max_dict.items() if v == max_temp][0]
 
    min_temp = numpy.min(min)
    date_min_temp = [k for k, v in date_min_dict.items() if v == min_temp][0]

    above_temp = len(numpy.where(max > float(above_thr))[0])
    below_temp = len(numpy.where(min < float(below_thr))[0])
    
    temp_stat = {
        "temperature":{
            "average": "{:.2f}".format(numpy.float64.item(average)),
            "average_by_day": date_mean_dict,
            "max": {
                "value": "{:.2f}".format(numpy.float64.item(max_temp)),
                "date_time": date_max_temp
            },
            "min": {
                "value": "{:.2f}".format(numpy.float64.item(min_temp)),
                "date_time": date_min_temp
            },
            "hours_above_threshold": above_temp,
            "hours_below_threshold": below_temp
        } 
    }
    json_data = json.dumps(temp_stat)
    json_object = json.loads(json_data)
    print(json.dumps(json_object, indent=4))


def obtain_prec_statistics(client,session,bbdd, name, start_date, end_date):
    
    if not bbdd:
        _, lat, lon = search_data_city(name, session)
        if lat == lon == float(0) :
            return 0
    else:
        data = json.loads(bbdd)
        lat = data.get("latitude")
        lon = data.get("longitude")   
         
    params_statistics = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["precipitation"]
    }
    responses = client.weather_api(ARCHIVE_PATH, params = params_statistics)
    response = responses[0]
    hourly = response.Hourly()
    precs = hourly.Variables(0).ValuesAsNumpy().tolist()
    
    total = numpy.sum(precs)
  
    date_hourly_range = pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
    )
    date_list = date_hourly_range.strftime("%Y-%m-%d").tolist()
    
    date_total_prec_dict = {}
    all_prec_by_day_dict = {}
    for key,value in zip(date_list, precs):
        date_total_prec_dict[key] = date_total_prec_dict.get(key,0) + value
        all_prec_by_day_dict.setdefault(key, []).append(value)
    
    days_with_prec = sum(1 for value in date_total_prec_dict.values() if value > 0)
    
    max_prec = numpy.max(precs)
    date_max_precp = [k for k, v in all_prec_by_day_dict.items() if max_prec in v][0]
    
    values = date_total_prec_dict.values()
    average = sum(values)/len(values)
    
    precs_stat = {
        "precipitation":{
            "total": total,
            "total_by_day": date_total_prec_dict,
            "days_with_precipitation": days_with_prec,
            "max": {
                "value": "{:.2f}".format(numpy.float64.item(max_prec)),
                "date_time": date_max_precp
            },
            "average": "{:.2f}".format(average)
        } 
    }
    
    json_data = json.dumps(precs_stat)
    json_object = json.loads(json_data)
    print(json.dumps(json_object, indent=4))
