# UKULIMA SAFI AI
# Architected by DELSTARFORD WORKS.CO.KE
# Script: Geolocation and Navigation Logic

import math
import urllib.parse
import pandas as pd 
class GeoGuide:
    def __init__(self):
        # Base URLs for Google Maps Intents
        self.MAPS_DIR_URL = "https://www.google.com/maps/dir/?api=1"
        self.MAPS_SEARCH_URL = "https://www.google.com/maps/search/?api=1"

    def generate_navigation_link(self, target_location, user_lat=None, user_lon=None):
        """
        Generates a smart Google Maps link to guide the user.
        
        Args:
            target_location (str): The address, name, or URL from your CSV.
            user_lat (float): The user's latitude (from gps_guide.js).
            user_lon (float): The user's longitude (from gps_guide.js).
            
        Returns:
            str: A clickable URL that opens Google Maps navigation.
        """
        if not target_location or pd.isna(target_location):
            return "#"

        # Case 1: The CSV already contains a specific Google Maps Link (e.g., https://goo.gl/...)
        if "http" in str(target_location):
            return target_location

        # Case 2: It is a place name (e.g., "Mombasa CBD"). We generate a Direction Link.
        # Encode the destination safely for URL (e.g., "Mombasa CBD" -> "Mombasa%20CBD")
        encoded_dest = urllib.parse.quote(str(target_location))
        
        if user_lat and user_lon:
            # If we know where the user is, give exact directions from their point
            return f"{self.MAPS_DIR_URL}&origin={user_lat},{user_lon}&destination={encoded_dest}&travelmode=driving"
        else:
            # If we don't know where the user is, just open the location on the map
            return f"{self.MAPS_SEARCH_URL}&query={encoded_dest}"

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculates the distance (in km) between two GPS points using the Haversine formula.
        Useful if you add 'latitude' and 'longitude' columns to your CSVs later.
        """
        try:
            R = 6371  # Radius of the earth in km
            dLat = math.radians(lat2 - lat1)
            dLon = math.radians(lon2 - lon1)
            
            a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
                 math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
                 math.sin(dLon / 2) * math.sin(dLon / 2))
            
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c # Distance in km
            return round(distance, 2)
        except Exception:
            return 99999.9 # Return high distance on error

    def find_nearest_location(self, user_lat, user_lon, locations_df):
        """
        Advanced: Sorts a DataFrame of locations by distance to the user.
        Requires 'latitude' and 'longitude' columns in your CSV.
        """
        if 'latitude' not in locations_df.columns or 'longitude' not in locations_df.columns:
            return locations_df # Return unsorted if no coords

        # Calculate distance for every row
        locations_df['distance_km'] = locations_df.apply(
            lambda row: self.calculate_distance(
                user_lat, user_lon, 
                float(row['latitude']), float(row['longitude'])
            ), axis=1
        )
        
        # Sort by nearest
        return locations_df.sort_values(by='distance_km').head(5)

# --- EXAMPLE USAGE ---
if __name__ == "__main__":
    geo = GeoGuide()
    
    # Test 1: Generating a link with User GPS
    print("Test 1 (With GPS):")
    link = geo.generate_navigation_link("Kedel Agrovet, Kakamega", -0.2827, 34.7519)
    print(f"Link: {link}")
    
    # Test 2: Generating a link without GPS (Search mode)
    print("\nTest 2 (No GPS):")
    link = geo.generate_navigation_link("Nairobi CBD")
    print(f"Link: {link}")