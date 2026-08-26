
import os
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

# Open-Meteo Geocoding & Weather APIs (Free, no API key required)
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_ICONS = {
    0: ("☀️ ", "Clear Sky", "bright_yellow"),
    1: ("🌤️ ", "Mainly Clear", "yellow"),
    2: ("⛅ ", "Partly Cloudy", "bright_white"),
    3: ("☁️ ", "Overcast", "white"),
    45: ("🌫️ ", "Foggy", "dim white"),
    61: ("🌧️ ", "Slight Rain", "cyan"),
    63: ("🌧️ ", "Moderate Rain", "blue"),
    71: ("❄️ ", "Snowfall", "bright_cyan"),
    95: ("⛈️ ", "Thunderstorm", "bold red"),
}

def get_weather(city_name: str):
    # Step 1: Geocode city name to lat/long
    geo_res = requests.get(GEO_URL, params={"name": city_name, "count": 1}).json()
    if not geo_res.get("results"):
        console.print(f"[bold red]Error:[/] City '{city_name}' not found.")
        return

    location = geo_res["results"][0]
    lat, lon = location["latitude"], location["longitude"]
    country = location.get("country", "")

    # Step 2: Fetch weather metrics
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code", "wind_speed_10m"],
    }
    data = requests.get(WEATHER_URL, params=params).json()["current"]

    # Step 3: Format and render UI
    code = data["weather_code"]
    icon, condition, color = WEATHER_ICONS.get(code, ("🌡️ ", "Unknown", "white"))

    body = Text()
    body.append(f"\n   {icon} {condition.upper()}\n\n", style=f"bold {color}")
    body.append(f"   Temperature : {data['temperature_2m']}°C (Feels like {data['apparent_temperature']}°C)\n")
    body.append(f"   Humidity    : {data['relative_humidity_2m']}%\n")
    body.append(f"   Wind Speed  : {data['wind_speed_10m']} km/h\n")

    panel = Panel(
        body,
        title=f"[bold gold1] Current Weather: {location['name']}, {country} [/bold gold1]",
        expand=False,
        border_style="cyan"
    )
    
    console.print(panel)

if __name__ == "__main__":
    city = input("Enter a city name: ").strip()
    if city:
        get_weather(city)