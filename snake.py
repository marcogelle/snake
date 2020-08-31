import pygame
import random
from typing import Tuple, Set

SCRN_HEIGHT = 600
SCRN_WIDTH = 600
FPS = 14
BG_COLOR = (0, 0, 0)
GRID_SIZE = 20
GRID_HEIGHT = SCRN_HEIGHT // GRID_SIZE
GRID_WIDTH = SCRN_WIDTH // GRID_SIZE

class Square:
    color = None

    def __init__(self, x: int, y: int, screen: pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.screen = screen

    def draw(self):
        x_coord = self.x * GRID_SIZE
        y_coord = self.y * GRID_SIZE
        pygame.draw.rect(self.screen, self.color, (x_coord, y_coord, GRID_SIZE, GRID_SIZE))

class SnakePart(Square):
    color = (102, 255, 0)

    def move(self, dx, dy) -> None:
        self.x += dx
        self.y += dy

class SnakeHead(SnakePart):
    color = (20, 200, 0)

class Snake:
    growth_factor = 3

    def __init__(self, x: int, y: int, screen: pygame.Surface) -> None:
        self.screen = screen
        self.parts = [SnakeHead(x, y, self.screen)]

    def __len__(self):
        return len(self.parts)

    def draw(self) -> None:
        for part in self.parts:
            part.draw()

    def move(self, dx, dy) -> None:
        head = self.parts[0]
        trail_x, trail_y = head.x, head.y
        head.move(dx, dy)
        for part in self.parts[1:]:
            dx, dy = trail_x - part.x, trail_y - part.y
            trail_x, trail_y = part.x, part.y
            part.move(dx, dy)

    def self_collide(self) -> bool:
        if (len(self) == 1 + Snake.growth_factor and
            len(self.positions()) == 1):
            return False

        head = self.parts[0]
        for p in self.parts[1:]:
            if head.x == p.x and head.y == p.y:
                return True
        return False

    def grow(self) -> None:
        tail = self.parts[-1]
        for _ in range(Snake.growth_factor):
            self.parts.append(SnakePart(tail.x, tail.y, self.screen))

    def head_x(self) -> int:
        return self.parts[0].x

    def head_y(self) -> int:
        return self.parts[0].y

    def positions(self) -> Set[Tuple[int, int]]:
        return {(p.x, p.y) for p in self.parts}

class Food(Square):
    color = (255, 0, 0)

    def spawn(self, snake: Snake):
        self.x = random.randrange(GRID_WIDTH)
        self.y = random.randrange(GRID_HEIGHT)
        snake_pos_set = snake.positions()
        while (self.x, self.y) in snake_pos_set:
            self.x = random.randrange(GRID_WIDTH)
            self.y = random.randrange(GRID_HEIGHT)

def update_snake_dir(snake: Snake, event: pygame.event.Event, dx: int, dy: int) -> Tuple[int, int]:
    if event.key in {pygame.K_UP, ord('w')} and (dy != 1 or len(snake) == 1):
        dx, dy = 0, -1
    if event.key in {pygame.K_DOWN, ord('s')} and (dy != -1 or len(snake) == 1):
        dx, dy = 0, 1
    if event.key in {pygame.K_LEFT, ord('a')} and (dx != 1 or len(snake) == 1):
        dx, dy = -1, 0
    if event.key in {pygame.K_RIGHT, ord('d')} and (dx != -1 or len(snake) == 1):
        dx, dy = 1, 0
    return dx, dy

def check_food(snake: Snake, food: Food) -> None:
    if food.x == snake.head_x() and food.y == snake.head_y():
        snake.grow()
        food.spawn(snake)

def redraw_screen(screen: pygame.Surface, snake: Snake, food: Food) -> None:
    screen.fill(BG_COLOR)
    snake.draw()
    food.draw()
    pygame.display.update()

def run_game() -> None:
    pygame.init()

    screen = pygame.display.set_mode((SCRN_WIDTH, SCRN_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    snake = Snake(random.randrange(0, GRID_WIDTH), random.randrange(0,
        GRID_HEIGHT), screen)
    dx, dy = 0, 0
    food = Food(random.randrange(0, GRID_WIDTH), random.randrange(0,
        GRID_HEIGHT), screen)

    # mainloop
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                dx, dy = update_snake_dir(snake, event, dx, dy)

        snake.move(dx, dy)
        if (snake.head_x() < 0 or snake.head_x() >= GRID_WIDTH or
            snake.head_y() < 0 or snake.head_y() >= GRID_HEIGHT):
            run = False

        if snake.self_collide():
            run = False

        check_food(snake, food)

        redraw_screen(screen, snake, food)

    print(f'Final snake length: {len(snake)}')

    pygame.quit()

if __name__ == '__main__':
    run_game()
