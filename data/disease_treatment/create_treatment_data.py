import os
import csv

def create_treatment_files():
    # --- CONFIGURATION ---
    # Base path for the new folder structure
    base_dir = os.path.join("data", "disease_treatment")
    
    # Define the 3 sub-paths
    paths = {
        "insecticides": os.path.join(base_dir, "insecticides"),
        "pesticides": os.path.join(base_dir, "pesticides"),
        "treatment_time": os.path.join(base_dir, "treatment_time")
    }

    # 1. Create Directories if they don't exist
    for key, path in paths.items():
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"📂 Created folder: {path}")

    # --- FILE 1: INSECTICIDES.CSV ---
    # Added 'Crop' column to link specific insecticides to crops
    insecticides_file = os.path.join(paths["insecticides"], "insecticides.csv")
    insecticides_data = [
        {"Crop": "Beans", "ID": "INS_001", "Trade_Name": "Confidor", "Active_Ingredient": "Imidacloprid", "Target_Pest": "Aphids, Whiteflies", "Dosage": "0.5 ml/L", "PHI_Days": "7"},
        {"Crop": "Maize", "ID": "INS_002", "Trade_Name": "Coragen", "Active_Ingredient": "Chlorantraniliprole", "Target_Pest": "Fall Armyworm", "Dosage": "0.3 ml/L", "PHI_Days": "14"},
        {"Crop": "Maize", "ID": "INS_003", "Trade_Name": "Thunder", "Active_Ingredient": "Beta-cyfluthrin", "Target_Pest": "Stalk Borer", "Dosage": "1.0 ml/L", "PHI_Days": "7"},
        {"Crop": "Tomatoes", "ID": "INS_004", "Trade_Name": "Match", "Active_Ingredient": "Lufenuron", "Target_Pest": "Caterpillars, Tuta Absoluta", "Dosage": "1.5 ml/L", "PHI_Days": "7"},
        {"Crop": "Wheat", "ID": "INS_005", "Trade_Name": "Actara", "Active_Ingredient": "Thiamethoxam", "Target_Pest": "Russian Wheat Aphid", "Dosage": "0.2 g/L", "PHI_Days": "21"},
        {"Crop": "Onions", "ID": "INS_006", "Trade_Name": "Confidor", "Active_Ingredient": "Imidacloprid", "Target_Pest": "Thrips", "Dosage": "0.5 ml/L", "PHI_Days": "14"},
        {"Crop": "Potatoes", "ID": "INS_007", "Trade_Name": "Belt", "Active_Ingredient": "Flubendiamide", "Target_Pest": "Potato Tuber Moth", "Dosage": "0.2 ml/L", "PHI_Days": "7"},
    ]
    write_csv(insecticides_file, insecticides_data)

    # --- FILE 2: PESTICIDES.CSV ---
    # Added 'Crop' column to link specific fungicides/bactericides to crops
    pesticides_file = os.path.join(paths["pesticides"], "pesticides.csv")
    pesticides_data = [
        {"Crop": "Tomatoes", "ID": "PES_001", "Trade_Name": "Ridomil Gold", "Type": "Fungicide", "Target_Disease": "Late Blight", "Dosage": "2.5 g/L", "Safety_Class": "Class III"},
        {"Crop": "Potatoes", "ID": "PES_002", "Trade_Name": "Ridomil Gold", "Type": "Fungicide", "Target_Disease": "Late Blight", "Dosage": "2.5 g/L", "Safety_Class": "Class III"},
        {"Crop": "Wheat", "ID": "PES_003", "Trade_Name": "Amistar Xtra", "Type": "Fungicide", "Target_Disease": "Wheat Rust, Septoria", "Dosage": "0.75 L/Ha", "Safety_Class": "Class II"},
        {"Crop": "Rice", "ID": "PES_004", "Trade_Name": "Nativo", "Type": "Fungicide", "Target_Disease": "Rice Blast", "Dosage": "0.5 g/L", "Safety_Class": "Class III"},
        {"Crop": "Beans", "ID": "PES_005", "Trade_Name": "Ortiva", "Type": "Fungicide", "Target_Disease": "Anthracnose, Rust", "Dosage": "1.0 ml/L", "Safety_Class": "Class U"},
        {"Crop": "Onions", "ID": "PES_006", "Trade_Name": "Mancozeb", "Type": "Fungicide", "Target_Disease": "Downy Mildew", "Dosage": "2.0 g/L", "Safety_Class": "Class III"},
        {"Crop": "Carrots", "ID": "PES_007", "Trade_Name": "Score 250 EC", "Type": "Fungicide", "Target_Disease": "Leaf Blight", "Dosage": "0.5 ml/L", "Safety_Class": "Class III"},
    ]
    write_csv(pesticides_file, pesticides_data)

    # --- FILE 3: TREATMENT.CSV ---
    # Added 'Crop' column to specify timing for specific crops
    treatment_file = os.path.join(paths["treatment_time"], "treatment.csv")
    treatment_data = [
        {"Crop": "Tomatoes", "Disease_Type": "Fungal (Blight)", "Preferred_Time": "Early Morning (6-9 AM)", "Frequency": "Every 7 Days", "Weather_Condition": "Dry Foliage", "Notes": "Critical during wet season."},
        {"Crop": "Maize", "Disease_Type": "Insect (Fall Armyworm)", "Preferred_Time": "Late Evening", "Frequency": "When pests appear", "Weather_Condition": "No Rain Forecast", "Notes": "Spray into the whorl (funnel)."},
        {"Crop": "Rice", "Disease_Type": "Fungal (Blast)", "Preferred_Time": "Early Morning", "Frequency": "At tillering stage", "Weather_Condition": "Calm Wind", "Notes": "Drain water before spraying if possible."},
        {"Crop": "Potatoes", "Disease_Type": "Fungal (Late Blight)", "Preferred_Time": "Morning", "Frequency": "Every 5-7 Days", "Weather_Condition": "Cool/Cloudy", "Notes": "Preventative spray is best."},
        {"Crop": "Wheat", "Disease_Type": "Fungal (Rust)", "Preferred_Time": "Morning", "Frequency": "At flag leaf stage", "Weather_Condition": "No Rain", "Notes": "Ensure coverage of upper leaves."},
        {"Crop": "Beans", "Disease_Type": "Fungal (Anthracnose)", "Preferred_Time": "Late Afternoon", "Frequency": "Every 10 Days", "Weather_Condition": "Dry", "Notes": "Avoid movement in wet field to stop spread."},
    ]
    write_csv(treatment_file, treatment_data)

    print("\n✅ Success! All treatment files have been generated with Crop columns.")

def write_csv(filepath, data):
    if not data:
        return
    
    # Ensure 'Crop' is the first column
    headers = list(data[0].keys())
    if "Crop" in headers and headers[0] != "Crop":
        headers.remove("Crop")
        headers.insert(0, "Crop")
    
    try:
        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"   📄 Generated: {filepath}")
    except IOError as e:
        print(f"   ❌ Error writing {filepath}: {e}")

if __name__ == "__main__":
    create_treatment_files()