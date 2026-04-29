import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

#  Image path
img_path = r"C:\Users\chanc\OneDrive\Documents\chanchal_0ss\Document-Forgery-Detection\Claim_Documents\3fa713df-544d-4311-9fc6-1654977686c3.jpeg"

img = cv2.imread(img_path)
if img is None:
    print("Image not found")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# STEP 1: Threshold
_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

# STEP 2: Thicken text
kernel = np.ones((3,3), np.uint8)
thresh = cv2.dilate(thresh, kernel, iterations=2)

# STEP 3: Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

regions = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if 30 < w < 500 and 10 < h < 150:
        regions.append((x, y, w, h))

regions = sorted(regions, key=lambda r: (r[1], r[0]))

output = img.copy()

#  Threshold
threshold = 0.8

# STEP 4: Compare regions
for i in range(len(regions)):
    x1, y1, w1, h1 = regions[i]
    roi1 = gray[y1:y1+h1, x1:x1+w1]

    for j in range(i+1, len(regions)):
        x2, y2, w2, h2 = regions[j]
        roi2 = gray[y2:y2+h2, x2:x2+w2]

        if abs(w1 - w2) > 10 or abs(h1 - h2) > 5:
            continue

        roi1_resized = cv2.resize(roi1, (80, 40))
        roi2_resized = cv2.resize(roi2, (80, 40))

        score, _ = ssim(roi1_resized, roi2_resized, full=True, win_size=7)

        if score > threshold:
            cv2.rectangle(output, (x1, y1), (x1+w1, y1+h1), (0,0,255), 2)
            cv2.rectangle(output, (x2, y2), (x2+w2, y2+h2), (0,0,255), 2)
            break

#  SAVE OUTPUT (NEW FILE NAME)
save_folder = "result"
os.makedirs(save_folder, exist_ok=True)

# new name add karo
file_name = "processed_" + os.path.basename(img_path)
save_path = os.path.join(save_folder, file_name)

cv2.imwrite(save_path, output)

#  SHOW RESULT
cv2.imshow("Result", output)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(" Saved as:", save_path)