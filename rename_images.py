import os

def force_rename_images():
    # --- CONFIGURATION ---
    # Path based on your screenshot: data -> crops_diseases -> images
    base_directory = os.path.join("data", "crops_diseases", "images")
    # ---------------------

    if not os.path.exists(base_directory):
        print(f"❌ Error: Directory not found: {base_directory}")
        return

    print(f"🚀 Starting rename process in: {base_directory}\n")

    # Walk through every subfolder
    for root, dirs, files in os.walk(base_directory):
        if root == base_directory:
            continue  # Skip the main 'images' folder, only do subfolders

        folder_name = os.path.basename(root)
        
        # Filter out system files like .DS_Store or Thumbs.db
        valid_files = [f for f in files if not f.startswith('.')]
        
        if not valid_files:
            print(f"⚠️  Skipping empty folder: {folder_name}")
            continue

        print(f"📂 Processing: {folder_name} ({len(valid_files)} files)")

        # Sort to keep order consistent
        valid_files.sort()

        # Step 1: Rename everything to a temporary unique name
        # This prevents "File already exists" errors if you run it twice
        temp_files = []
        for i, filename in enumerate(valid_files):
            old_path = os.path.join(root, filename)
            file_ext = os.path.splitext(filename)[1].lower() # Force lowercase extension
            
            # If no extension, assume .jpg (rare fix for bad datasets)
            if not file_ext:
                file_ext = ".jpg"

            temp_name = f"TEMP_RENAME_{i}{file_ext}"
            temp_path = os.path.join(root, temp_name)
            
            try:
                os.rename(old_path, temp_path)
                temp_files.append(temp_name)
            except Exception as e:
                print(f"   ❌ Error renaming {filename}: {e}")

        # Step 2: Rename temporary files to 1.jpg, 2.jpg...
        for i, temp_filename in enumerate(temp_files, start=1):
            temp_path = os.path.join(root, temp_filename)
            file_ext = os.path.splitext(temp_filename)[1]
            
            new_name = f"{i}{file_ext}"
            new_path = os.path.join(root, new_name)
            
            try:
                os.rename(temp_path, new_path)
            except Exception as e:
                print(f"   ❌ Error finalizing {new_name}: {e}")

    print("\n✅ Done! Check your folders now.")

if __name__ == "__main__":
    force_rename_images()