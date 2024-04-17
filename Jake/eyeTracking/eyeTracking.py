import cv2
import numpy as np


# init part
face_cascade = cv2.CascadeClassifier('Jake/Resources/HaarCascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('Jake/Resources/HaarCascades/haarcascade_eye.xml')
detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(detector_params)

class Eyes:
    def __init__(self):
        self.right_x = None
        self.right_y = None
        self.left_x = None
        self.left_y = None


def detect_faces(img, cascade):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = cascade.detectMultiScale(gray_frame, 1.3, 5)
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


def detect_eyes(img, cascade):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = cascade.detectMultiScale(gray_frame, 1.3, 5)  # detect eyes
    width = np.size(img, 1)  # get face frame width
    height = np.size(img, 0)  # get face frame height
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


def cut_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 4)
    img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)

    return img


def blob_process(img, threshold, detector):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=5)
    img = cv2.medianBlur(img, 5)
    keypoints = detector.detect(img)

    if keypoints:
        i = 0
        for keypoint in keypoints:
            if keypoint.size <10:
                keypoints[i].size = 0
            i+=1

        print(keypoints[0].size)
        cv2.imshow('blob', img)

    return keypoints, img

def take_center(keypoints):
    if keypoints:
        # Get the first keypoint
        k = keypoints[0]
        # Get the x, y coordinates and size of the keypoint
        x = k.pt[0]
        y = k.pt[1]
        # Return the center of the keypoint
        return int(x), int(y)
    else:
        return None
    
def adjust_threshold(img, initial_threshold, detector):
    threshold = initial_threshold
    for _ in range(255):  # range of possible threshold values
        keypoints = blob_process(img, threshold, detector)
        if len(keypoints) == 2:  # if two keypoints are detected (for two eyes)
            return threshold  # return the current threshold
        elif len(keypoints) < 2:  # if less than two keypoints are detected
            threshold += 1  # increase the threshold
        else:  # if more than two keypoints are detected
            threshold -= 1  # decrease the threshold
        if threshold < 0 or threshold > 255:  # if threshold is out of range
            break
    return threshold  # return the final threshold after the loop

def nothing(x):
    pass




def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')
    cv2.createTrackbar('threshold', 'image', 0, 255, nothing)
    threshold = 20
    while True:
        _, frame = cap.read()
        face_frame = detect_faces(frame, face_cascade)
        if face_frame is not None:
            eyes = detect_eyes(face_frame, eye_cascade)
            for eye in eyes:
                if eye is not None:
                    # threshold = adjust_threshold(face_frame, threshold, detector) # automatic threshold adjustment
                    threshold  = cv2.getTrackbarPos('threshold', 'image')
                    eye = cut_eyebrows(eye)
                    keypoints , blob = blob_process(eye, threshold, detector)
                    eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                    center = take_center(keypoints)
                    print(f'center: {center}')
        frame = cv2.flip(frame, 1)
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()