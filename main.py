import os
import hashlib
import argparse


def calculate_file_hash(file_path):
    # Calculate the file's hash
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicate_files_in_folders(folder_paths):
    # Dictionary to store file sizes and their content hashes
    file_info = {}
    duplicates = []

    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_size = os.path.getsize(file_path)
                file_hash = calculate_file_hash(file_path)

                # Check if the file size and hash already exist in the dictionary
                if (file_size, file_hash) in file_info:
                    duplicates.append((file_path, file_info[(file_size, file_hash)]))
                else:
                    file_info[(file_size, file_hash)] = file_path

    return duplicates


def delete_duplicate_files_with_prompt(duplicates):
    for duplicate in duplicates:
        file1, file2 = duplicate
        print(f"Duplicate files found:")
        print(f"File 1: {file1}")
        print(f"File 2: {file2}")

        user_input = input(
            "Both files are potential duplicates. Do you want to delete one of them? (yes/no): ").strip().lower()
        if user_input == "yes":
            file_to_delete = file1  # Change this based on your preference
            os.remove(file_to_delete)
            print(f"Deleted: {file_to_delete}")
        else:
            print("No action taken.")
        print("")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find and delete potential duplicate files.")
    parser.add_argument('folder_paths', nargs='+', help="List of folder paths to check for potential duplicates.")
    args = parser.parse_args()

    folder_paths = args.folder_paths
    duplicates = find_duplicate_files_in_folders(folder_paths)

    if duplicates:
        print("Found the following potential duplicate files:")
        delete_duplicate_files_with_prompt(duplicates)
    else:
        print("No potential duplicate files found.")
