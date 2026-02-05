import os
import csv
import requests
import time

# --- CONFIGURATION ---
# 1. PASTE YOUR UNSPLASH ACCESS KEY HERE
ACCESS_KEY = "utZdJjUBeWLIMjbDHZrZ83oV9v2QMak5LA_pqJTo05E" 

# 2. FOLDERS
BASE_DIR = os.path.join("data", "crops_growth_stage")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
CSV_FILE = os.path.join(IMAGES_DIR, "growth_stage_images.csv")

# Ensure directories exist
os.makedirs(IMAGES_DIR, exist_ok=True)

def fetch_growth_stage_data():
    # --- DATA DEFINITION ---
    # Crop, Growth_Stage, Age, Time_Taken, Diseases
    raw_data = [
        # Tomatoes
        ("Tomatoes", "Seedling", "2 weeks", "14 days", "Early Blight;Late Blight;Septoria Leaf Spot"),
        ("Tomatoes", "Vegetative", "4 weeks", "28 days", "Early Blight;Late Blight"),
        ("Tomatoes", "Budding", "6 weeks", "42 days", "Late Blight;Septoria Leaf Spot"),
        ("Tomatoes", "Flowering", "8 weeks", "56 days", "Early Blight;Late Blight"),
        ("Tomatoes", "Fruiting", "10 weeks", "70 days", "Late Blight;Septoria Leaf"),
        # Potatoes
        ("Potatoes", "Seedling", "3 weeks", "21 days", "Early Blight;Late Blight;Blackleg"),
        ("Potatoes", "Vegetative", "5 weeks", "35 days", "Early Blight;Late Blight"),
        ("Potatoes", "Budding", "7 weeks", "49 days", "Late Blight;Blackleg"),
        ("Potatoes", "Flowering", "9 weeks", "63 days", "Early Blight;Late Blight"),
        ("Potatoes", "Fruiting", "11 weeks", "77 days", "Late Blight;Blackleg"),
        # Wheat
        ("Wheat", "Seedling", "2 weeks", "14 days", "Rust;Fusarium Head Blight"),
        ("Wheat", "Vegetative", "4 weeks", "28 days", "Rust;Fusarium Head Blight"),
        ("Wheat", "Budding", "6 weeks", "42 days", "Fusarium Head Blight"),
        ("Wheat", "Flowering", "8 weeks", "56 days", "Rust;Fusarium Head Blight"),
        ("Wheat", "Fruiting", "10 weeks", "70 days", "Rust;Fusarium Head Blight"),
        # Rice
        ("Rice", "Seedling", "3 weeks", "21 days", "Bacterial Leaf Blight;Rice Blast"),
        ("Rice", "Vegetative", "5 weeks", "35 days", "Bacterial Leaf Blight;Rice Blast"),
        ("Rice", "Budding", "7 weeks", "49 days", "Rice Blast"),
        ("Rice", "Flowering", "9 weeks", "63 days", "Bacterial Leaf Blight;Rice Blast"),
        ("Rice", "Fruiting", "11 weeks", "77 days", "Bacterial Leaf Blight;Rice Blast"),
        # Maize
        ("Maize", "Seedling", "2 weeks", "14 days", "Gray Leaf Spot;Northern Corn Leaf Blight"),
        ("Maize", "Vegetative", "4 weeks", "28 days", "Gray Leaf Spot;Northern Corn Leaf Blight"),
        ("Maize", "Budding", "6 weeks", "42 days", "Northern Corn Leaf Blight"),
        ("Maize", "Flowering", "8 weeks", "56 days", "Gray Leaf Spot;Northern Corn Leaf Blight"),
        ("Maize", "Fruiting", "10 weeks", "70 days", "Gray Leaf Spot;Northern Corn Leaf Blight"),
        # Soybeans
        ("Soybeans", "Seedling", "2 weeks", "14 days", "Soybean Cyst Nematode"),
        ("Soybeans", "Vegetative", "4 weeks", "28 days", "Soybean Cyst Nematode;Brown Spot"),
        ("Soybeans", "Budding", "6 weeks", "42 days", "Brown Spot"),
        ("Soybeans", "Flowering", "8 weeks", "56 days", "Soybean Cyst Nematode;Brown Spot"),
        ("Soybeans", "Fruiting", "10 weeks", "70 days", "Soybean Cyst Nematode"),
        # Carrots
        ("Carrots", "Seedling", "2 weeks", "14 days", "Alternaria Leaf Blight;Root Knot Nematode"),
        ("Carrots", "Vegetative", "4 weeks", "28 days", "Alternaria Leaf Blight;Root Knot Nematode"),
        ("Carrots", "Budding", "6 weeks", "42 days", "Root Knot Nematode"),
        ("Carrots", "Flowering", "8 weeks", "56 days", "Alternaria Leaf Blight;Root Knot Nematode"),
        ("Carrots", "Fruiting", "10 weeks", "70 days", "Alternaria Leaf Blight;Root Knot Nematode"),
        # Onions
        ("Onions", "Seedling", "3 weeks", "21 days", "Downy Mildew;Fusarium Basal Rot;Neck Rot"),
        ("Onions", "Vegetative", "5 weeks", "35 days", "Downy Mildew;Fusarium Basal Rot"),
        ("Onions", "Budding", "7 weeks", "49 days", "Fusarium Basal Rot;Neck Rot"),
        ("Onions", "Flowering", "9 weeks", "63 days", "Downy Mildew;Fusarium Basal Rot"),
        ("Onions", "Fruiting", "11 weeks", "77 days", "Downy Mildew;Neck Rot"),
        # Beans
        ("Beans", "Seedling", "2 weeks", "14 days", "Anthracnose;Bacterial Blight"),
        ("Beans", "Vegetative", "4 weeks", "28 days", "Anthracnose;Bacterial Blight"),
        ("Beans", "Budding", "6 weeks", "42 days", "Bacterial Blight"),
        ("Beans", "Flowering", "8 weeks", "56 days", "Anthracnose;Bacterial Blight"),
        ("Beans", "Fruiting", "10 weeks", "70 days", "Anthracnose;Bacterial Blight"),
    ]

    print(f"🚀 Starting process for {len(raw_data)} rows...")
    
    csv_rows = []
    
    for item in raw_data:
        crop, stage, age, time_taken, diseases = item
        
        # specific search query for Unsplash
        search_query = f"{crop} plant {stage} stage"
        
        # Define filename: e.g., Tomatoes_Seedling.jpg
        filename = f"{crop}_{stage}.jpg".replace(" ", "_")
        local_path = os.path.join(IMAGES_DIR, filename)
        
        # Path relative to project root for the CSV
        csv_path = os.path.join("data", "crops_growth_stage", "images", filename).replace("\\", "/")

        # --- DOWNLOAD LOGIC ---
        downloaded = False
        if "YOUR_UNSPLASH_ACCESS_KEY" not in ACCESS_KEY:
            # Try to download from API
            url = "https://api.unsplash.com/search/photos"
            params = {
                "query": search_query,
                "per_page": 1,
                "orientation": "landscape"
            }
            headers = {"Authorization": f"Client-ID {ACCESS_KEY}"}
            
            try:
                if not os.path.exists(local_path):
                    print(f"   ⬇️  Fetching: {search_query}...")
                    response = requests.get(url, params=params, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        if data['results']:
                            image_url = data['results'][0]['urls']['regular']
                            img_data = requests.get(image_url).content
                            with open(local_path, 'wb') as f:
                                f.write(img_data)
                            downloaded = True
                            time.sleep(1) # Be polite to API
                        else:
                            print(f"      ⚠️ No results found for {search_query}")
                    else:
                        print(f"      ❌ API Error: {response.status_code}")
                else:
                    print(f"   ✅ Exists: {filename}")
                    downloaded = True
            except Exception as e:
                print(f"      ❌ Error: {e}")
        else:
            # Placeholder mode (No API Key provided)
            if not os.path.exists(local_path):
                 print(f"   ℹ️  Skipping download (No API Key). CSV will point to: {filename}")
        
        # Add to CSV rows
        csv_rows.append({
            "crop": crop,
            "growth_stage": stage,
            "age": age,
            "time_taken": time_taken,
            "possible_stage_diseases": diseases,
            "image": csv_path
        })

    # --- WRITE CSV ---
    headers = ["crop", "growth_stage", "age", "time_taken", "possible_stage_diseases", "image"]
    
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(csv_rows)
        
    print(f"\n✅ Finished! Data saved to: {CSV_FILE}")
    if "YOUR_UNSPLASH" in ACCESS_KEY:
        print("⚠️ NOTE: Images were NOT downloaded because no API Key was provided.")
        print("   The CSV was created successfully, but image files are missing.")
        print("   To fix: Get a key from unsplash.com/developers and paste it in the script.")

if __name__ == "__main__":
    fetch_growth_stage_data()