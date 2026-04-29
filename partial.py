import cv2
import pytesseract
import numpy as np
from pdf2image import convert_from_path
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

INPUT_FOLDER = "Claim_Documents"
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------------------------
# PDF → Image
# ---------------------------
def pdf_to_images(pdf_path):
    paths = []

    images = convert_from_path(pdf_path, poppler_path=r"C:\Program Files\poppler-25.07.0\Library\bin")


    for i, img in enumerate(images):
        path = f"{OUTPUT_FOLDER}/temp_{i}.png"
        img.save(path)
        paths.append(path)

    return paths

# ---------------------------
# Load files
# ---------------------------
def load_files():
    paths = []

    for file in os.listdir(INPUT_FOLDER):
        full = os.path.join(INPUT_FOLDER, file)

        if file.endswith(".pdf"):
            paths.extend(pdf_to_images(full))
        elif file.endswith((".jpg", ".png", ".jpeg")):
            paths.append(full)

    return paths

# ---------------------------
# OCR
# ---------------------------
def extract_text(img):
    return pytesseract.image_to_string(img)

# ---------------------------
# AI Detection (Heuristic)
# ---------------------------
def detect_regions(image):
    h, w, _ = image.shape
    regions = []

    size = 150
    step = 80

    for y in range(0, h - size, step):
        for x in range(0, w - size, step):
            patch = image[y:y+size, x:x+size]

            gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)

            variance = np.var(gray)
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges) / (size * size)

            # AI-like condition
            if variance < 400 and edge_density < 0.05:
                regions.append((x, y, size, size))

    return regions

# ---------------------------
# MAIN
# ---------------------------
def run():
    files = load_files()

    for path in files:
        print("Processing:", path)

        img = cv2.imread(path)

        # OCR
        text = extract_text(img)
        print("Text:", text[:100])

        # Detect
        regions = detect_regions(img)

        for (x, y, w, h) in regions:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)

        name = os.path.basename(path).split('.')[0]
        cv2.imwrite(f"{OUTPUT_FOLDER}/{name}_result.png", img)

    print("✅ Done")

run()