import cv2 as cv
import numpy as np

ratio = 6
kernel_size = 3
window_name = 'Edge Map'

def detectFromNew(img):
    img = cv.imdecode(np.frombuffer(img, np.uint8), -1)
    # img = np.ndarray(img)
    # img = cv.imread(img)
    src_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_blur = cv.blur(src_gray, (3, 3))

    low_threshold = 60
    detected_edges = cv.Canny(img_blur, low_threshold, low_threshold * ratio, kernel_size)

    detected_edges = detected_edges[140:480, 0:640]

    lines = cv.HoughLinesP(detected_edges, 2, np.pi / 180, 1, 15, 5)
    return lines, detected_edges

    # for line in lines:
    #     x1, y1, x2, y2 = line[0]
    #     cv.line(detected_edges, (x1, y1), (x2, y2), (255, 255, 255), 3)
    #
    # cv.imshow(window_name, detected_edges)
    # cv.namedWindow(window_name)
    # cv.waitKey()
