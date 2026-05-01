from C2_Overwrite import detect_overwrite_c2

def run_c2(image_path):
    img, detections = detect_overwrite_c2(image_path)

    results = []
    for d in detections:
        results.append({
            "bbox": d["bbox"],
            "features": {"overwrite": True}
        })

    return results, img