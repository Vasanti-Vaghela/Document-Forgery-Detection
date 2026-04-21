import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open("text.png.png")
img2 = Image.open("text2.png.png")


text = pytesseract.image_to_string(img)
text2 = pytesseract.image_to_string(img2)

print(text)
print(text2)