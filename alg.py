# This is a sample Python script.
import os
import re
import cv2
import cv2.cv2
import numpy as np
from tqdm import tqdm_notebook
import matplotlib.pyplot as plt
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from algo2 import detectFromNew

def detect():
    return detectFrom('a3.jpg')


def Hough(img):
    img = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = 255 - img

    stencil = np.zeros_like(img)

    polygon = np.array([[0, 150], [0, 700], [1000, 700], [900, 150]])

    cv2.fillConvexPoly(stencil, polygon, 1)

    img = cv2.bitwise_and(img, img, mask=stencil)

    ret, thresh = cv2.threshold(img, 145, 255, cv2.THRESH_BINARY)

    # lines = cv2.HoughLinesP(thresh, 145, np.pi / 180, 200)
    lines = cv2.HoughLinesP(thresh, 145, np.pi / 180, 200, minLineLength=200, maxLineGap=600)

    return lines

def findLines(img):
    img = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
    img = np.ndarray(img)
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.flip(img,1)
    # img = 255 - img
    img = cv2.cv2.blur(img, (3, 3))

    low_thr = 100
    detected_edges = cv2.cv2.Canny(img, low_thr, low_thr * 3, 3)
    # detected_edges = detected_edges[200:400, 0:640]

    ret, thresh = cv2.threshold(detected_edges, 145, 255, cv2.THRESH_BINARY)
    lines = cv2.HoughLinesP(thresh, 145, np.pi / 180, 200, minLineLength=200, maxLineGap=600)

    # lines = Hough(detected_edges)
    # plt.figure(figsize=(10, 10))
    # plt.imshow(lines, cmap="gray")
    # plt.show()

    return lines, img


def detectFrom(img):
    lines, img = detectFromNew(img)

    # create a copy of the original frame
    dmy = img.copy()

    sumSlopes = 0
    # draw Hough lines
    if lines is None:
        return 500, dmy, 320, 0, 0
    ymin = 600
    xmin = 0
    leftcount, rightcount = 0, 0
    numSlopes = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if y1 < ymin:
            ymin = y1
            xmin = x1
        if y2 < ymin:
            ymin = y2
            xmin = x2
        if x1 > 340:
            rightcount += 1
        else:
            leftcount += 1
        if x2 > 340:
            rightcount += 1
        else:
            leftcount += 1
        if x2 == x1:
            continue
        slope = (y2-y1)/(x2-x1)
        slopeabs = abs(slope)
        # plt.imshow(dmy)
        # plt.show()
        if 0.5 < slopeabs < 2 or True:
            sumSlopes += slope
            numSlopes += 1
        cv2.line(dmy, (x1, y1), (x2, y2), (255, 0, 0), 3)
    # print(ymin)
    # print(xmin)
    if numSlopes == 0:
        return 500, dmy, xmin, leftcount, rightcount
    slopeAvg = sumSlopes/numSlopes
    print(slopeAvg)
    return slopeAvg, dmy, xmin, leftcount, rightcount

    # plot frame
    # plt.figure(figsize=(10, 10))
    # plt.imshow(dmy, cmap="gray")
    # plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    detect()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
