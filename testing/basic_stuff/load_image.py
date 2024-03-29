import cv2 as cv

# Load the image
image = cv.imread('/Users/jacob_kitz/Desktop/hgn_processing/HGN_Classification/testing/mr_kitty.jpeg')

# Check if image loading was successful
if image is None:
    print('Could not open or find the image')
else:
    # Display the image
    cv.imshow('image', image)

    # img instantly closes w/o this
    cv.waitKey(0) # wait for key    
    cv.destroyAllWindows() # close the window