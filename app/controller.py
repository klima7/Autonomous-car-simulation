import math
import util


class Controller:

    def __init__(self, car):
        self.car = car

    def start(self):
        target = [20.75, -23.925]

        while True:
            self.car.refresh()
            self.car.navigate(target)
            self.car.apply()
