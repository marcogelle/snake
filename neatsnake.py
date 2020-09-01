import pygame
import random
from typing import Tuple, Set
import os
import neat
import playsnake

DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
RIGHT = {DIRS[0]: DIRS[1], DIRS[1]: DIRS[2], DIRS[2]: DIRS[3], DIRS[3]: DIRS[0],
    (0, 0): DIRS[random.randrange(4)]}
LEFT = {DIRS[0]: DIRS[3], DIRS[3]: DIRS[2], DIRS[2]: DIRS[1], DIRS[1]: DIRS[0],
    (0, 0): DIRS[random.randrange(4)]}

def get_inputs(snake, food):
    inputs = [0] * (playsnake.GRID_HEIGHT * playsnake.GRID_WIDTH)
    sn_pos = snake.positions()
    i = 0
    for y in range(playsnake.GRID_HEIGHT):
        for x in range(playsnake.GRID_WIDTH):
            if x == food.x and y == food.y:
                inputs[i] = 1
            elif x == snake.head_x() and y == snake.head_y():
                inputs[i] = -2
            elif (x, y) in sn_pos:
                inputs[i] = -1
            i += 1
    return inputs

def orient_neat_snake(snake, net, inputs):
    output = net.activate(inputs)

    max_i, max_out = 0, output[0]
    for i, o in enumerate(output[1:], 1):
        if o > max_out:
            max_i = i
            max_out = o

    # print(f'output: {output}')
    if max_i == 0:
        pass
    elif max_i == 1:
        snake.dx, snake.dy = LEFT[(snake.dx, snake.dy)]
    elif max_i == 2:
        snake.dx, snake.dy = RIGHT[(snake.dx, snake.dy)]
    else:
        assert RuntimeError("The neural net has more than 3 outputs????")

def eval_genomes(genomes, config):
    pygame.init()
    screen = pygame.display.set_mode((playsnake.SCRN_WIDTH,
        playsnake.SCRN_HEIGHT))
    pygame.display.set_caption("First Individual of this Population")
    clock = pygame.time.Clock()
    # screen = None

    nets = []
    snakes = []
    food_list = []
    gen_list = []
    ids = []
    for id, genome in genomes:
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
        ids.append(id)

    no_food = [0] * len(snakes)
    first = True
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
            orient_neat_snake(snake, net, inputs)
            genome.fitness += 0.1
            snake.move()
            assert snake.dy != 0 or snake.dx != 0

        for i, snake in enumerate(snakes):
            if (playsnake.outside(snake.head_x(), snake.head_y()) or
                snake.self_collide()):
                if ids[i] == 1:
                    print(f'{ids[i]} popped due to death')
                    playsnake.redraw_screen(screen, snakes[0], food_list[0])
                nets.pop(i)
                snakes.pop(i)
                food_list.pop(i)
                gen_list.pop(i)
                no_food.pop(i)
                ids.pop(i)
                if i == 0:
                    first = False

        for i, (snake, food, genome) in enumerate(zip(snakes, food_list, gen_list)):
            if playsnake.update_food(snake, food):
                genome.fitness += 10
                no_food[i] = 0
            else:
                no_food[i] += 1

        nf_thresh = 100
        for i, nf in enumerate(no_food):
            if nf >= nf_thresh:
                gen_list[i].fitness -= 70
        for i, nf in enumerate(no_food):
            if nf >= nf_thresh:
                if ids[i] == 1:
                    print(f'{ids[i]} popped due to time out')
                    playsnake.redraw_screen(screen, snakes[0], food_list[0])
                nets.pop(i)
                snakes.pop(i)
                food_list.pop(i)
                gen_list.pop(i)
                no_food.pop(i)

                ids.pop(i)
                if i == 0:
                    first = False

        if first:
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
    winner = p.run(eval_genomes, 500)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
