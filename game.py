import pygame
from sys import exit
from random import randint


# Draw a random donut from the list of donut images
def draw_donut():
    number = randint(1, 6)
    random_donut = 'donut' + str(number) + '.png'
    return random_donut


# Draw a random position for a random donut
def draw_position():
    x, y = randint(0, width - 40), randint(0, height - 40)
    return x, y


pygame.init()
screen_size = width, height = 900, 563
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('SNAKE')
clock = pygame.time.Clock()

# Donut with rect
donut = pygame.image.load(f'donuts/{draw_donut()}').convert_alpha()
donut_rect = donut.get_rect(topleft=(draw_position()))

snake = pygame.image.load('snake/snake-head.png').convert_alpha()
snake_rect = snake.get_rect(center=(width / 2, height / 2))
move = (0, 0)

# Labels for buttons which are selected by player
pressed_keys = {'up': False, 'down': False, 'right': False, 'left': False}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Check the key event and change the type of snake's movement
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        move = (0, -2)
    if pressed[pygame.K_DOWN]:
        move = (0, 2)
    if pressed[pygame.K_LEFT]:
        move = (-2, 0)
    if pressed[pygame.K_RIGHT]:
        move = (2, 0)

    # Move the snake
    snake_rect = snake_rect.move(move)

    screen.fill((222, 238, 235))
    screen.blit(donut, donut_rect)
    screen.blit(snake, snake_rect)
    pygame.display.update()
    clock.tick(60)
