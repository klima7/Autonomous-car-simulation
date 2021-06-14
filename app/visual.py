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


class SignType(Enum):
    STOP = 0
    WALKWAY = 1
    ROUNDABOUT = 2
    PARKING = 3
    LIMIT = 4
    ONEWAY = 5
    DEADEND = 6
    TRAFFIC_LIGHTS = 7
    UNKNOWN = 8
    REVERSED = 9


class FoundSign:

    IMAGE_SIZE = 25

    def __init__(self, stick, image):
        self.stick = stick
        self.head = self.find_sign_head()
        self.head_image = self.cut_head_image(image)
        self.scaled_head_image = self.scale_head_image()
        self.type = self.recognize_sign()

    def find_sign_head(self):
        x, y, h = self.stick
        head_size = int(SIGN_HEAD2STICK_FACTOR * h)
        return x - head_size // 2, y - head_size, head_size

    def cut_head_image(self, image):
        x, y, a = self.head
        if x < 0 or y < 0 or x + a >= CAMERA_IMAGE_WIDTH or y + a >= CAMERA_IMAGE_HEIGHT:
            return None
        return image[y:y + a, x:x + a]

    def scale_head_image(self):
        if self.head_image is None:
            return None

        size = [self.IMAGE_SIZE, self.IMAGE_SIZE]
        scaled = cv2.resize(self.head_image, size)
        return scaled

    def recognize_sign(self):
        if self.head_image is None:
            return SignType.UNKNOWN
        if self.is_reversed():
            return SignType.REVERSED
        return SignType.UNKNOWN

    def is_reversed(self):
        mask = cv2.inRange(self.head_image, np.array([20, 0, 190]), np.array([40, 50, 250]))
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        full_height = self.head[2]
        for contour in contours:
            _, _, _, h = cv2.boundingRect(contour)
            if cv2.contourArea(contour)/h >= 5 and h >= full_height / 4 * 3:
                return True
        return False

    def get_distance(self):
        height = self.stick[2]
        numerator = CAMERA_IMAGE_HEIGHT * SIGN_REAL_HEIGHT
        denominator = 2 * height * math.tan(util.deg2rad(PERSPECTIVE_ANGLE/2))
        return numerator / denominator

    def get_angle(self):
        x = self.stick[0]
        diff = x - CAMERA_IMAGE_WIDTH / 2
        a_diff = abs(diff)
        a_angle = a_diff * util.deg2rad(PERSPECTIVE_ANGLE/2) / (CAMERA_IMAGE_WIDTH / 2)
        angle = a_angle if diff > 0 else -a_angle
        return angle

    def draw(self, hsv_image):
        head_start = (self.head[0], self.head[1])
        head_end = (self.head[0]+self.head[2], self.head[1]+self.head[2])
        cv2.rectangle(hsv_image, head_start, head_end, (0, 0, 0), 2)

        stick_start = (self.stick[0], self.stick[1])
        stick_end = (self.stick[0], self.stick[1]+self.stick[2])
        cv2.line(hsv_image, stick_start, stick_end, (0, 0, 0), 2)

        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(hsv_image, self.type.name, (head_start[0], head_start[1]), font, 1, (0, 0, 0), 1, cv2.LINE_AA)

        x = head_start[0]-self.IMAGE_SIZE
        y = head_start[1]-20
        if x >= 0 and y >= 0:
            a = self.scaled_head_image.shape[0]
            hsv_image[y:y+a, x:x+a] = self.scaled_head_image


def find_signs(image):
    if image is None:
        return

    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    sticks = find_sticks(hsv_image)
    signs = [FoundSign(stick, hsv_image) for stick in sticks]

    for sign in signs:
        if sign.head_image is not None:
            sign.draw(hsv_image)
    cv2.imshow('Frame', cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR))
    cv2.waitKey(1)

    return signs


def find_sticks(hsv_image):
    sticks = []
    mask = cv2.inRange(hsv_image, np.array([20, 0, 105]), np.array([40, 10, 120]))
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        contour = contours[i]
        x, y, w, h = cv2.boundingRect(contour)
        if h > 15:
            sticks.append((x+w//2, y, h))
    return sticks


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

