import os
import cv2
import pytesseract
import pandas as pd
import numpy as np
from pdf2image import convert_from_path
import fitz  
import os

def pdf_to_images(pdf_path, output_folder="temp_images"):
    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)
    image_paths = []

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for i, page in enumerate(doc):
        pix = page.get_pixmap()

        img_name = f"{base_name}_page_{i+1}.jpg"
        img_path = os.path.join(output_folder, img_name)

        pix.save(img_path)
        image_paths.append(img_path)

    return image_paths


if __name__ == "__main__":
    pdf_path = "sample.pdf"   

    image_files = pdf_to_images(pdf_path)

    print("Extracted Images:")
    for img in image_files:
        print(img)

# Load image/pdf
def load_document(file_path):
    ext = file_path.lower().split('.')[-1]

    if ext in ['png', 'jpg', 'jpeg']:
        img = cv2.imread(file_path)
        return [img]

    elif ext == 'pdf':
        pages = convert_from_path(file_path)
        images = []
        for page in pages:
            img = np.array(page)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            images.append(img)
        return images

    return []

# Extract OCR features
def extract_features(img):
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DATAFRAME)
    data = data.dropna()

    if len(data) < 2:
        return [0, 0, 0]

    spaces = []
    for i in range(len(data)-1):
        gap = data.iloc[i+1]['left'] - (data.iloc[i]['left'] + data.iloc[i]['width'])
        spaces.append(gap)

    spacing_std = pd.Series(spaces).std()
    avg_conf = data['conf'].mean()
    line_std = data.groupby('line_num')['top'].mean().std()

    return [spacing_std, avg_conf, line_std]

# Suspicion score
def suspicion_score(features):
    spacing_std, avg_conf, line_std = features
    score = 0

    if spacing_std < 2:
        score += 1
    if avg_conf > 95:
        score += 1
    if line_std < 1:
        score += 1

    return score

folder = "Claim_Documents"

for file in os.listdir(folder):
    path = os.path.join(folder, file)

    try:
        pages = load_document(path)
        total_score = 0

        for img in pages:
            features = extract_features(img)
            total_score += suspicion_score(features)

        avg_score = total_score / len(pages)

        if avg_score >= 2:
            result = "Likely AI-generated"
        else:
            result = "Likely Real"

        print(f"{file} --> {result}| Score: {avg_score}")

    except Exception as e:
        print(f"{file} --> Error: {e}")