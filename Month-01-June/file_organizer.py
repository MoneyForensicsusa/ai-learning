import os
import shutil
def organize_folder(folder_path):
    files = os.listdir(folder_path)
    moved = 0

    type_map = {
        ".txt": "text_files",
        ".py": "python_files",
        ".csv": "data_files",
        ".jpg": "images",
        ".png": "images"
    }

    for filename in files:
        ext = os.path.splitext(filename)[1].lower()
        if ext not in type_map:
            continue
        dest = os.path.join(folder_path, type_map[ext])
        os.makedirs(dest, exist_ok=True)
        src = os.path.join(folder_path, filename)
        shutil.move(src, dest)
        moved += 1
    
    print(f"Done. Moved {moved} files.")

organize_folder("test_folder")



