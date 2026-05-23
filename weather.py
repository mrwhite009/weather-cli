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
                         params={"name": city, "count": 5}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("results"):
            return None
        return data["results"]
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        console.print(f"[red]Error: {e}[/red]")
        return None

def pick_result(results):
    if len(results) == 1:
        return results[0]
    console.print("Multiple results found:")
    for i, r in enumerate(results):
        admin = r.get("admin1", "")
        console.print(f"  [{i + 1}] {r["name"]}, {admin}, {r["country"]}")
    while True:
        try:
            choice = int(console.input("Pick one: ")) - 1
            if 0 <= choice < len(results):
                return results[choice]
        except ValueError:
            pass
        console.print("[red]Invalid choice[/red]")