from CameraController import CameraController
import cv2

if __name__ == '__main__':
    cam = CameraController()
    cam.start()

    cv2.namedWindow("Output", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Output", cv2.WND_PROP_FULLSCREEN, 1)

    try:
        while True:
            current_frame = cam.get_image()

            if current_frame is not None:
                cv2.imshow("Output", current_frame)

            key = cv2.waitKey(10)

    except KeyboardInterrupt:
        cam.stop()
        cam.join()
        cv2.destroyAllWindows()
        pass