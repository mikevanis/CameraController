import threading
import cv2
import numpy as np
import imutils
try:
    import picamera
    picamera_exists = True
except ImportError:
    picamera_exists = False


class CameraController(threading.Thread):

    def __init__(self, width=320, height=240, use_splitter_port=False, splitter_width=1920, splitter_height=1080):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.cancelled = False

        self.width = width
        self.height = height
        self.use_splitter_port = use_splitter_port
        self.splitter_width = splitter_width
        self.splitter_height = splitter_height

        if picamera_exists:
            # Use pi camera
            print("INFO: picamera module exists.")
        else:
            # Use webcam
            print("INFO: picamera module not found. Using oCV VideoCapture instead.")
            self.capture = cv2.VideoCapture(0)

            if use_splitter_port is True:
                self.capture.set(3, splitter_width)
                self.capture.set(4, splitter_height)
            else:
                self.capture.set(3, width)
                self.capture.set(4, height)

        self.image = None
        self.splitter_image = None

    def run(self):
        while not self.is_stopped():
            if picamera_exists:
                # Get image from Pi camera
                pass
            else:
                # Get image from webcam
                if self.use_splitter_port:
                    ret, self.splitter_image = self.capture.read()
                    self.image = imutils.resize(self.splitter_image, width=self.width, height=self.height)
                else:
                    ret, self.image = self.capture.read()

                if self.image is None:
                    print("WARNING: Got empty image.")

    def stop(self):
        self._stop_event.set()

        if picamera_exists:
            # Close pi camera
            pass
        else:
            # Close webcam
            cv2.VideoCapture(0).release()

        print('Cancelling...')

    def is_stopped(self):
        return self._stop_event.is_set()

    def get_image(self):
        return self.image

    def get_splitter_image(self):
        if picamera_exists:
            pass
        else:
            return self.splitter_image
