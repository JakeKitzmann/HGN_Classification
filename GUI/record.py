import cv2
import threading 

import time

def recordVideo():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_file = 'GUI/videoTests/output.mp4'
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (frame_width, frame_height))

    start_time = time.time()
    recording_duration = 5  # Duration in seconds

    while cap.isOpened() and time.time() - start_time < recording_duration:
        ret, frame = cap.read()
        print(time.time())
        if not ret:
            print("Error: Failed to read frame.")
            break

        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("recording ended")



'''
def recordVideo():
    # Create a VideoCapture object to capture video from the default webcam (usually index 0)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    # Define the codec and create a VideoWriter object
    # FourCC is a 4-byte code used to specify the video codec
    # 'XVID' is a widely supported codec, but you may need to change it based on your system
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # Set the output file name and format
    output_file = 'GUI/videoTests/output.avi'
    # Set the frame width and height (adjust these values as needed)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # Create the VideoWriter object
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (frame_width, frame_height))

    # Capture video until the user presses 'q' to quit
    while cap.isOpened() :
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            print("Error: Failed to read frame.")
            break

        # Display the frame
        #cv2.imshow('Webcam', frame)

        # Write the frame to the output file
        out.write(frame)

        # Check for the 'q' key press to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

'''