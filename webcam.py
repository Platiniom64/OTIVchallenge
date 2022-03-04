import numpy as np
import cv2 as cv
from datetime import datetime

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera, none connected")
    exit()



# path to directory where the saved captures should go
DIRECTORY_CAPTURES = "captures/"

while True:

    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

    # save the current frame is 's' key is pressed
    if cv.waitKey(1) == ord('s'):
        cv.imwrite(DIRECTORY_CAPTURES + "capture " + str(datetime.now()) + ".jpg", frame)



# When everything done, release the capture
cap.release()
cv.destroyAllWindows()