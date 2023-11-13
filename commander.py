import random
from Models.car import Car
from Models.route import Route
import neat
from Routes.TestRoutes import generate_test_routes


class Commander:
    def __init__(self, factor=0.0002, factor_battery=0.005, factor_stops=0.04, width=1024, height=728, number_of_routes=5, routes=None):
        self.__number_of_routes = number_of_routes
        self.__fitness_factor = factor
        self.__fitness_factor_battery = factor_battery
        self.__fitness_factor_stops = factor_stops
        self.__width = width
        self.__height = height
        self.__y_pos = self.__height / 2
        self.__routes = routes
        self.__test_routes = []
        if self.__routes is None:
            self.__routes = []
            self.generate_routes()
        self.__cars = []

    def get_routes(self):
        return self.__routes

    def evaluate_routes(self, genomes, config):
        for genome_id, genome in genomes:
            genome.fitness = 0.0
            penalized = False
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            car = Car(genome_id)
            self.__cars.append(car)

            for route in self.__routes:

                remaining_distance = route.route_length
                previous_distance = 0

                for charger_index, charger in enumerate(route.get_chargers()):

                    current_distance = charger.get_pos().get_x() - previous_distance

                    if not car.check_if_can_drive_distance(current_distance):
                        penalized = True
                        # print(f"Car {car.car_id} went OUT OF BATTERY ({car.get_battery_level():0.2f}%) "
                        #       f"when trying to travel distance: {current_distance}km to next charger")
                        break

                    car.use_battery(current_distance)
                    car.travel_distance(current_distance)

                    previous_distance = charger.get_pos().get_x()

                    if charger_index == len(route.get_chargers())-1:
                        break

                    next_charger_pos = route.get_chargers()[charger_index + 1].get_pos().get_x()

                    distance_to_next_station = next_charger_pos - current_distance
                    remaining_distance -= current_distance

                    # normalize data
                    normalized_remaining_distance = remaining_distance / 1000
                    normalized_current_battery_level = car.get_battery_level() / 100
                    normalized_distance_to_next_station = distance_to_next_station / 1000
                    normalized_time_used = car.get_time_used_in_min() / 1000

                    nn_inputs = [normalized_remaining_distance, normalized_current_battery_level,
                                 normalized_distance_to_next_station, normalized_time_used]

                    nn_output = net.activate(nn_inputs)

                    if nn_output[0] > 0.5:  # Stop at the station if the output is greater than 0.5
                        car.charge_battery_to_percentage(self.map_to_output_range(nn_output[1]) * 100)
                    # print(f"Car {car.car_id} used currently: {car.get_time_used_in_min()} minutes "
                    #       f"to travel distance: {car.get_distance_traveled()}km "
                    #       f"with battery level {car.get_battery_level():0.2f}%")

                if penalized:
                    genome.fitness += 0.0
                else:
                    genome.fitness += (1 - (car.get_time_used_in_min() * self.__fitness_factor) -
                                       (car.get_battery_level() * self.__fitness_factor_battery) -
                                       (car.get_number_of_stops() * self.__fitness_factor_stops))

                car.reset()

                # print(f"Car reached destination with battery level {car.get_battery_level():0.2f}% "
                #       f"and time used for traveling {car.get_time_used_in_min()} minutes")

    def test_neat(self, config, winner_genome, number_of_tests, add_manual_routes=True):
        self.generate_test_routes(number_of_tests, add_manual_routes)
        passed_tests = 0
        net = neat.nn.FeedForwardNetwork.create(winner_genome, config)
        car = Car(1)

        for i, route in enumerate(self.__test_routes):

            print(f"\n===============================================================")
            print(f"Test nr.{i} for route length {route.route_length}km")
            print(f"===============================================================\n")
            route.print_route_info()

            remaining_distance = route.route_length
            previous_distance = 0

            for charger_index, charger in enumerate(route.get_chargers()):

                current_distance = charger.get_pos().get_x() - previous_distance

                if not car.check_if_can_drive_distance(current_distance):
                    penalized = True
                    # print(f"Car {car.car_id} went OUT OF BATTERY ({car.get_battery_level():0.2f}%) "
                    #       f"when trying to travel distance: {current_distance}km to next charger")
                    break

                car.use_battery(current_distance)
                car.travel_distance(current_distance)

                previous_distance = charger.get_pos().get_x()

                if charger_index == len(route.get_chargers()) - 1:
                    break

                next_charger_pos = route.get_chargers()[charger_index + 1].get_pos().get_x()

                distance_to_next_station = next_charger_pos - current_distance
                remaining_distance -= current_distance

                # normalize data
                normalized_remaining_distance = remaining_distance / 1000
                normalized_current_battery_level = car.get_battery_level() / 100
                normalized_distance_to_next_station = distance_to_next_station / 1000
                normalized_time_used = car.get_time_used_in_min() / 1000

                nn_inputs = [normalized_remaining_distance, normalized_current_battery_level,
                             normalized_distance_to_next_station, normalized_time_used]

                nn_output = net.activate(nn_inputs)

                if nn_output[0] > 0.5:  # Stop at the station if the output is greater than 0.5
                    car.charge_battery_to_percentage(self.map_to_output_range(nn_output[1]) * 100)
                #print(f"Car {car.car_id} used currently: {car.get_time_used_in_min()} minutes "
                #      f"to travel distance: {car.get_distance_traveled()}km "
                #      f"with battery level {car.get_battery_level():0.2f}%")

            #print(f"Car reached destination with battery level {car.get_battery_level():0.2f}% "
            #      f"and time used for traveling {car.get_time_used_in_min()} minutes")

            car.print_car_info()
            passed = car.get_distance_traveled() == route.route_length

            if passed:
                passed_tests += 1
                print(f"Car PASSED test! Traveled distance Traveled distance "
                      f"{car.get_distance_traveled()}/{route.route_length}km")
            else:
                print(
                    f"Car FAILED test and did not reached the target. Traveled distance "
                    f"{car.get_distance_traveled()}/{route.route_length}km")
            car.reset()
        print(f"\nTOTAL PASSED TESTS: {passed_tests}/{len(self.__test_routes)}")
        return passed_tests

    @staticmethod
    def map_to_output_range(value):
        return (value + 1) / 2.0

    def train_neat(self, config, population, number_of_generations=100):
        global conf
        conf = config
        print("Running generations...")
        winner = population.run(self.evaluate_routes, n=number_of_generations)
        best_genome = winner
        print()
        print(f"Best genome:\n{best_genome}\n")
        print(f"\nFITNESS: {best_genome.fitness}\n")

        return winner

    def get_car_by_genome_id(self, car_id):
        for car in self.__cars:
            if car.car_id == car_id:
                return car

    def generate_routes(self):
        for i in range(0, self.__number_of_routes):
            route_length = random.randint(500, 4000)
            route = Route(i, route_length=route_length)
            route.generate()
            self.__routes.append(route)

    def generate_test_routes(self, number_of_tests, add_manual_routes):
        for i in range(0, number_of_tests):
            route_length = random.randint(400, 5000)
            route = Route(i, route_length=route_length)
            route.generate()
            self.__test_routes.append(route)
        if add_manual_routes:
            self.__test_routes.extend(generate_test_routes())

    def print_routes_info(self):
        for route in self.__routes:
            route.print_route_info()
