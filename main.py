
from retry_requests import retry
import api.provider as pv

client = pv.setup_client()
# Setup the Open-Meteo API client with cache and retry on error

rs = client._session
city_name = input("Enter the name of the city: ")
start_date = input( "fecha inicio (aaaa-mm-dd): ")
end_date = input( "fecha fin (aaaa-mm-dd): ")
df_weather = pv.get_hourly_weater(client, rs, city_name, start_date, end_date)

print( "Hourly Weather Data: ")
print(df_weather.head())