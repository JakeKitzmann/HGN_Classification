import cv2 as cv

# Load an image
img = cv.imread('/Users/jacob_kitz/Desktop/hgn_processing/HGN_Classification/testing/image_processing/mr_kitty.jpg')

# Check if image is loaded fine
if img is None:
    print('Could not open or find the image')
else:
    print('Image loaded successfully')

