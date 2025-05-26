import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    if (ret):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        ub = np.array([50, 40, 40])
        ua = np.array([80, 255, 255])
        mask = cv.inRange(hsv, ub, ua)
        res = cv.bitwise_and(img, img, mask=mask)
        
        cv.imshow('res', res)
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break
    else:
        break

cap.release()
cv.destroyAllWindows