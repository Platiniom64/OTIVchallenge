import numpy as np
import cv2 as cv
from datetime import datetime
import time

# * --------- parameters of the module --------- 

# path to directory where the saved captures should go
DIRECTORY_CAPTURES = "captures/"


def main():

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera, it is not connected")
        exit()


    # set the webcam speed capture
    cap.set(cv.CAP_PROP_FPS, 15)

    # variables used to calculate the actual frame rate
    time_last_frame = time.time()
    time_current_frame = time.time()

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # display frame rate
        time_current_frame = time.time()
        time_elapsed = time_current_frame - time_last_frame
        frames_per_second = 1 / time_elapsed
        cv.putText(frame, "FPS: " + str("{:5.2f}".format(frames_per_second)), (10,100), font, 4,(255,255,255),2,cv.LINE_AA)
        time_last_frame = time_current_frame

        # check if user wants to quit
        if cv.waitKey(1) == ord('q'):
            break

        # save the current frame if 's' key is pressed
        if cv.waitKey(1) == ord('s'):
            cv.imwrite(DIRECTORY_CAPTURES + "capture " + str(datetime.now()) + ".jpg", frame)
        
        cv.imshow('frame', frame)


    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()