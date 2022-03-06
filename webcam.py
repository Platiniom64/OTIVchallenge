import cv2 as cv
from datetime import datetime
import time
import pingparsing

# * --------- parameters of the module --------- 

# path to directory where the saved captures should go
DIRECTORY_CAPTURES = "captures/"

# host to get the rrt from
HOST = "google.com"
PING_PER_FRAME = 1      # number of packets that should be sent for calculating rtt to the host

# settings of camera
FPS = 15                # depends on the camera used


def main():

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera, it is not connected")
        exit()

    # set the webcam speed capture
    cap.set(cv.CAP_PROP_FPS, FPS)

    # variables used to calculate the actual frame rate
    time_last_frame = time.time()
    time_current_frame = time.time()

    # used for calculating the rtt
    trans = pingparsing.PingTransmitter()
    trans.destination = HOST
    trans.count = PING_PER_FRAME
    trans.timeout = str((1 / FPS) * 1000) + "ms"   # amount of ms for each frame
    outputTextRtt = ""

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # display frame rate
        time_current_frame = time.time()
        time_elapsed = time_current_frame - time_last_frame
        frames_per_second = 1 / time_elapsed
        cv.putText(frame, "FPS: " + str("{:5.2f}".format(frames_per_second)), (10,50), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2,cv.LINE_AA)
        time_last_frame = time_current_frame

        # display rtt to host
        result = trans.ping()
        if result.stderr != "":
            outputTextRtt = "ERROR : " + result.stderr
        else:
            result_parsed = pingparsing.PingParsing().parse(result)
            if (result_parsed.packet_loss_count) == PING_PER_FRAME:
                outputTextRtt = "packet lost, no reading"
            else:
                outputTextRtt = "rtt to " + HOST + " : " + "{:4.2f}".format(result_parsed.rtt_avg) + " ms"
        cv.putText(frame, outputTextRtt, (10,100), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2,cv.LINE_AA)


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