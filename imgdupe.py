# Date: 01-18-2026
# File: imgdupe.py
# Programmer: Nicholas M. Vuletich

import os
import json
import hashlib

"""
    Duplicate media finder (v2).

    Scans a folder including subfolders, hashes media files and detects duplicates
    based on matching hashes. Writes duplicates to store.json and prints total space
    that could be freed.
"""

#---------------Helper Functions---------------

def file_binary(file_path: str) -> bytes:
    """Reads a file as bytes for hashing."""
    with open (file_path, "rb") as bf:
        return bf.read()
    
def write_json(target_list: list[dict]) -> None:
    """Writes duplicates list to store.json."""
    with open("store.json", "w", encoding="utf-8") as f:
        json.dump(target_list, f, indent=4)

def get_extensions(choice: str) -> tuple[str, ...]:
    videos = ('.mp4', '.mov')
    photos = ('.jpg', '.png' , '.jpeg', '.heic', '.heif', '.arw', '.dng', '.nef',
              '.tiff', '.tif', '.webp', '.gif', '.bmp', '.cr2', '.cr3', '.orf', '.rw2', '.raf')
    
    if choice == "1":
        return videos
    elif choice == "2":
        return photos
    elif choice == "3":
        return videos + photos
    else:
        return photos # default media type
    
    
#---------------Main functions---------------

def make_list(folder_path: str, extensions: tuple[str, ...]) -> tuple[list[dict], list[dict]]:
    """
    Scans a single directory and collects the supported media files.
    Returns both files metadata and a list of subdirectories.
    """
    media_files = []
    folders = []

    for entry in os.scandir(folder_path):
        if entry.name.startswith('.'):
            continue
            
        if entry.is_file() and entry.name.lower().endswith(extensions):
            path = os.path.normpath(entry.path)
            size_mb = entry.stat().st_size / (1024 * 1024)
            file_hash = hashlib.md5(file_binary(entry.path)).hexdigest()

            media_files.append({
                "name": entry.name,
                "path": path,
                "size_mb": size_mb,
                "hash": file_hash

            })
        
        if entry.is_dir():
            dir_path = os.path.normpath(entry.path)
            folders.append({
                "dir": entry.name,
                "dir_path": dir_path
            })

    return media_files, folders
    

def sub_dir_files(folder: str, extensions: tuple[str, ...]) -> tuple[list[dict], list[dict]]:
    """
    Recursively scans a directory by expanding the folder list
    as new subdirectories are discovered.
    """
    master_media = []
    master_folders = []

    media_files, folders= make_list(folder, extensions)
    master_media.extend(media_files)
    master_folders.extend(folders)

    for subdir in master_folders:
        sub_media, sub_folders= make_list(subdir["dir_path"], extensions)
        master_media.extend(sub_media)
        master_folders.extend(sub_folders)
    
    return master_media, master_folders

def compare(path: str) -> None:
    """
    Finds duplicate files in a directory tree using file hashes.
    Outputs total reclaimable size and writes duplicates to JSON.
    """
    print("Running Compare...")
    print("Scanning Path", path)

    if not os.path.isdir(path):
        print("Error: Folder path not found.")
        return

    user_input = input("Choose a media to compare: (1) Video  (2) Photo  (3) Video + Photo: ").strip()
    exts = get_extensions(user_input)
    master_list, _ = sub_dir_files(path, exts)

    seen_hashes = set()
    duplicates = []
    total_size_mb = 0.0

    for item in master_list:
        if item["hash"] in seen_hashes:
            total_size_mb += item["size_mb"]
            duplicates.append(item)
        else:
            seen_hashes.add(item["hash"])

    
    print(f"Total size that can be freed is {total_size_mb:.2f} MB.")
    print(f"Found {len(master_list)} files to scan.")
    print(f"Duplicates found: {len(duplicates)}")

    write_json(duplicates)
