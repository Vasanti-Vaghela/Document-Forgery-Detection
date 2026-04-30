import cv2
import numpy as np
import pytesseract

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


#  BBOX MERGING FUNCTION 
def merge_boxes(boxes, iou_threshold=0.3):

    if not boxes:
        return []

    merged = []

    for box in boxes:
        x, y, w, h = box
        merged_flag = False

        for i in range(len(merged)):
            mx, my, mw, mh = merged[i]

            x1, y1, x2, y2 = x, y, x+w, y+h
            mx1, my1, mx2, my2 = mx, my, mx+mw, my+mh

            ix1 = max(x1, mx1)
            iy1 = max(y1, my1)
            ix2 = min(x2, mx2)
            iy2 = min(y2, my2)

            iw = max(0, ix2 - ix1)
            ih = max(0, iy2 - iy1)

            intersection = iw * ih
            union = (w*h) + (mw*mh) - intersection

            iou = intersection / union if union != 0 else 0

            if iou > iou_threshold:
                nx1 = min(x1, mx1)
                ny1 = min(y1, my1)
                nx2 = max(x2, mx2)
                ny2 = max(y2, my2)

                merged[i] = [nx1, ny1, nx2-nx1, ny2-ny1]
                merged_flag = True
                break

        if not merged_flag:
            merged.append(box)

    return merged


# MAIN FUNCTION
def detect_overwrite_c2(image_path):

    img = cv2.imread(image_path)

    if img is None:
        print("Image not found")
        return None, []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    raw_boxes = []
    detections = []

    n = len(data['text'])

    for i in range(n):

        text = data['text'][i].strip()

        if text == "":
            continue

        if len(text) < 3:
            continue

        try:
            conf = int(data['conf'][i])
        except:
            continue

        x = data['left'][i]
        y = data['top'][i]
        w = data['width'][i]
        h = data['height'][i]

        if h < 15:
            continue

        aspect_ratio = w / h if h != 0 else 0
        if aspect_ratio > 5:
            continue

        roi = gray[y:y+h, x:x+w]

        if roi.size == 0:
            continue

        # Ignore clean printed text
        if text.isalpha() and conf > 70:
            continue

        # Feature 1: low confidence
        low_conf = conf < 50

        # Feature 2: variance
        variance = np.var(roi)
        high_variance = variance > 1000

        # Feature 3: mixed characters
        weird_text = any(c.isdigit() for c in text) and any(c.isalpha() for c in text)

        # Feature 4: edges
        edges = cv2.Canny(roi, 50, 150)
        edge_density = np.sum(edges) / (w * h)
        strong_edges = edge_density > 20

        # Feature 5: stroke density
        _, thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((2, 2), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)

        stroke_pixels = np.sum(dilated > 0)
        stroke_density = stroke_pixels / (w * h)
        thick_stroke = stroke_density > 0.25

        # Scoring
        score = 0

        if low_conf:
            score += 1
        if high_variance:
            score += 1
        if weird_text:
            score += 1
        if strong_edges:
            score += 1
        if thick_stroke:
            score += 1

        if score >= 4:
            raw_boxes.append([x, y, w, h])

    # MERGE BOXES
    merged_boxes = merge_boxes(raw_boxes)

    # DRAW FINAL OUTPUT
    for (x, y, w, h) in merged_boxes:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

        detections.append({
            "bbox": [x, y, w, h]
        })

    return img, detections


# RUN 
if __name__ == "__main__":
    image_path = r"C:\Users\Zaid\Document-Forgery-Detection\Claim_Documents\000893__PMJAY_UP_S_G_2025_R2_2026030910078737__pushpa_2nd_ot_1.jpeg"

    img, detections = detect_overwrite_c2(image_path)

    if img is not None:
        print("\nFinal Detections:")
        for d in detections:
            print(d)

        cv2.imshow("C2 Overwrite Detection", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()