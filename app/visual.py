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
