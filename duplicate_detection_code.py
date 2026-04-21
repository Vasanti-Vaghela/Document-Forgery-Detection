# =========================
# 🔴 1. IMPORT LIBRARIES
# =========================
import cv2
import numpy as np


# =========================
# 🔴 2. LOAD IMAGES
# =========================
image_paths = ["doc1.png", "doc2.png", "doc3.png"]

images = []

for path in image_paths:
    img = cv2.imread(path)
    
    if img is None:
        print(f"❌ Error loading {path}")
        continue
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    images.append(gray)


# =========================
# 🔴 3. ORB FEATURE EXTRACTION
# =========================
orb = cv2.ORB_create(nfeatures=1000)

keypoints = []
descriptors = []

for img in images:
    kp, des = orb.detectAndCompute(img, None)
    keypoints.append(kp)
    descriptors.append(des)


# =========================
# 🔴 4. MATCHING + CATEGORY DETECTION
# =========================
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

threshold = 0.6

results = []

for i in range(len(images)):
    for j in range(i+1, len(images)):
        
        if descriptors[i] is None or descriptors[j] is None:
            continue
        
        matches = bf.match(descriptors[i], descriptors[j])
        matches = sorted(matches, key=lambda x: x.distance)

        # similarity score
        sim = len(matches) / max(len(descriptors[i]), len(descriptors[j]))

        kp1 = len(keypoints[i])
        kp2 = len(keypoints[j])

        categories = []

        # =========================
        # 🔴 CATEGORY LOGIC
        # =========================

        # C1: Copy-Paste
        if sim > 0.9:
            categories.append("C1: Copy-Paste")

        # C2: Overwriting
        elif 0.8 < sim <= 0.9:
            categories.append("C2: Overwriting")

        # C5: Merged
        elif 0.6 < sim <= 0.8:
            categories.append("C5: Merged Documents")

        # C3: Added Content
        if kp2 > kp1 * 1.2:
            categories.append("C3: Added Content")

        # C4: Removed Content
        if kp2 < kp1 * 0.8:
            categories.append("C4: Removed Content")

        # C7: Irregular Pattern
        if len(matches) < 10:
            categories.append("C7: Irregular Pattern")

        # C8: AI Generated (low features)
        if kp1 < 50 or kp2 < 50:
            categories.append("C8: Possible AI Generated")

        # C9: Partial Edit
        if 0.5 < sim < 0.85:
            categories.append("C9: Partial Edit")

        # C10: No Forgery
        if sim < 0.5:
            categories.append("C10: No Forgery")

        # =========================
        # 🔴 SAVE RESULT
        # =========================
        results.append({
            "image_1": i,
            "image_2": j,
            "similarity": round(sim, 2),
            "categories": ", ".join(set(categories))
        })

        # =========================
        # 🔴 SHOW ORIGINAL + MATCH
        # =========================
        match_img = cv2.drawMatches(
            images[i], keypoints[i],
            images[j], keypoints[j],
            matches[:30], None, flags=2
        )

        cv2.imshow(f"Match {i}-{j}", match_img)


# =========================
# 🔴 5. PRINT FINAL RESULTS
# =========================
print("\n========== FINAL OUTPUT ==========\n")

for r in results:
    print(f"Image {r['image_1']} ↔ Image {r['image_2']}")
    print(f"Similarity: {r['similarity']}")
    print(f"Categories: {r['categories']}")
    print("---------------------------------")


# =========================
# 🔴 6. CLOSE WINDOWS
# =========================
cv2.waitKey(0)
cv2.destroyAllWindows()