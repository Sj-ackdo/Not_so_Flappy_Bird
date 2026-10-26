import mediapipe as mp
import cv2
import time
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles

latest_frame = None
mid_hand = None

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

def draw_landmarks_on_image(rgb_image, detection_result):
    global mid_hand

    annotated_image = np.copy(rgb_image)
    if detection_result is None:
        mid_hand = None
        return annotated_image

    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    
    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        # Draw the hand landmarks.
        mp_drawing.draw_landmarks(
        annotated_image,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style())

        # Get the top left corner of the detected hand's bounding box.
        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        
        #for hand in hand_landmarks_list: 
        mid_hand = (int(sum(x_coordinates)/len(x_coordinates) * width), 
                    int(sum(y_coordinates)/len(y_coordinates) * height))
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        # Draw handedness (left or right hand) on the image.
        cv2.putText(annotated_image, f"{handedness[0].category_name}",
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

    return annotated_image

def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global latest_frame
    global annotated_image

    rgb_image = output_image.numpy_view()
    annotated_image = draw_landmarks_on_image(rgb_image, result)
    latest_frame = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
    print("frame: {}".format(result))

options = HandLandmarkerOptions(
    base_options = BaseOptions(model_asset_path='./hand_landmarker.task'),
    running_mode = VisionRunningMode.LIVE_STREAM,
    num_hands = 1,
    result_callback = print_result
)
