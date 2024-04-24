import cv2 as cv
import numpy as np

# Load Haar cascades
eye_cascade = cv.CascadeClassifier('Jake/Resources/HaarCascades/haarcascade_eye.xml')
face_cascade = cv.CascadeClassifier('Jake/Resources/HaarCascades/haarcascade_frontalface_default.xml')

# Load img detector parameters
detector_params = cv.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv.SimpleBlobDetector_create(detector_params)

#load image
img = cv.imread('Jake/Resources/Photos/woman.jpg')

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

# commented to not show the incorrect segmentations in screenshots
# Eye segmentation
#for (ex, ey, ew, eh) in eyes:
 #   cv.rectangle(face, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

cv.imshow('Eye Segmentation', img) # notice the problem with eyes detected around nose and mouth




# Eye Correction
width = np.size(img, 1)  # get face frame width
height = np.size(img, 0)  # get face frame height

print(f'width: {width}, height: {height}')

eyes_corrected = []
for (x, y, w, h) in eyes:
        print(f'x: {x}, y: {y}, w: {w}, h: {h}')
        if y > 200:
            pass
        else:
            eyes_corrected.append((x, y, w, h))
        
for (ex, ey, ew, eh) in eyes_corrected:
    cv.rectangle(face, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
cv.imshow('Eye Segmentation Corrected', img)

# pull eye img
x, w, y, h = eyes_corrected[0]
eye = face[y:y+h, x:x+w]
cv.imshow('Eye', eye)

# cut out eyebrows
def cut_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 4)
    img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)

    return img

eye_no_brow = cut_eyebrows(eye)
cv.imshow('no brow', eye_no_brow)

# blob processing
def blob_process(img, threshold, detector):
    gray_frame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, img = cv.threshold(gray_frame, threshold, 255, cv.THRESH_BINARY)
    img = cv.erode(img, None, iterations=2)
    img = cv.dilate(img, None, iterations=5)
    img = cv.medianBlur(img, 5)
    img = cv.erode(img, None, iterations=5)
    keypoints = detector.detect(img)

    cv.imshow('blob', img)

    return keypoints

# blob processing
keypoints = blob_process(eye_no_brow, 55, detector)

# draw keypoints
#key = cv.drawKeypoints(eye_no_brow, keypoints, eye_no_brow, (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#cv.imshow('keypoints', eye_no_brow)

# only keep center keypoint
def keep_center_keypoint(keypoints):
    center_keypoint = None
    eye_center = [len(eye_no_brow[0]) // 2, len(eye_no_brow) // 2]  # center of the eye
    min_distance = float('inf')

    for keypoint in keypoints:
        keypoint_center = [keypoint.pt[0], keypoint.pt[1]]  # center of the keypoint
        distance = (keypoint_center[0] - eye_center[0]) ** 2 + (keypoint_center[1] - eye_center[1]) ** 2  # calculate the distance
        if distance < min_distance:
            min_distance = distance
            center_keypoint = keypoint

    keypoints = [center_keypoint] if center_keypoint is not None else []

    return keypoints

keypoints = keep_center_keypoint(keypoints)

# draw keypoints on eye
key = cv.drawKeypoints(eye_no_brow, keypoints, eye_no_brow, (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv.imshow('keypoints', img)


# Wait for a key press and close all windows
cv.waitKey(0)
cv.destroyAllWindows()