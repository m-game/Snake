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

caption_show = "snake"
pygame.display.set_caption(caption_show)

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

ARROW_R = 0
ARROW_D = 1
ARROW_L = 2
ARROW_U = 3

SPEED = 0
BLOCK_SIZE = 18
PLANT_SIZE = 20
CHINK_SIZE = (PLANT_SIZE - BLOCK_SIZE) / 2

caption = f"snake speed: {SPEED}"
sleep = False
alive = True
arrow = ARROW_R
food_x, food_y = PLANT_SIZE, PLANT_SIZE
head_x, head_y = PLANT_SIZE, PLANT_SIZE
snake_length = 0
snake_body = []

i = 1
while True:
    clock.tick(60)
    event: EventType
    for event in pygame.event.get():
        assert isinstance(event.type, int)
        if event.type in (QUIT, QUIT):
            sys.exit()
        if event.type in (KEYDOWN, KEYDOWN):
            if event.key == pygame.K_RIGHT:
                arrow = ARROW_R if arrow != ARROW_L else arrow
            elif event.key == pygame.K_DOWN:
                arrow = ARROW_D if arrow != ARROW_U else arrow
            elif event.key == pygame.K_LEFT:
                arrow = ARROW_L if arrow != ARROW_R else arrow
            elif event.key == pygame.K_UP:
                arrow = ARROW_U if arrow != ARROW_D else arrow
            elif event.key == pygame.K_SPACE:
                sleep = not sleep
                if not alive:
                    caption = f"snake speed: {SPEED}"
                    sleep = False
                    alive = True
                    arrow = ARROW_R
                    food_x, food_y = PLANT_SIZE, PLANT_SIZE
                    head_x, head_y = PLANT_SIZE, PLANT_SIZE
                    snake_length = 0
                    snake_body = []
            elif event.key == pygame.K_PAGEUP:
                SPEED = SPEED + 1 if SPEED < 10 else SPEED
                caption = f"snake speed: {SPEED}"
            elif event.key == pygame.K_PAGEDOWN:
                SPEED = SPEED - 1 if SPEED > 1 else SPEED
                caption = f"snake speed: {SPEED}"

    # 更新标题
    if caption_show != caption:
        pygame.display.set_caption(caption)
        caption_show = caption

    # 游戏停止控制
    if sleep or not alive:
        continue

    # 速度控制
    if i % (11 - SPEED) == 0:
        i = 1
        # 生成食物
        if (food_x, food_y) in [(head_x, head_y)] + snake_body:
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

        # 判断墙壁边界
        if head_x < 0 or head_y < 0 or head_x > size[0] - 1 or head_y > size[1] - 1:
            caption = f"snake speed: {SPEED} die"
            alive = False
            continue
        if (head_x, head_y) in snake_body:
            caption = f"snake speed: {SPEED} die"
            alive = False
            continue

        # 吃食物长大
        if (head_x, head_y) == (food_x, food_y):
            snake_length += 1

        # 更新画面
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, (food_x + CHINK_SIZE, food_y + CHINK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for x, y in snake_body:
            pygame.draw.rect(screen, WHITE, (x + CHINK_SIZE, y + CHINK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, GREEN, (head_x + CHINK_SIZE, head_y + CHINK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.update()
    i += 1
