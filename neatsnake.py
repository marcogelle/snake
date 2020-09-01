import pygame
import random
from typing import Tuple, Set
import os
import neat
import playsnake

def get_inputs(snake, food):
    return [1] * 24 # dummy function, will replace later

def orient_neat_snake(net, snake, food):
    # dummy function, will replace later
    snake.dx = 1
    snake.dy = 0

def eval_genomes(genomes, config):
    pygame.init()
    screen = pygame.display.set_mode((playsnake.SCRN_WIDTH,
        playsnake.SCRN_HEIGHT))
    pygame.display.set_caption("Snake from First Genome of this Population")
    clock = pygame.time.Clock()

    nets = []
    snakes = []
    food_list = []
    gen_list = []
    for _, genome in genomes:
        genome.fitness = 0

        net = neat.nn.FeedForwardNetwork.create(genome, config)
        snake = playsnake.Snake(random.randrange(0, playsnake.GRID_WIDTH),
            random.randrange(0, playsnake.GRID_HEIGHT), screen)
        food = playsnake.Food(random.randrange(0, playsnake.GRID_WIDTH),
            random.randrange(0, playsnake.GRID_HEIGHT), screen)

        nets.append(net)
        snakes.append(snake)
        food_list.append(food)
        gen_list.append(genome)

    run = True
    while run and snakes:
        clock.tick(playsnake.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        for net, snake, food, genome in zip(nets, snakes, food_list, gen_list):
            inputs = get_inputs(snake, food)
            orient_neat_snake(net, snake, food)
            genome.fitness += 0.1
            snake.move()

        for i, snake in enumerate(snakes):
            if (playsnake.outside(snake.head_x(), snake.head_y()) or
                snake.self_collide()):
                nets.pop(i)
                snakes.pop(i)
                food_list.pop(i)
                gen_list.pop(i)

        for snake, food, genome in zip(snakes, food_list, gen_list):
            if playsnake.update_food(snake, food):
                genome.fitness += 10

        if snakes:
            playsnake.redraw_screen(screen, snakes[0], food_list[0])

    pygame.quit()

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
