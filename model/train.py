# UKULIMA SAFI AI
# Architected by DELSTARFORD WORKS.CO.KE
# Script: Professional Model Training

import os
import json
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from preprocess import get_disease_data_generators, get_growth_data_generators

# --- CONFIGURATION ---
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
EPOCHS = 20                # Higher epochs, but EarlyStopping will stop it when ready
LEARNING_RATE = 0.0001
IMG_SHAPE = (224, 224, 3)

def build_model(num_classes):
    """
    Builds a professional Transfer Learning model using MobileNetV2.
    """
    # 1. Load Base Model (MobileNetV2)
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=IMG_SHAPE)
    
    # 2. Freeze base model to keep pre-trained ImageNet knowledge
    base_model.trainable = False 

    # 3. Add Custom Head for our specific task
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x) # Increased density for better feature mapping
    x = Dropout(0.4)(x)                 # Higher dropout to prevent overfitting
    predictions = Dense(num_classes, activation='softmax')(x)

    # 4. Compile
    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer=Adam(learning_rate=LEARNING_RATE), 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
    return model

def save_class_indices(generator, filename):
    """Saves the map of '0' -> 'Tomato___Early_blight' to a JSON file."""
    class_indices = generator.class_indices
    # Invert to: {0: "Tomat4o___Early_blight", ...}
    labels = {v: k for k, v in class_indices.items()}
    
    save_path = os.path.join(MODEL_DIR, filename)
    with open(save_path, 'w') as f:
        json.dump(labels, f)
    print(f"   📄 Saved class indices to: {filename}")

def train_task(task_name, generator_func, model_filename, indices_filename):
    """
    Generic function to train any model (Disease or Growth) with professional callbacks.
    """
    print(f"\n🚀 --- Starting Training: {task_name} ---")
    
    try:
        # 1. Get Data
        train_gen, val_gen = generator_func()
        num_classes = len(train_gen.class_indices)
        print(f"   📊 Found {num_classes} classes for {task_name}.")

        # 2. Build Model
        model = build_model(num_classes)
        
        # 3. Define Professional Callbacks
        model_path = os.path.join(MODEL_DIR, model_filename)
        
        callbacks = [
            # Save the model ONLY when validation accuracy improves (Best Version)
            ModelCheckpoint(model_path, monitor='val_accuracy', save_best_only=True, verbose=1),
            
            # Stop training if validation loss doesn't improve for 5 epochs (Saves time)
            EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1),
            
            # Reduce learning rate if accuracy gets stuck (Fine-tuning)
            ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6, verbose=1)
        ]

        # 4. Train
        history = model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=EPOCHS,
            callbacks=callbacks
        )

        # 5. Save Labels
        save_class_indices(train_gen, indices_filename)
        print(f"✅ Success! Best {task_name} model saved to: {model_path}")

    except Exception as e:
        print(f"❌ Error training {task_name}: {e}")
        # Hint: Usually happens if data folders are empty or paths are wrong
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 1. Train Disease Detection Model
    train_task(
        task_name="Disease Detection",
        generator_func=get_disease_data_generators,
        model_filename="disease_model.h5",
        indices_filename="disease_indices.json"
    )

    # 2. Train Growth Stage Model
    train_task(
        task_name="Growth Stage Detection",
        generator_func=get_growth_data_generators,
        model_filename="growth_model.h5",
        indices_filename="growth_indices.json"
    )