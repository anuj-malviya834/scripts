import os
import shutil

# === CONFIG ===
MAIN_FOLDER = r"C:\Users\HP\Downloads\psd"  # replace with your main folder path

def flatten_psd_folders(main_folder):
    for root, dirs, files in os.walk(main_folder, topdown=False):
        # Ignore the main folder itself
        if root == main_folder:
            continue

        for file in files:
            if file.lower().endswith(".psd"):     # if you want all file then replace (if file.lower().endswith(".psd"):) with (if True:)
                source = os.path.join(root, file)
                destination = os.path.join(main_folder, file)

                # If same name PSD exists, rename to avoid overwrite
                if os.path.exists(destination):
                    base, ext = os.path.splitext(file)
                    count = 1
                    while os.path.exists(os.path.join(main_folder, f"{base}_{count}{ext}")):
                        count += 1
                    destination = os.path.join(main_folder, f"{base}_{count}{ext}")

                print(f"Moving: {source} → {destination}")
                shutil.move(source, destination)

        # After moving, delete the empty folder
        if not os.listdir(root):
            os.rmdir(root)
            print(f"Deleted empty folder: {root}")

if __name__ == "__main__":
    flatten_psd_folders(MAIN_FOLDER)
