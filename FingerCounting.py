import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm


detector = htm.HandDetector(detection_confidence=0.8)
cap = cv2.VideoCapture(1)

FOLDER_PATH = 'Pictures/Fingers'

current_time = 0
previous_time = 0

image_list = os.listdir(FOLDER_PATH)

over_lay_list = []
for img_path in image_list:
    image = cv2.imread(f"{FOLDER_PATH}/{img_path}")
    image = cv2.resize(image, (90, 300))
    over_lay_list.append(image)

tips_id = [4, 6, 12, 16, 20]

while True:
    sucess, img = cap.read()
    img = detector.find_hands(img)
    land_mark_list = detector.find_position(img, draw=False)

    if len(land_mark_list) != 0:
        fingers = []

        if land_mark_list[tips_id[0]][1] > land_mark_list[tips_id[0] -1] [1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if land_mark_list[tips_id[id]] [2] < land_mark_list[tips_id[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        total_fingers = fingers.count(1)
        img[0:300, 0:90] = over_lay_list[total_fingers]

    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, f'FPS:{int(fps)}', (10, 340), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("web cam feed", img)
    key_code = cv2.waitKey(1)
    if key_code == 13:
        cv2.destroyAllWindows()
        break