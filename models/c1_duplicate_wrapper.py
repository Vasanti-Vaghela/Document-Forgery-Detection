import cv2
from duplicate_model import (
    load_image,
    preprocess_image,
    extract_regions,
    find_duplicate_regions
)

def run_c1(image_path):

    try:
        img = load_image(image_path)
    except:
        return [], None

    gray, thresh = preprocess_image(img)

    regions = extract_regions(thresh)

    duplicates = find_duplicate_regions(gray, regions)

    results = []

    for (x, y, w, h) in duplicates:
        results.append({
            "bbox": [x, y, w, h],
            "features": {"duplicate": True}
        })

    return results, img