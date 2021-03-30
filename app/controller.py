import time


class Controller:

    def __init__(self, simulation, car):
        self.simulation = simulation
        self.car = car

    def start(self):
        self.car.set_wheels_by_radius(0)
        self.car.set_force(60)
        self.car.set_velocity(20)

        self.loop()

    def loop(self):
        while True:
            self.update()

    def update(self):
        # Pijany kierowca
        self.car.set_wheels_by_radius(2)
        time.sleep(2)
        self.car.set_wheels_by_radius(-2)
        time.sleep(2)
