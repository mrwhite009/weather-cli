#!/usr/bin/env python3
import argparse
import httpx

def get_weather(city, days=3):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    resp = httpx.get(geo_url, params={"name": city, "count": 1})
    geo_data = resp.json()
    if not geo_data.get("results"):
        print(f"City not found: {city}")
        return
    r = geo_data["results"][0]
    lat, lon = r["latitude"], r["longitude"]
    name = r["name"]
    
    print(f"\n📍 {name}")
    print("=" * 40)
    
    weather_url = "https://api.open-meteo.com/v1/forecast"
    resp = httpx.get(weather_url, params={
        "latitude": lat, "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min", "weathercode"],
        "forecast_days": days,
        "timezone": "auto"
    })
    data = resp.json()["daily"]
    
    for i in range(days):
        hi = data["temperature_2m_max"][i]
        lo = data["temperature_2m_min"][i]
        date = data["time"][i]
        print(f"{date}: {lo}°C ~ {hi}°C")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("city")
    parser.add_argument("-d", "--days", type=int, default=3)
    args = parser.parse_args()
    get_weather(args.city, args.days)

if __name__ == "__main__":
    main()