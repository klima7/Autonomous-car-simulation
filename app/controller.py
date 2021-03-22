import time


class Controller:

    def __init__(self, simulation, car):
        self.simulation = simulation
        self.car = car

    def start(self):
        self.simulation.restart()
        self.loop()

    def loop(self):
        while True:
            self.update()
            time.sleep(0.1)

    def update(self):
        self.simulation.print("updating")
