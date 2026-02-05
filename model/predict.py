# UKULIMA SAFI AI
# Architected by DELSTARFORD WORKS.CO.KE
# Script: Prediction and Logic

import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# --- ROBUST IMPORT LOGIC ---
# This fixes the "No module named preprocess" error
try:
    # When running from main.py
    from model.preprocess import load_treatment_data, load_contact_data
except ImportError:
    # When running directly inside model folder
    from preprocess import load_treatment_data, load_contact_data

# --- CONFIGURATION ---
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

class UkulimaAI:
    def __init__(self):
        print(" Loading UKULIMA SAFI AI Models...")
        self.disease_model = self._load_model('disease_model.h5')
        self.growth_model = self._load_model('growth_model.h5')
        
        self.disease_labels = self._load_labels('disease_indices.json')
        self.growth_labels = self._load_labels('growth_indices.json')
        
        # Load Databases
        self.treatment_db = load_treatment_data()
        self.contact_db = load_contact_data()
        
        print(" Models and All Databases Loaded.")

    def _load_model(self, filename):
        path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(path):
            return tf.keras.models.load_model(path)
        print(f"Warning: Model {filename} not found in {MODEL_DIR}")
        return None

    def _load_labels(self, filename):
        path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return {int(k): v for k, v in json.load(f).items()}
        return {}

    def prepare_image(self, img_path):
        """Loads and preprocesses a single image for prediction."""
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0
        return img_array

    def get_contact_suggestions(self, crop_name, region=None):
        """
        Filters Agrovets and Agronomists based on Crop and Region.
        """
        suggestions = {
            "agrovets": [],
            "agronomists": []
        }

        # Helper to filter dataframe safely
        def filter_db(df, crop, region):
            if df.empty: return []
            
            # 1. Filter by Crop (Case insensitive)
            filtered = df[df['crop'].astype(str).str.contains(crop, case=False, na=False)]
            
            # 2. Filter by Region if provided
            if region and not filtered.empty:
                region_match = filtered[filtered['region'].astype(str).str.contains(region, case=False, na=False)]
                if not region_match.empty:
                    filtered = region_match
            
            return filtered.to_dict(orient='records')

        # Get Agrovets
        suggestions['agrovets'] = filter_db(self.contact_db['agrovets'], crop_name, region)
        
        # Get Agronomists
        suggestions['agronomists'] = filter_db(self.contact_db['agronomists'], crop_name, region)

        return suggestions

    def get_recommendations(self, crop, disease):
        recs = {
            "insecticide": "None specific found.",
            "pesticide": "None specific found.",
            "advice": "Consult an agronomist for specific advice."
        }

        # Search Pesticides
        if not self.treatment_db['pesticides'].empty:
            df = self.treatment_db['pesticides']
            match = df[
                (df['Crop'].str.contains(crop, case=False, na=False)) & 
                (df['Target_Disease'].str.contains(disease, case=False, na=False))
            ]
            if not match.empty:
                row = match.iloc[0]
                recs["pesticide"] = f"{row['Trade_Name']} ({row['Type']}) - {row['Dosage']}"

        # Search Insecticides
        if not self.treatment_db['insecticides'].empty:
            df = self.treatment_db['insecticides']
            match = df[
                (df['Crop'].str.contains(crop, case=False, na=False)) & 
                (df['Target_Pest'].str.contains(disease, case=False, na=False))
            ]
            if not match.empty:
                row = match.iloc[0]
                recs["insecticide"] = f"{row['Trade_Name']} - {row['Dosage']}"

        # Search Advice
        if not self.treatment_db['advice'].empty:
            df = self.treatment_db['advice']
            match = df[df['Crop'].str.contains(crop, case=False, na=False)]
            if not match.empty:
                row = match.iloc[0]
                recs["advice"] = f"{row['Preferred_Time']} | {row['Frequency']} | {row['Notes']}"

        return recs

    def predict(self, img_path, user_region="Kakamega"):
        """Main prediction function."""
        if not self.disease_model or not self.growth_model:
            return {"error": "Models not trained yet."}

        try:
            processed_img = self.prepare_image(img_path)

            # --- 1. PREDICT DISEASE ---
            d_preds = self.disease_model.predict(processed_img)
            d_class_idx = np.argmax(d_preds, axis=1)[0]
            d_confidence = float(np.max(d_preds))
            raw_disease_label = self.disease_labels.get(d_class_idx, "Unknown")
            
            if "___" in raw_disease_label:
                parts = raw_disease_label.split("___")
                crop_name = parts[0].replace("_", " ").strip()
                disease_name = parts[1].replace("_", " ").strip()
            else:
                crop_name = "Unknown"
                disease_name = raw_disease_label

            # --- 2. PREDICT GROWTH STAGE ---
            g_preds = self.growth_model.predict(processed_img)
            g_class_idx = np.argmax(g_preds, axis=1)[0]
            growth_stage = self.growth_labels.get(g_class_idx, "Unknown")

            # --- 3. GET TREATMENT & CONTACTS ---
            treatments = self.get_recommendations(crop_name, disease_name)
            contacts = self.get_contact_suggestions(crop_name, user_region)

            return {
                "crop": crop_name,
                "disease": disease_name,
                "confidence": round(d_confidence * 100, 2),
                "growth_stage": growth_stage,
                "treatment": treatments,
                "contacts": contacts 
            }
        except Exception as e:
            print(f"Prediction Error: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    ai = UkulimaAI()
    print("AI System Loaded Successfully.")