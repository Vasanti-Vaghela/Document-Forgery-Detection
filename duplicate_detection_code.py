import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image
img = cv2.imread("document2.png")
if img is None:
    print("Image not found")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ORB feature detection
orb = cv2.ORB_create(3000)
keypoints, descriptors = orb.detectAndCompute(gray, None)

if descriptors is None:
    print("No features detected")
    exit()

# KNN Matching
bf = cv2.BFMatcher(cv2.NORM_HAMMING)
matches = bf.knnMatch(descriptors, descriptors, k=2)

# Relaxed Lowe's ratio test
good = []
for m, n in matches:
    if m.queryIdx != m.trainIdx and m.distance < 0.9 * n.distance:
        good.append(m)

# Fallback if too few matches
if len(good) < 10:
    print("Using relaxed matching fallback...")
    for m, n in matches:
        if m.queryIdx != m.trainIdx:
            good.append(m)

# Collect points
points = np.array([keypoints[m.queryIdx].pt for m in good])
print("Duplicate points:", len(points))

# Clustering
clusters = []
for p in points:
    added = False
    for cluster in clusters:
        if np.linalg.norm(p - cluster[0]) < 80:  # relaxed
            cluster.append(p)
            added = True
            break
    if not added:
        clusters.append([p])

# Draw bounding boxes
output = img.copy()
for cluster in clusters:
    if len(cluster) < 5:  # relaxed
        continue

    cluster = np.array(cluster).astype(np.int32)
    x, y, w, h = cv2.boundingRect(cluster)

    cv2.rectangle(output, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv2.putText(output, "Duplicate", (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

# Show result
output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(10,10))
plt.imshow(output_rgb)
plt.title("Duplicate Detection (C1)")
plt.axis("off")
plt.show()