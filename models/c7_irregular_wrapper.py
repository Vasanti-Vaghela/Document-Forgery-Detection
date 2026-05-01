import cv2
from irregular_spacing import (
    load_image,
    preprocess_image,
    get_valid_boxes,
    group_into_lines,
    detect_suspicious_spaces
)

def run_c7(image_path):

    try:
        img = load_image(image_path)
    except:
        return [], None

    processed = preprocess_image(img)
    boxes = get_valid_boxes(processed)
    lines = group_into_lines(boxes)
    suspicious = detect_suspicious_spaces(lines)

    results = []

    for (x, y, w, h) in suspicious:
        results.append({
            "bbox": [x, y, w, h],
            "features": {"spacing": True}
        })

    return results, img