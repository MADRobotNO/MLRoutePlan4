import os
import time
import neat

from commander import Commander

GENERATIONS = 100

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

    commander = Commander(manual=True)
    commander.get_route().print_route_info()

    commander.train_neat(config, population, GENERATIONS)
