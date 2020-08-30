import pygame
import random
from typing import Tuple

SCRN_HEIGHT = 600
SCRN_WIDTH = 600
FPS = 13
BG_COLOR = (0, 0, 0) # black
GRID_SIZE = 20
assert SCRN_HEIGHT % GRID_SIZE == 0
GRID_HEIGHT = SCRN_HEIGHT // GRID_SIZE
assert SCRN_WIDTH % GRID_SIZE == 0
GRID_WIDTH = SCRN_WIDTH // GRID_SIZE

pygame.init()

screen = pygame.display.set_mode((SCRN_HEIGHT, SCRN_WIDTH))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

class Square:
    color = None

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def draw(self):
        x_coord = self.x * GRID_SIZE
        y_coord = self.y * GRID_SIZE
        pygame.draw.rect(screen, self.color, (x_coord, y_coord, GRID_SIZE, GRID_SIZE))

class Food(Square):
    color = (255, 0, 0) # red

    def spawn(self): # TODO: do not spawn where snake is
        self.x = random.randrange(0, GRID_WIDTH)
        self.y = random.randrange(0, GRID_HEIGHT)

class SnakePart(Square):
    color = (102, 255, 0) # green

    def move(self, dx, dy) -> None:
        self.x += dx
        self.y += dy

class Snake:
    def __init__(self, x: int, y: int) -> None:
        self.parts = [SnakePart(x, y)]

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

    def grow(self) -> None:
        tail = self.parts[-1]
        self.parts.append(SnakePart(tail.x, tail.y))

    def head_x(self) -> int:
        return self.parts[0].x

    def head_y(self) -> int:
        return self.parts[0].y

def update_snake_dir(keys: Tuple[bool, ...], dx: int, dy: int) -> Tuple[int, int]:
    if keys[pygame.K_UP]:
        dx, dy = 0, -1
    if keys[pygame.K_DOWN]:
        dx, dy = 0, 1
    if keys[pygame.K_LEFT]:
        dx, dy = -1, 0
    if keys[pygame.K_RIGHT]:
        dx, dy = 1, 0
    return dx, dy

def checkFood() -> None:
    if food.x == snake.head_x() and food.y == snake.head_y():
        snake.grow()
        food.spawn()

def redrawGameWindow() -> None:
    screen.fill(BG_COLOR)
    snake.draw()
    food.draw()
    pygame.display.update()

snake = Snake(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
food = Food(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
dx, dy = 0, 0

# mainloop
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False

    dx, dy = update_snake_dir(keys, dx, dy)
    snake.move(dx, dy)
    if (snake.head_x() < 0 or snake.head_x() >= GRID_WIDTH or
        snake.head_y() < 0 or snake.head_y() >= GRID_HEIGHT):
        run = False

    checkFood()
    redrawGameWindow()

pygame.quit()
