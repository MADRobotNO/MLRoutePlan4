import route
from car import Car
from charger import Charger
from route import Route, MAX_DISTANCE
import neat


class Commander:
    def __init__(self, factor=0.0002, factor_stops=0.02, width=1024, height=728, manual=False):
        self.__fitness_factor = factor
        self.__fitness_factor_stops = factor_stops
        self.__width = width
        self.__height = height
        self.__y_pos = self.__height / 2
        self.__route = Route(self.__y_pos)
        if manual:
            chargers = [Charger(1, 50, self.__y_pos),
                        Charger(2, 123, self.__y_pos),
                        Charger(3, 253, self.__y_pos),
                        Charger(4, 311, self.__y_pos),
                        Charger(5, 366, self.__y_pos),
                        Charger(6, 402, self.__y_pos),
                        Charger(7, 455, self.__y_pos),
                        Charger(8, 511, self.__y_pos),
                        Charger(9, 587, self.__y_pos),
                        Charger(10, 657, self.__y_pos),
                        Charger(11, 703, self.__y_pos),
                        Charger(12, 789, self.__y_pos),
                        Charger(13, 800, self.__y_pos),
                        Charger(14, 856, self.__y_pos),
                        Charger(15, 907, self.__y_pos),
                        Charger(16, 944, self.__y_pos),
                        Charger(17, MAX_DISTANCE, self.__y_pos)]
            self.__route.create_rute_manually(chargers)
        else:
            self.__route.generate()
        self.__cars = []

    def re_generate_route(self):
        print("Re-generating route")
        self.__route.generate()

    def get_route(self):
        return self.__route

    def __check_if_arrived_at_charger(self, car_x_pos):
        for charger in self.__route.get_chargers():
            if charger.get_pos().get_x() == car_x_pos:
                return charger

    def evaluate_route(self, genomes, config):
        for genome_id, genome in genomes:
            genome.fitness = 0
            penalized = False
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            car = Car(genome_id)
            self.__cars.append(car)

            remaining_distance = MAX_DISTANCE
            previous_distance = 0

            for charger_index, charger in enumerate(self.__route.get_chargers()):

                current_distance = charger.get_pos().get_x() - previous_distance

                if not car.check_if_can_drive_distance(current_distance):
                    penalized = True
                    # print(f"Car {car.car_id} went OUT OF BATTERY ({car.get_battery_level():0.2f}%) "
                    #       f"when trying to travel distance: {current_distance}km to next charger")
                    break

                car.use_battery(current_distance)
                car.travel_distance(current_distance)

                previous_distance = charger.get_pos().get_x()

                if charger_index == len(self.__route.get_chargers())-1:
                    break

                next_charger_pos = self.__route.get_chargers()[charger_index + 1].get_pos().get_x()

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
                genome.fitness = 0.0
            else:
                genome.fitness = (1 - (car.get_time_used_in_min() * self.__fitness_factor) -
                                  (car.get_battery_level() * self.__fitness_factor) -
                                  (car.get_number_of_stops() * self.__fitness_factor_stops))

                # print(f"Car reached destination with battery level {car.get_battery_level():0.2f}% "
                #       f"and time used for traveling {car.get_time_used_in_min()} minutes")

            #car.reset()
            #print()

    def test_neat(self, net):
        remaining_distance = MAX_DISTANCE
        previous_distance = 0
        car = Car(1)

        for charger_index, charger in enumerate(self.__route.get_chargers()):

            current_distance = charger.get_pos().get_x() - previous_distance

            if not car.check_if_can_drive_distance(current_distance):
                penalized = True
                # print(f"Car {car.car_id} went OUT OF BATTERY ({car.get_battery_level():0.2f}%) "
                #       f"when trying to travel distance: {current_distance}km to next charger")
                break

            car.use_battery(current_distance)
            car.travel_distance(current_distance)

            previous_distance = charger.get_pos().get_x()

            if charger_index == len(self.__route.get_chargers()) - 1:
                break

            next_charger_pos = self.__route.get_chargers()[charger_index + 1].get_pos().get_x()

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
                car.charge_battery_to_percentage(self.map_to_output_range(nn_output[1]) * 100, True)
            print(f"Car {car.car_id} used currently: {car.get_time_used_in_min()} minutes "
                  f"to travel distance: {car.get_distance_traveled()}km "
                  f"with battery level {car.get_battery_level():0.2f}%")

        print(f"Car reached destination with battery level {car.get_battery_level():0.2f}% "
              f"and time used for traveling {car.get_time_used_in_min()} minutes")

    @staticmethod
    def map_to_output_range(value):
        return (value + 1) / 2.0

    def train_neat(self, config, population, number_of_generations=100):
        global conf
        conf = config
        print("Running generations...")
        winner = population.run(self.evaluate_route, n=number_of_generations)
        best_genome = winner
        best_net = neat.nn.FeedForwardNetwork.create(best_genome, config)
        #print(f"Scenario with {len(self.__route.get_chargers())} charging stations")
        #print(f"Best Car id {best_genome.key}, Fitness: {best_genome.fitness}")
        print()
        print(f"Best genome:\n{best_genome}\n")
        car = self.get_car_by_genome_id(best_genome.key)
        print(car.print_car_info())

        self.test_neat(best_net)


    def get_car_by_genome_id(self, car_id):
        for car in self.__cars:
            if car.car_id == car_id:
                return car
