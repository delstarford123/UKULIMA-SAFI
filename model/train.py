# UKULIMA SAFI AI
# Architected by DELSTARFORD WORKS.CO.KE
# Script: Professional Model Training with Active Learning

import os
import json
import shutil # <--- Added for moving files
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# Handle imports safely
try:
    from model.preprocess import get_disease_data_generators, get_growth_data_generators
except ImportError:
    from preprocess import get_disease_data_generators, get_growth_data_generators

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data') # Points to /data
EPOCHS = 20
LEARNING_RATE = 0.0001
IMG_SHAPE = (224, 224, 3)

def merge_verified_data():
    """
    ACTIVE LEARNING LOGIC:
    Checks the 'retrain_dataset' folder for any images verified by experts.
    Moves them into the main 'crops_diseases' folder so the model learns from them.
    """
    print("\n🔄 Checking for new expert-verified data...")
    
    retrain_source = os.path.join(DATA_DIR, 'retrain_dataset')
    training_dest = os.path.join(DATA_DIR, 'crops_diseases', 'images')
    
    if not os.path.exists(retrain_source):
        print("   No new data found (folder does not exist).")
        return

    count = 0
    # Walk through the retrain folder
    for root, dirs, files in os.walk(retrain_source):
        for file in files:
            if file.endswith(('jpg', 'jpeg', 'png')):
                # 1. Identify Source File
                src_path = os.path.join(root, file)
                
                # 2. Identify Class Name (Folder Name)
                # Structure is retrain_dataset/Tomato___Blight/img.jpg
                class_name = os.path.basename(root)
                
                # 3. Create Destination Path
                dest_folder = os.path.join(training_dest, class_name)
                os.makedirs(dest_folder, exist_ok=True)
                dest_path = os.path.join(dest_folder, file)
                
                # 4. Move the file
                try:
                    shutil.move(src_path, dest_path)
                    count += 1
                except Exception as e:
                    print(f"   Error moving {file}: {e}")

    if count > 0:
        print(f"   ✅ Merged {count} new verified images into the training set!")
    else:
        print("   No new images to merge.")

def build_model(num_classes):
    """Builds a professional Transfer Learning model using MobileNetV2."""
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=IMG_SHAPE)
    base_model.trainable = False 

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.4)(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer=Adam(learning_rate=LEARNING_RATE), 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
    return model

def save_class_indices(generator, filename):
    class_indices = generator.class_indices
    labels = {v: k for k, v in class_indices.items()}
    save_path = os.path.join(BASE_DIR, filename)
    with open(save_path, 'w') as f:
        json.dump(labels, f)
    print(f"   📄 Saved class indices to: {filename}")

def train_task(task_name, generator_func, model_filename, indices_filename):
    print(f"\n🚀 --- Starting Training: {task_name} ---")
    
    try:
        train_gen, val_gen = generator_func()
        
        if not train_gen:
            print("   ❌ No data found. Skipping.")
            return

        num_classes = len(train_gen.class_indices)
        print(f"   📊 Found {num_classes} classes for {task_name}.")

        model = build_model(num_classes)
        model_path = os.path.join(BASE_DIR, model_filename)
        
        callbacks = [
            ModelCheckpoint(model_path, monitor='val_accuracy', save_best_only=True, verbose=1),
            EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1),
            ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6, verbose=1)
        ]

        model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=EPOCHS,
            callbacks=callbacks
        )

        save_class_indices(train_gen, indices_filename)
        print(f"✅ Success! Best {task_name} model saved to: {model_path}")

    except Exception as e:
        print(f"❌ Error training {task_name}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # --- STEP 1: MERGE NEW DATA FIRST ---
    # This ensures the model learns from the expert inputs
    merge_verified_data()

    # --- STEP 2: TRAIN MODELS ---
    train_task(
        task_name="Disease Detection",
        generator_func=get_disease_data_generators,
        model_filename="disease_model.h5",
        indices_filename="disease_indices.json"
    )

    train_task(
        task_name="Growth Stage Detection",
        generator_func=get_growth_data_generators,
        model_filename="growth_model.h5",
        indices_filename="growth_indices.json"
    )