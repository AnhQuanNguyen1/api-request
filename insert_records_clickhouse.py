import os
import clickhouse_connect
from datetime import datetime
from api_request import fetch_data, mock_fetch_data
# ===== Config (set bằng env cho tiện) =====
# CH_HOST = os.getenv("CH_HOST", "localhost")
# CH_PORT = int(os.getenv("CH_PORT", "8123"))          
# CH_USER = os.getenv("CH_USER", "default")
# CH_PASSWORD = os.getenv("CH_PASSWORD", "")
# CH_DATABASE = os.getenv("CH_DATABASE", "weather")

# Nếu ClickHouse Cloud dùng HTTPS:
# CH_SECURE = os.getenv("CH_SECURE", "false").lower() == "true"

def connect_to_clickhouse():
    try:
        client = clickhouse_connect.get_client(
            host='p4i376wb1s.ap-southeast-2.aws.clickhouse.cloud',
            user='default',
            password='TN.BR0QPadE62',
            secure=True
        )
        print("Result:", client.query("SELECT 1").result_set[0][0])
        return client
    except Exception  as e:
        print(f"Database connection failed: {e}")
        raise

def create_table(client):
    print("Creating table if not exist...")
    
    try: 
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS default.raw_weather_data
        (
            id UUID DEFAULT generateUUIDv4(),
            city String,
            temperature Float32,
            weather_descriptions String,
            wind_speed Float32,
            `time` DateTime,
            inserted_at DateTime DEFAULT now(),
            utc_offset String
        )
        ENGINE = MergeTree
        ORDER BY (city, time)
        """
        client.command(create_sql)
        
    except Exception as e:
        print(f"Failed to create table: {e}")
        raise

def insert_records_clickhouse(client, n_records=20000, query="New York", country="United States of America"):
    rows = []

    for _ in range(n_records):
        data = mock_fetch_data(query=query, country=country)
        weather = data["current"]
        location = data["location"]

        localtime_str = location.get("localtime")  # "YYYY-MM-DD HH:MM"
        if isinstance(localtime_str, str) and len(localtime_str) == 16:
            localtime_str += ":00"
        event_time = datetime.fromisoformat(localtime_str)

        rows.append((
            location.get("name"),
            float(weather.get("temperature")) if weather.get("temperature") is not None else None,
            (weather.get("weather_descriptions") or [""])[0],
            float(weather.get("wind_speed")) if weather.get("wind_speed") is not None else None,
            event_time,
            str(location.get("utc_offset")),
        ))

    client.insert(
        "default.raw_weather_data",
        rows,
        column_names=["city", "temperature", "weather_descriptions", "wind_speed", "time", "utc_offset"],
    )

    return n_records  # optional
    
def main():
    try:
        data = mock_fetch_data()
        # data = fetch_data()
        client = connect_to_clickhouse()
        # create_table(client)
        insert_records_clickhouse(client, n_records=100000, query="Phu Tho", country="Viet Nam")
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        
    finally:
        if 'client' in locals():
            client.close()
            print("Clickhouse connection closed.")