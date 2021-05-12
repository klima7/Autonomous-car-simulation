from routing import RouteFinder
from driving import Driver


class Controller:

    def __init__(self, car, mm):
        self.car = car
        self.mm = mm

    def start(self):
        self.car.refresh()
        self.car.cur_path = self.car.closest_path
        self.car.apply()

        pos_start = self.mm.get_path_by_id(self.car.closest_path)
        pos_1 = self.mm.get_structure_by_name("RoundaboutPaths0").paths[0]

        router = RouteFinder()
        route0 = router.find_route(pos_start, pos_1)
        route1 = router.find_route(pos_1, pos_start)

        driver = Driver(self.car)
        driver.add_route(route0)
        driver.add_route(route1)

        while True:
            self.car.refresh()
            driver.drive()
            self.car.apply()
