import pygame
from sys import exit

pygame.init()
screen_size = width, height = 900, 563
screen = pygame.display.set_mode((width, height))
screen.fill((222, 238, 235))
pygame.display.set_caption('SNAKE')
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(60)
