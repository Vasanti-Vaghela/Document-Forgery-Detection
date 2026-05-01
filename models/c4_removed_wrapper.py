import cv2
import numpy as np
from removingcontent import detect_image, load_model, BASELINE_STATS_PATH, MODEL_PATH
from removingcontent import IMG_SIZE
from tensorflow.keras.models import load_model as keras_load_model
import numpy as np


def get_bboxes_from_mask(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # ignore small noise
        if w*h < 500:
            continue

        boxes.append([x, y, w, h])

    return boxes


def run_c4(image_path):

    # load model
    model = keras_load_model(MODEL_PATH, compile=False)
    mean_score, std_score = np.load(BASELINE_STATS_PATH)

    img = cv2.imread(image_path)
    orig = img.copy()

    # resize
    img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE)) / 255.0
    recon = model.predict(img_resized[np.newaxis,...])[0]

    error = np.abs(img_resized - recon)
    heatmap = np.mean(error, axis=2)

    heatmap_norm = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min())
    mask = (heatmap_norm > 0.15).astype(np.uint8)

    # resize mask to original size
    mask_full = cv2.resize(mask, (orig.shape[1], orig.shape[0]))

    # get bounding boxes
    boxes = get_bboxes_from_mask(mask_full)

    results = []

    for (x, y, w, h) in boxes:
        results.append({
            "bbox": [x, y, w, h],
            "features": {"removed": True}
        })

    return results, orig