import requests

def get_weather(city):
    # Geocoding API: converts city name to coordinates.
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo = requests.get(geo_url, params={"name": city, "count": 1, "language": "en"}, timeout=10)
    geo.raise_for_status()
    locations = geo.json().get("results", [])
    if not locations:
        raise ValueError("City not found.")

    place = locations[0]
    lat, lon = place["latitude"], place["longitude"]

    # Open-Meteo weather API: no API key required.
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather = requests.get(
        weather_url,
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "timezone": "auto",
        },
        timeout=10,
    )
    weather.raise_for_status()
    return place, weather.json()["current"]

def main():
    print("=== Weather App ===")
    city = input("Enter city name: ").strip()
    if not city:
        print("Please enter a city.")
        return

    try:
        place, current = get_weather(city)
        print(f"\nLocation: {place['name']}, {place.get('country', '')}")
        print(f"Temperature: {current['temperature_2m']} °C")
        print(f"Humidity: {current['relative_humidity_2m']} %")
        print(f"Wind speed: {current['wind_speed_10m']} km/h")
        print(f"Weather code: {current['weather_code']}")
    except requests.RequestException:
        print("Network/API error. Check your internet connection and try again.")
    except ValueError as exc:
        print(exc)

if __name__ == "__main__":
    main()
