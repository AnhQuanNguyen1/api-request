import requests

api_url = "http://api.weatherstack.com/current?access_key=7ac12934ae616cf30b0abe21b9ca48a5&query=New%20York"

def fetch_data():
    print("Fetching data from api weather data ...")
    try:    
        response = requests.get(api_url)
        response.raise_for_status()
        print(f"API response thành công, {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def mock_fetch_data():
    return {'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2025-12-19 04:06', 'localtime_epoch': 1766117160, 'utc_offset': '-5.0'}, 'current': {'observation_time': '09:06 AM', 'temperature': 12, 'weather_code': 296, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0033_cloudy_with_light_rain_night.png'], 'weather_descriptions': ['Light Rain'], 'astro': {'sunrise': '07:16 AM', 'sunset': '04:31 PM', 'moonrise': '07:15 AM', 'moonset': '03:52 PM', 'moon_phase': 'New Moon', 'moon_illumination': 1}, 'air_quality': {'co': '144.85', 'no2': '16.05', 'o3': '70', 'so2': '2.65', 'pm2_5': '5.05', 'pm10': '6.05', 'us-epa-index': '1', 'gb-defra-index': '1'}, 'wind_speed': 27, 'wind_degree': 169, 'wind_dir': 'S', 'pressure': 1011, 'precip': 0, 'humidity': 83, 'cloudcover': 100, 'feelslike': 10, 'uv_index': 0, 'visibility': 16, 'is_day': 'no'}}
