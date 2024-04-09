import cv2 as cv
import numpy as np

# Load Haar cascades
eye_cascade = cv.CascadeClassifier('/Users/jacob_kitz/Desktop/hgn_processing/HGN_Classification/Jake/Resources/HaarCascades/haarcascade_eye.xml')
face_cascade = cv.CascadeClassifier('/Users/jacob_kitz/Desktop/hgn_processing/HGN_Classification/Jake/Resources/HaarCascades/haarcascade_frontalface_default.xml')

# Load img detector parameters
detector_params = cv.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv.SimpleBlobDetector_create(detector_params)

#load image
img = cv.imread('/Users/jacob_kitz/Desktop/hgn_processing/HGN_Classification/Jake/Resources/Photos/woman.jpg')

cv.imshow('Woman Raw', img)

# Grayscale for detection

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# Face segmentation
for (x, y, z, h) in faces:
    cv.rectangle(img, (x, y), (x+z, y+h), (255, 255, 0), 2)
    
cv.imshow('Face Segmentation', img)

# Cut out the face
gray_face = gray[y:y+h, x:x+z]
face = img[y:y+h, x:x+z]
eyes = eye_cascade.detectMultiScale(gray_face)

# Eye segmentation
for (ex, ey, ew, eh) in eyes:
    cv.rectangle(face, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

cv.imshow('Eye Segmentation', img) # notice the problem with eyes detected around nose and mouth