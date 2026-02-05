# UKULIMA SAFI
# Architected by DELSTARFORD WORKS.CO.KE
# Script: Main Application Entry Point (Flask Server)

import os
import logging
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# --- IMPORT CUSTOM MODULES ---
# We wrap imports in try-except to debug path issues easily
try:
    from model.predict import UkulimaAI
    from model.gps_location import GeoGuide  # Matches your file structure
    from weather_api.weather import WeatherService
    from weather_api.weather_crop_logics import WeatherCropBrain
except ImportError as e:
    print(f"Critical Import Error: {e}")
    print("   Ensure all folders (model, weather_api) have an __init__.py file.")
    exit(1)

# --- CONFIGURATION ---
app = Flask(__name__)

# Configure Upload Folder
# We use absolute paths to avoid confusion
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit uploads to 16MB

# --- INITIALIZE SERVICES (Load them once at startup) ---
print("\n🔌 Initializing UKULIMA SAFI Services...")

try:
    # 1. Load AI Brain
    ai_system = UkulimaAI()
    
    # 2. Load Tools
    geo_tool = GeoGuide()
    weather_service = WeatherService()
    weather_brain = WeatherCropBrain()
    
    print("All Services Loaded Successfully!\n")

except Exception as e:
    print(f" Warning: Some services failed to load: {e}")
    print("   The app will run, but predictions might fail.\n")


# --- WEB PAGE ROUTES ---

@app.route('/')
def home():
    """Renders the Landing Page."""
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    """Renders the Main AI Tool."""
    return render_template('dashboard.html')

@app.route('/guide')
def guide():
    """Renders the GPS Guide Page."""
    return render_template('gps_guide.html')

@app.route('/indoor')
def indoor():
    return render_template('indoor_farming.html')

@app.route('/outdoor')
def outdoor():
    return render_template('outdoor_farming.html')

@app.route('/shops')
def shops():
    return render_template('available_shops.html')

@app.route('/vets')
def vets():
    return render_template('available_vets.html')


# --- API ROUTES (The Logic) ---

@app.route('/predict', methods=['POST'])
def predict():
    """
    Main API Endpoint:
    1. Receives Image & User Region
    2. Runs AI Prediction
    3. Fetches Weather
    4. Generates Map Links
    5. Returns JSON to Frontend
    """
    # 1. Validate Input
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    # 2. Get User Context (Region & GPS)
    user_region = request.form.get('region', 'Kakamega')
    
    # Safely convert GPS strings to floats (handle empty or null values)
    try:
        raw_lat = request.form.get('lat')
        raw_lon = request.form.get('lon')
        user_lat = float(raw_lat) if raw_lat else None
        user_lon = float(raw_lon) if raw_lon else None
    except ValueError:
        user_lat, user_lon = None, None

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        try:
            # 3. Save Image
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # 4. Run AI Prediction
            # This calls predict.py which finds disease, growth stage, treatment & contacts
            print(f"Analyzing image for region: {user_region}...")
            ai_result = ai_system.predict(filepath, user_region)

            if "error" in ai_result:
                 return jsonify({'error': ai_result['error']}), 500

            # 5. Fetch Real-time Weather
            weather_data = weather_service.get_current_weather(user_region)
            
            # 6. Generate Smart Weather Advice
            weather_advice = ""
            if weather_data:
                weather_advice = weather_brain.analyze_weather(weather_data, ai_result['crop'])
            else:
                weather_advice = "Could not fetch live weather. Proceed with standard care."

            # 7. Enhance Contacts with Navigation Links
            # We add specific Google Maps links based on the user's actual GPS
            
            # Process Agrovets
            if 'contacts' in ai_result and 'agrovets' in ai_result['contacts']:
                for shop in ai_result['contacts']['agrovets']:
                    # Use specific location if available, else use Region
                    target = shop.get('location') or f"{shop['agrovet']}, {shop['region']}"
                    shop['map_link'] = geo_tool.generate_navigation_link(target, user_lat, user_lon)

            # Process Agronomists
            if 'contacts' in ai_result and 'agronomists' in ai_result['contacts']:
                for doc in ai_result['contacts']['agronomists']:
                    target = doc.get('location') or f"{doc['agronomist']}, {doc['region']}"
                    doc['map_link'] = geo_tool.generate_navigation_link(target, user_lat, user_lon)

            # 8. Construct Final Response
            # We use a relative path for the image_url so the browser can load it
            relative_image_path = f"static/uploads/{filename}"
            
            response = {
                'success': True,
                'prediction': ai_result, # Contains crop, disease, growth, treatment, contacts
                'weather': {
                    'data': weather_data,
                    'advice': weather_advice
                },
                'image_url': relative_image_path
            }

            return jsonify(response)

        except Exception as e:
            print(f" Error during prediction: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': 'Internal Server Error during analysis.'}), 500

@app.route('/weather_check', methods=['GET'])
def weather_check():
    """Helper route to check weather without uploading an image."""
    try:
        region = request.args.get('region', 'Kakamega')
        data = weather_service.get_current_weather(region)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the app
    print("UKULIMA SAFI  Server is Running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)