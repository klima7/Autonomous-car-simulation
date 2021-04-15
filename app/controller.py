import math
import util


class Controller:

    def __init__(self, car):
        self.car = car

    def start(self):
        target = [20.75, -23.925]

        while True:
            self.car.refresh()
            diff = [self.car.gps[0]-target[0], self.car.gps[1]-target[1]]
            target_angle = util.rad2deg(math.atan2(diff[1], diff[0]) + math.pi)
            car_angle = util.rad2deg(self.car.orient + math.pi)
            diff_angle = car_angle - target_angle

            if diff_angle > 180:
                diff_angle = 180 - diff_angle
            if diff_angle < -180:
                diff_angle = 360 + diff_angle

            diff_angle = min(20, diff_angle)
            diff_angle = max(-20, diff_angle)

            self.car.target_velocity = 20
            self.car.set_wheels_by_angle(diff_angle)
            self.car.apply()
