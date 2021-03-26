import time


class Controller:

    def __init__(self, simulation, car):
        self.simulation = simulation
        self.car = car

    def start(self):
        self.car.set_angle(90)
        self.car.set_left_angle(self.close_ackerman_angle(0.1, self.car))
        self.car.set_right_angle(self.far_ackerman_angle(0.1, self.car))
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

    def close_ackerman_angle(self, r, vehicle): # r - promien zakretu
        return vehicle.length/(r - (vehicle.width/2))

    def far_ackerman_angle(self, r, vehicle): #r - promien zakretu
        return vehicle.length / (r + (vehicle.width / 2))
