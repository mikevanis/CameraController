#!/usr/bin/python
from CameraController import CameraController
import cv2
import time
import RPi.GPIO as GPIO

if __name__ == '__main__':

    print("Starting camera controller...")
    cam = CameraController(use_splitter_port=True)
    cam.start()

    switch = 22
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(switch, GPIO.IN, GPIO.PUD_UP)

    cv2.namedWindow("Output", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Output", cv2.WND_PROP_FULLSCREEN, 1)

    while True:
        if GPIO.input(switch) is False:
            current_high_res_frame = cam.get_splitter_image()
            cv2.imwrite('high_res_image.jpg', current_high_res_frame)
            time.sleep(0.2)

        current_frame = cam.get_image()

        if current_frame is not None:
            cv2.imshow("Output", current_frame)

        key = cv2.waitKey(10)
