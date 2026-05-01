from partial import detect_regions
import cv2

def run_c9(image_path):
    img = cv2.imread(image_path)
    result = detect_regions(img, show=False)

    if result == "FAKE":
        return [{
            "bbox": [0, 0, 100, 100],
            "features": {"partial_edit": True}
        }], None

    return [], None