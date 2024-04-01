# Basic code to filter out and track blue object in a range of shades


import cv2 as cv
import numpy as np

cap = cv.VideoCapture(1)

while True:
    _, frame = cap.read()
    frame = cv.flip(frame, 1)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) # convert BGR to HSV

    # hsv is [hue (0,179), saturation(0,255), value(0,255)]


    # define color value for blue in hsv
    lower_blue = np.array([95, 30, 30])
    upper_blue = np.array([130, 255, 255])

    mask = cv.inRange(hsv, lower_blue, upper_blue) # threshold the hsv image to get only blue colors

    res = cv.bitwise_and(frame, frame, mask=mask) # only show the pixel values in the desired range

    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('res', res)

    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()