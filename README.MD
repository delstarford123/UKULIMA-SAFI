UKULIMA SAFI AI

UKULIMA SAFI AI is an advanced agricultural intelligence system designed to empower farmers with real-time crop diagnostics, treatment advice, and expert connections.

Using deep learning (CNNs) and location-based services, it acts as a digital agronomist—detecting diseases, analyzing growth stages, checking weather conditions, and guiding farmers to the nearest help.

Key Features

AI Disease Detection: Instantly identifies crop diseases (Blights, Rusts, Spots) from a simple photo.

Growth Stage Analysis: Determines if a crop is in Seedling, Vegetative, or Fruiting stage to tailor advice.

Smart Treatment Logic: Prescribes specific insecticides and fungicides based on the exact disease found.

Weather Integration: Connects to OpenWeatherMap to advise on spraying conditions (e.g., "Don't spray, rain expected").

GPS Expert Guide: Uses Geolocation to direct farmers to the nearest registered Agrovets and Agronomists via Google Maps.

Offline Capable: The AI brain and contact databases work fully offline (only Weather/Maps require internet).

System Architecture

The project is structured for modularity and scalability:

UKULIMA SAFI AI/
│
├── main.py                  # ENTRY POINT: Flask Server & Logic Coordinator
├── requirements.txt         # List of all dependencies
├── README.md                # Documentation
├── .env                     # API Keys (Weather)
│
├── model/                   # THE BRAIN (AI & Logic)
│   ├── train.py             # Script to train the AI models (MobileNetV2)
│   ├── preprocess.py        # Data loading & augmentation logic
│   ├── predict.py           # Core inference engine (Prediction + Advice)
│   ├── geolocation.py       # GPS & Navigation logic
│   ├── disease_model.h5     # Trained Disease Model
│   ├── growth_model.h5      # Trained Growth Model
│   └── *.json               # Class index mappings
│
├── weather_api/             # ☁️ WEATHER MODULE
│   ├── weather.py           # OpenWeatherMap API Connector
│   └── weather_crop_logics.py # Agricultural logic based on weather data
│
├── data/                    # 💾 DATABASE (CSV & Images)
│   ├── crops_diseases/      # Training images for diseases
│   ├── crops_growth_stage/  # Training images for growth stages
│   ├── disease_treatment/   # CSVs: insecticides, pesticides, timing
│   ├── agrovets_and_agronomists/ # CSVs: Contact details & locations
│   └── crops/               # General crop info
│
├── static/                  # 🎨 FRONTEND ASSETS
│   ├── css/                 # Styles (Maroon & Green Theme)
│   ├── js/                  # Interactivity (GPS, Uploads)
│   └── uploads/             # Temp folder for user images
│
└── templates/               # 📄 HTML VIEWS
    ├── home.html            # Landing Page
    ├── dashboard.html       # Main AI Tool
    ├── gps_guide.html       # Location Finder
    └── ... (other pages)


🛠️ Installation Guide

Follow these steps to set up the project locally.

1. Prerequisites

Python 3.9 or higher

pip (Python Package Manager)

2. Clone & Setup

# Clone the repository (if using git) or download the folder
cd "UKULIMA SAFI AI"

# Create a Virtual Environment (Recommended)
python -m venv .venv

# Activate it:
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt


4. Configure API Keys

Create a file named .env in the root folder and add your OpenWeatherMap key:

OPENWEATHER_API_KEY=your_api_key_here


 Usage

1. Train the AI (First Run Only)

If you haven't trained the models yet, run this command. It uses Transfer Learning (MobileNetV2) to train on your data in data/crops_diseases.

python model/train.py


Wait until you see  Success! Best Disease Detection model saved.

2. Run the Application

Start the Flask server:

python main.py


3. Access the Dashboard

Open your web browser and go to:
 https://www.google.com/search?q=http://127.0.0.1:5000

User Interface (Theme)

The application uses a Maroon & Green color scheme to symbolize:

Maroon: Earth, Soil, and Trusted Expertise.

Green: Growth, Crops, and Vitality.

Main Dashboard

Upload: Select a crop image.

Region: Enter your location (defaults to "Kakamega").

Analyze: Click the button to run the AI.

The results will show:

Diagnosis: (e.g., Tomato Early Blight)

Treatment: (e.g., Ridomil Gold)

Weather Advice: (e.g., High humidity detected, avoid spraying now.)

Nearest Help: A list of Agrovets with "Get Directions" buttons.

 How the AI Works

Input: The user uploads an image.

Preprocessing: The image is resized to 224x224 pixels and normalized (preprocess.py).

Inference:

Model A (disease_model.h5) predicts the disease class.

Model B (growth_model.h5) predicts the growth stage.

Logic Layer: predict.py takes the predicted class (e.g., "Tomato_Blight") and queries the CSV database in data/disease_treatment/ to find the matching chemical recommendations.

Contextual Layer: It cross-references the user's GPS with agrovets_region.csv to find local experts.

 Contributing

Contributions are welcome! Please follow these steps:

Fork the repository.

Create a feature branch (git checkout -b feature/NewFeature).

Commit your changes.

Push to the branch.

Open a Pull Request.

License & Credits

Architected by: DELSTARFORD WORKS.CO.KE



Location: Kakamega, Kenya


The UKULIMA SAFI ,is an AI model that does the disease setection on crops ,the stage of growth of the crop,the disease affecting the crop by that time ,the stage of effect and how to help the plant.Then after the detection process the AI gives the nearest agrovet and the nearest agronomist to him for advice and solution.

The AI as static folder with css subfolder with css.style, it also have js subfolder with main.js for all the javascript codes for the project, it also has a base.html for the footer and Header, and the navigation bar that should be in all the pages and professional it works.

The data folder with the subfolders with every data.

The models folder with the scripts for the AI Model eg train.py,preprocess.py and predict.py

The templates folder have all the html pages,using the externall CSS and JS

The weather_api folder holds the weather brain for the AI model ,so that it can advice with the knowledge of weather and the parameters on weather to give a better prediction and guide accordingly. It has the weather_crop_logics.py file with the rules to follow when giving the responses and predictions based on the weather. It has the weather.py file with the access to the open weather api for that and how it is to give it.

The UKULIMA SAFI , Is achitected by DELSTARFORD WORKS.CO.KE