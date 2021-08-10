import cv2
import mediapipe as mp
import time


class HandDetector():
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            mode, max_hands, detection_confidence, tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for hand_land_mark in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, hand_land_mark, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_number=0, draw=True):
        landmark_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_number]
            for id, landmark in enumerate(my_hand.landmark):
                hight, witdh, channel = img.shape
                cx, cy = int(landmark.x*witdh), int(landmark.y*hight)
                landmark_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return landmark_list


def main():
    cap = cv2.VideoCapture(1)
    detector = HandDetector()
    currunt_time = 0
    previous_time = 0

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        land_mark_positions = detector.find_position(img)
        # Show FPS On Screen
        currunt_time = time.time()
        fps = 1/(currunt_time - previous_time)
        previous_time = currunt_time
        cv2.putText(img, str(int(fps)), (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 0, 255), 3)

        cv2.imshow('Image', img)
        key_code = cv2.waitKey(1)
        if key_code == 13:
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
