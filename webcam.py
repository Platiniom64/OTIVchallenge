import numpy as np
import cv2 as cv
from datetime import datetime

# * --------- parameters of the module --------- 

# path to directory where the saved captures should go
DIRECTORY_CAPTURES = "captures/"


def main():

    cap = cv.VideoCapture(0)

    # set the frame rate of the capture
    cap.set(cv.CAP_PROP_FPS, 15)

    if not cap.isOpened():
        print("Cannot open camera, it is not connected")
        exit()

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        cv.imshow('frame', frame)
        

        # check if user wants to quit
        if cv.waitKey(1) == ord('q'):
            break

        # save the current frame if 's' key is pressed
        if cv.waitKey(1) == ord('s'):
            cv.imwrite(DIRECTORY_CAPTURES + "capture " + str(datetime.now()) + ".jpg", frame)


    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()