import threading
import cv2
import numpy as np
import imutils
import time
import logging
try:
    import picamera
    import picamera.array
    picamera_exists = True
except ImportError:
    picamera = None
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

        # Truncate and open log file
        with open('camera_controller.log', 'w'):
            pass
        logging.basicConfig(filename='camera_controller.log', level=logging.DEBUG)

        if picamera_exists:
            # Use pi camera
            logging.info("picamera module exists.")
            camera = picamera.PiCamera()
            camera.framerate = 30

            if use_splitter_port is True:
                logging.info("Using splitter port")
                camera.resolution = (self.splitter_width, self.splitter_height)
                self.picamera_splitter_capture = picamera.array.PiRGBArray(camera)
                self.picamera_capture = picamera.array.PiRGBArray(camera, size=(self.width, self.height))
                self.picamera_splitter_stream = camera.capture_continuous(self.picamera_splitter_capture, format="bgr",
                                                                          use_video_port=True)
                self.picamera_stream = camera.capture_continuous(self.picamera_capture, format="bgr",
                                                                 use_video_port=True, splitter_port=2,
                                                                 resize=(self.width, self.height))

            else:
                camera.resolution = (self.width, self.height)
                self.picamera_capture = picamera.array.PiRGBArray(camera)
                self.picamera_stream = camera.capture_continuous(self.picamera_capture, format="bgr",
                                                                 use_video_port=True)
                time.sleep(2)

        else:
            # Use webcam
            logging.info("picamera module not found. Using oCV VideoCapture instead.")
            self.capture = cv2.VideoCapture(0)

            if use_splitter_port is True:
                logging.info("Using splitter port")
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
                s = self.picamera_stream.next()
                self.image = s.array
                self.picamera_capture.truncate(0)
                self.picamera_capture.seek(0)

                if self.image is None:
                    logging.warning("Got empty image.")

            else:
                # Get image from webcam
                if self.use_splitter_port:
                    ret, self.splitter_image = self.capture.read()
                    self.image = imutils.resize(self.splitter_image, width=self.width, height=self.height)
                else:
                    ret, self.image = self.capture.read()

                if self.image is None:
                    logging.warning("Got empty image.")

    def stop(self):
        self._stop_event.set()

        if picamera_exists:
            # Close pi camera
            pass
        else:
            # Close webcam
            cv2.VideoCapture(0).release()

        logging.info('Cancelling...')

    def is_stopped(self):
        return self._stop_event.is_set()

    def get_image(self):
        return self.image

    def get_splitter_image(self):
        logging.info("Requested splitter image.")
        if self.use_splitter_port:
            if picamera_exists:
                s = self.picamera_splitter_stream.next()
                self.picamera_splitter_capture.truncate(0)
                self.picamera_splitter_capture.seek(0)
                return s.array

            else:
                return self.splitter_image
        else:
            logging.warning("Splitter image was not opened in constructor.")
            return None
