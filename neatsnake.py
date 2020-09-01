import pygame
import random
from typing import Tuple, Set
import os
import neat
import visualize
import playsnake

def get_inputs(snake, food, dx, dy):
    pass

def orient_neat_snake(net, snake, food, genome):
    pass

def eval_genomes(genomes, config):
    nets = []
    snakes = []
    food_list = []
    gen_list = []
    for _, genome in genomes:
        genome.fitness = 0

        net = neat.nn.FeedForwardNetwork.create(genome, config)
        snake = playsnake.Snake(random.randrange(0, playsnake.GRID_WIDTH),
            random.randrange(0, playsnake.GRID_HEIGHT))
        food = playsnake.Food(random.randrange(0, playsnake.GRID_WIDTH),
            random.randrange(0, playsnake.GRID_HEIGHT))

        nets.append(net)
        snakes.append(snake)
        food_list.append(food)
        gen_list.append(genome)

    while len(snakes) > 0:
        for net, snake, food, genome in zip(nets, snakes, food_list, gen_list):
            inputs = get_inputs(snake, food)
            orient_neat_snake(net, snake, food, genome)
            genome.fitness += 0.1
            snake.move()

        for i, snake in enumerate(snakes):
            if (playsnake.outside(snake.head_x(), snake.head_y()) or
                snake.self_collide()):
                nets.pop(i)
                snakes.pop(i)
                food_list.pop(i)
                gen_list.pop(i)

        playsnake.check_food(snake, food)

def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
