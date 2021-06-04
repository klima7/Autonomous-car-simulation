import cv2
import numpy as np
from enum import Enum, auto


class TrafficLightColor(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()
    NONE = auto()


def recognize_light_color(image):
    if image is None:
        return TrafficLightColor.NONE

    image = image[:, image.shape[1] // 2:]

    lower_red = np.array([0, 150, 20])
    upper_red = np.array([10, 255, 255])

    if check_light_color(image, lower_red, upper_red):
        return TrafficLightColor.RED

    lower_green = np.array([50, 150, 20])
    upper_green = np.array([80, 255, 255])

    if check_light_color(image, lower_green, upper_green):
        return TrafficLightColor.GREEN

    lower_yellow = np.array([15, 150, 20])
    upper_yellow = np.array([35, 255, 255])

    if check_light_color(image, lower_yellow, upper_yellow):
        return TrafficLightColor.YELLOW

    return TrafficLightColor.NONE


def check_light_color(img, lower, upper):
    image = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(image, lower, upper)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if (-1 <= w - h <= 1) and cv2.contourArea(contour) > 40:
            return True

    return False
