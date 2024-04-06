import cv2 as cv

# img = cv .imread('Jake/photos/mr_kitty.jpeg')

# cv.imshow('Mr. Kitty', img)


capture = cv.VideoCapture('Jake/Resources/Videos/dog.mp4')

while True:
    isTrue, frame = capture.read()
    cv.imshow('Video', frame)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

capture.release()
cv.destroyAllWindows()