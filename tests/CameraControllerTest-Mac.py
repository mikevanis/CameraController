import cv2
import sys
sys.path.append('..')
from CameraController import CameraController

if __name__ == '__main__':
    # Create new instance
    cam = CameraController.CameraController(use_splitter_port=True)
    cam.start()

    try:
        while True:
            # Get latest frame and display it
            current_frame = cam.get_image()
            current_splitter_frame = cam.get_splitter_image()

            if current_frame is not None:
                cv2.imshow("frame", current_frame)
            if current_splitter_frame is not None:
                cv2.imshow("splitter_frame", current_splitter_frame)

            key = cv2.waitKey(10)

    except KeyboardInterrupt:
        cam.stop()
        cam.join()
        cv2.destroyAllWindows()
        pass
