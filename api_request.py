import random
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
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

def mock_fetch_data(query="New York", country="United States of America", unit="m"):
    now_local = datetime.now(ZoneInfo("America/New_York"))
    now_utc = datetime.now(timezone.utc)

    weather_samples = [
        (296, "Light Rain", "wsymbol_0033_cloudy_with_light_rain_night.png"),
        (302, "Moderate Rain", "wsymbol_0034_cloudy_with_heavy_rain_night.png"),
        (116, "Partly Cloudy", "wsymbol_0008_clear_sky_night.png"),
        (122, "Overcast", "wsymbol_0004_black_low_cloud.png"),
        (113, "Clear", "wsymbol_0008_clear_sky_night.png"),
        (143, "Mist", "wsymbol_0006_mist.png"),
        (308, "Heavy Rain", "wsymbol_0034_cloudy_with_heavy_rain_night.png"),
        (332, "Light Snow", "wsymbol_0011_light_snow_showers_night.png"),
    ]
    weather_code, weather_desc, icon_file = random.choice(weather_samples)

    temperature = random.randint(-8, 18)
    wind_speed = random.randint(0, 45)
    wind_degree = random.randint(0, 359)
    dirs = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    wind_dir = dirs[int(wind_degree / 22.5) % 16]
    humidity = random.randint(30, 100)
    cloudcover = random.randint(0, 100)
    pressure = random.randint(990, 1035)
    visibility = random.randint(1, 16)
    precip = round(random.uniform(0, 15), 1)
    feelslike = temperature + random.randint(-4, 3)
    uv_index = random.randint(0, 3)

    def clamp_airq(x, lo, hi):
        return str(round(max(lo, min(hi, x)), 2))

    air_quality = {
        "co": clamp_airq(random.uniform(50, 400), 0, 1000),
        "no2": clamp_airq(random.uniform(1, 80), 0, 200),
        "o3": clamp_airq(random.uniform(5, 120), 0, 300),
        "so2": clamp_airq(random.uniform(0, 30), 0, 200),
        "pm2_5": clamp_airq(random.uniform(0, 40), 0, 500),
        "pm10": clamp_airq(random.uniform(0, 60), 0, 500),
        "us-epa-index": str(random.randint(1, 6)),
        "gb-defra-index": str(random.randint(1, 10)),
    }

    is_day = "yes" if 6 <= now_local.hour < 18 else "no"

    return {
        "request": {"type": "City", "query": f"{query}, {country}", "language": "en", "unit": unit},
        "location": {
            "name": query,
            "country": country,
            "region": query,
            "lat": str(round(random.uniform(40.4, 41.0), 3)),
            "lon": str(round(random.uniform(-74.3, -73.7), 3)),
            "timezone_id": "America/New_York",
            "localtime": now_local.strftime("%Y-%m-%d %H:%M"),
            "localtime_epoch": int(now_utc.timestamp()),
            "utc_offset": "-5.0",
        },
        "current": {
            "observation_time": now_local.strftime("%I:%M %p"),
            "temperature": temperature,
            "weather_code": weather_code,
            "weather_icons": [f"https://cdn.worldweatheronline.com/images/wsymbols01_png_64/{icon_file}"],
            "weather_descriptions": [weather_desc],
            "astro": {
                "sunrise": "07:16 AM",
                "sunset": "04:31 PM",
                "moonrise": "07:15 AM",
                "moonset": "03:52 PM",
                "moon_phase": random.choice(
                    ["New Moon", "Waxing Crescent", "First Quarter", "Full Moon", "Waning Crescent"]
                ),
                "moon_illumination": random.randint(0, 100),
            },
            "air_quality": air_quality,
            "wind_speed": wind_speed,
            "wind_degree": wind_degree,
            "wind_dir": wind_dir,
            "pressure": pressure,
            "precip": precip,
            "humidity": humidity,
            "cloudcover": cloudcover,
            "feelslike": feelslike,
            "uv_index": uv_index,
            "visibility": visibility,
            "is_day": is_day,
        },
    }



