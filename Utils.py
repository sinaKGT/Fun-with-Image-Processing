import cv2
import numpy as np


def get_countours(img, threshold=[100, 100], show_canny=False, min_area=1000, filter=0, draw=False):

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # This is use for nose reduction
    img_blur = cv2.GaussianBlur(gray_img, (7, 7), 0)

    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    img_canny = cv2.Canny(img_blur, threshold[0], threshold[1])

    kernel = np.ones((2, 2))
    img_dialataion = cv2.dilate(img_canny, kernel, iterations=2)
    img_threshold = cv2.erode(img_dialataion, kernel, iterations=2)

    if show_canny:
        # Resize image
        img_canny = cv2.resize(img_canny, (590, 851))
        cv2.imshow("image", img_canny)

    countours, hiearchy = cv2.findContours(
        img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    final_countours = []
    for i in countours:
        area = cv2.contourArea(i)
        if area > min_area:
            peri = cv2.arcLength(i, True)
            # True means out contour is closed
            approximation = cv2.approxPolyDP(i, 0.02*peri, True)
            bonunding_box = cv2.boundingRect(approximation)
            # filter is number of points
            # for example rectacgle has 4 dots and we should filter the result by 4 dot so
            # we just have a shapes with 4 dots
            if filter > 0:
                if len(approximation) == filter:
                    final_countours.append(
                        [len(approximation), area, approximation, bonunding_box, i])
            else:
                final_countours.append(
                    [len(approximation), area, approximation, bonunding_box, i])
    final_countours = sorted(final_countours, key=lambda x: x[1], reverse=True)

    if draw:
        for con in final_countours:
            cv2.drawContours(img, con[4], -1, (0, 0, 255), 3)

    return img, final_countours


def reorder(my_points):
    # print("This is my points")
    # print(my_points.shape)
    my_new_points = np.zeros_like(my_points)
    my_points = my_points.reshape((4, 2))
    add = my_points.sum(1)
    my_new_points[0] = my_points[np.argmin(add)]
    my_new_points[3] = my_points[np.argmax(add)]
    diff = np.diff(my_points, axis=1)
    my_new_points[1] = my_points[np.argmin(diff)]
    my_new_points[2] = my_points[np.argmax(diff)]
    return my_new_points


def warp_image(img, points, width, hight, pad=20):
    # print(points)
    points = reorder(points)

    point1 = np.float32(points)
    point2 = np.float32([[0, 0], [width, 0], [0, hight], [width, hight]])
    matrix = cv2.getPerspectiveTransform(point1, point2)
    img_warp = cv2.warpPerspective(img, matrix, (width, hight))
    img_warp = img_warp[pad:img_warp.shape[0] - pad, pad:img_warp.shape[1]-pad]
    return img_warp


def find_distance(point1, point2):
    return ((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)**0.5
