# Programmer: Nicholas Vuletich
# File name: imgsort.py
# Date: 01-18-2026

""" 
Image Sorter v2
Sorts images in a folder based on size, name, or date.
It also sorts on ascending or descending order.
The program will also tell the user if the image 
is blurry based on the Laplacian Variance if the user would like.
"""

import os
import datetime
import cv2

SCAN_EXTS = (
    ".jpg", ".jpeg", ".png", ".heic", ".heif",
    ".tiff", ".tif", ".webp", ".gif", ".bmp",
    ".arw", ".dng", ".nef", ".cr2", ".cr3", ".orf", ".rw2", ".raf")

BLUR_EXTS = (".jpg", ".jpeg", ".png")


#-----------------------FUNCTIONS-----------------------#

def print_order() -> None:
    """Prints sorting order options."""
    print("Sort in ascending (asc) or descending (desc) order? ")
    print("  asc: Name A → Z | Size Small → Large | Date Old → New")
    print("  desc: Name Z → A | Size Large → Small | Date New → Old")
    
def blur(files: list[dict], threshold: float = 100.0) -> list[dict]:
    """
    Detect blur using Laplacian variance.

    Returns:
        variance_list: list of dicts with variance and blur flag per image
    """
    variance_list = []

    for item in files:
        path = item.get("path")
        if not path:
            variance_list.append({
                "var" : None,
                "blur" : None
            })
            continue

        if not path.lower().endswith(BLUR_EXTS):
            variance_list.append({
                "var" : None,
                "blur" : None
            })
            continue

        photo = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        if photo is not None:
            variance = cv2.Laplacian(photo, cv2.CV_64F).var()
            is_blurry = variance < threshold
            variance_list.append({
                "var" : variance,
                "blur" : is_blurry
            })
        else:
            print(f"ERROR! Image could not be loaded: {path}")
            variance_list.append({
                "var" : None,
                "blur" : None
            })

    return variance_list


def file_info(folder_path: str) -> list[dict]:
    """Collects image file metadata (name, size (MB), date, timestamp) from a folder."""
    
    if not os.path.isdir(folder_path):
        print("Error: Folder path not found.")
        return []

    image_files = []

    for root, _, files in os.walk(folder_path):
        for name in files:
            if name.lower().endswith(SCAN_EXTS):
                full_path = os.path.join(root, name)

                try:
                    stat = os.stat(full_path)
                except OSError:
                    continue

                size_mb = stat.st_size / (1024 * 1024)
                timestamp = stat.st_mtime
                formatted_date = datetime.datetime.fromtimestamp(timestamp).strftime("%m/%d/%Y %H:%M:%S")

                image_files.append({
                "name": name,
                "path": full_path,
                "size": size_mb,
                "date": formatted_date,
                "timestamp" : timestamp
                })

    return image_files
    

def blur_print(files: list[dict], choice: str) -> None:
    """Prints sorted images with blur/sharpness info."""

    variances = blur(files)
    print()

    if choice in ("name", "size", "date"):
        print(f"Sorting by: {choice}")


    print()
    print(f"{'Name':<40} {'Sharpness':<10} {'Size (MB)':>12}    {'Date & Time'}")
    print('-' * 114)


    for item, blur_data in zip(files, variances):
        if blur_data["blur"] is None:
            status = "N/A"
        elif blur_data["blur"]:
            status = "blurry"
        else:
            status = "sharp"
        var_str = "N/A".rjust(8) if blur_data["var"] is None else f"{blur_data['var']:8.2f}"
        print(f"{item['name']:<40} {status:<10} {item['size']:>9.2f} MB"
              f"     {item['date']}    (Blur Variance: {var_str})")
        

def reg_print(files: list[dict], choice: str) -> None:
    """Prints sorted images without blur detection."""
    print()

    if choice in ("name", "size", "date"):
        print(f"Sorting by: {choice}")

    print()
    print(f"{'Name':<40} {'Size (MB)':>13}    {'Time'}")
    print('-' * 65)

    for img in files:
        print(f"{img['name']:<40}{img['size']:>10.2f} MB     {img['date']}")


def sort(image_files: list[dict], choice: str, sort_dec: str) -> list[dict]:
    """Sorts image files by name, size, or date in asc/desc order."""
    reverse = (sort_dec == "desc")

    if choice == "name":
        image_files.sort(key=lambda x: x["name"].lower(), reverse=reverse)
    elif choice == "size":
        image_files.sort(key=lambda x: x["size"], reverse=reverse)
    elif choice == "date": 
        image_files.sort(key=lambda x: x["timestamp"], reverse=reverse)
    else:
        print("Error:: Sort type not supported. Sorting by default sort: name")
        image_files.sort(key=lambda x: x["name"].lower(), reverse=reverse)

    return image_files


