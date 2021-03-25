from api.b0RemoteApi import RemoteApiClient
import math
import numpy as np


class Car:

    def __init__(self, client: RemoteApiClient):
        self.client = client

        _, self.front_left_wheel = self.client.simxGetObjectHandle('FrontLeftSteerJoint', client.simxServiceCall())
        _, self.front_right_wheel = self.client.simxGetObjectHandle('FrontRightSteerJoint', client.simxServiceCall())
        _, self.back_left_wheel = self.client.simxGetObjectHandle('BackLeftWheelJoint', client.simxServiceCall())
        _, self.back_right_wheel = self.client.simxGetObjectHandle('BackRightWheelJoint', client.simxServiceCall())
        _, self.camera = self.client.simxGetObjectHandle('CarVision1', client.simxServiceCall())

    def set_force(self, force):
        self.client.simxSetJointMaxForce(self.back_left_wheel, force, self.client.simxDefaultPublisher())
        self.client.simxSetJointMaxForce(self.back_right_wheel, force, self.client.simxDefaultPublisher())

    def set_angle(self, angle):
        self.client.simxSetJointTargetPosition(self.front_left_wheel, self.to_radians(angle), self.client.simxDefaultPublisher())
        self.client.simxSetJointTargetPosition(self.front_right_wheel, self.to_radians(angle), self.client.simxDefaultPublisher())

    def set_velocity(self, velocity):
        self.client.simxSetJointTargetVelocity(self.back_left_wheel, velocity, self.client.simxDefaultPublisher())
        self.client.simxSetJointTargetVelocity(self.back_right_wheel, velocity, self.client.simxDefaultPublisher())

    def get_camera_image(self):
        _, size, data = self.client.simxGetVisionSensorImage(self.camera, False, self.client.simxServiceCall())
        data = [x for x in data]
        image = np.array(data, dtype=np.uint8)
        image.resize([size[1], size[0], 3])
        return image

    @staticmethod
    def to_radians(degrees):
        return degrees * math.pi / 180
