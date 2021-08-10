# step1: hand trakcing
# step2: finger detection
# step3: select specifc finger
# step4: calculate distace between two finger
# step5: mapping finger distance to system volumn
# step6: control system volumn
import cv2
import numpy as np
import math
import HandTrackingModule as htm
import time

# This imports is for pycaw audio library
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def main():
    # Some Initialazation
    CIRCLE_RADIOUS = 10
    FINGER_DOT_COLOR = (255, 255, 255)
    LINE_COLOR = (255, 0, 0)
    current_time = 0
    previous_time = 0

    cap = cv2.VideoCapture(1)
    detector = htm.HandDetector(
        max_hands=1, detection_confidence=0.7, tracking_confidence=0.5)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume_range = volume.GetVolumeRange()
    min_volume = volume_range[0]
    max_volume = volume_range[1]
    vol = 0
    vol_bar = 400
    # Some Initialazation

    # This line is for change output size by mouse
    cv2.namedWindow("Hand Volumn Controler", cv2.WINDOW_FREERATIO)
    while True:
        success, img = cap.read()
        #img = cv2.resize(img, (700, 500))

        # Detecting hands by using our hand detector module
        detector.find_hands(img, draw=True)

        # Giving Landmarks for doing action by that
        landmark_list = detector.find_position(img, draw=False)

        if len(landmark_list) != 0:
            # The x and y cordinate of our fingers
            x1, y1 = landmark_list[4][1], landmark_list[4][2]
            x2, y2 = landmark_list[8][1], landmark_list[8][2]
            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

            # Draw small circle on the fingers position
            cv2.circle(img, (x1, y1), CIRCLE_RADIOUS,
                       FINGER_DOT_COLOR, cv2.FILLED)
            cv2.circle(img, (x2, y2), CIRCLE_RADIOUS,
                       FINGER_DOT_COLOR, cv2.FILLED)

            # Draw small circle on ther cernter of line between two finger point
            cv2.circle(img, (center_x, center_y), CIRCLE_RADIOUS +
                       4, FINGER_DOT_COLOR, cv2.FILLED)

            # Draw line between two finger
            cv2.line(img, (x1, y1), (x2, y2), LINE_COLOR, 3)

            length = math.hypot(x2 - x1, y2 - y1)

            # Hand Range 50, 300
            # Volumn Range min, max
            volume_value = np.interp(
                length, [50, 300], [min_volume, max_volume])
            vol_bar = np.interp(length, [50, 300], [400, 150])
            vol = np.interp(length, [50, 300], [0, 100])
            volume.SetMasterVolumeLevel(int(volume_value), None)

            # Change color based on touch
            if length < 50:
                cv2.circle(img, (center_x, center_y), CIRCLE_RADIOUS+4,
                           (0, 255, 0), cv2.FILLED)

            if length > 250:
                cv2.circle(img, (center_x, center_y), CIRCLE_RADIOUS+4,
                           (0, 0, 255), cv2.FILLED)

        # Draw progress bar
        cv2.rectangle(img, (48, 148), (87, 402), (0, 0, 0), 2)
        cv2.rectangle(img, (50, int(vol_bar)),
                      (85, 400), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f'{int(vol)} %', (40, 440), cv2.FONT_HERSHEY_DUPLEX,
                    1, (0, 0, 255), 3)

        # Calculte FPS of frame and write on screen
        current_time = time.time()
        fps = 1/(current_time - previous_time)
        previous_time = current_time
        cv2.putText(img, f"FPS:{int(fps)}", (15, 45), cv2.FONT_HERSHEY_DUPLEX,
                    1, (255, 0, 0), 2)

        cv2.imshow("Hand Volumn Controler", img)

        key_code = cv2.waitKey(1)
        if key_code == 13:
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
