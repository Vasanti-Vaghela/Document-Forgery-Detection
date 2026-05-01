from C3_Added import detect_added_c3
import cv2

def run_c3(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return [], None

    _, detections = detect_added_c3(img)

    results = []

    for d in detections:
        results.append({
            "bbox": d["bbox"],
            "features": {"added": True}
        })

    return results, img