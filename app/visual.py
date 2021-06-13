import cv2
import numpy as np
from enum import Enum, auto
import util
import math


SIGN_HEAD2STICK_FACTOR = 0.57
PERSPECTIVE_ANGLE = 60
CAMERA_IMAGE_HEIGHT = 512
CAMERA_IMAGE_WIDTH = 512
SIGN_REAL_HEIGHT = 0.48978


def find_signs(image):
    if image is None:
        return

    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    sticks = find_signs_sticks(hsv_image)
    heads = [find_sign_head(stick) for stick in sticks]
    draw_rectangles(hsv_image, heads)

    cv2.imshow('Frame', cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR))
    cv2.waitKey(1)


def find_signs_sticks(hsv_image):
    sticks = []

    mask = cv2.inRange(hsv_image, np.array([0, 0, 70]), np.array([3, 3, 85]))

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(hsv_image, contours, -1, (0, 0, 255), 1)
    for i in range(len(contours)):
        contour = contours[i]
        x, y, w, h = cv2.boundingRect(contour)
        if h > 15:
            sticks.append((x+w//2, y, h))

    return sticks


def find_sign_head(stick):
    x, y, h = stick
    print(calc_distance(h), util.rad2deg(calc_angle(x)))
    head_size = int(SIGN_HEAD2STICK_FACTOR * h)
    return x - head_size//2, y - head_size, head_size, head_size


def calc_distance(height):
    numerator = CAMERA_IMAGE_HEIGHT * SIGN_REAL_HEIGHT
    denominator = 2 * height * math.tan(util.deg2rad(PERSPECTIVE_ANGLE/2))
    return numerator / denominator


def calc_angle(x):
    diff = x - CAMERA_IMAGE_WIDTH / 2
    a_diff = abs(diff)
    a_angle = a_diff * util.deg2rad(PERSPECTIVE_ANGLE/2) / (CAMERA_IMAGE_WIDTH / 2)
    angle = a_angle if diff > 0 else -a_angle
    return angle


def draw_rectangles(image, rectangles):
    for rectangle in rectangles:
        start = (rectangle[0], rectangle[1])
        end = (rectangle[0]+rectangle[2], rectangle[1]+rectangle[3])
        cv2.rectangle(image, start, end, (0, 0, 0), 2)


class TrafficLightColor(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()
    NONE = auto()


def recognize_light_color(image):
    if image is None:
        return TrafficLightColor.NONE

    image = image[:, image.shape[1] // 2:]

    if check_light_color(image, [0, 240, 150], [5, 255, 190]):
        return TrafficLightColor.RED

    if check_light_color(image, [58, 240, 150], [62, 255, 190]):
        return TrafficLightColor.GREEN

    if check_light_color(image, [28, 240, 150], [30, 255, 190]):
        return TrafficLightColor.YELLOW

    return TrafficLightColor.NONE


def check_light_color(img, lower, upper):
    image = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(image, np.array(lower), np.array(upper))

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if (abs(w - h) <= 30) and cv2.contourArea(contour) > 40:
            return True

    return False

