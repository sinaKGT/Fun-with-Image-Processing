import cv2
import mediapipe as mp
import time
import os

from time import sleep
from datetime import datetime
from mediapipe.python.solutions import face_detection



cap = cv2.VideoCapture(1)




mp_face_detection = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(0.75)





previous_time = 0
current_time = 0
while True:
    TIMER = 30
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = face_detection.process(img_rgb)
    if results.detections:
        for id, detection in enumerate(results.detections):
            bounding_box = detection.location_data.relative_bounding_box
            image_height, image_width, image_channel = img.shape
            bounding_box = int(bounding_box.xmin * image_width), int(bounding_box.ymin * image_height), \
                            int(bounding_box.width * image_width), int(bounding_box.height * image_height)

            cv2.rectangle(img, bounding_box, (255, 0, 0), 2)
            cv2.putText(img, f'{int(detection.score[0]*100)}%', (bounding_box[0], bounding_box[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                1, (255, 0, 0), 2)

            print("Someone is in the picture")
            capture_time = time.ctime()
            name = str(capture_time) + ".jpg"
            name = name.replace(" ", "-")
            name = name.replace(":", "-")
            path = "Interance/"+name
            cv2.imwrite(path, img)
            # tell the program to wait for 10 second
            cv2.waitKey(10000)
        else:
            pass
 
    key_code = cv2.waitKey(1)
    if key_code == 13:
        cv2.destroyAllWindows()
        break