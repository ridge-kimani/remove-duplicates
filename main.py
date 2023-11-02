import os
import hashlib
import argparse


def find_duplicate_files_in_folders(folder_paths):
    file_hashes = {}
    duplicates = []

    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                with open(file_path, 'rb') as file:
                    file_hash = hashlib.md5(file.read()).hexdigest()
                if file_hash in file_hashes:
                    duplicates.append((file_path, file_hashes[file_hash]))
                else:
                    file_hashes[file_hash] = file_path

    return duplicates


def delete_duplicate_files(duplicates):
    for duplicate in duplicates:
        file_to_delete, original_file = duplicate
        print(f"Deleting duplicate file: {file_to_delete}")
        os.remove(file_to_delete)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find and delete duplicate files.")
    parser.add_argument('folder_paths', nargs='+', help="List of folder paths to check for duplicates.")
    args = parser.parse_args()

    paths = args.folder_paths
    duplicate_files = find_duplicate_files_in_folders(paths)

    if duplicate_files:
        print("Found the following duplicate files:")
        for duplicate_file in duplicate_files:
            print(f"{duplicate_file[0]} (duplicate of {duplicate_file[1]})")
        delete_duplicate_files(duplicate_files)
    else:
        print("No duplicate files found.")
