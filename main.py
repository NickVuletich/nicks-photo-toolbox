# Date: 01-12-26
# File: main.py
# Programmer: Nicholas M. Vuletich

import imgdupe
import imgsort
import time
import os


def program_picker(tool_choice: str, path: str) -> None:
    """Routes user to the selected tool."""
    if tool_choice == '1':
        img_sort(path)
    
    elif tool_choice == '2':
        img_dupe(path)
    else:
        print("Invalid input!!! Quitting...")
        return

def img_sort(folder_path: str) -> None:
    """Runs the image sorting tool."""
    choice = input("What would you like to sort by: 'name', 'size', 'date': ").strip().lower()

    if choice not in ("name", "size", "date"):
        print("Not a valid sort type. Defaulting to 'name'.")
        choice = "name"

    blur_choice = input("Do you want to know if the image is blurry or not: 'yes', 'no': ").strip().lower()

    if blur_choice not in ("yes", "no"):
        print("Not a valid input. Defaulting to 'no'.")
        blur_choice = "no"

    imgsort.print_order()
    sort_dec = input("Enter 'asc' or 'desc': ").strip().lower()

    if sort_dec not in ("asc", "desc"):
        print("Not a valid sort order. Defaulting to 'asc'.")
        sort_dec = "asc"

    print(f"Scanning Path {folder_path}")


    image_files = imgsort.file_info(folder_path)
    image_files = imgsort.sort(image_files, choice, sort_dec)

    if blur_choice == "yes":
        imgsort.blur_print(image_files, choice)
    elif blur_choice == "no":
        imgsort.reg_print(image_files, choice)

def img_dupe(folder_path: str) -> None:
    """Runs the image duplicate finder tool."""
    start_time = time.time()
    imgdupe.compare(folder_path)
    elapsed = time.time() - start_time
    print(f"Total time elapsed {elapsed:.2f}.")
    print("Done running!!!")

def main() -> None:

    path_choice = input("Enter the folder path to scan. (ex. /Users/john/Desktop/Photos): ").strip()

    if not os.path.isdir(path_choice):
        print("Error: Folder path not found. Quitting...")
        return

    choice_1 = input("Choose a tool: (1) Sort images  (2) Find duplicates: ").strip()

    program_picker(choice_1, path_choice)



if __name__ == "__main__":
    main()