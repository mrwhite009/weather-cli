#!/usr/bin/env python3
"""weather-cli — terminal weather forecasts via Open-Meteo."""
import argparse
import sys
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

WEATHER_CODES = {
    0: ("☀️", "Clear"), 1: ("🌤️", "Mostly clear"), 2: ("⛅", "Partly cloudy"),
    3: ("☁️", "Overcast"), 45: ("🌫️", "Fog"), 51: ("🌦️", "Drizzle"),
    61: ("🌧️", "Rain"), 71: ("🌨️", "Snow"), 80: ("🌦️", "Showers"),
    95: ("⛈️", "Thunderstorm"), 96: ("🌩️", "Hail")
}

def geocode(city):
    try:
        resp = httpx.get("https://geocoding-api.open-meteo.com/v1/search",
                         params={"name": city, "count": 1}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("results"):
            return None
        r = data["results"][0]
        return {"lat": r["latitude"], "lon": r["longitude"],
                "name": r["name"], "country": r.get("country", "")}
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        console.print(f"[red]Error: {e}[/red]")
        return None

def fetch_forecast(lat, lon, days):
    resp = httpx.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": lat, "longitude": lon, "forecast_days": days,
        "daily": ["temperature_2m_max", "temperature_2m_min",
                  "weathercode", "precipitation_sum"],
        "timezone": "auto"
    }, timeout=10)
    resp.raise_for_status()
    return resp.json()["daily"]

def display_forecast(geo, forecast):
    console.print(f"\n📍 [bold]{geo["name"]}[/bold], {geo["country"]}")
    table = Table(title="Forecast", box=box.ROUNDED)
    table.add_column("Date", style="cyan")
    table.add_column("Weather")
    table.add_column("High", justify="right")
    table.add_column("Low", justify="right")
    table.add_column("Rain", justify="right")
    
    days = forecast["time"]
    for i in range(len(days)):
        code = forecast["weathercode"][i]
        emoji, label = WEATHER_CODES.get(code, ("❓", "Unknown"))
        hi = forecast["temperature_2m_max"][i]
        lo = forecast["temperature_2m_min"][i]
        rain = forecast["precipitation_sum"][i]
        table.add_row(days[i], f"{emoji} {label}", f"{hi}°", f"{lo}°", f"{rain}mm")
    
    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Terminal weather forecasts")
    parser.add_argument("city", help="City name")
    parser.add_argument("-d", "--days", type=int, default=3, help="Forecast days (1-7)")
    parser.add_argument("-s", "--simple", action="store_true", help="Simple output")
    args = parser.parse_args()
    
    if args.days < 1 or args.days > 7:
        console.print("[red]Days must be between 1 and 7[/red]")
        sys.exit(1)
    
    geo = geocode(args.city)
    if not geo:
        console.print(f"[red]City not found: {args.city}[/red]")
        sys.exit(1)
    
    forecast = fetch_forecast(geo["lat"], geo["lon"], args.days)
    if args.simple:
        for i, d in enumerate(forecast["time"]):
            print(f"{d}: {forecast["temperature_2m_min"][i]}~{forecast["temperature_2m_max"][i]}°C")
    else:
        display_forecast(geo, forecast)

if __name__ == "__main__":
    main()