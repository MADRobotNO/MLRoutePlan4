import random
from Models.point import IPoint
from Models.position import Position


class Charger(IPoint):
    def __init__(self, charger_id, x, y=0):
        self.charger_id = charger_id
        self.__position = Position(x, y)
        self.__charging_power = random.choice([150, 200, 250])

    def get_pos(self):
        return self.__position

    def get_charging_power(self):
        return self.__charging_power
