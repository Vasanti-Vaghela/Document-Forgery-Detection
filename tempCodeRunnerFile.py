import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image
img = cv2.imread("document2.png")
if img is None:
    print("Image not found")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Improve contrast (important for real images)
gray = cv2.equalizeHist(gray)

# ORB features
orb = cv2.ORB_create(4000)
kp, des = orb.detectAndCompute(gray, None)

if des is None:
    print("No features detected")
    exit()

# KNN matching
bf = cv2.BFMatcher(cv2.NORM_HAMMING)
matches = bf.knnMatch(des, des, k=2)

# Lowe's ratio test
good = []
for m, n in matches:
    if m.queryIdx != m.trainIdx and m.distance < 0.85 * n.distance:
        good.append(m)

print("Good matches:", len(good))

# Extract matched point pairs
pts1 = []
pts2 = []

for m in good:
    p1 = kp[m.queryIdx].pt
    p2 = kp[m.trainIdx].pt

    # ignore very close points (same area)
    if np.linalg.norm(np.array(p1) - np.array(p2)) > 20:
        pts1.append(p1)
        pts2.append(p2)

pts1 = np.array(pts1)
pts2 = np.array(pts2)

# Combine both sets
all_points = np.vstack((pts1, pts2)) if len(pts1) > 0 else []

# Clustering
clusters = []

for p in all_points:
    added = False
    for cluster in clusters:
        if np.linalg.norm(p - cluster[0]) < 60:
            cluster.append(p)
            added = True
            break
    if not added:
        clusters.append([p])

# Draw results
output = img.copy()

for cluster in clusters:
    if len(cluster) < 15:  # ignore noise
        continue

    cluster = np.array(cluster).astype(np.int32)
    x, y, w, h = cv2.boundingRect(cluster)

    cv2.rectangle(output, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv2.putText(output, "Duplicate", (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

# Show
output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(10,10))
plt.imshow(output_rgb)
plt.title("Duplicate Detection (Improved)")
plt.axis("off")
plt.show()