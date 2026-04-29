import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim


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

    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=2)

    return gray, thresh


# -------------------------------
# Extract Regions
# -------------------------------
def extract_regions(thresh):
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    regions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if 30 < w < 500 and 10 < h < 150:
            regions.append((x, y, w, h))

    regions = sorted(regions, key=lambda r: (r[1], r[0]))

    return regions


# -------------------------------
# Compare Regions (SSIM)
# -------------------------------
def find_duplicate_regions(gray, regions, threshold=0.8):
    duplicates = []

    for i in range(len(regions)):
        x1, y1, w1, h1 = regions[i]
        roi1 = gray[y1:y1+h1, x1:x1+w1]

        for j in range(i + 1, len(regions)):
            x2, y2, w2, h2 = regions[j]
            roi2 = gray[y2:y2+h2, x2:x2+w2]

            # size check
            if abs(w1 - w2) > 10 or abs(h1 - h2) > 5:
                continue

            roi1_resized = cv2.resize(roi1, (80, 40))
            roi2_resized = cv2.resize(roi2, (80, 40))

            score, _ = ssim(roi1_resized, roi2_resized, full=True, win_size=7)

            if score > threshold:
                duplicates.append((x1, y1, w1, h1))
                duplicates.append((x2, y2, w2, h2))
                break

    return duplicates


# -------------------------------
# Draw Boxes
# -------------------------------
def draw_boxes(img, boxes):
    output = img.copy()

    for (x, y, w, h) in boxes:
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return output


# -------------------------------
# Save Output
# -------------------------------
def save_output(img, original_path, folder="result"):
    os.makedirs(folder, exist_ok=True)

    file_name = "processed_" + os.path.basename(original_path)
    save_path = os.path.join(folder, file_name)

    cv2.imwrite(save_path, img)

    return save_path


# -------------------------------
# Main Pipeline
# -------------------------------
def detect_duplicate_forgery(image_path):
    img = load_image(image_path)

    gray, thresh = preprocess_image(img)

    regions = extract_regions(thresh)

    duplicates = find_duplicate_regions(gray, regions)

    result = draw_boxes(img, duplicates)

    save_path = save_output(result, image_path)

    return result, save_path


# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    img_path = r"C:\Users\chanc\OneDrive\Documents\chanchal_0ss\Document-Forgery-Detection\Claim_Documents\3fa713df-544d-4311-9fc6-1654977686c3.jpeg"

    result, path = detect_duplicate_forgery(img_path)
    # cv2.imwrite(save_path, output)
    cv2.imshow("Duplicate Detection (Red Boxes)", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # print("Saved as:", path)