import random
import Models.car as car
from Models.charger import Charger
from Models.point import Point


class Route:
    __chargers = []
    __distance = 0
    MIN_DISTANCE_BETWEEN_CHARGERS = 3

    def __init__(self, route_id, route_length=1000, y_pos=0):
        self.route_id = route_id
        self.route_length = route_length
        self.__y_pos = y_pos
        self.__min_no_of_chargers = int(route_length/100)
        self.__max_no_of_chargers = self.route_length / self.MIN_DISTANCE_BETWEEN_CHARGERS
        self.__start_point = Point(self.__distance, self.__y_pos)
        self.__stop_point = Point(self.route_length, self.__y_pos)

    def get_all_points(self):
        points = [self.__start_point] + self.__chargers + [self.__stop_point]
        return points

    def get_chargers(self):
        return self.__chargers

    def print_route_info(self):
        print(f"##### Route info - id: {self.route_id} #####")
        print(f"Route length {self.route_length}km")
        print(f"Number of chargers {len(self.__chargers)}")
        # for charger in self.get_chargers():
        #     print(f"Charger id:{charger.charger_id} at {charger.get_pos().get_x()}km")
        print(f"##### Route info - end #####\n")

    def __gen_chargers(self):
        distance = 0
        last_id = 0
        max_distance = (self.route_length / self.__min_no_of_chargers).__floor__()
        if max_distance > car.CAR_RANGE:
            max_distance = car.CAR_RANGE
        for i in range(1, self.__max_no_of_chargers.__floor__()):
            distance_between = random.randrange(self.MIN_DISTANCE_BETWEEN_CHARGERS, max_distance)
            remaining_distance = self.route_length - distance

            if distance_between > remaining_distance:
                distance_between = remaining_distance

            distance += distance_between

            if self.route_length - distance == 0:
                # No need for more chargers
                break

            charger = Charger(i, distance, self.__y_pos)
            self.__chargers.append(charger)

            if i == self.__max_no_of_chargers and remaining_distance > 0:
                print("re-generate")
                self.generate()
                break

            last_id = i

        # end point is always charger
        charger = Charger(last_id + 1, self.route_length, self.__y_pos)
        self.__chargers.append(charger)

    def generate(self, new_route_length=None):
        self.__distance = 0
        self.__chargers = []
        if new_route_length is not None:
            self.route_length = new_route_length
        self.__gen_chargers()

    def get_stop_point(self):
        return self.__stop_point

    def add_chargers_manually(self, list_of_chargers):
        self.__distance = self.route_length
        self.__chargers = list_of_chargers
