from mergedetecter import detect_image

def run_c5(image_path):
    result = detect_image(image_path, show=False)

    if result == "MERGED":
        return [{
            "bbox": [0, 0, 100, 100],  # fallback (no bbox)
            "features": {"merged": True}
        }], None

    return [], None