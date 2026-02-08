# UKULIMA SAFI AI
# Architected by DELSTARFORD WORKS.CO.KE
# Script: Main Application Entry Point (Flask Server)

import os
import logging
import random
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime

# --- IMPORT CUSTOM MODULES ---
try:
    from model.predict import UkulimaAI
    from model.gps_location import GeoGuide
    from weather_api.weather import WeatherService
    from weather_api.weather_crop_logics import WeatherCropBrain
except ImportError as e:
    print(f"❌ Critical Import Error: {e}")
    print("   Ensure all folders (model, weather_api) have an __init__.py file.")
    exit(1)

# --- CONFIGURATION ---
app = Flask(__name__)

# Configure Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
DOCS_FOLDER = os.path.join(BASE_DIR, 'static' , 'documents') # PDFs are in /static/

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOCS_FOLDER'] = DOCS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit uploads to 16MB


# --- AGRI-BRAIN: ADVANCED LOGIC CLASS ---
class AgriBrain:
    def calculate_irrigation(self, crop, rainfall, moisture):
        """Calculates irrigation needs (Simplified for demo)."""
        # Crop Coefficients (Kc)
        kc_map = {"Maize": 1.15, "Beans": 1.05, "Tomatoes": 1.10, "Potatoes": 1.15}
        kc = kc_map.get(crop, 1.0)
        
        et_zero = 5  # Standard daily evapotranspiration (mm)
        field_capacity = 40 # Soil water holding capacity (mm)
        
        # Formula: ETc = ET0 * Kc
        etc = et_zero * kc
        
        # Net Water Loss = Crop Consumption - Rainfall
        water_loss = etc - float(rainfall)
        current_moisture = float(moisture)

        # Only irrigate if moisture drops below 50% of capacity
        if current_moisture < (field_capacity * 0.5):
            irrigation_required = max(0, water_loss + (field_capacity - current_moisture))
            return round(irrigation_required, 2)
        return 0.0

    def estimate_carbon(self, area, crop, practice):
        """Estimates Carbon Sequestration and potential credit value."""
        area = float(area)
        # Factors: Tons of CO2 per hectare per year
        factors = {"Maize": 0.5, "Beans": 0.3, "Trees": 5.0, "Coffee": 3.5}
        
        # No-till farming sequesters more carbon
        practice_multiplier = 1.2 if practice == "no-till" else 1.0
        
        sequestration = area * factors.get(crop, 0.2) * practice_multiplier
        
        # Approximate Value: $15 per ton of CO2
        value = sequestration * 15 
        return round(sequestration, 2), round(value, 2)

    def forecast_prices(self, crop):
        """
        Mock forecasting logic for demo.
        (Real world would use Prophet model on CSV history).
        """
        base_price = {"Maize": 3500, "Beans": 8000, "Tomatoes": 5000}.get(crop, 3000)
        
        dates = []
        prices = []
        # Generate prediction for next 3 months
        for i in range(1, 4): 
            dates.append(f"Month {i}")
            # Add random market fluctuation
            change = random.randint(-500, 800)
            prices.append(base_price + change)
        
        return dates, prices

# --- INITIALIZE SERVICES ---
print("\n Initializing UKULIMA SAFI Services...")
try:
    ai_system = UkulimaAI()
    geo_tool = GeoGuide()
    weather_service = WeatherService()
    weather_brain = WeatherCropBrain()
    agri_brain = AgriBrain() # Initialize new logic
    print("All Services Loaded Successfully!\n")
except Exception as e:
    print(f"Warning: Some services failed to load: {e}")


# =========================================================
#                    WEB PAGE ROUTES
# =========================================================

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/guide')
def guide():
    """GPS Guide Page with Agrovets & Agronomists data."""
    agrovets = ai_system.contact_db.get('agrovets', [])
    agronomists = ai_system.contact_db.get('agronomists', [])
    
    if hasattr(agrovets, 'to_dict'): agrovets = agrovets.to_dict(orient='records')
    if hasattr(agronomists, 'to_dict'): agronomists = agronomists.to_dict(orient='records')

    return render_template('gps_guide.html', agrovets=agrovets, agronomists=agronomists)

@app.route('/indoor')
def indoor():
    return render_template('farming_guide.html', mode='indoor')

@app.route('/outdoor')
def outdoor():
    return render_template('farming_guide.html', mode='outdoor')

# Compatibility Routes
@app.route('/indoorfarming')
def indoorfarming():
    return render_template('farming_guide.html', mode='indoor')

@app.route('/outdoorfarming')
def outdoorfarming():
    return render_template('farming_guide.html', mode='outdoor')

@app.route('/shops')
def shops():
    return render_template('availlable_shops.html')

@app.route('/vets')
def vets():
    return render_template('availlable_vets.html')

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/market')
def market():
    return render_template('market_prices.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/tools')
def tools():
    """Hub for Professional Tools (Irrigation, Carbon, Forecast)."""
    return render_template('pro_tools.html')

# --- ADD AT TOP WITH IMPORTS ---
import shutil # For moving files
import json

# --- UPDATE THE EXPERT ROUTE ---
@app.route('/expert')
def expert():
    """Expert Verification Portal"""
    # Load the list of known diseases so the expert can choose from them
    disease_classes = []
    try:
        with open(os.path.join(BASE_DIR, 'model', 'disease_indices.json'), 'r') as f:
            indices = json.load(f)
            # JSON is {"0": "Tomato_Blight"}, we want just the names values
            disease_classes = list(indices.values())
            disease_classes.sort()
    except:
        disease_classes = ["Error loading classes"]

    return render_template('expert_portal.html', diseases=disease_classes)

# --- ADD NEW API ROUTE FOR VERIFICATION ---
@app.route('/api/submit_verification', methods=['POST'])
def submit_verification():
    """
    Moves the verified image to a 'retrain_dataset' folder structure.
    This prepares the data for the next training cycle.
    """
    data = request.json
    image_filename = data.get('filename')
    correct_label = data.get('correct_label') # e.g., "Tomato___Early_blight"
    notes = data.get('notes')

    if not image_filename or not correct_label:
        return jsonify({'error': 'Missing data'}), 400

    # 1. Define Paths
    source_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    
    # Create a specific folder for retrain data
    retrain_dir = os.path.join(BASE_DIR, 'data', 'retrain_dataset', correct_label)
    os.makedirs(retrain_dir, exist_ok=True)
    
    # Generate new filename with timestamp to avoid duplicates
    new_filename = f"verified_{datetime.now().strftime('%Y%m%d%H%M%S')}_{image_filename}"
    destination_path = os.path.join(retrain_dir, new_filename)

    try:
        # 2. Copy the file to the retrain folder
        if os.path.exists(source_path):
            shutil.copy2(source_path, destination_path)
            
            # Optional: Save notes to a log file
            log_path = os.path.join(BASE_DIR, 'data', 'retrain_dataset', 'expert_logs.txt')
            with open(log_path, "a") as log:
                log.write(f"{datetime.now()}: {new_filename} verified as {correct_label}. Notes: {notes}\n")

            return jsonify({'success': True, 'message': f'Image saved to {correct_label} for retraining.'})
        else:
            return jsonify({'error': 'Original image not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download PDF guides from static folder."""
    try:
        return send_from_directory(app.config['DOCS_FOLDER'], filename, as_attachment=False)
    except FileNotFoundError:
        return "File not found.", 404

@app.route('/api/calc_irrigation', methods=['POST'])
def calc_irrigation():
    data = request.json
    result = agri_brain.calculate_irrigation(
        data.get('crop'), data.get('rainfall'), data.get('moisture')
    )
    return jsonify({'needed': result})

@app.route('/api/calc_carbon', methods=['POST'])
def calc_carbon():
    data = request.json
    tonnes, val = agri_brain.estimate_carbon(
        data.get('area'), data.get('crop'), data.get('practice')
    )
    return jsonify({'tonnes': tonnes, 'value': val})

@app.route('/api/forecast', methods=['POST'])
def forecast():
    data = request.json
    dates, prices = agri_brain.forecast_prices(data.get('crop'))
    return jsonify({'dates': dates, 'prices': prices})

# --- AI PREDICTION API ---

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    user_region = request.form.get('region', 'Kakamega')
    
    try:
        user_lat = float(request.form.get('lat')) if request.form.get('lat') else None
        user_lon = float(request.form.get('lon')) if request.form.get('lon') else None
    except ValueError:
        user_lat, user_lon = None, None

    if file:
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # 1. AI Prediction
            print(f" Analyzing image for region: {user_region}...")
            ai_result = ai_system.predict(filepath, user_region)

            if "error" in ai_result:
                 return jsonify({'error': ai_result['error']}), 500

            # 2. Weather Data
            weather_data = weather_service.get_current_weather(user_region)
            weather_advice = ""
            if weather_data:
                weather_advice = weather_brain.analyze_weather(weather_data, ai_result['crop'])
            else:
                weather_advice = "Could not fetch live weather. Proceed with standard care."

            # 3. GPS Navigation Links
            if 'contacts' in ai_result:
                for shop in ai_result['contacts'].get('agrovets', []):
                    target = shop.get('location') or f"{shop['agrovet']}, {shop['region']}"
                    shop['map_link'] = geo_tool.generate_navigation_link(target, user_lat, user_lon)

                for doc in ai_result['contacts'].get('agronomists', []):
                    target = doc.get('location') or f"{doc['agronomist']}, {doc['region']}"
                    doc['map_link'] = geo_tool.generate_navigation_link(target, user_lat, user_lon)

            # 4. Response
            response = {
                'success': True,
                'prediction': ai_result,
                'weather': {'data': weather_data, 'advice': weather_advice},
                'image_url': f"static/uploads/{filename}"
            }

            return jsonify(response)

        except Exception as e:
            print(f" Error during prediction: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': 'Internal Server Error during analysis.'}), 500
    
    return jsonify({'error': 'File error'}), 400

@app.route('/weather_check', methods=['GET'])
def weather_check():
    """Helper route to check weather."""
    try:
        region = request.args.get('region', 'Kakamega')
        data = weather_service.get_current_weather(region)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(" UKULIMA SAFI AI Server is Running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)