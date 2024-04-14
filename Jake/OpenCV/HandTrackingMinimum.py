import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands() # default parameters work pretty well though
#hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
# static image trackign is for if it is tracking on each frame -- slows down code

while True:

    success, img = cap.read()
    img = cv.flip(img, 1)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLims in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLims, mpHands.HAND_CONNECTIONS)
            
    cv.imshow('Image', img)
    cv.waitKey(1)