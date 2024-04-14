import cv2 as cv

img = cv.imread('Jake/Resources/Photos/cat_large.jpg')

def rescaleFrame(frame, scale = 0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

# only works for LIVE video
def changeRes(width, height):
    capture.set(3, width)
    capture.set(4, height)

    return

capture = cv.VideoCapture('Jake/Resources/Videos/dog.mp4')

# while True:
#     isTrue, frame = capture.read()
#     frame_resized = rescaleFrame(frame, scale=0.4)
#     cv.imshow('Video', frame)
#     cv.imshow('Video Resized', frame_resized)

#     if cv.waitKey(20) & 0xFF==ord('d'):
#         break

cv.waitKey(0)