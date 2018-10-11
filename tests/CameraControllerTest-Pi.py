#!/usr/bin/python3
import cv2
import sys
sys.path.append('..')
from CameraController import CameraController
import time
import RPi.GPIO as GPIO

if __name__ == '__main__':

    print("Starting camera controller...")
    cam = CameraController.CameraController(use_splitter_port=True)
    cam.start()

    switch = 22
    GPIO.setmode(GPIO.BCM)
    gpio.setwarnings(False)
    GPIO.setup(22, GPIO.IN, GPIO.PUD_UP)

    cv2.namedWindow("Output", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Output", cv2.WND_PROP_FULLSCREEN, 1)

    while True:
        if GPIO.input(22) == False:
            print("Button pressed.")
            current_high_res_frame = cam.get_splitter_image()
            cv2.imwrite('high_res_image.jpg', current_high_res_frame)
            time.sleep(0.2)

        current_frame = cam.get_image()

        if current_frame is not None:
            cv2.imshow("Output", current_frame)

        key = cv2.waitKey(10)
