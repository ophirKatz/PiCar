
from __future__ import print_function
import cv2 as cv
import argparse

import numpy as np

max_lowThreshold = 100
window_name = 'Edge Map'
title_trackbar = 'Min Threshold:'
ratio = 3
kernel_size = 3


parser = argparse.ArgumentParser(description='Code for Canny Edge Detector tutorial.')
parser.add_argument('--input', help='Path to input image.', default='lubin34.jpg')
args = parser.parse_args()
src = cv.imread(cv.samples.findFile(args.input))
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
img_blur = cv.blur(src_gray, (3,3))

low_threshold = 100
detected_edges = cv.Canny(img_blur, low_threshold, low_threshold*ratio, kernel_size)

detected_edges = detected_edges[240:480, 0:640]

lines = cv.HoughLinesP(detected_edges, 2, np.pi / 180, 1, 15, 5)

for line in lines:
    x1, y1, x2, y2 = line[0]
    cv.line(detected_edges, (x1,y1), (x2,y2), (255,255,255), 3)

cv.imshow(window_name, detected_edges)
cv.namedWindow(window_name)
cv.waitKey()




