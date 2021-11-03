# This is a sample Python script.
import os
import re
import cv2
import numpy as np
from tqdm import tqdm_notebook
import matplotlib.pyplot as plt
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

yellow_HSV_th_min = np.array([0, 70, 70])
yellow_HSV_th_max = np.array([50, 255, 255])


def thresh_frame_in_HSV(frame, min_values, max_values, verbose=False):
    """
    Threshold a color frame in HSV space
    """
    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    min_th_ok = np.all(HSV > min_values, axis=2)
    max_th_ok = np.all(HSV < max_values, axis=2)

    out = np.logical_and(min_th_ok, max_th_ok)

    if verbose:
        plt.imshow(out, cmap='gray')
        plt.show()

    return out


def yellow_lines(frame):
    # create a zero array

    h, w = frame.shape[:2]
    binary = np.zeros(shape=(h, w), dtype=np.uint8)
    # highlight yellow lines by threshold in HSV color space
    HSV_yellow_mask = thresh_frame_in_HSV(frame, yellow_HSV_th_min, yellow_HSV_th_max, verbose=False)
    binary = np.logical_or(binary, HSV_yellow_mask)
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(binary.astype(np.uint8), cv2.MORPH_CLOSE, kernel)

    stencil = np.zeros_like(closing)

    w, h = closing.shape
    thres = int(np.floor(0.4 * h))
    # specify coordinates of the polygon
    polygon = np.array([[0, thres], [0, h], [900, h], [900, thres]])

    # fill polygon with ones
    cv2.fillConvexPoly(stencil, polygon, 1)

    # apply polygon as a mask on the frame
    closing = cv2.bitwise_and(closing, closing, mask=stencil)
    return cv2.HoughLinesP(closing, 140, np.pi / 180, 200, minLineLength=20, maxLineGap=10)


def detect():
    img1 = cv2.imread('lubin18.jpg')
    yellowlines = yellow_lines(img1)
    img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img = 255 - img

    w, h = img.shape
    # create a zero array
    stencil = np.zeros_like(img)

    # specify coordinates of the polygon
    thresh = int(0.4 * h)
    polygon = np.array([[0, thresh], [0, h],[900, h], [900, thresh]])

    # fill polygon with ones
    cv2.fillConvexPoly(stencil, polygon, 1)

    # apply polygon as a mask on the frame
    img = cv2.bitwise_and(img, img, mask=stencil)


    # apply image thresholding
    ret, thresh = cv2.threshold(img, 145, 255, cv2.THRESH_BINARY)

    blackLines = cv2.HoughLinesP(thresh, 145, np.pi / 180, 100,minLineLength=40, maxLineGap=10)

    center_x = w / 2
    center_y = h / 2
    # create a copy of the original frame
    dmy = img1.copy()
    sumSlopes = 0
    # draw Hough lines
    yellow_count_x_left_center = 0
    yellow_count_x_right_center = 0
    yellow_count_total = 0


    """yellow_count_total = yellow_count_x_left_center + yellow_count_x_right_center
    print(yellow_count_x_right_center / yellow_count_total)
    print(yellow_count_x_left_center / yellow_count_total)
    if yellow_count_x_right_center / yellow_count_total >= 0.7:
        print("yellow right go left")
    elif yellow_count_x_left_center / yellow_count_total >= 0.7:
        print("yellow left go right")
    else:
        print("BAD")"""
    state = "right"
    count_x_left_center = 0
    count_x_right_center = 0
    if blackLines is not None:
        for line in blackLines:
            x1, y1, x2, y2 = line[0]
            if y2 < 300:
                continue
            """ Counting number of points which are left and right of center """
            if x1 < center_x:
                count_x_left_center += 1
            if x1 > center_x:
                count_x_right_center += 1
            cv2.line(dmy, (x1, y1), (x2, y2), (70, 70, 0), 3)

        count_total = count_x_right_center + count_x_left_center
        print(count_x_right_center/count_total)
        print(count_x_left_center/count_total)
        if count_x_right_center / count_total >= 0.7:
            state = "right"
        elif count_x_left_center / count_total >= 0.7:
            state = "left"
        else:
            state = "center"
        print("go", state)

    if yellowlines is not None and blackLines is None:
        print("go ", state)
    for line in yellowlines:
        x1, y1, x2, y2 = line[0]
        cv2.line(dmy, (x1, y1), (x2, y2), (255, 0, 0), 3)
    # plot frame
    plt.figure(figsize=(10, 10))
    plt.imshow(dmy, cmap="gray")
    plt.show()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    detect()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
