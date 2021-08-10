import cv2
import numpy as np
import cvzone
import os

from cvzone.SelfiSegmentationModule import SelfiSegmentation


def main():
    CAMERA_SIZE = (640, 480)
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FPS, 60)
    segmentor = SelfiSegmentation()
    fps_reader = cvzone.FPS()
    background_image_list = os.listdir("Pictures/background_pictures")
    img_List = []
    index_image = 0
    for img_path in background_image_list:
        img = cv2.imread(f'Pictures/background_pictures/{img_path}')
        img = cv2.resize(img, CAMERA_SIZE) 
        img_List.append(img)
    



    while True:
        success, img = cap.read()
        if not success:
            continue
        img = cv2.resize(img, CAMERA_SIZE) 
        output = segmentor.removeBG(img, img_List[index_image], threshold=0.6)
        #img_stacked = cvzone.stackImages([img, output], 2, 1)
        #_, img_stacked = fps_reader.update(img_stacked, color=(0 ,0 ,255))
        #cv2.imshow('Image', img_stacked)
        cv2.imshow('output', output)
        
        
        key_code = cv2.waitKey(1)
        if key_code == ord('n'):
            if index_image < len(img_List) - 1:
                index_image +=1
        elif key_code == ord('p'):
            if index_image > 0:
                index_image -=1
        elif key_code == 13 or key_code == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()
