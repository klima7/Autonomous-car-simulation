import time


class Controller:

    def __init__(self, simulation, car):
        self.simulation = simulation
        self.car = car

    def start(self):
        self.car.set_wheels_by_radius(0)
        self.car.set_force(60)
        self.car.set_running_lights(True)
        self.loop()

    def loop(self):
        while True:
            self.update()

    def update(self):
        # Pijany kierowca
        self.car.set_velocity(10)

        self.car.set_wheels_by_angle(0)
        time.sleep(3)

        self.car.set_wheels_by_radius(1)
        self.car.enable_right_indicators()
        time.sleep(3)

        self.car.set_wheels_by_radius(-1)
        self.car.enable_left_indicators()
        time.sleep(3)

        self.car.set_velocity(0)
        self.car.set_wheels_by_angle(0)
        self.car.disable_indicators()
        self.car.set_stop_lights(True)
        time.sleep(1)

        self.car.set_stop_lights(False)
        time.sleep(1)

        self.car.set_reversing_lights(True)
        self.car.set_velocity(-10)
        time.sleep(3)

        self.car.set_wheels_by_radius(1)
        self.car.enable_right_indicators()
        time.sleep(3)

        self.car.set_wheels_by_radius(-1)
        self.car.enable_left_indicators()
        time.sleep(3)

        self.car.disable_indicators()
        self.car.set_reversing_lights(False)
