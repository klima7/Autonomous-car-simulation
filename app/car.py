import math

import numpy as np

import util
from api.b0RemoteApi import RemoteApiClient
from util import Point


class Car:

    LENGTH = 0.316
    WIDTH = 0.213
    TURNING_ANGLE = math.pi / 3

    INDICATORS_DISABLED = 0
    INDICATORS_LEFT = 1
    INDICATORS_RIGHT = 2
    INDICATORS_HAZARD = 3

    def __init__(self, client: RemoteApiClient):
        self._client = client
        _, self.camera_handle = self._client.simxGetObjectHandle('ViewCamera', self._client.simxServiceCall())

        self.velocity = 0
        self.left_angle = 0
        self.right_angle = 0

        self.indicators_lights = Car.INDICATORS_DISABLED
        self.stop_lights = False
        self.running_lights = False
        self.reverse_lights = False

        self.gps = None
        self.orient = None
        self.view = None

    def refresh(self):
        _, *data = self._client.simxCallScriptFunction("get_state@Car", "sim.scripttype_childscript", [], self._client.simxServiceCall())
        self.gps = Point(*data[0][0:2])
        self.orient = data[1]

        steering_data = data[2]
        self.velocity = steering_data[0]
        self.left_angle, self.right_angle = steering_data[1]

        lights_data = data[3]
        self.indicators_lights = lights_data[0]
        self.stop_lights = bool(lights_data[1])
        self.running_lights = bool(lights_data[2])
        self.reverse_lights = bool(lights_data[3])

        self.view = self._get_camera_view()

    def _get_camera_view(self):
        _, size, view = self._client.simxGetVisionSensorImage(self.camera_handle, False, self._client.simxServiceCall())
        view = [b for b in view]
        view = np.array(view, dtype=np.uint8)
        view.resize((size[1], size[0], 3))
        view = np.flipud(view)
        return view

    def apply(self):
        steering_data = [self.velocity, self.left_angle, self.right_angle]
        lights_data = [self.indicators_lights, int(self.stop_lights), int(self.running_lights), int(self.reverse_lights)]

        data = [steering_data, lights_data]
        self._client.simxCallScriptFunction("set_state@Car", "sim.scripttype_childscript", data, self._client.simxServiceCall())

    def navigate(self, target: Point):
        diff = [target.x-self.gps.x, target.y-self.gps.y]
        target_angle = util.get_vector_angle(diff)
        car_angle = self.orient
        diff_angle = car_angle - target_angle

        diff_angle = min(self.TURNING_ANGLE, diff_angle)
        diff_angle = max(-self.TURNING_ANGLE, diff_angle)

        diff_angle = util.rad2deg(diff_angle)
        self.set_wheels_by_angle(diff_angle)

    def set_wheels_by_radius(self, radius):
        close_angle = math.atan(Car.LENGTH / (abs(radius) - Car.WIDTH/2))
        far_angle = math.atan(Car.LENGTH / (abs(radius) + Car.WIDTH / 2))

        if radius < 0:
            left_angle, right_angle = far_angle, close_angle
        else:
            left_angle, right_angle = -close_angle, -far_angle

        self.right_angle = left_angle
        self.left_angle = right_angle

    def set_wheels_by_angle(self, angle):
        radius = Car.LENGTH / math.tan(util.deg2rad(angle)) if angle != 0 else math.inf
        self.set_wheels_by_radius(radius)

    @property
    def preview_point(self):
        preview_point = util.move_forward(self.gps, self.orient, 1)
        return preview_point
