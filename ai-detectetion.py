import cv2

import pytesseract
img=cv2.imread("ai_generated.png")
text=pytesseract.image_to_string(img,config="--psm 6")
print(text)