#!/usr/bin/env python3
"""weather-cli — terminal weather forecasts via Open-Meteo."""
import argparse
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
WEATHER_CODES = {0: "☀️ Clear", 1: "🌤️ Mostly clear", 2: "⛅ Partly cloudy", 3: "☁️ Overcast", 45: "🌫️ Fog", 51: "🌦️ Drizzle", 61: "🌧️ Rain", 71: "🌨️ Snow", 80: "🌦️ Showers", 95: "⛈️ Thunderstorm"}

def geocode(city):
    resp = httpx.get("https://geocoding-api.open-meteo.com/v1/search", params={"name": city, "count": 1})
    data = resp.json()
    if not data.get("results"):
        console.print(f"[red]City not found: {city}[/red]")
        return None
    r = data["results"][0]
    return {"lat": r["latitude"], "lon": r["longitude"], "name": r["name"], "country": r.get("country", "")}

def fetch_forecast(lat, lon, days):
    resp = httpx.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": lat, "longitude": lon, "forecast_days": days,
        "daily": ["temperature_2m_max", "temperature_2m_min", "weathercode", "precipitation_sum"],
        "timezone": "auto"
    })
    return resp.json()["daily"]