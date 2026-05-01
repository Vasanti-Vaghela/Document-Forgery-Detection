import cv2
from duplicate_detection_code import detect_duplicate


def run_c1(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return []

    detections = detect_duplicate(img)

    # add category
    for d in detections:
        d["features"] = {"duplicate": True}

    return detections