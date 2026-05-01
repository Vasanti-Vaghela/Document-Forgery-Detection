import cv2
import numpy as np
import pytesseract
import os

if os.name == "nt":  # Windows only
    possible_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(possible_path):
        pytesseract.pytesseract.tesseract_cmd = possible_path


def _has_neighbors(box, all_boxes, thresh_x=60, thresh_y=30):
    x, y, w, h = box
    cx, cy = x + w/2, y + h/2
    count = 0
    for bx in all_boxes:
        x2, y2, w2, h2 = bx
        c2x, c2y = x2 + w2/2, y2 + h2/2
        if abs(cx - c2x) < thresh_x and abs(cy - c2y) < thresh_y:
            count += 1
    return count > 2


def detect_added_c3(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    detections = []
    all_boxes = []

    n = len(data['text'])

    for i in range(n):
        w = data['width'][i]
        h = data['height'][i]
        if w > 0 and h > 0:
            all_boxes.append([data['left'][i], data['top'][i], w, h])

    H, W = gray.shape

    # global height reference (for font consistency)
    heights = [h for h in data['height'] if h > 0]
    avg_height = np.mean(heights) if heights else 0

    for i in range(n):

        text = data['text'][i].strip()
        if text == "" or len(text) < 2:
            continue

        try:
            conf = int(data['conf'][i])
        except:
            continue

        x = data['left'][i]
        y = data['top'][i]
        w = data['width'][i]
        h = data['height'][i]

        if w <= 10 or h <= 10:
            continue

        aspect_ratio = w / float(h)
        if aspect_ratio > 6:
            continue

        roi = gray[y:y+h, x:x+w]
        if roi.size == 0:
            continue

        area = w * h

        mean_intensity = np.mean(roi)
        variance = np.var(roi)

        edges = cv2.Canny(roi, 50, 150)
        edge_density = np.sum(edges) / (area + 1)

        _, thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        stroke_density = np.sum(thresh == 0) / (area + 1)

        # PRINTED FILTER
        if conf > 70 and variance < 180 and edge_density < 4 and stroke_density < 0.32:
            continue

        # NEIGHBOR FILTER
        if _has_neighbors([x, y, w, h], all_boxes):
            continue

        # LINE FILTER
        same_line = 0
        for j in range(n):
            if i == j:
                continue
            if abs(y - data['top'][j]) < 10:
                same_line += 1

        if same_line >= 3:
            continue

        # HEADER FILTER
        if text.isupper() and conf > 70:
            continue

        # FEATURES
        score = 0

        if conf < 55:
            score += 1

        if variance > 300:
            score += 1

        if edge_density > 5:
            score += 1

        if stroke_density > 0.4:
            score += 1

        if area < 2500:
            score += 1

        if mean_intensity > 200 and variance > 250:
            score += 1

        # FONT SIZE INCONSISTENCY
        if avg_height > 0 and abs(h - avg_height) > 0.5 * avg_height:
            score += 1

        # TEXT TYPE
        if any(c.isdigit() for c in text) and any(c.isalpha() for c in text):
            score += 1

        # MARGIN
        if x < 0.15*W or x > 0.85*W or y < 0.15*H or y > 0.85*H:
            score += 1

        # FINAL DECISION
        if score >= 5:
            detections.append({
                "bbox": [x, y, w, h]
            })

    # MERGE
    final = []
    for box in detections:
        x, y, w, h = box["bbox"]

        keep = True
        for f in final:
            fx, fy, fw, fh = f["bbox"]
            if abs(x - fx) < 25 and abs(y - fy) < 25:
                keep = False
                break

        if keep:
            final.append(box)

    return image, final


# TEST
if __name__ == "__main__":

    img_path = r"C:\Users\Zaid\Document-Forgery-Detection\Claim_Documents\000893__PMJAY_UP_S_G_2025_R2_2026030910078737__pushpa_2nd_ot_1.jpeg"

    img = cv2.imread(img_path)

    if img is None:
        print("Image not found")
        exit()

    out, dets = detect_added_c3(img)

    print("\nC3 Detections:\n", dets)

    for d in dets:
        x, y, w, h = d["bbox"]
        cv2.rectangle(out, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("C3 FINAL", out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()