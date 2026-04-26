import cv2
import numpy as np
import pytesseract
from difflib import SequenceMatcher
from skimage.metrics import structural_similarity as ssim

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image
img = cv2.imread("document3.png")
if img is None:
    print("Image not found")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# STEP 1: Threshold
_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

# STEP 2: Merge text into lines
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,5))
thresh = cv2.dilate(thresh, kernel, iterations=2)

# STEP 3: Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

regions = []

# STEP 4: Extract valid regions
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    if 80 < w < 800 and 25 < h < 200:
        regions.append((x, y, w, h))

# Sort regions
# regions = sorted(regions, key=lambda r: (r[1], r[0]))

# print("Total regions:", len(regions))

output = img.copy()

# -------- OCR ONCE (for speed) --------
def get_text(roi):
    return pytesseract.image_to_string(roi, config='--psm 6').strip()

texts = []
for (x, y, w, h) in regions:
    roi = gray[y:y+h, x:x+w]
    texts.append(get_text(roi))

# Fuzzy matching
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# STEP 5: Compare regions
for i in range(len(regions)):
    x1, y1, w1, h1 = regions[i]
    roi1 = gray[y1:y1+h1, x1:x1+w1]
    text1 = texts[i]

    for j in range(i+1, len(regions)):
        x2, y2, w2, h2 = regions[j]
        roi2 = gray[y2:y2+h2, x2:x2+w2]
        text2 = texts[j]

        # SIZE FILTER
        if abs(w1 - w2) > 60 or abs(h1 - h2) > 30:
            continue

        # DISTANCE FILTER
        distance = abs(x1 - x2) + abs(y1 - y2)
        if distance < 50:
            continue

        # SAME REGION BAND (relaxed)
        if abs(y1 - y2) > 200:
            continue

        # -------- TEXT MATCH --------
        if text1 and text2:
            if similar(text1, text2) > 0.7:
                cv2.rectangle(output, (x1,y1), (x1+w1,y1+h1), (0,0,255), 2)
                cv2.rectangle(output, (x2,y2), (x2+w2,y2+h2), (0,0,255), 2)
                break

        # -------- IMAGE MATCH (STRONG FIX) --------
        roi1_resized = cv2.resize(roi1, (200, 80))
        roi2_resized = cv2.resize(roi2, (200, 80))

        roi1_blur = cv2.GaussianBlur(roi1_resized, (5,5), 0)
        roi2_blur = cv2.GaussianBlur(roi2_resized, (5,5), 0)

        score, _ = ssim(roi1_blur, roi2_blur, full=True)

        if score > 0.60:
            cv2.rectangle(output, (x1,y1), (x1+w1,y1+h1), (0,0,255), 2)
            cv2.rectangle(output, (x2,y2), (x2+w2,y2+h2), (0,0,255), 2)
            break

# STEP 6: Save + Show
cv2.imwrite("output.png", output)
print("Output saved as output.png")

cv2.imshow("Forgery Detection Result", output)
cv2.waitKey(0)
cv2.destroyAllWindows()