import numpy as np
import cv2
from lane_detection import draw_lanes


def draw_lines(img, lines):
    # lines has coordinate in array like [[[x1,y1,x2,y2]], [[....]]]
    try:
        for line in lines:
            # line is [[x1,y1,x2,y2]] and line[0] is [x1,y1,x2,y2]
            # coords is [x1,y1,x2,y2] and coords[0] is x1 and so on
            coords = line[0]
            # cv2.line draws line in img. its parameter are (image, from:(x1,y1), to:(x2,y2), color[R,G,B],
            # width of line in pixel)
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 255], 3)
    except Exception as e:
        print(str(e))


def region_of_interest(img, vertices):
    # creating blank mask same size as img
    mask = np.zeros_like(img)
    # filling the desired vertices polygon with 255 i.e 1
    cv2.fillPoly(mask, vertices, 255)
    # now only the desired area is 1 and other is 0
    masked_img = cv2.bitwise_and(img, mask)

    return masked_img


def process_img(image):
    org_image = image
    # Converting to grayscale
    grayscale = cv2.cvtColor(org_image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('window3', grayscale)
    # edge detection
    processed_image = cv2.Canny(grayscale, threshold1=150, threshold2=250)
    cv2.imshow('window3', processed_image)
    # creating vertices for region of interest

    # 6 sides polygon
    vertices = np.array([[10, 500], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500]])
    # 10 sides polygon remove hood or something right in front of car from region of interest
    vertices2 = np.array(
        [[10, 500], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500], [700, 500], [500, 400], [300, 400],
         [100, 500]])
    processed_image = region_of_interest(processed_image, [vertices2])

    # Added Gaussian blur               src_img         kernel_size     sigmaX
    processed_image = cv2.GaussianBlur(processed_image, (5, 5), 0)
    # Note: If sigmaX is set to 0, the standard deviation is computed based on the kernel size.
    # Higher values of sigmaX result in a wider and smoother blur.

    # HoughLines is technique used for detecting straight lines in an image.
    # The P stands for probabilistic Hough line transform which is more efficient.
    # Parameter: (src_image, rho, theta, threshold, minLineLength, maxLineGap)
    lines = cv2.HoughLinesP(processed_image, 1, np.pi / 180, 180, np.array([]), 100, 5)
    # draw_lines(processed_image, lines)
    m1 = 0
    m2 = 0
    try:
        # getting 2 line l1 and l2 to draw
        l1, l2 , m1, m2= draw_lanes(org_image, lines)
        # drawing lines on original image
        cv2.line(org_image, (l1[0], l1[1]), (l1[2], l1[3]), [255, 0, 0], 10)
        cv2.line(org_image, (l2[0], l2[1]), (l2[2], l2[3]), [255, 0, 0], 10)
    except Exception as e:
        print(str(e))

    return processed_image, org_image, m1, m2



