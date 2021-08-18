"""
The 4 step that we should take to have a good edge detection:
Step 1) Noise Reduction
    a Gaussian blur filter is used to essentially remove
    or minimize unnecessary detail that could lead to undesirable edges
Step 2) Calculating Intensity Gradient of the Image
"""
import cv2
import Utils as utils

# flag that use for turn on or off the webcam
use_webcam = False

# path to the image test
path_to_picture = "Pictures/Cart/cart2.jpeg"

# capture the video from the webcam
cap = cv2.VideoCapture(1)

# number that use for scaling down the input image
scale_factor = 3

# standard size of a4 paper
a4paper_width = 210 * scale_factor
a4paper_height = 297 * scale_factor


while True:
    if use_webcam:
        success, img = cap.read()
    else:
        img = cv2.imread(path_to_picture)

    # get countours of the image
    img, conts = utils.get_countours(
        img, show_canny=True, min_area=5000, filter=4)

    # if countoures is in the image
    if len(conts) != 0:
        # biggest countours in the image should be a4 paper
        # because conts are sorted so conts[0][2] is the biggest ara in the image
        biggest = conts[0][2]

        # we warp the image based on the biggest countours in the picture
        # whitch is a4 paper
        img_warp = utils.warp_image(
            img, biggest, a4paper_width, a4paper_height)

        # then for the second time get countours based on the warp image which is a4 paper
        img2, contours_in_a4_paper = utils.get_countours(
            img_warp, min_area=5000, filter=4,
            threshold=[20, 20], draw=False)

        # if contours is avalible in the a4 paper
        # which in our case is our rectangels
        if len(conts) != 0:
            for contours in contours_in_a4_paper:
                # we should reorder the main point of rectangle with correct order
                # because we want to calcucate the size of of the object it should be fixed
                # that means left upper shlould always be first element then right uppper and so
                nPoints = utils.reorder(contours[2])

                # calulate the distance between these 4 dots
                nW = round((utils.find_distance(
                    nPoints[0][0]//scale_factor, nPoints[1][0]//scale_factor)/10), 1)
                nH = round((utils.find_distance(
                    nPoints[0][0]//scale_factor, nPoints[2][0]//scale_factor)/10), 1)

                # Draw a line in the shape with 4 point, color, thickness, linetype, shif and tip length
                cv2.arrowedLine(img2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                                (0, 0, 255), 2, 8, 0, 0.07)
                cv2.arrowedLine(img2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                                (0, 0, 255), 2, 8, 0, 0.07)

                # contours[3] is the 4 dots of area of the contours in correct order
                x, y, w, h = contours[3]

                # Draw size of the object in half of the x and y
                cv2.putText(img2, '{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 0, ), 2)
                cv2.putText(img2, '{}cm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 0, ), 2)

        # Show final Image
        cv2.imshow('A4', img2)

    key_code = cv2.waitKey(1)
    if key_code == 13:
        cv2.destroyAllWindows()
        break
