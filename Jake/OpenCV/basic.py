import cv2 as cv

img = cv.imread('Jake/Resources/Photos/lady.jpg')
cv.imshow('Cat', img)

# convert to greyscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

# blur
blur = cv.GaussianBlur(gray, (3,3), cv.BORDER_DEFAULT) # (7,7) is the kernel size (must be odd numbers)
cv.imshow('Blur', blur)

# edge cascade, using blur to reduce amount of edges
# more blur = less edges
canny = cv.Canny(blur, 125, 175) # 125 is the lower threshold, 175 is the upper threshold
cv.imshow('Canny Edges', canny)

# dilating the image, dilating is making the edges thicker
dilated = cv.dilate(canny, (3,3), iterations=3) # iterations is how many times you want to dilate
cv.imshow('Dilated', dilated)

# eroding, opposite of dilating -- doesn't work perfectly but it brings it close back to normal
eroded = cv.erode(dilated, (3,3), iterations=3)
cv.imshow('Eroded', eroded)

# resize
resized = cv.resize(img, (500,500), interpolation=cv.INTER_AREA) # INTER_LINEAR is the default (better for shrinking), INTER_CUBIC is better for enlarging, INTER_LANCZOS4 is the best for shrinking
# inter_cubic is the slowest
cv.imshow('Resized', resized)

# cropping
cropped = img[50:200, 200:400]
cv.imshow('Cropped', cropped)




cv.waitKey(0)