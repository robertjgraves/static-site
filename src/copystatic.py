import os
import shutil

def copy_folder_recursive(source_folder, destination_folder):
    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        
        for item in os.listdir(source_folder):
            source_item_path = os.path.join(source_folder, item)
            destination_item_path = os.path.join(destination_folder, item)
    
            if os.path.isfile(source_item_path):
                shutil.copy2(source_item_path, destination_item_path)
            elif os.path.isdir(source_item_path):
                copy_folder_recursive(source_item_path, destination_item_path)
    
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_directory_contents(dir_path):
    try:
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    
    except FileNotFoundError:
        print(f"Directory '{dir_path} not found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
