class Position:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def move_x_by(self, distance):
        self.__x += distance
