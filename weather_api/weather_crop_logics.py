# UKULIMA SAFI AI
# Architected by DELSTARFORD WORKS.CO.KE
# Script: Agricultural Weather Logic

class WeatherCropBrain:
    def __init__(self):
        pass


    def analyze_weather(self, weather_data, crop_name="General"):
        """
        Analyzes weather data and returns specific farming advice.
        """
        if not weather_data:
            return "Weather data unavailable. Cannot provide specific advice."

        temp = weather_data['temp']
        humidity = weather_data['humidity']
        condition = weather_data['condition'].lower()
        advice = []

        # --- 1. GENERAL RAIN LOGIC ---
        if "rain" in condition or "drizzle" in condition or "thunderstorm" in condition:
            advice.append("**Do Not Spray:** Avoid applying pesticides or fertilizers today as rain will wash them off.")
            advice.append(" **Drainage:** Ensure field drainage channels are open to prevent waterlogging.")
        
        elif "clear" in condition and temp > 25:
            advice.append(" **Spraying:** Conditions are ideal for foliar spraying (best in early morning/late evening).")

        # --- 2. HUMIDITY LOGIC (Disease Risk) ---
        if humidity > 80:
            advice.append(f"**High Disease Risk:** High humidity ({humidity}%) favors fungal diseases like Blight and Mildew.")
            if crop_name.lower() in ["tomato", "potato"]:
                advice.append("   -> **Action:** Scout for Early/Late Blight spots immediately. Consider preventive fungicide if no rain is forecast.")
        
        elif humidity < 40:
            advice.append(" **Dry Air:** Low humidity increases water loss. Monitor soil moisture closely.")

        # --- 3. TEMPERATURE LOGIC ---
        if temp > 30:
            advice.append(" **Heat Stress:** Temperatures are high. Irrigate in the evening to reduce evaporation loss.")
            if crop_name.lower() in ["maize", "corn"]:
                advice.append("   -> **Action:** High heat during pollination (tasseling) can reduce yield. Ensure soil is moist.")
        
        elif temp < 12:
            advice.append(" **Cold Stress:** Low temperatures may slow growth.")
        
        # --- 4. WIND LOGIC ---
        if weather_data.get('wind_speed', 0) > 5: # > 5 m/s is breezy
            advice.append(" **High Wind:** Avoid spraying; chemicals may drift to non-target crops.")

        # If no specific warnings, give a green light
        if not advice:
            advice.append("**Good Conditions:** Weather is generally favorable for standard field operations.")

        return "\n".join(advice)

# --- TEST BLOCK ---
if __name__ == "__main__":
    brain = WeatherCropBrain()
    
    # Mock Data for Testing
    test_weather = {
        'temp': 22,
        'humidity': 85,
        'condition': 'Clouds',
        'wind_speed': 2
    }
    
    print("--- Analysis for Tomato ---")
    print(brain.analyze_weather(test_weather, "Tomato"))