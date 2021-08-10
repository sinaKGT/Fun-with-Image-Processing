import cv2
import numpy as np
import cvzone
import os


from cvzone.SelfiSegmentationModule import SelfiSegmentation

cap = cv2.VideoCapture(1)
while True:
    success, img = cap.read()

    segmentor = SelfiSegmentation()
    fps_reader = cvzone.FPS()
    output = segmentor.removeBG(img, (255, 0, 0), threshold=0.7)
    cv2.imshow("Image", output)

    key_code = cv2.waitKey(1)
    if key_code == 13 or key_code == ord('q'):
        cv2.destroyAllWindows()
        break
