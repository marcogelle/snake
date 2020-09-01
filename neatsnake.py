import pygame
import random
from typing import Tuple, Set
import os
import neat
import visualize
import snake

def eval_genomes(genomes, config):
    snk = Snake(random.randrange(0, snake.GRID_WIDTH), random.randrange(0,
        snake.GRID_HEIGHT))
    food = Food(random.randrange(0, snake.GRID_WIDTH), random.randrange(0,
        GRID_HEIGHT))
    dx, dy = 0, 0

    run = True
    while run:


        snk.move(dx, dy)
        if (snk.head_x() < 0 or snk.head_x() >= GRID_WIDTH or
            snk.head_y() < 0 or snk.head_y() >= GRID_HEIGHT):
            run = False

        if snk.self_collide():
            run = False

        snake.check_food(snk, food)

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
