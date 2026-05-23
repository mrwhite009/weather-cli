#!/usr/bin/env python3
import argparse
import httpx
from rich.console import Console
from rich.table import Table

console = Console()
WEATHER_CODES = {0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️", 45: "🌫️", 51: "🌦️", 61: "🌧️", 71: "🌨️", 95: "⛈️"}

def get_weather(city, days=3):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    resp = httpx.get(geo_url, params={"name": city, "count": 1})
    geo_data = resp.json()
    if not geo_data.get("results"):
        console.print(f"[red]City not found: {city}[/red]")
        return
    r = geo_data["results"][0]
    lat, lon = r["latitude"], r["longitude"]
    name, country = r["name"], r.get("country", "")
    
    console.print(f"\n📍 [bold]{name}[/bold], {country}")
    
    table = Table(title="Forecast")
    table.add_column("Date")
    table.add_column("Weather")
    table.add_column("High")
    table.add_column("Low")
    
    weather_url = "https://api.open-meteo.com/v1/forecast"
    resp = httpx.get(weather_url, params={
        "latitude": lat, "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min", "weathercode"],
        "forecast_days": days, "timezone": "auto"
    })
    data = resp.json()["daily"]
    
    for i in range(days):
        hi = data["temperature_2m_max"][i]
        lo = data["temperature_2m_min"][i]
        code = data["weathercode"][i]
        emoji = WEATHER_CODES.get(code, "❓")
        table.add_row(data["time"][i], emoji, f"{hi}°C", f"{lo}°C")
    
    console.print(table)