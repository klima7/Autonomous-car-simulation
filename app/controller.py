import time


class Controller:

    def __init__(self, simulation, car):
        self.simulation = simulation
        self.car = car

    def start(self):
        self.car.set_angle(0)
        self.car.set_velocity(20)
        self.car.set_force(60)

        self.loop()

    def loop(self):
        while True:
            self.update()

    def update(self):
        self.car.set_velocity(20)
        time.sleep(3)
        self.car.set_velocity(0)
        time.sleep(2)
