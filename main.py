import os
import pickle
import time
from datetime import datetime
import neat
from Routes.TrainRoutes import generate_train_routes
from commander import Commander


if __name__ == '__main__':
    start_time = time.ctime()
    print(f"\nStart time: {start_time}\n")

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    population = neat.Population(config)

    # Add statistics
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(10, filename_prefix='ML_Models/Checkpoints/neat-checkpoint-'))

    no_of_generations = int(input("Enter number of generations for training: "))
    try:
        no_of_generations = int(no_of_generations)
    except:
        no_of_generations = 1

    manual_routes = generate_train_routes()
    commander = Commander(routes=manual_routes)
    print()
    commander.print_routes_info()

    winner = commander.train_neat(config, population, no_of_generations)
    user_input = input("Would You like to save model? (If Yes input Y, otherwise input anything. Then press Enter): ")

    if user_input.upper() == 'Y':
        now_datetime = datetime.now().strftime("%d%m%Y_%H%M%S")
        with open(f"ml_models/{now_datetime}.pickle", "wb") as f:
            pickle.dump(winner, f)
        print(f"Model saved in ml_models/{now_datetime}.pickle")

    number_of_tests = input("Enter number of test You want to preform: ")
    try:
        number_of_tests = int(number_of_tests)
    except:
        number_of_tests = 0

    if number_of_tests > 0:
        print("\n===== TESTS =====")
        passed_tests = commander.test_neat(config, winner, number_of_tests, add_manual_routes=True)
        print(f"\nTOTAL PASSED TESTS: {passed_tests}/{number_of_tests}")

