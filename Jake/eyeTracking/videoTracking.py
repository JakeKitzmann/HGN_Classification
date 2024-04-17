import cv2
import numpy as np


# init part
face_cascade = cv2.CascadeClassifier('/Users/jacob_kitz/Desktop/hgn_processing/HGN_Classification/Jake/Resources/HaarCascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/Users/jacob_kitz/Desktop/hgn_processing/HGN_Classification/Jake/Resources/HaarCascades/haarcascade_eye.xml')
detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(detector_params)


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

  #  print('face at time: ', cv2.getTickCount())
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

  
  #  print(f'eye at time: {cv2.getTickCount()}')
    return left_eye, right_eye


def cut_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 4)
    img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)

    return img


def blob_process(img, threshold, detector, eye):

    gray_eye = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_eye = cv2.GaussianBlur(gray_eye, (9, 9), 0)
    gray_eye = cv2.medianBlur(gray_eye, 3)
    

    _, img = cv2.threshold(gray_eye, threshold, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2)
    img = cv2.erode(img, None, iterations=7)
    keypoints = detector.detect(img)

    if len(keypoints) > 1:
        # calculate the center of the image
        h, w = img.shape[:2]
        center = (w / 2, h / 2)

        # calculate the distance of each keypoint from the center
        distances = [cv2.norm((kp.pt[0] - center[0], kp.pt[1] - center[1])) for kp in keypoints]

        # find the index of the keypoint closest to the center
        closest_index = np.argmin(distances)

        # keep only the closest keypoint
        keypoints = [keypoints[closest_index]]


    return keypoints, img, gray_eye


def nothing(x):
    pass


def main():
    cap = cv2.VideoCapture('/Users/jacob_kitz/Desktop/hgn_processing/HGN_Classification/Jake/Resources/Videos/oldie.mp4')
    cv2.namedWindow('image')
    cv2.createTrackbar('threshold', 'image', 0, 255, nothing)
    threshold = 55
    while True:
        _, frame = cap.read()
        face_frame = detect_faces(frame, face_cascade)
        eyeNum = 0
        if face_frame is not None:
            eyes = detect_eyes(face_frame, eye_cascade)
            for eye in eyes:
                if eye is not None:
                    #threshold  =  cv2.getTrackbarPos('threshold', 'image')
                    eye = cut_eyebrows(eye)
                    keypoints, thresholdedFrame, eyeFrame = blob_process(eye, threshold, detector, eyeNum)
                    #print(threshold)
                    eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                    eyeNum+= 1
        frame = cv2.flip(frame, 1)
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()