import os
import cv2
from pdf2image import convert_from_path

POPPLER_PATH = r"C:\Program Files\poppler-25.07.0\Library\bin"

def pdf_to_images(pdf_path, output_folder="temp_pages"):
    os.makedirs(output_folder, exist_ok=True)

    images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    paths = []

    for i, img in enumerate(images):
        path = os.path.join(output_folder, f"page_{i}.png")
        img.save(path)
        paths.append(path)

    return paths


def load_input(path):
    if path.lower().endswith(".pdf"):
        return pdf_to_images(path)
    else:
        return [path]