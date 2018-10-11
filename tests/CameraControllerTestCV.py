import os
os.chdir("/home/pi/CameraController/tests")
import sys
sys.path.append('..')
from CameraController import CameraController
import cv2
import imutils

if __name__ == '__main__':
    # Create new instance
    cam = CameraController()
    cam.start()

    #cv2.namedWindow("Output", cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty("Output", cv2.WND_PROP_FULLSCREEN, 1)

    try:
        while True:
            # Get latest frame and display it
            current_frame = cam.get_image()

            if current_frame is not None:
                lines = imutils.auto_canny(current_frame)
                cv2.imshow("Output", lines)

            key = cv2.waitKey(10)

    except KeyboardInterrupt:
        cam.stop()
        cam.join()
        cv2.destroyAllWindows()
        pass