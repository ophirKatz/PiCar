# This is a sample Python script.
import os
import re
import cv2
import numpy as np
from tqdm import tqdm_notebook
import matplotlib.pyplot as plt
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def detect():
    return detectFrom('a3.jpg')


def detectFrom(img):
    img = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
    # img = np.ndarray(img)
    # img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img = cv2.flip(img,1)
    img = 255 - img

    # create a zero array
    stencil = np.zeros_like(img)

    # specify coordinates of the polygon
    polygon = np.array([[0, 150], [0, 700],[1000, 700], [900, 150]])

    # fill polygon with ones
    cv2.fillConvexPoly(stencil, polygon, 1)

    # apply polygon as a mask on the frame
    img = cv2.bitwise_and(img, img, mask=stencil)



    # plot masked frame
    # plt.figure(figsize=(10, 10))
    # plt.imshow(img, cmap="gray")
    # plt.show()
    # apply image thresholding
    ret, thresh = cv2.threshold(img, 145, 255, cv2.THRESH_BINARY)

    # plot image
    # plt.figure(figsize=(10,10))
    # plt.imshow(thresh, cmap= "gray")
    # plt.show()

    lines = cv2.HoughLinesP(thresh, 145, np.pi / 180, 200,minLineLength=300, maxLineGap=400)

    # create a copy of the original frame
    dmy = img.copy()

    sumSlopes = 0
    # draw Hough lines
    if lines is None:
        return 1, dmy, 320
    ymax = 600
    xmax = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if y1 < ymax:
            ymax = y1
            xmax = x1
        if y2 < ymax:
            ymax = y2
            xmax = x2
        if x2 == x1:
            continue
        slope = (y2-y1)/(x2-x1)
        sumSlopes += slope
        cv2.line(dmy, (x1, y1), (x2, y2), (255, 0, 0), 3)
    print(ymax)
    print(xmax)
    res = sumSlopes/len(lines)
    print(res)
    return res, dmy, xmax

    # plot frame
    # plt.figure(figsize=(10, 10))
    # plt.imshow(dmy, cmap="gray")
    # plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    detect()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
