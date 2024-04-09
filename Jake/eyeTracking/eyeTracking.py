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

# Eye function
def detect_eyes(img, classifier):
    gray_frame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray_frame, 1.3, 5)# detect eyes
    width = np.size(img, 1) # get face frame width
    height = np.size(img, 0) # get face frame height

    left_eye = None
    right_eye = None

    for (x, y, w, h) in eyes:
        if y > height / 2:
            pass

        eyecenter = x + w / 2  # get the eye center

        if eyecenter < width * 0.5:
            left_eye = img[y:y + h, x:x + w]
        else:
            right_eye = img[y:y + h, x:x + w]

    return left_eye, right_eye

# Face function
def detect_faces(img, classifier):
    gray_frame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    coords = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1:
        biggest = coords
    else:
        return None
    for (x, y, w, h) in biggest:
        frame = img[y:y + h, x:x + w]
    return frame

# eyebrow removal
def remove_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 4) # eyebrow is the first 1/4 of the image every time
    img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)

    return img

# blob detection
# might have to make a function to remove edge of eyes as well, shadow can be a problem
def process_blobs(img, threshold, detector):
    gray_frame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, img = cv.threshold(gray_frame, threshold, 255, cv.THRESH_BINARY)
    img = cv.erode(img, None, iterations=2)
    img = cv.dilate(img, None, iterations=4)
    img = cv.medianBlur(img, 5)
    keypoints = detector.detect(img)
    return keypoints

def nothing(x):
    pass

def main():
    cap = cv.VideoCapture(0)
    cv.namedWindow('Pupil Tracker')
    cv.createTrackbar('threshold', 'image', 0, 255, nothing)
    while True:
        _, frame = cap.read()
        face_frame = detect_faces(frame, face_cascade)
        if face_frame is not None:
            eyes = detect_eyes(face_frame, eye_cascade)
            for eye in eyes:
                if eye is not None:
                    threshold = cv.getTrackbarPos('threshold', 'image')
                    eye = remove_eyebrows(eye)
                    keypoints = process_blobs(eye, threshold, detector)
                    eye = cv.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv.imshow('image', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()