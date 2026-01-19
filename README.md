# Nick's Photo Toolbox
This is a Python-based command-line toolkit that is used for organizing and analyzing large photo and media folders.

I built this to solve a problem I run into a lot as a photographer. The problem of managing folders full of images, spotting duplicates, and trying to see which photos are actually usable is a big one for me. 

This project is both a practical tool and an evolving learning project. It reflects my approach of learning by building real, usable software. 

---

## Features

### Image Sorter
- Recursively scans folders and subfolders
- Sorts images by:
    - Name
    - File size
    - Date modified
- Supports ascending or descending order
- Optional blur detection using Laplacian variance
- Clean, readable CLI output
- Handles common image and raw formats

### Duplicate Finder
- Recursively scans directories
- Detects duplicate media using hashing
- Supports:
    - Photos only
    - Videos only
    - Photos + Videos
- Reports:
    - Total files scanned
    - Duplicate count
    - Potential storage savings
- Outputs duplicate metadata to `store.json`

---

## Design Idea
- Modular architecture (each tool lives in its own file)
- Clear separation between:
    - File scanning
    - Processing logic
    - CLI interaction
- Explicit type hints for readability and maintainability
- CLI output designed to be readable, not just functional

This repo reflects how I approach building tools. I solve a real world problem first, then refine the structure and clarity afterward.

---

## How to run
1. Run `python main.py` in the terminal
2. Enter a folder path
3. Follow the prompts in the terminal

---

## Technologies Used
- Python
- OpenCV (`cv2`)
- File system traversal (`os.walk`, `os.scandir`)
- Hashing (`hashlib`)
- JSON output

---

## Future Improvements
- Image preview or auto move/delete options
- Packaging as an installable CLI tool
- Add more tools

---

## Example Outputs

### Sort

``` text
Enter the folder path to scan. (ex. /Users/john/Desktop/Photos): /Users/nick/Documents/nicks-photo-toolbox/media
Choose a tool: (1) Sort images  (2) Find duplicates: 1
What would you like to sort by: 'name', 'size', 'date': size
Do you want to know if the image is blurry or not: 'yes', 'no': yes
Sort in ascending (asc) or descending (desc) order? 
  asc: Name A → Z | Size Small → Large | Date Old → New
  desc: Name Z → A | Size Large → Small | Date New → Old
Enter 'asc' or 'desc': asc

Sorting by: size

Name                                     Sharpness     Size (MB)    Date & Time
------------------------------------------------------------------------------------------------------------------
animals-10008941_1920.jpg                sharp           0.19 MB     01/18/2026 20:32:17    (Blur Variance:   225.11)
piano-10046998_1920.jpg                  sharp           0.28 MB     01/18/2026 20:33:00    (Blur Variance:   214.91)
lantern-8818968_1920.jpg                 sharp           0.30 MB     01/18/2026 20:32:17    (Blur Variance:   137.54)
lantern-8818968_1920.jpg                 sharp           0.30 MB     01/18/2026 20:32:33    (Blur Variance:   137.54)
giant-panda-10039235_1920.jpg            sharp           0.44 MB     01/18/2026 20:32:17    (Blur Variance:   991.71)
giant-panda-10039235_1920.jpg            sharp           0.44 MB     01/18/2026 20:32:33    (Blur Variance:   991.71)

```
### Duplicate finder - CLI output

``` text
Enter the folder path to scan. (ex. /Users/john/Desktop/Photos): /Users/nick/Documents/nicks-photo-toolbox/media
Choose a tool: (1) Sort images  (2) Find duplicates: 2
Running Compare...
Scanning Path /Users/nick/Documents/nicks-photo-toolbox/media
Choose a media to compare: (1) Video  (2) Photo  (3) Video + Photo: 3
Total size that can be freed is 0.74 MB.
Found 7 files to scan.
Duplicates found: 2
Total time elapsed 2.63.
Done running!!!
```
### Duplicate finder - store.json
``` text
[
    {
        "name": "giant-panda-10039235_1920.jpg",
        "path": "/Users/nick/Documents/nicks-photo-toolbox/media/sub-media/giant-panda-10039235_1920.jpg",
        "size_mb": 0.44065189361572266,
        "hash": "c98fe1246a6c73f0b6f9d470f4c9019b"
    },
    {
        "name": "lantern-8818968_1920.jpg",
        "path": "/Users/nick/Documents/nicks-photo-toolbox/media/sub-media/lantern-8818968_1920.jpg",
        "size_mb": 0.29710865020751953,
        "hash": "7a8ac51c21b2e7e25b843770e99eaab9"
    }
]
```
---

## Author
### Nicholas M. Vuletich
Computer Science student | Photographer | Builder

