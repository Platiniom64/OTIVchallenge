"""
This module shows the stream of frames from the webcam, and in parallel shows the rtt time to a host.
press   'q' to quit
        's' to save the current frame. By default the saved frames go to the 'captures' directory

external dependencies used:
    openscv         4.2.0
    pingparsing     1.4.0

Vladimir Hanin
07/03/2022
"""

import cv2 as cv
from datetime import datetime
import time
import pingparsing
import threading



# * --------- parameters of the module --------- 

DIRECTORY_CAPTURES = "captures/"    # path to directory where the saved captures should go

HOST = "google.com"                 # host to get the rrt from
NUM_PACKETS_PING = 3                # number of packets that should be sent for calculating rtt to the host
FPS = 15                            # fps of capture, depends on the camera used


# * --------- private variables
outputTextRtt = "calculating rtt to host ..."       # variable used between the two thead to display result of rtt
stopCalcuatingRtt = False                           # used as a flag for the secondary thread to stop




def ping_host():
    """
    method that represents the work that has to be done by secondary thread
    in order to calculate the rtt to the host.
    """

    global outputTextRtt  

    trans = pingparsing.PingTransmitter()
    trans.destination = HOST
    trans.count = NUM_PACKETS_PING
    trans.timeout = str(NUM_PACKETS_PING) + "sec"  # timeout of max 1 sec per packets

    while True:

        result = trans.ping()

        # if ping fails, it prints error to stderr stream
        if result.stderr != "":
            outputTextRtt = "PING ERROR : " + result.stderr

        # if ping succeeded
        else:

            result_parsed = pingparsing.PingParsing().parse(result)

            # if all packets were lot, can't get the average rtt
            if (result_parsed.packet_loss_count) == NUM_PACKETS_PING:
                outputTextRtt = "rtt packet(s) lost, no reading"

            else:
                outputTextRtt = "rtt to " + HOST + " : " + "{:4.2f}".format(result_parsed.rtt_avg) + " ms"
        
        if stopCalcuatingRtt:
            break

def main():
    """
    main method of the main thread.
    It starts the capture and the secondary threads.
    """

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera, it is not connected")
        exit()

    # set the webcam speed capture
    cap.set(cv.CAP_PROP_FPS, FPS)

    # variables used to calculate the actual frame rate
    time_last_frame = time.time()
    time_current_frame = time.time()

    # create secondary thread that calculates rtt
    threading.Thread(target=ping_host).start()


    while True:

        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # calculate and display frame rate
        time_current_frame = time.time()
        time_elapsed = time_current_frame - time_last_frame
        frames_per_second = 1 / time_elapsed
        cv.putText(frame, "FPS: " + str("{:5.2f}".format(frames_per_second)), (10,30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255),2,cv.LINE_AA)
        time_last_frame = time_current_frame

        # display rtt result
        cv.putText(frame, outputTextRtt, (10,60), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255),2,cv.LINE_AA)

        # check if user wants to quit
        if cv.waitKey(10) == ord('q'):
            break

        # save the current frame if 's' key is pressed
        if cv.waitKey(50) == ord('s'):
            cv.imwrite(DIRECTORY_CAPTURES + "capture " + str(datetime.now()) + ".jpg", frame)
        
        cv.imshow('webcam capture', frame)


    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

    # don't forget to stop secondary threads
    global stopCalcuatingRtt
    stopCalcuatingRtt = True

if __name__ == "__main__":
    main()