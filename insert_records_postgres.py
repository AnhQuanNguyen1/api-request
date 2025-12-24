import psycopg2

from api_request import mock_fetch_data, fetch_data

def connect_to_db():
    print("Connecting to Postgres DB  ...")
    try:
        conn = psycopg2.connect(
            host="ep-restless-glitter-a7s8v0rp-pooler.ap-southeast-2.aws.neon.tech",
            port=5432,
            dbname="neondb",
            user="neondb_owner",
            password="npg_Bem1Gw6gDIPL",
            sslmode="require",
            channel_binding="require"
        )
        print(conn)
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise
        
def create_table(conn):
    print("Creating table if not exist...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature FLOAT,
                weather_descriptions TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT
            );
        """)
        conn.commit()
        print("Table was created.")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise

from datetime import datetime
from psycopg2.extras import execute_values

def insert_records_postgres(conn, n_records=20000, query="New York", country="United States of America"):
    rows = []

    for _ in range(n_records):
        data = mock_fetch_data(query=query, country=country)
        weather = data["current"]
        location = data["location"]

        localtime_str = location.get("localtime")  # "YYYY-MM-DD HH:MM"
        if isinstance(localtime_str, str) and len(localtime_str) == 16:
            localtime_str += ":00"
        event_time = datetime.fromisoformat(localtime_str) if localtime_str else None

        rows.append((
            location.get("name"),
            float(weather.get("temperature")) if weather.get("temperature") is not None else None,
            (weather.get("weather_descriptions") or [""])[0],
            float(weather.get("wind_speed")) if weather.get("wind_speed") is not None else None,
            event_time,
            str(location.get("utc_offset")) if location.get("utc_offset") is not None else None,
        ))

    sql = """
        INSERT INTO raw_weather_data
            (city, temperature, weather_descriptions, wind_speed, time, utc_offset)
        VALUES %s
    """

    with conn.cursor() as cur:
        execute_values(cur, sql, rows, page_size=5000)
    conn.commit()

    return n_records

    
def main():
    try:
        # data = mock_fetch_data()
        data = mock_fetch_data()
        conn = connect_to_db()
        # create_table(conn)
        insert_records_postgres(conn, n_records=100000, query="Phu Tho", country="Viet Nam")
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")
