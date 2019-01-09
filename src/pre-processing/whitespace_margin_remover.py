import numpy as np
import cv2

def getROI(image):
    h,w,_ = image.shape
    left_boundary = int(0.025*w)
    right_boundary = int(0.975*w)
    top_boundary = int(0.025*h)
    bottom_boundary = int(0.975*h)

    image = image[top_boundary:bottom_boundary,left_boundary:right_boundary]

    img = image
    img = cv2.medianBlur(img,9)
    # while True:
    #     cv2.imshow("Input", img)
    #     k = cv2.waitKey(30) & 0xff
    #     if k == 27:
    #         break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255*(gray < 128).astype(np.uint8)

    coords = cv2.findNonZero(gray)
    x,y,w,h = cv2.boundingRect(coords)
    rect = image[y:y+h, x:x+w]

    return rect