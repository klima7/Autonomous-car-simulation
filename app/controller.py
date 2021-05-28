from driving import Driver
from time import time


class Controller:

    def __init__(self, car, mm):
        self.car = car
        self.mm = mm

    def start(self):
        self.car.refresh()

        driver = Driver(self.car, self.mm)
        driver.add_target('RoundaboutPaths2')
        driver.add_target('RoundaboutPaths1')
        driver.add_target('RoundaboutPaths0')
        driver.add_target('RoundaboutPaths3')

        while True:
            start = time()
            self.car.refresh()
            driver.drive()
            self.car.apply()
            print(time() - start)
