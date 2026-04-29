import cv2
import numpy as np

# Load image
img_path = r"C:\Users\chanc\OneDrive\Documents\chanchal_0ss\Document-Forgery-Detection\Claim_Documents\3fa713df-544d-4311-9fc6-1654977686c3.jpeg"

img = cv2.imread(img_path)
if img is None:
    print("Image not found")
    exit()

output = img.copy()

# STEP 1: Preprocess
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

kernel = np.ones((2,2), np.uint8)
dilated = cv2.dilate(thresh, kernel, iterations=1)

# STEP 2: Find contours
contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

boxes = [cv2.boundingRect(c) for c in contours]

# Remove noise
boxes = [b for b in boxes if b[2] > 10 and b[3] > 10]

# STEP 3: Group boxes into lines
lines = []
y_threshold = 15

for box in sorted(boxes, key=lambda b: b[1]):
    x, y, w, h = box
    placed = False

    for line in lines:
        _, ly, _, lh = line[0]
        if abs(y - ly) < y_threshold:
            line.append(box)
            placed = True
            break

    if not placed:
        lines.append([box])

# STEP 4: Process each line
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

    # STEP 5: Only RED suspicious boxes
    for i, j, gap in pairs:
        if gap > threshold:
            x, y, w, h = line[j]
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 2)

# STEP 6: Show result
cv2.imshow("Forgery Detection (Only Suspicious)", output)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save output
cv2.imwrite("linewise_forgery_red_only.png", output)