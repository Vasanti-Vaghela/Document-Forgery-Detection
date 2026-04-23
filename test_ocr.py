
import pytesseract
from PIL import 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
img = Image.open("text.png.png")
text = pytesseract.image_to_string(img)
print(text)


