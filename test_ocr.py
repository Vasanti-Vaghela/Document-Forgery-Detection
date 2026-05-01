
import pytesseract
from PIL import Image
import os

if os.name == "nt":  # Windows only
    possible_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(possible_path):
        pytesseract.pytesseract.tesseract_cmd = possible_path
img = Image.open("text.png.png")
text = pytesseract.image_to_string(img)
print(text)


