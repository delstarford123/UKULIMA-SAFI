# UKULIMA SAFI AI
# Architected by DELSTARFORD WORKS.CO.KE
# Script: Preprocessing and Data Loading

import os
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Points to root
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Image Parameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

def get_disease_data_generators():
    """
    Creates generators for the Disease Dataset (Folder-based structure).
    """
    disease_dir = os.path.join(DATA_DIR, 'crops_diseases', 'images')
    
    if not os.path.exists(disease_dir):
        print(f"❌ Error: Disease directory missing at {disease_dir}")
        return None, None

    # Augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2 
    )

    print(f"   📂 Loading Disease Data from: {disease_dir}")
    train_gen = train_datagen.flow_from_directory(
        disease_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val_gen = train_datagen.flow_from_directory(
        disease_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    return train_gen, val_gen

def get_growth_data_generators():
    """
    Creates generators for the Growth Stage Dataset (CSV-based structure).
    """
    growth_dir = os.path.join(DATA_DIR, 'crops_growth_stage', 'images')
    csv_path = os.path.join(growth_dir, 'growth_stage_images.csv')

    if not os.path.exists(csv_path):
        print(f"❌ Error: Growth CSV missing at {csv_path}")
        return None, None

    # Load CSV
    df = pd.read_csv(csv_path)
    
    # Ensure image paths in CSV match local filenames
    # This strips any extra paths and keeps just "Tomato_seedling.jpg"
    df['filename'] = df['image'].apply(lambda x: os.path.basename(x))

    # --- DEBUG: CHECK FOR MISSING FILES ---
    # This helps you solve the "13 invalid images" warning
    missing_files = []
    for filename in df['filename']:
        full_path = os.path.join(growth_dir, filename)
        if not os.path.exists(full_path):
            missing_files.append(filename)
            
    if missing_files:
        print(f"   ⚠️  WARNING: {len(missing_files)} images listed in CSV are missing from folder!")
        # Print first 3 missing to help debug
        print(f"      Missing examples: {missing_files[:3]}")

    print(f"   📂 Loading Growth Data from CSV: {csv_path}")
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    try:
        train_gen = train_datagen.flow_from_dataframe(
            dataframe=df,
            directory=growth_dir,
            x_col="filename",
            y_col="growth_stage",
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='training'
        )

        val_gen = train_datagen.flow_from_dataframe(
            dataframe=df,
            directory=growth_dir,
            x_col="filename",
            y_col="growth_stage",
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='validation'
        )
        return train_gen, val_gen

    except Exception as e:
        print(f"❌ Error creating growth generator: {e}")
        return None, None

def load_treatment_data():
    """Loads treatment CSVs into a dictionary."""
    treatment_dir = os.path.join(DATA_DIR, 'disease_treatment')
    data = {}
    
    try: data['insecticides'] = pd.read_csv(os.path.join(treatment_dir, 'insecticides', 'insecticides.csv'))
    except: data['insecticides'] = pd.DataFrame()

    try: data['pesticides'] = pd.read_csv(os.path.join(treatment_dir, 'pesticides', 'pesticides.csv'))
    except: data['pesticides'] = pd.DataFrame()

    try: data['advice'] = pd.read_csv(os.path.join(treatment_dir, 'treatment_time', 'treatment.csv'))
    except: data['advice'] = pd.DataFrame()

    return data

def load_contact_data():
    """Loads Agrovets and Agronomists data."""
    contact_dir = os.path.join(DATA_DIR, 'agrovets_and_agronomists')
    data = {}

    try:
        path = os.path.join(contact_dir, 'agrovets_region.csv')
        if os.path.exists(path):
            data['agrovets'] = pd.read_csv(path)
            data['agrovets'].columns = data['agrovets'].columns.str.strip()
        else: data['agrovets'] = pd.DataFrame()
    except: data['agrovets'] = pd.DataFrame()

    try:
        path = os.path.join(contact_dir, 'agronomist_region.csv')
        if os.path.exists(path):
            data['agronomists'] = pd.read_csv(path)
            data['agronomists'].columns = data['agronomists'].columns.str.strip()
        else: data['agronomists'] = pd.DataFrame()
    except: data['agronomists'] = pd.DataFrame()

    return data

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("\n🔬 --- TESTING DATA LOADING ---")
    
    # Test 1: Disease Images
    print("\n1. Testing Disease Generators...")
    d_train, d_val = get_disease_data_generators()
    if d_train:
        # Note: DirectoryIterator has 'num_classes'
        print(f"   ✅ Disease Data: Found {d_train.samples} training images belonging to {d_train.num_classes} classes.")

    # Test 2: Growth Images
    print("\n2. Testing Growth Generators...")
    g_train, g_val = get_growth_data_generators()
    if g_train:
        # Note: DataFrameIterator does NOT have 'num_classes'. We use len(class_indices) instead.
        num_growth_classes = len(g_train.class_indices)
        print(f"   ✅ Growth Data: Found {g_train.samples} training images belonging to {num_growth_classes} classes.")

    # Test 3: Contacts
    print("\n3. Testing Contact Data...")
    contacts = load_contact_data()
    print(f"   ✅ Agrovets Loaded: {len(contacts['agrovets'])} entries")
    print(f"   ✅ Agronomists Loaded: {len(contacts['agronomists'])} entries")

    print("\n✨ Preprocessing Check Complete!")