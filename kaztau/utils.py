import os
from typing import List


def get_all_path_file_from_folder(path: str) -> List[str]:
    images = []
    valid_images = [".jpg", ".jpeg", ".JPG", ".JPEG", ".gif", ".png"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        images.append(os.path.join(path, f))
    return images
