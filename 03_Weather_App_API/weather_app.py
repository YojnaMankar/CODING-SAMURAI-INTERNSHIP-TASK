import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    if not API_KEY:
        print("❌ API key not found. Please check your .env file.")
        return

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        if response.status_code == 404:
            print("❌ City not found. Please check the city name.")
            return

        if response.status_code == 401:
            print("❌ Invalid API key or API key is not activated.")
            return

        response.raise_for_status()

        data = response.json()

        city_name = data["name"]
        country = data["sys"]["country"]
        temperature_c = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        temperature_f = (temperature_c * 9 / 5) + 32

        print("\n================================")
        print("          WEATHER APP")
        print("================================")
        print(f"📍 Location      : {city_name}, {country}")
        print(f"🌡️ Temperature   : {temperature_c:.1f} °C")
        print(f"🌡️ Temperature   : {temperature_f:.1f} °F")
        print(f"💧 Humidity      : {humidity}%")
        print(f"☁️ Condition     : {description.title()}")
        print(f"💨 Wind Speed    : {wind_speed} m/s")
        print("================================")

    except requests.exceptions.Timeout:
        print("❌ Request timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        print("❌ Internet connection error.")

    except requests.exceptions.RequestException as error:
        print(f"❌ API error: {error}")


def main():
    print("\n=== Weather App ===")

    while True:
        city = input("\nEnter city name (or 'exit' to quit): ").strip()

        if city.lower() == "exit":
            print("👋 Weather App closed.")
            break

        if not city:
            print("❌ Please enter a city name.")
            continue

        get_weather(city)


if __name__ == "__main__":
    main()