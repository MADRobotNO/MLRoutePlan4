from Models.position import Position

CAR_RANGE = 560
BATTERY_SIZE_IN_KWH = 81

# Charging speed given current battery level (current battery percentage, charging speed in kw
CHARGING_SPEED_TABLE = [
    (0, 250), (1, 250), (2, 250), (3, 250), (4, 250),
    (5, 250), (6, 250), (7, 250), (8, 250), (9, 250),
    (10, 250), (11, 246), (12, 233), (13, 220), (14, 211),
    (15, 200), (16, 197), (17, 193), (18, 190), (19, 188),
    (20, 183), (21, 179), (22, 175), (23, 172), (24, 171),
    (25, 167), (26, 165), (27, 162), (28, 159), (29, 157),
    (30, 154), (31, 151), (32, 148), (33, 146), (34, 143),
    (35, 139), (36, 138), (37, 135), (38, 132), (39, 130),
    (40, 128), (41, 125), (42, 123), (43, 122), (44, 118),
    (45, 117), (46, 114), (47, 112), (48, 110), (49, 108),
    (50, 105), (51, 103), (52, 101), (53, 99), (54, 97),
    (55, 94), (56, 93), (57, 91), (58, 89), (59, 85),
    (60, 84), (61, 81), (62, 79), (63, 79), (64, 77),
    (65, 76), (66, 75), (67, 74), (68, 73), (69, 72),
    (70, 71), (71, 70), (72, 69), (73, 67), (74, 66),
    (75, 65), (76, 64), (77, 62), (78, 61), (79, 61),
    (80, 60), (81, 58), (82, 56), (83, 53), (84, 50),
    (85, 48), (86, 45), (87, 43), (88, 42), (89, 41),
    (90, 39), (91, 38), (92, 36), (93, 35), (94, 32),
    (95, 30), (96, 27), (97, 25), (98, 22), (99, 18), (100, 13)
]


class Car:
    __max_charge_level = 100
    __current_battery_level = 100

    __one_km_in_percentage = __max_charge_level / CAR_RANGE
    __distance_traveled = 0
    __time_used = 0
    __total_charging_time = 0
    __charging_stops = 0

    def __init__(self, car_id, y=1, speed_km_h=100):
        self.car_id = car_id
        self.__position = Position(0, y)
        self.__speed_km_h = speed_km_h

    def get_pos(self):
        return self.__position

    def use_battery(self, distance):
        self.__current_battery_level -= (distance * self.__one_km_in_percentage)

    def check_if_can_drive_distance(self, distance):
        return self.__current_battery_level - (distance * self.__one_km_in_percentage) >= 0

    def get_battery_level(self):
        return self.__current_battery_level

    def get_distance_traveled(self):
        return self.__distance_traveled

    def get_time_used_in_min(self):
        return self.__time_used.__floor__()

    def get_speed(self):
        return self.__speed_km_h

    def print_car_info(self):
        print(f"####### Car id {self.car_id} - start #######")
        print(f"Speed: {self.__speed_km_h}km/h")
        print(f"Battery: {self.__current_battery_level:.2f}%")
        print(f"Distance traveled: {self.get_distance_traveled()}km")
        print(f"Total time used: {self.get_time(self.get_time_used_in_min())[0]} hours "
              f"{self.get_time(self.get_time_used_in_min())[1]} minutes")
        print(f"Charging time: {self.get_time(self.__total_charging_time)[0]} hours "
              f"{self.get_time(self.__total_charging_time)[1]} minutes, ")
        print(f"Driving time: {self.get_time(self.get_time_used_in_min() - self.__total_charging_time)[0]} hours "
              f"{self.get_time(self.get_time_used_in_min() - self.__total_charging_time)[1]} minutes, ")
        print(f"Charging stops: {self.__charging_stops}")
        print(f"####### Car info - end #######\n")

    @staticmethod
    def get_time(time_in_minutes):
        hours = int(time_in_minutes/60).__floor__()
        minutes = int(((time_in_minutes/60) % 1)*60)
        return hours, minutes

    def charge_battery_to_percentage(self, target_percentage, debug=False):
        charging_time = 0
        current_charging_speed = 0
        previous_battery_level = self.__current_battery_level

        while self.__current_battery_level < target_percentage:
            # get current charging speed
            next_battery_level = 0
            for el_index, el in enumerate(CHARGING_SPEED_TABLE):
                if self.__current_battery_level < el[0]:
                    current_charging_speed = el[1]
                    if el_index == len(CHARGING_SPEED_TABLE) - 1:
                        next_battery_level = 100
                    else:
                        next_battery_level = CHARGING_SPEED_TABLE[el_index + 1][0]
                    break

            current_energy = BATTERY_SIZE_IN_KWH * (self.__current_battery_level / 100)
            target_energy = BATTERY_SIZE_IN_KWH * (next_battery_level / 100)
            energy_needed = target_energy - current_energy

            current_charging_time = (energy_needed / current_charging_speed) * 60

            # update total charging time
            charging_time += current_charging_time

            # print(f"Current bat. level: {self.__current_battery_level:0.2f}% => {next_battery_level}%, "
            #       f"Charging speed: {current_charging_speed}kWh, curr. charging time {current_charging_time}, "
            #       f"Total charging time: {charging_time}")

            # update car data after charging to next percentage level
            self.__time_used += current_charging_time
            self.__current_battery_level = next_battery_level

        if debug:
            print(f"Charging car {self.car_id} from {previous_battery_level:0.2f}% => {target_percentage:0.4f}% "
                  f"used {charging_time:0.2f} minutes")

        self.__total_charging_time += charging_time
        self.__charging_stops += 1
        return charging_time

    def reset(self):
        self.__time_used = 0
        self.__current_battery_level = 100
        self.__distance_traveled = 0
        self.__total_charging_time = 0
        self.__charging_stops = 0

    def travel_distance(self, current_distance):
        self.__distance_traveled += current_distance
        self.__time_used += (current_distance / self.get_speed()) * 60

    def get_number_of_stops(self):
        return self.__charging_stops
