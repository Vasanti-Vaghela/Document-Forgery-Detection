
#functions in open cv
#1. cv2.imread() - to read an image
#2. cv2.imshow() - to display an image
#3. cv2.waitKey() - to wait for a key press
#4. cv2.destroyAllWindows() - to close all windows
#5. cv2.imwrite() - to save an image
#6. cv2.cvtColor() - to convert an image from one color space to another
#7. cv2.resize() - to resize an image
#8. cv2.rotate() - to rotate an image
#9. cv2.flip() - to flip an image
#10. cv2.GaussianBlur() - to blur an image
#11. cv2.Canny() - to detect edges in an image
#12. cv2.threshold() - to apply a threshold to an image
#13. cv2.findContours() - to find contours in an image
#14. cv2.drawContours() - to draw contours on an image
#15. cv2.HoughLines() - to detect lines in an image
#16. cv2.HoughCircles() - to detect circles in an image
#17. cv2.Sobel() - to apply the Sobel operator to an image
#18. cv2.Laplacian() - to apply the Laplacian operator to an image
#19. cv2.Canny() - to detect edges in an image  
import cv2  
img=cv2.imread("bill-img.png")
cv2.imshow("bill",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
