# UKULIMA SAFI AI
# Architected by DELSTARFORD WORKS.CO.KE
# Script: Weather Fetching Service

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherService:
    def __init__(self):
        
        self.api_key = os.getenv("OPENWEATHER_API_KEY", "624cb78f6f0d63ef99e8a708fe4099f9")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_current_weather(self, city="Kakamega"):
        """
        Fetches real-time weather for a specific city/region.
        """
        if not self.api_key or "YOUR_" in self.api_key:
            print("❌ Error: Missing OpenWeatherMap API Key.")
            return None

        try:
            # Construct the API request
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric" # Returns Temp in Celsius
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract clean, useful data
                weather_info = {
                    "city": data["name"],
                    "temp": round(data["main"]["temp"], 1),        # e.g., 24.5°C
                    "humidity": data["main"]["humidity"],          # e.g., 65%
                    "condition": data["weather"][0]["main"],       # e.g., "Rain", "Clear"
                    "description": data["weather"][0]["description"], # e.g., "light rain"
                    "wind_speed": data["wind"]["speed"]            # e.g., 3.5 m/s
                }
                return weather_info
            
            else:
                print(f"⚠️ Weather API Error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return None

# --- TEST BLOCK ---
if __name__ == "__main__":
    service = WeatherService()
    # Test with a Kenyan city
    data = service.get_current_weather("Nairobi")
    if data:
        print(f"📍 Location: {data['city']}")
        print(f"🌡️ Temp: {data['temp']}°C")
        print(f"💧 Humidity: {data['humidity']}%")
        print(f"☁️ Condition: {data['description']}")