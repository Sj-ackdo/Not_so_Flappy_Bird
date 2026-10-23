import mediapipe as mp
import cv2
import time
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import landmark_setup as setup

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

def hand_landmarker(cap):
    with HandLandmarker.create_from_options(setup.options) as landmarker:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty capture frame")
                continue

            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            timestamp_ms = time.monotonic_ns() // 1_000_000
            landmarker.detect_async(mp_image, timestamp_ms)
            
            #if setup.latest_frame is not None:
            #    cv2.imshow("hand", setup.latest_frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break


