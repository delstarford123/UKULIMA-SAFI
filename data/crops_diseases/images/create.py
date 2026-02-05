import os
import csv

def create_disease_csv():
    # --- CONFIGURATION ---
    # Path to your images: data -> crops_diseases -> images
    base_directory = os.path.join("data", "crops_diseases", "images")
    output_file = "disease_images.csv"
    # ---------------------

    if not os.path.exists(base_directory):
        print(f"❌ Error: Directory not found: {base_directory}")
        return

    # --- 1. DEFINING THE DATA DICTIONARY ---
    # Maps specific folder names to Clean Crop Names and Descriptions
    
    disease_info_map = {
        # --- TOMATOES ---
        'Tomato___Early_blight': {
            'Crop': 'Tomato', 'Disease': 'Early Blight',
            'Description': 'A fungal disease causing dark spots on leaves and fruit',
            'Treatment': 'Use fungicides and practice crop rotation'
        },
        'Tomato___Late_blight': {
            'Crop': 'Tomato', 'Disease': 'Late Blight',
            'Description': 'A serious disease that causes dark lesions on leaves and fruit',
            'Treatment': 'Remove infected plants and use resistant varieties'
        },
        'Tomato___Septoria_leaf_spot': {
            'Crop': 'Tomato', 'Disease': 'Septoria Leaf Spot',
            'Description': 'A fungal disease causing small circular spots on leaves',
            'Treatment': 'Apply fungicides and ensure proper spacing for air circulation'
        },
        'Tomato___Bacterial_spot': {
            'Crop': 'Tomato', 'Disease': 'Bacterial Spot',
            'Description': 'Bacterial disease causing small, dark spots on leaves and fruits',
            'Treatment': 'Use copper-based bactericides and disease-free seeds'
        },
        'Tomato___Target_Spot': {
            'Crop': 'Tomato', 'Disease': 'Target Spot',
            'Description': 'Fungal disease causing target-like concentric rings on leaves',
            'Treatment': 'Apply fungicides and improve air circulation'
        },
        'Tomato___Leaf_Mold': {
            'Crop': 'Tomato', 'Disease': 'Leaf Mold',
            'Description': 'Fungal disease causing yellow spots on upper leaves and gray mold below',
            'Treatment': 'Reduce humidity and use fungicides'
        },
        'Tomato___Tomato_mosaic_virus': {
            'Crop': 'Tomato', 'Disease': 'Mosaic Virus',
            'Description': 'Viral disease causing mottled leaves and stunted growth',
            'Treatment': 'Remove infected plants; sanitize tools (no cure)'
        },
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
            'Crop': 'Tomato', 'Disease': 'Yellow Leaf Curl Virus',
            'Description': 'Viral disease causing yellowing and upward curling of leaves',
            'Treatment': 'Control whiteflies which spread the virus; use resistant varieties'
        },
        'Tomato___Spider_mites Two-spotted_spider_mite': {
            'Crop': 'Tomato', 'Disease': 'Spider Mites',
            'Description': 'Tiny pests causing yellow stippling on leaves',
            'Treatment': 'Use miticides or insecticidal soap'
        },
        'Tomato___healthy': {
            'Crop': 'Tomato', 'Disease': 'Healthy',
            'Description': 'Plant is healthy.',
            'Treatment': 'Continue standard care.'
        },

        # --- MAIZE (CORN) ---
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': {
            'Crop': 'Maize', 'Disease': 'Gray Leaf Spot',
            'Description': 'Causes grayish lesions on leaves',
            'Treatment': 'Use resistant varieties and crop rotation'
        },
        'Corn_(maize)___Northern_Leaf_Blight': {
            'Crop': 'Maize', 'Disease': 'Northern Corn Leaf Blight',
            'Description': 'Leads to long, elliptical lesions on leaves',
            'Treatment': 'Apply fungicides and plant resistant hybrids'
        },
        'Corn_(maize)___Common_rust_': {
            'Crop': 'Maize', 'Disease': 'Rust',
            'Description': 'Fungal disease causing orange-red pustules on leaves',
            'Treatment': 'Use resistant varieties and fungicides'
        },
        'Corn_(maize)___healthy': {
            'Crop': 'Maize', 'Disease': 'Healthy',
            'Description': 'Plant is healthy.',
            'Treatment': 'Continue standard care.'
        },

        # --- RICE ---
        'Rice Blast': {
             'Crop': 'Rice', 'Disease': 'Rice Blast',
             'Description': 'Fungal disease causing lesions on leaves and stems',
             'Treatment': 'Apply fungicides and manage water levels'
        },
        'Rice___Bacterial_leaf_blight': {
            'Crop': 'Rice', 'Disease': 'Bacterial Leaf Blight',
            'Description': 'Causes yellowing and wilting of leaves',
            'Treatment': 'Use resistant varieties and proper field sanitation'
        },

        # --- WHEAT ---
        'Wheat aphid': {'Crop': 'Wheat', 'Disease': 'Aphid', 'Description': 'Small insects sucking sap, causing yellowing', 'Treatment': 'Use insecticides'},
        'Wheat black rust': {'Crop': 'Wheat', 'Disease': 'Black Rust', 'Description': 'Dark reddish-brown pustules on stems', 'Treatment': 'Use resistant varieties'},
        'Wheat Brown leaf Rust': {'Crop': 'Wheat', 'Disease': 'Brown Rust', 'Description': 'Orange-brown pustules on leaves', 'Treatment': 'Fungicides'},
        'Wheat leaf blight': {'Crop': 'Wheat', 'Disease': 'Leaf Blight', 'Description': 'Large irregular spots on leaves', 'Treatment': 'Fungicides'},
        'Wheat mite': {'Crop': 'Wheat', 'Disease': 'Mite', 'Description': 'Tiny pests causing leaf discoloration', 'Treatment': 'Miticides'},
        'Wheat powdery mildew': {'Crop': 'Wheat', 'Disease': 'Powdery Mildew', 'Description': 'White powdery patches on leaves', 'Treatment': 'Fungicides'},
        'Wheat scab': {'Crop': 'Wheat', 'Disease': 'Scab', 'Description': 'Bleaching of grain heads', 'Treatment': 'Fungicides and crop rotation'},
        'Wheat Stem fly': {'Crop': 'Wheat', 'Disease': 'Stem Fly', 'Description': 'Larvae bore into stems causing dead hearts', 'Treatment': 'Insecticides'},

        # --- SOYBEANS ---
        'Soybean___healthy': {
            'Crop': 'Soybean', 'Disease': 'Healthy',
            'Description': 'Plant is healthy.',
            'Treatment': 'Continue standard care.'
        },

         # --- CHERRY ---
        'Cherry_(including_sour)___Powdery_mildew': {
            'Crop': 'Cherry', 'Disease': 'Powdery Mildew',
            'Description': 'White powdery fungal growth on leaves',
            'Treatment': 'Fungicides'
        }
    }

    print(f"🚀 Scanning {base_directory} to generate CSV...")

    rows = []
    
    # --- 2. WALK DIRECTORIES ---
    for root, dirs, files in os.walk(base_directory):
        if root == base_directory:
            continue
            
        folder_name = os.path.basename(root)
        
        # Filter strictly for images
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp'))]
        # Sort files specifically to ensure 1.jpg, 2.jpg, 10.jpg sort correctly naturally
        image_files.sort(key=lambda x: int(os.path.splitext(x)[0]) if os.path.splitext(x)[0].isdigit() else x)
        
        if not image_files:
            continue

        # --- 3. DETERMINE METADATA ---
        if folder_name in disease_info_map:
            # Exact match found
            info = disease_info_map[folder_name]
            crop = info['Crop']
            disease = info['Disease']
            desc = info['Description']
            treat = info['Treatment']
        else:
            # FALLBACK: Clean the name automatically
            # Example: "Corn_(maize)___healthy" -> Crop: Maize
            
            # 1. clean Crop Name
            if "Corn" in folder_name:
                crop = "Maize"
            elif "Tomato" in folder_name:
                crop = "Tomato"
            elif "Potato" in folder_name:
                crop = "Potato"
            elif "Wheat" in folder_name:
                crop = "Wheat"
            elif "Rice" in folder_name:
                crop = "Rice"
            elif "Soybean" in folder_name:
                crop = "Soybean"
            elif "Cherry" in folder_name:
                crop = "Cherry"
            else:
                # Last resort: take the first word before any separator
                crop = folder_name.split("_")[0].split(" ")[0]

            # 2. clean Disease Name
            if "___" in folder_name:
                disease = folder_name.split("___")[1].replace("_", " ")
            else:
                # Attempt to remove the crop name from the folder to get disease
                disease = folder_name.replace(crop, "").strip(" _")

            desc = "Description not available in preset."
            treat = "Consult an agronomist."

        # --- 4. CREATE ROW FOR EACH IMAGE ---
        for image_file in image_files:
            rel_path = os.path.join("data", "crops_diseases", "images", folder_name, image_file)
            rel_path = rel_path.replace("\\", "/") # Normalize for CSV

            rows.append({
                "crop": crop,
                "disease": disease,
                "image_location": rel_path,
                "description": desc,
                "treatment": treat
            })

    # --- 5. WRITE CSV ---
    headers = ["crop", "disease", "image_location", "description", "treatment"]
    
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
            
        print(f"✅ Success! Generated '{output_file}' with {len(rows)} rows.")
        print(f"   Sample check -> Crop: '{rows[0]['crop']}', Disease: '{rows[0]['disease']}'")
        
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")

if __name__ == "__main__":
    create_disease_csv()