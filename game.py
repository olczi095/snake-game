import pygame
from sys import exit
from random import randint


def draw_donut():
    number = randint(1, 6)
    random_donut = 'donut' + str(number) + '.png'
    return random_donut


pygame.init()
screen_size = width, height = 900, 563
screen = pygame.display.set_mode((width, height))
screen.fill((222, 238, 235))
pygame.display.set_caption('SNAKE')
clock = pygame.time.Clock()
donut = pygame.image.load(f'donuts/{draw_donut()}').convert_alpha()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(60)
