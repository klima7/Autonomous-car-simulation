import time

from paths import *


class Controller:

    def __init__(self, car):
        self.car = car
        self.pm = PathsManager(self.car._client)

    def start(self):
        path = Path(self.car._client, 1071)

        while True:
            self.car.refresh()
            self.car.navigate(self.car.target_point)
            if self.car.target_point == path.end:
                self.car.cur_path = self.pm.find_subsequent_paths(path)[0].handle
                path = Path(self.car._client, self.car.cur_path)
            self.car.apply()
