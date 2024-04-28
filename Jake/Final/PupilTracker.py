import cv2 as cv
import numpy as np
import Eye
import csv

class PupilTracker:
    def __init__(self):
        self.face_cascade = cv.CascadeClassifier('Jake/Resources/HaarCascades/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv.CascadeClassifier('Jake/Resources/HaarCascades/haarcascade_eye.xml')
        self.detector_params = cv.SimpleBlobDetector_Params()
        self.detector_params.filterByArea = True
        self.detector_params.maxArea = 1500
        self.detector = cv.SimpleBlobDetector_create(self.detector_params)
        self.fourcc = cv.VideoWriter_fourcc(*'MP4V')


    def detect_faces(self, img):
            gray_frame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            coords = self.face_cascade.detectMultiScale(gray_frame, 1.3, 5) # coordinates of the face
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
            return frame # face frame
            
    def detect_eyes(self, img):
        gray_frame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        eyes = self.eye_cascade.detectMultiScale(gray_frame, 1.3, 5)  # detect eyes
        width = np.size(img, 1)  # get face frame width
        height = np.size(img, 0)  # get face frame height
        eyeA = None
        eyeB = None
        sides = []

        if len(eyes) == 2:
            for (x, y, w, h) in eyes:
                    if y > height / 2:
                        pass
                    eyecenter = x + w / 2  # get the eye center
                    if eyecenter < width * 0.5:
                        sides.append(0) # 0 is left side of face
                        eyeA = img[y:y + h, x:x + w]
                    else:
                        sides.append(1) # 1 is right side of face
                        eyeB = img[y:y + h, x:x + w]
            
        return eyeA, eyeB, sides # eye frames and their side of the face
       

    def cut_eyebrows(self, img):
        height, width = img.shape[:2]
        eyebrow_h = int(height / 4)
        img = img[eyebrow_h:height, 0:width]
        return img
    
    def blob_process(self, eye_frame, threshold):
        eye_frame = cv.cvtColor(eye_frame, cv.COLOR_BGR2GRAY)
        _, eye_frame = cv.threshold(eye_frame, threshold, 255, cv.THRESH_BINARY)
        eye_frame = cv.erode(eye_frame, None, iterations=2)
        eye_frame = cv.dilate(eye_frame, None, iterations=4)
        eye_frame = cv.medianBlur(eye_frame, 5)
        keypoints = self.detector.detect(eye_frame) # find blob keypoints

        # remove small keypoints (can be adjusted depending on person)
        if keypoints:
            i = 0
            for keypoint in keypoints:
                if keypoint.size <15:
                    keypoints[i].size = 0
                i+=1

            return keypoints
        else:
            return None

    # callback function for trackbar
    def nothing(self, x):
        pass


    # process on live video
    def runLive(self, output):

        # video capture
        cap = cv.VideoCapture(0)
        cv.namedWindow('image')
        cv.createTrackbar('threshold', 'image', 0, 255, self.nothing)
        threshold = 20

        # position storage for each eye
        leftEye = Eye.Eye()
        rightEye = Eye.Eye()

        # magnitude storage for each eye (pupil to center of eye vector magnitude)
        leftEyeVectors = []
        rightEyeVectors = []
        
        # data acquisition loop
        while True:
            _, frame = cap.read()

            # commented out to allow for eye detection w/o full face detection
            face_frame = self.detect_faces(frame)
            if face_frame is not None:

                eyeA, eyeB, sides = self.detect_eyes(frame)
                eyes = [eyeA, eyeB]

                idx = 0 # index for sides

                # for each eye edtected
                for eye in eyes:
                    if eye is not None:

                        # keypoint acquisition
                        threshold  = cv.getTrackbarPos('threshold', 'image')
                        eye = self.cut_eyebrows(eye)
                        keypoints = self.blob_process(eye, threshold)
                        eye = cv.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                        # keypoint storage
                        if keypoints is not None:
                            if sides[idx] == 0:
                                leftEye.x, leftEye.y = keypoints[0].pt[0], keypoints[0].pt[1]
                                leftEye.center_x, leftEye.center_y = eye.shape[1] / 2, eye.shape[0] / 2
                            else:
                                rightEye.x, rightEye.y = keypoints[0].pt[0], keypoints[0].pt[1]
                                rightEye.center_x, rightEye.center_y = eye.shape[1] / 2, eye.shape[0] / 2

                        idx += 1 # increment index
            
            # debug
            print('---------')
            print('Left Eye: ', leftEye.x, leftEye.y)
            print('Right Eye: ', rightEye.x, rightEye.y)

            # magnitude calculation and storage
            if leftEye.x is not None and rightEye.x is not None:
                magnitudeL= leftEye.magnitude()
                print('Left Eye Center to Pupil Vector Magnitude: ', magnitudeL)
                MagnitudeR = rightEye.magnitude()
                print('Right Eye Center to Pupil Vector Magnitude: ', MagnitudeR)

                # storage
                leftEyeVectors.append(magnitudeL)
                rightEyeVectors.append(MagnitudeR)

            
            # look like mirror
            frame = cv.flip(frame, 1)

            # display
            cv.imshow('image', frame)

            # exit condition
            if cv.waitKey(1) & 0xFF == ord('q'):

                # write to csv
                with open(output, 'a', newline='') as file:
                    writer = csv.writer(file)

                    for i in range(len(leftEyeVectors)):
                        writer.writerow([leftEyeVectors[i], rightEyeVectors[i]])

                cap.release()
                cv.destroyAllWindows()
                
                print('Data Acquisition Complete')
                break

    # process stored mp4 video
    def runVideo(self, video, threshold, output):

        cap = cv.VideoCapture(video)
        cv.namedWindow('image')

        # position storage for each eye
        leftEye = Eye.Eye()
        rightEye = Eye.Eye()

        # magnitude storage for each eye (pupil to center of eye vector magnitude)
        leftEyeVectors = []
        rightEyeVectors = []
        
        # data acquisition loop
        while cap.isOpened():
            _, frame = cap.read()

            if frame is None:
                break

            # commented out to allow for eye detection w/o full face detection
            face_frame = self.detect_faces(frame)
            if face_frame is not None:

                eyeA, eyeB, sides = self.detect_eyes(frame)
                eyes = [eyeA, eyeB]

                idx = 0 # index for sides

                # for each eye edtected
                for eye in eyes:
                    if eye is not None:

                        # keypoint acquisition
                        eye = self.cut_eyebrows(eye)
                        keypoints = self.blob_process(eye, threshold)
                        eye = cv.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                        # keypoint storage
                        if keypoints is not None:
                            if sides[idx] == 0:
                                leftEye.x, leftEye.y = keypoints[0].pt[0], keypoints[0].pt[1]
                                leftEye.center_x, leftEye.center_y = eye.shape[1] / 2, eye.shape[0] / 2
                            else:
                                rightEye.x, rightEye.y = keypoints[0].pt[0], keypoints[0].pt[1]
                                rightEye.center_x, rightEye.center_y = eye.shape[1] / 2, eye.shape[0] / 2

                        idx += 1 # increment index
            

            # debug
            print('---------')
            print('Left Eye: ', leftEye.x, leftEye.y)
            print('Right Eye: ', rightEye.x, rightEye.y)

            # magnitude calculation and storage
            if leftEye.x is not None and rightEye.x is not None:
                magnitudeL= leftEye.magnitude()
                print('Left Eye Center to Pupil Vector Magnitude: ', magnitudeL)
                MagnitudeR = rightEye.magnitude()
                print('Right Eye Center to Pupil Vector Magnitude: ', MagnitudeR)

                # storage
                leftEyeVectors.append(magnitudeL)
                rightEyeVectors.append(MagnitudeR)

        # write to csv
        with open(output, 'w', newline='') as file:
            writer = csv.writer(file)

            for i in range(len(leftEyeVectors)):
                writer.writerow([leftEyeVectors[i], rightEyeVectors[i], 1])

        cap.release()
        cv.destroyAllWindows()

        print('Data Acquisition Complete')

    # record video
    def record(self, output):
        cap = cv.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        out = cv.VideoWriter(output, self.fourcc, 20.0, (640, 480))

        while True:
            ret, frame = cap.read()
            out.write(frame)

            # flip the frame in the x-axis
            frame = cv.flip(frame, 1)
            cv.imshow('original', frame)


            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv.destroyAllWindows()


