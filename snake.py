import pygame
import random

SCRN_HEIGHT = 600
SCRN_WIDTH = 600
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
    color = (255, 0, 0)

class SnakePart(Square):
    color = (102, 255, 0)

class Snake:
    def __init__(self, x: int, y: int) -> None:
        self.head = SnakePart(x, y)

    def draw(self) -> None:
        self.head.draw()

def redrawGameWindow() -> None:
    screen.fill(BG_COLOR)
    snake.draw()
    food.draw()

    pygame.display.update()

snake = Snake(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
food = Food(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
run = True
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    if keys[pygame.K_UP]:
        pass
    if keys[pygame.K_DOWN]:
        pass
    if keys[pygame.K_LEFT]:
        pass
    if keys[pygame.K_RIGHT]:
        pass

    redrawGameWindow()

pygame.quit()
