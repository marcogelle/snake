import pygame

SCRN_HEIGHT = 600
SCRN_WIDTH = 600
BG_COLOR = (0, 0, 0)
GRID_SIZE = 20
assert SCRN_HEIGHT % GRID_SIZE == 0
assert SCRN_WIDTH % GRID_SIZE == 0

pygame.init()

screen = pygame.display.set_mode((SCRN_HEIGHT, SCRN_WIDTH))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

class Food:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        pass

def redrawGameWindow():
    screen.fill(BG_COLOR)

snake = Snake()
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
