import cv2
import numpy as np


# -------------------------------
# Load Image
# -------------------------------
def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise ValueError("Image not found")
    return img


# -------------------------------
# Preprocessing
# -------------------------------
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    return dilated


# -------------------------------
# Get Bounding Boxes
# -------------------------------
def get_valid_boxes(processed_img):
    contours, _ = cv2.findContours(processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = [cv2.boundingRect(c) for c in contours]

    # Remove noise
    boxes = [b for b in boxes if b[2] > 10 and b[3] > 10]

    return boxes


# -------------------------------
# Group boxes into lines
# -------------------------------
def group_into_lines(boxes, y_threshold=15):
    lines = []

    for box in sorted(boxes, key=lambda b: b[1]):
        x, y, w, h = box
        placed = False

        for line in lines:
            _, ly, _, _ = line[0]

            if abs(y - ly) < y_threshold:
                line.append(box)
                placed = True
                break

        if not placed:
            lines.append([box])

    return lines


# -------------------------------
# Detect suspicious gaps
# -------------------------------
def detect_suspicious_spaces(lines):
    suspicious_boxes = []

    for line in lines:
        line = sorted(line, key=lambda b: b[0])

        spaces = []
        pairs = []

        for i in range(len(line) - 1):
            x1, y1, w1, h1 = line[i]
            x2, y2, w2, h2 = line[i + 1]

            gap = x2 - (x1 + w1)

            if gap > 0:
                spaces.append(gap)
                pairs.append((i, i + 1, gap))

        if len(spaces) == 0:
            continue

        mean_space = np.mean(spaces)
        threshold = mean_space * 1.8

        for i, j, gap in pairs:
            if gap > threshold:
                suspicious_boxes.append(line[j])

    return suspicious_boxes


# -------------------------------
# Draw Red Boxes
# -------------------------------
def draw_boxes(img, boxes):
    output = img.copy()

    for (x, y, w, h) in boxes:
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return output


# -------------------------------
# Main Pipeline Function
# -------------------------------
def detect_forgery(image_path):
    img = load_image(image_path)

    processed = preprocess_image(img)
    boxes = get_valid_boxes(processed)
    lines = group_into_lines(boxes)
    suspicious = detect_suspicious_spaces(lines)

    result = draw_boxes(img, suspicious)

    return result


# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    img_path = r"C:\Users\chanc\OneDrive\Documents\chanchal_0ss\Document-Forgery-Detection\Claim_Documents\3fa713df-544d-4311-9fc6-1654977686c3.jpeg"

    result = detect_forgery(img_path)

    cv2.imshow("Forgery Detection (Only Red)", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # cv2.imwrite("linewise_forgery_red_only.png", result)