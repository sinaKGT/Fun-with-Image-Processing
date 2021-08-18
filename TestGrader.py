import cv2 
import imutils
import numpy as np

from imutils import contours
from imutils.perspective import four_point_transform

answer_sheet_path = "Pictures/Sheet/1.png"

correct = 0
wrong = 0
ANSWER_KEY = {
    0: 0,
    1: 1,
    2: 2,
    3: 1,
    4: 2,
    5: 1,
    6: 0,
    7: 1,
    8: 1}
total_qus = len(ANSWER_KEY)

img = cv2.imread(answer_sheet_path)

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(gray_img, (5, 5), 0)
edged = cv2.Canny(blurred_image, 75, 200)



cnt = cv2.findContours(
    edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


cnt = imutils.grab_contours(cnt)


doc_cnt = None

if len(cnt) > 0:
    cnt = sorted(cnt, key=cv2.contourArea, reverse=True)
    for c in cnt:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            doc_cnt = approx
            break

paper = four_point_transform(img, doc_cnt.reshape(4, 2))
warped = four_point_transform(gray_img, doc_cnt.reshape(4, 2))


thresh = cv2.threshold(
    warped, 200, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

cnt = cv2.findContours(
    thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnt = imutils.grab_contours(cnt)
question_conturs = []

for c in cnt:
    (x, y, w ,h) = cv2.boundingRect(c)

    area = w / float(h)

    if w >= 20 and h >= 20 and area >= 0.9 and area <= 4.1:
        question_conturs.append(c)

for (q, i) in enumerate(np.arange(0, len(question_conturs), 4)):
    cnt = contours.sort_contours(question_conturs[i: i+4])[0]

    bubbled = None

    for (j, c) in enumerate(cnt):

        mask = np.zeros(thresh.shape, dtype='uint8')
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)

        if bubbled is None or total > bubbled[0]:
            bubbled = (total, j)
        color = (0, 0, 255)
        k = ANSWER_KEY[q]
        if k == bubbled[1]:
            color = (0, 255, 0)
            correct += 1
            cv2.drawContours(paper, [cnt[k]], -1, color, 3)
        else:
            wrong += 1
            cv2.drawContours(paper, [cnt[k]], -1, (0, 0, 255), 3)


correct = ((correct//4) + 1)
wrong = (wrong//4)

score = (((correct*3) - wrong) / (3 * total_qus)) * 100
cv2.putText(paper, "Your Score is: {:.2f}%".format(score), (60, 460),
           cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (0, 0, 255), 2)

cv2.imshow("Exam Results", paper)

while True:
    key_code = cv2.waitKey(1)
    if key_code == 13:
        cv2.destroyAllWindows()
        break