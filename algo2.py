import cv2 as cv
import cv2.cv2
import numpy as np

ratio = 5
kernel_size = 3
window_name = 'Edge Map'

def detectFromNew(img):
    img = cv.imdecode(np.frombuffer(img, np.uint8), -1)
    src_gray = cv.cvtColor(img, cv2.cv2.COLOR_BGR2GRAY)
    img_blur = cv.blur(src_gray, (2, 2))

    low_threshold = 100
    detected_edges = cv.Canny(img_blur, low_threshold, low_threshold * ratio, kernel_size)

    detected_edges = detected_edges[240:480, 0:640]

    lines = cv.HoughLinesP(detected_edges, 2, np.pi / 180, 1, 15, 5)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(detected_edges, (x1, y1), (x2, y2), (255, 255, 255), 3)

    return lines, detected_edges
    #
    # cv.imshow(window_name, detected_edges)
    # cv.namedWindow(window_name)
    # cv.waitKey()
