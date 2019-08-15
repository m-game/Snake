import random
import sys

import pygame
# from pygame.examples.glcube import CUBE_COLORS
from pygame.event import EventType
from pygame.locals import *

# Initialize the game engine
pygame.init()
pygame.font.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the height and width of the screen
size = [640, 480]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("snake")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

ARROW_R = 0
ARROW_D = 1
ARROW_L = 2
ARROW_U = 3

BLOCK_SIZE = 8
PLANT_SIZE = 10
CHINK_SIZE = (PLANT_SIZE - BLOCK_SIZE) / 2

arrow = ARROW_R
food_x, food_y = -PLANT_SIZE, -PLANT_SIZE
head_x, head_y = PLANT_SIZE, PLANT_SIZE
snake_length = 0
snake_body = []

while True:
    event: EventType
    for event in pygame.event.get():
        assert isinstance(event.type, int)
        if event.type in (QUIT, QUIT):
            sys.exit()
        if event.type in (KEYDOWN, KEYDOWN):
            if event.key == pygame.K_RIGHT:
                arrow = ARROW_R
            elif event.key == pygame.K_DOWN:
                arrow = ARROW_D
            elif event.key == pygame.K_LEFT:
                arrow = ARROW_L
            elif event.key == pygame.K_UP:
                arrow = ARROW_U
    # 生成食物
    if food_x == -10 and food_y == -10:
        food_x = random.randint(0, (size[0] / PLANT_SIZE) - 1) * PLANT_SIZE
        food_y = random.randint(0, (size[1] / PLANT_SIZE) - 1) * PLANT_SIZE

    # 蛇走一步
    snake_body.append((head_x, head_y))
    if arrow == ARROW_R:
        head_x, head_y = head_x + PLANT_SIZE, head_y
    elif arrow == ARROW_D:
        head_x, head_y = head_x, head_y + PLANT_SIZE
    elif arrow == ARROW_L:
        head_x, head_y = head_x - PLANT_SIZE, head_y
    elif arrow == ARROW_U:
        head_x, head_y = head_x, head_y - PLANT_SIZE
    while len(snake_body) > snake_length:
        snake_body.pop(0)

    if head_x < 0 or head_y < 0 or head_x > size[0] - 1 or head_y > size[1] - 1:
        arrow = ARROW_R
        food_x, food_y = -PLANT_SIZE, -PLANT_SIZE
        head_x, head_y = PLANT_SIZE, PLANT_SIZE
        snake_length = 0
        snake_body = []

    if (head_x, head_y) == (food_x, food_y):
        food_x, food_y = -PLANT_SIZE, -PLANT_SIZE
        snake_length += 1

    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, (food_x + CHINK_SIZE, food_y + CHINK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, WHITE, (head_x + CHINK_SIZE, head_y + CHINK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    for x, y in snake_body:
        pygame.draw.rect(screen, WHITE, (x + CHINK_SIZE, y + CHINK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.display.update()
    pygame.time.delay(100)

