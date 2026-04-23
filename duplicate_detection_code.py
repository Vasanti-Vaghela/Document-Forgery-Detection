import cv2
import numpy as np

# Load image
img = cv2.imread("document.png")
if img is None:
    print("Image not found")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 🔥 STEP 1: Strong threshold (important fix)
_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

# 🔥 STEP 2: Thicken text (VERY IMPORTANT)
kernel = np.ones((3,3), np.uint8)
thresh = cv2.dilate(thresh, kernel, iterations=2) #2 to 1

# 🔥 STEP 3: Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Filter large text regions
regions = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 30 and h > 10:   # tuned for your image
        regions.append((x, y, w, h))

# Sort by top position (optional)
regions = sorted(regions, key=lambda r: (r[1],r[0]))

output = img.copy()

# 🔥 STEP 4: Compare regions
for i in range(len(regions)):
    x1, y1, w1, h1 = regions[i]
    roi1 = gray[y1:y1+h1, x1:x1+w1]

    for j in range(i+1, len(regions)):
        x2, y2, w2, h2 = regions[j]
        roi2 = gray[y2:y2+h2, x2:x2+w2]

        # Resize to same size
        roi2_resized = cv2.resize(roi2, (w1, h1))

        # Compare similarity
        diff = cv2.absdiff(roi1, roi2_resized)
        score = np.mean(diff)

        # 🔥 STRICT match condition
        if score < 15:
            cv2.rectangle(output, (x1, y1), (x1+w1, y1+h1), (0,0,255), 2)
            cv2.rectangle(output, (x2, y2), (x2+w2, y2+h2), (0,0,255), 2)

# Show result
cv2.imshow("FINAL RESULT", output)
cv2.waitKey(0)
cv2.destroyAllWindows()