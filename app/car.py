import math
from enum import Enum
import numpy as np
import util
from util import Point
from api.b0RemoteApi import RemoteApiClient


class Lights:

    class Indicators(Enum):
        DISABLED = 0
        LEFT = 1
        RIGHT = 2
        HAZARD_LIGHTS = 3

    def __init__(self):
        self.indicators = Lights.Indicators.DISABLED
        self.stop = False
        self.running = False
        self.reverse = False

    def get_vector(self):
        return [self.indicators.value, int(self.stop), int(self.running), int(self.reverse)]

    def set_vector(self, vector):
        self.indicators = Lights.Indicators(vector[0])
        self.stop = bool(vector[1])
        self.running = bool(vector[2])
        self.reverse = bool(vector[3])


class AckermanSteering:

    TURNING_ANGLE = math.pi / 3

    def __init__(self):
        self.velocity = 0
        self.left_angle = 0
        self.right_angle = 0

    def get_vector(self):
        return [self.velocity, self.left_angle, self.right_angle]

    def set_vector(self, vector):
        self.velocity = vector[0]
        self.left_angle, self.right_angle = vector[1]

    def set_wheels_by_radius(self, radius):
        """positive radius - right, negative - left"""
        close_angle = math.atan(Car.LENGTH / (abs(radius) - Car.WIDTH/2))
        far_angle = math.atan(Car.LENGTH / (abs(radius) + Car.WIDTH / 2))

        if radius < 0:
            left_angle, right_angle = far_angle, close_angle
        else:
            left_angle, right_angle = -close_angle, -far_angle

        self.right_angle = left_angle
        self.left_angle = right_angle

    def set_wheels_by_angle(self, angle):
        """positive angle - right, negative - left"""
        radius = Car.LENGTH / math.tan(util.deg2rad(angle)) if angle != 0 else math.inf
        self.set_wheels_by_radius(radius)


class Car:
    
    LENGTH = 0.316
    WIDTH = 0.213

    def __init__(self, client: RemoteApiClient):
        self._client = client
        _, self.camera_handle = self._client.simxGetObjectHandle('ViewCamera', self._client.simxServiceCall())

        self.gps = None
        self.orient = None
        self.view = None

        self.steering = AckermanSteering()
        self.lights = Lights()

    def refresh(self):
        _, *data = self._client.simxCallScriptFunction("get_state@Car", "sim.scripttype_childscript", [], self._client.simxServiceCall())
        self.gps = Point(*data[0][0:2])
        self.orient = data[1]
        self.steering.set_vector(data[2])
        self.lights.set_vector(data[3])
        self.view = self._get_camera_view()

    def _get_camera_view(self):
        _, size, view = self._client.simxGetVisionSensorImage(self.camera_handle, False, self._client.simxServiceCall())
        view = [b for b in view]
        view = np.array(view, dtype=np.uint8)
        view.resize((size[1], size[0], 3))
        view = np.flipud(view)
        return view

    def apply(self):
        data = [self.steering.get_vector(), self.lights.get_vector()]
        self._client.simxCallScriptFunction("set_state@Car", "sim.scripttype_childscript", data, self._client.simxServiceCall())

    def navigate(self, target: Point):
        diff = [target.x-self.gps.x, target.y-self.gps.y]
        target_angle = util.get_vector_angle(diff)
        car_angle = self.orient
        diff_angle = car_angle - target_angle

        diff_angle = min(self.steering.TURNING_ANGLE, diff_angle)
        diff_angle = max(-self.steering.TURNING_ANGLE, diff_angle)

        diff_angle = util.rad2deg(diff_angle)
        self.steering.set_wheels_by_angle(diff_angle)

    @property
    def preview_point(self):
        preview_point = util.move_forward(self.gps, self.orient, 1)
        return preview_point
