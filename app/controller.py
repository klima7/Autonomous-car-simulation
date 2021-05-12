from pathfinder import PathFinder
from pathfollower import PathFollower


class Controller:

    def __init__(self, car, mm):
        self.car = car
        self.mm = mm

    def start(self):
        self.car.refresh()
        self.car.cur_path = self.car.closest_path
        self.car.apply()

        start = self.mm.get_path_by_id(self.car.closest_path)
        end = self.mm.get_structure_by_name("RoundaboutPaths0").paths[0]

        finder = PathFinder()
        path = finder.find_path(start, end)
        follower = PathFollower(self.car, path)

        while True:
            self.car.refresh()
            follower.follow()
            self.car.apply()
