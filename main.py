import math
import sys, time, http.client
from urllib.request import urlopen
import cv2 as cv
import cv2.cv2
import matplotlib.pyplot as plt
import requests
from math import atan
from random import randrange

import algo2
from alg import detectFrom

from PIL import Image
import io

# Set speed content, and speed level content
MAX_SPEED = 100
REV_SPEED = 20
LOW_SPEED = 30
MIN_SPEED = 40
SPEED_LEVEL_1 = MIN_SPEED
SPEED_LEVEL_2 = (MAX_SPEED - MIN_SPEED) / 4 * 1 + MIN_SPEED
SPEED_LEVEL_3 = (MAX_SPEED - MIN_SPEED) / 4 * 2 + MIN_SPEED
SPEED_LEVEL_4 = (MAX_SPEED - MIN_SPEED) / 4 * 3 + MIN_SPEED
SPEED_LEVEL_5 = MAX_SPEED
SPEED = [0, SPEED_LEVEL_1, SPEED_LEVEL_2, SPEED_LEVEL_3, SPEED_LEVEL_4, SPEED_LEVEL_5]

HOST = '192.168.2.118'
PORT = '8000'

# BASE_URL is variant use to save the format of host and port
BASE_URL = 'http://' + HOST + ':' + PORT + '/'


def __request__(url, times=10):
    for x in range(times):
        try:
            requests.get(url)
            return 0
        except:
            print("Connection error, try again")
    print("Abort")
    return -1


def run_speed(speed):
    url = BASE_URL + 'run/?speed=' + speed
    __request__(url)


def set_speed_level(speed):  # set speed to server
    run_speed(speed)


def run_action(cmd):
    url = BASE_URL + 'run/?action=' + cmd
    print('url: %s' % url)
    __request__(url)


def drive():
    run_action('forward')


class QueryImage:
    def __init__(self, host, port=8080, argv="/?action=snapshot"):
        # default port 8080, the same as mjpg-streamer server
        self.host = host
        self.port = port
        self.argv = argv

    def queryImage(self):
        http_data = http.client.HTTPConnection(self.host, self.port)
        http_data.putrequest('GET', self.argv)
        http_data.putheader('Host', self.host)
        http_data.putheader('User-agent', 'python-http.client')
        http_data.putheader('Content-type', 'image/jpeg')
        http_data.endheaders()
        returnmsg = http_data.getresponse()

        return returnmsg.read()


def alg(data):
    if randrange(10) > 5:
        return 'fwleft'
    return 'fwright'


def turnleft():
    run_action('fwturn:70')


def turnright():
    run_action('fwturn:110')


def mid_point(points):
    xSum, ySum = 0, 0
    l = len(points)
    for p in points:
        xSum += p[0]
        ySum += p[1]
    return int(xSum / l), int(ySum / l)


mid_low_point = (320, 480)


def get_mid_angle(point):
    dx = point[0]-mid_low_point[0]
    # dy = point[1]-mid_low_point[1]
    dy = 0-mid_low_point[1]
    angle = math.degrees(atan(abs(dx) / abs(dy)))
    print('computed angle: ' + str(int(angle)))
    return angle


def ready():
    run_action('stop')
    run_action('fwready')
    run_action('bwready')
    run_action('camready')
    run_action('camdown')
    set_speed_level(str(LOW_SPEED))
    run_action('forward')


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    countLeft = 0
    countRight = 0
    #run_action('stop')
    #sys.exit()
    queryImage = QueryImage(HOST)
    ready()
    last = 'fwstraight'
    countNoLines = 0
    while True:
        img = queryImage.queryImage()

        # Move to alg
        detected = detectFrom(img)
        # detected = algo2.detectFromNew(img)
        """if detected is None or detected is int:
            continue"""
        leftcount, rightcount, leftPoints, rightPoints, img = detected
        # slope, dmy, xmax, leftcount, rightcount = detected
        if leftcount == rightcount == 0:
            countNoLines += 1
            print('no lines found')
            action = 'fwstraight'
            if 'fwturn' in last:
                action = 'fwturn:' + str(180-int(last.split(':')[1]))
            last = action
            run_action(action)
            # if last == 'fwleft':
            #     # last = 'fwright'
            #     run_action('fwturn:110')
            #     # turnright()
            # else:
            #     # last = 'fwleft'
            #     run_action('fwturn:70')
            #     # turnleft()
            run_action('backward')
            if countNoLines >= 3:
                countNoLines = 0
                run_action('forward')
            # run_action(last)
            # countNoLines += 1
            # if countNoLines >= 2:
            #     countNoLines = 0
            #     if last == 'fwleft':
            #         last = 'fwright'
            #         run_action('fwturn:135')
            #         # turnright()
            #     else:
            #         last = 'fwleft'
            #         run_action('fwturn:45')
            #         # turnleft()
            # run_action('fwstraight')
            continue
        if leftcount > rightcount:
            mid = mid_point(leftPoints)
            x, y = mid
            angle = get_mid_angle(mid)
            angle = 90 - angle
            # angle = 0.8 * angle
            # run_action('stop')
            aturn = 'fwturn:' + str(int(max(angle, 60)))
            print('turn command: ' + aturn)
            run_action(aturn)
            last = aturn
            if img is not None:
                cv2.line(img, (x, 0), mid_low_point, (255, 255, 255), 3)
                run_action('stop')
                plt.imshow(img)
                plt.show()
                run_action('forward')
            # run_action('forward')
            # turnleft()
            # last = aturn
        else:
            mid = mid_point(rightPoints)
            x, y = mid
            angle = get_mid_angle(mid)
            angle = 90 + angle
            # angle = 0.8 * angle
            # run_action('stop')
            aturn ='fwturn:' + str(int(min(angle + 90, 120)))
            print('turn command: ' + aturn)
            run_action(aturn)
            last = aturn
            if img is not None:
                cv2.line(img, (x, 0), mid_low_point, (255, 255, 255), 3)
                run_action('stop')
                plt.imshow(img)
                plt.show()
                run_action('forward')
            # run_action('forward')
            # turnright()
            # last = aturn

        run_action('forward')
        # run_action('fwstraight')
        # print(xmax)
        # if xmax > 330:
        #    run_action('fwright')
        # elif xmax < 310:
        #    run_action('fwleft')
        # if 0 <= slope < 10:
        #     countLeft += 1
        #     run_action('fwleft')
        # elif -10 < slope < 0:
        #     run_action('fwright')

        # time.sleep(0.1)
        # run_action('fwstraight')
    # run_action('camleft')

    # run_action('camdown')
    # # run_action('stop')
    # set_speed_level(str(SPEED_LEVEL_1))
    # run_action('forward')
    # for i in range(30):
    #     img = queryImage.queryImage()
    #
    #     image = Image.open(io.BytesIO(img))
    #     image.save('lubin'+str(i + 50)+'.jpg')
    #     time.sleep(0.2)

    # set_speed_level(str(SPEED_LEVEL_2))
    # run_action('forward')
    # time.sleep(3)
    # run_action('stop')
