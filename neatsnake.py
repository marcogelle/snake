import pygame
import random
from typing import Tuple, Set
import os
import neat
import visualize
import playsnake

def get_inputs(snake, food, dx, dy):
    pass

def eval_genomes(genomes, config):
    nets = []
    snakes = []
    food_list = []
    ge = []
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
        ge.append(genome)





    dx, dy = 0, 0

    run = True
    while run:
        inputs = get_inputs(snake, food, dx, dy)



        snake.move(dx, dy)
        if (playsnake.outside(snake.head_x(), snake.head_y())):
            run = False

        if snake.self_collide():
            run = False

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
