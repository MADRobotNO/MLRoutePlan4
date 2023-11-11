import random

import Models.car as car
from Models.charger import Charger
from Models.point import Point

MAX_DISTANCE = 999
MIN_DISTANCE_BETWEEN_CHARGERS = 3
MAX_NUMBER_OF_CHARGERS = MAX_DISTANCE/MIN_DISTANCE_BETWEEN_CHARGERS


class Route:
    __chargers = []
    __distance = 0

    def __init__(self, y_pos=0, min_no_of_chargers=3):
        self.__y_pos = y_pos
        self.__min_no_of_chargers = min_no_of_chargers
        self.__start_point = Point(self.__distance, self.__y_pos)
        self.__stop_point = Point(MAX_DISTANCE, self.__y_pos)

    def get_all_points(self):
        points = [self.__start_point] + self.__chargers + [self.__stop_point]
        return points

    def get_chargers(self):
        return self.__chargers

    def print_route_info(self):
        print(f"##### Route info - start #####\n")
        print(f"Number of chargers {len(self.__chargers)}\n")
        for charger in self.get_chargers():
            print(f"Charger id:{charger.charger_id} at {charger.get_pos().get_x()}km")
        print(f"\n##### Route info - end #####\n")

    def __gen_chargers(self):
        distance = 0
        last_id = 0
        max_distance = (MAX_DISTANCE / self.__min_no_of_chargers).__floor__()
        if max_distance > car.CAR_RANGE:
            max_distance = car.CAR_RANGE
        for i in range(1, MAX_NUMBER_OF_CHARGERS.__floor__()):
            distance_between = random.randrange(MIN_DISTANCE_BETWEEN_CHARGERS, max_distance)
            remaining_distance = MAX_DISTANCE - distance

            if distance_between > remaining_distance:
                distance_between = remaining_distance

            distance += distance_between

            if MAX_DISTANCE - distance == 0:
                # No need for more chargers
                break

            charger = Charger(i, distance, self.__y_pos)
            self.__chargers.append(charger)

            if i == MAX_NUMBER_OF_CHARGERS and remaining_distance > 0:
                print("re-generate")
                self.generate()
                break

            last_id = i

        # end point is always charger
        charger = Charger(last_id + 1, MAX_DISTANCE, self.__y_pos)
        self.__chargers.append(charger)

    def generate(self):
        self.__distance = 0
        self.__chargers = []
        self.__gen_chargers()

    def get_stop_point(self):
        return self.__stop_point

    def create_rute_manually(self, list_of_chargers):
        self.__distance = 0
        self.__chargers = list_of_chargers
