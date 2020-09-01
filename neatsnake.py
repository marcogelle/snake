import pygame
import random
from typing import Tuple, Set
import os
import neat
import playsnake

DISPLAY = False

def get_inputs(snake, food):
    x, y = snake.head_x(), snake.head_y()
    inputs = []

    # Distance to food
    inputs.append(food.x - x)
    inputs.append(food.y - y)

    # Distances to walls
    inputs.append(y)
    inputs.append(playsnake.GRID_HEIGHT - y)
    inputs.append(x)
    inputs.append(playsnake.GRID_WIDTH - x)

    # Distances to snake parts. -1 if no snake part in that direction.
    pos = snake.positions()
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)):
        x1, y1 = x, y
        i = 0
        found = False
        while not playsnake.outside(x1, y1):
            x1 += dx
            y1 += dy
            i += 1
            if (x1, y1) in pos:
                inputs.append(i)
                found = True
                break
        if not found:
            inputs.append(0)

    return inputs

def orient_neat_snake(snake, net, inputs):
    output = net.activate(inputs)

    max_i, max_out = 0, output[0]
    for i, o in enumerate(output[1:], 1):
        if o > max_out:
            max_i = i

    if max_i == 0:
        snake.dx, snake.dy = 0, -1
    elif max_i == 1:
        snake.dx, snake.dy = 0, 1
    elif max_i == 2:
        snake.dx, snake.dy = -1, 0
    elif max_i == 2:
        snake.dx, snake.dy = 1, 0
    else:
        assert RuntimeError("The neural net has more than 4 outputs????")

def eval_genomes(genomes, config):
    screen, clock = None, None
    if DISPLAY:
        pygame.init()
        screen = pygame.display.set_mode((playsnake.SCRN_WIDTH,
            playsnake.SCRN_HEIGHT))
        pygame.display.set_caption("First Individual of this Population")
        clock = pygame.time.Clock()
    else:
        screen = None

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

    no_food = [0] * len(snakes)
    first = True
    run = True
    while run and snakes:
        if DISPLAY:
            clock.tick(playsnake.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

        for net, snake, food, genome in zip(nets, snakes, food_list, gen_list):
            inputs = get_inputs(snake, food)
            orient_neat_snake(snake, net, inputs)
            genome.fitness += 0.1
            snake.move()

        for i, snake in enumerate(snakes):
            if (playsnake.outside(snake.head_x(), snake.head_y()) or
                snake.self_collide()):
                nets.pop(i)
                snakes.pop(i)
                food_list.pop(i)
                gen_list.pop(i)
                no_food.pop(i)
                if i == 0:
                    first = False

        for i, (snake, food, genome) in enumerate(zip(snakes, food_list, gen_list)):
            if playsnake.update_food(snake, food):
                genome.fitness += 10
                no_food[i] = 0
            else:
                no_food[i] += 1

        eleven = 100
        for i, nf in enumerate(no_food):
            if nf >= eleven:
                gen_list[i].fitness -= 100
        for i, nf in enumerate(no_food):
            if nf >= eleven:
                nets.pop(i)
                snakes.pop(i)
                food_list.pop(i)
                gen_list.pop(i)
                no_food.pop(i)
                if i == 0:
                    first = False

        if DISPLAY and first:
            playsnake.redraw_screen(screen, snakes[0], food_list[0])

    if DISPLAY:
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
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
