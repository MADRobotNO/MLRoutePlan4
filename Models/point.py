from abc import ABC, abstractmethod

from Models.position import Position


class IPoint(ABC):
    @abstractmethod
    def get_pos(self):
        pass


class Point(IPoint):
    def __init__(self, x, y):
        self.__position = Position(x, y)

    def get_pos(self):
        return self.__position
