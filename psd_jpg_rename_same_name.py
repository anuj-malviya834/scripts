import os
import sys

def rename_psd_files(folder_path, base_name):
    """
    Rename all PSD and JPG files in a folder with format: base_name (n).psd
    
    Args:
        folder_path (str): Path to the folder containing PSD files
        base_name (str): Base name for renaming (e.g., "premium")
    """
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder '{folder_path}' does not exist!")
        return
    
    psd_files = []
    for file in os.listdir(folder_path):
        if file.lower().endswith('.psd'):
            psd_files.append(file)
    
    if not psd_files:
        print(f"❌ No PSD files found in '{folder_path}'")
        return
    
    print(f"📁 Found {len(psd_files)} PSD files in '{folder_path}'")
    print(f"🏷️  Renaming with base name: '{base_name}'")
    print("=" * 60)
    
    psd_files.sort()
    
    renamed_count = 0
    rename_mapping = []
    missing_jpgs = []
    
    for i, old_psd_filename in enumerate(psd_files, 1):
        # Create new filenames with format: base_name (n).psd
        new_psd_filename = f"{base_name} ({i}).psd"
        new_jpg_filename = f"{base_name} ({i}).jpg"
        
        # Get corresponding JPG filename
        old_jpg_filename = old_psd_filename.replace('.psd', '.jpg').replace('.PSD', '.jpg')
        
        # Full paths for PSD
        old_psd_path = os.path.join(folder_path, old_psd_filename)
        new_psd_path = os.path.join(folder_path, new_psd_filename)
        
        # Full paths for JPG
        old_jpg_path = os.path.join(folder_path, old_jpg_filename)
        new_jpg_path = os.path.join(folder_path, new_jpg_filename)
        
        # Check if new PSD filename already exists
        if os.path.exists(new_psd_path) and old_psd_path != new_psd_path:
            print(f"⚠️  Skipping: '{new_psd_filename}' already exists")
            continue
        
        # Skip if PSD is already the correct name
        if old_psd_filename == new_psd_filename:
            print(f"✅ Already correct: '{old_psd_filename}' → '{new_psd_filename}'")
            rename_mapping.append((old_psd_filename, new_psd_filename))
            continue
        
        try:
            # Rename the PSD file
            os.rename(old_psd_path, new_psd_path)
            print(f"✅ Renamed PSD: '{old_psd_filename}' → '{new_psd_filename}'")
            
            # Check if corresponding JPG exists and rename it
            if os.path.exists(old_jpg_path):
                # Check if new JPG filename already exists
                if os.path.exists(new_jpg_path) and old_jpg_path != new_jpg_path:
                    print(f"⚠️  JPG exists but target name taken: '{new_jpg_filename}'")
                elif old_jpg_filename != new_jpg_filename:
                    os.rename(old_jpg_path, new_jpg_path)
                    print(f"✅ Renamed JPG: '{old_jpg_filename}' → '{new_jpg_filename}'")
                else:
                    print(f"✅ JPG already correct: '{old_jpg_filename}'")
            else:
                missing_jpgs.append(old_jpg_filename)
                print(f"⚠️  Missing JPG: '{old_jpg_filename}' not found for '{old_psd_filename}'")
            
            rename_mapping.append((old_psd_filename, new_psd_filename))
            renamed_count += 1
            
        except Exception as e:
            print(f"❌ Error renaming '{old_psd_filename}': {e}")
    
    print("=" * 60)
    print(f"🎉 Successfully renamed {renamed_count} PSD files!")
    
    # Print missing JPGs summary
    if missing_jpgs:
        print(f"\n⚠️  MISSING JPG FILES ({len(missing_jpgs)}):")
        print("-" * 40)
        for missing_jpg in missing_jpgs:
            print(f"❌ {missing_jpg}")
    else:
        print(f"\n✅ All JPG files found and renamed!")
    
    # Print mapping for CSV update
    print("\n📋 MAPPING FOR CSV UPDATE:")
    print("Old Name → New Name")
    print("-" * 40)
    for old_name, new_name in rename_mapping:
        # Remove .psd extension for CSV
        old_base = old_name.replace('.psd', '')
        new_base = new_name.replace('.psd', '')
        print(f"{old_base} → {new_base}")
    
    return rename_mapping

def main():
    print("🔄 PSD File Renamer")
    print("=" * 30)

    folder_path = r"C:\Users\HP\AppData\Roaming\albumai\templates\stylish psd"
    base_name = "stylish psd"

    if not folder_path or not base_name:
        print("❌ Both folder path and base name are required!")
        return

    print(f"\n📋 SUMMARY:")
    print(f"Folder: {folder_path}")
    print(f"Base name: {base_name}")

    confirm = input("\n❓ Proceed with renaming? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ Operation cancelled.")
        return

    rename_psd_files(folder_path, base_name)

if __name__ == "__main__":
    main()
