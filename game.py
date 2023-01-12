import pygame
from sys import exit
from random import randint, choice


# Draw a random donut from the list of donut images
def draw_donut():
    number = randint(1, 6)
    random_donut = 'donut' + str(number) + '.png'
    return random_donut


# Draw a random position for a random donut
def draw_position():
    scope_x = [i for i in range(0, 801) if i % 40 == 0]
    scope_y = [i for i in range(0, 481) if i % 40 == 0]
    x, y = choice(scope_x), choice(scope_y)
    return x, y


# Draw a grid for game board
def draw_grid():
    grid_color = (222, 255, 235)
    block_size = 40
    for x in range(0, width, block_size):
        for y in range(0, height, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, grid_color, rect, 1)


# Return multiple of 20 based on snake coordinate
def multiple_20(pos):
    if pos % 40 > 20:
        while pos % 40 != 0:
            pos += 1
    else:
        while pos % 40 != 0:
            pos -= 1
    return pos


# Draw the snake's head on the screen
def build_snake():
    screen.blit(snake_head, snake_rect)


pygame.init()
screen_size = width, height = 840, 520
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('SNAKE')
clock = pygame.time.Clock()
game_active = True
points = 0
snake_positions = []

# Donut with rect
donut = pygame.image.load(f'donuts/{draw_donut()}').convert_alpha()
donut_rect = donut.get_rect(topleft=(draw_position()))

# Snake with rect
snake_head = pygame.image.load('snake/snake-head.png').convert_alpha()
snake_rect = snake_head.get_rect(center=(width / 2, height / 2))
move = (0, 0)

# Labels for buttons which are selected by player
pressed_keys = {'up': False, 'down': False, 'right': False, 'left': False}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_active:
        # Check the key event and change the type of snake's movement
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            move = (0, -2)
            snake_rect.x = multiple_20(snake_rect.x)
        if pressed[pygame.K_DOWN]:
            move = (0, 2)
            snake_rect.x = multiple_20(snake_rect.x)
        if pressed[pygame.K_LEFT]:
            move = (-2, 0)
            snake_rect.y = multiple_20(snake_rect.y)
        if pressed[pygame.K_RIGHT]:
            move = (2, 0)
            snake_rect.y = multiple_20(snake_rect.y)

        # Check if the snake is out of the screen
        if snake_rect.left < 0 or snake_rect.right > width or snake_rect.top < 0 or snake_rect.bottom > height:
            game_active = False

        # Collect info about the position of the snake's head
        snake_positions.append(snake_rect)

        # Move the snake
        snake_rect = snake_rect.move(move)

        screen.fill((222, 238, 235))

        # Create the grid on the screen
        draw_grid()

        # Set the donut and the snake
        screen.blit(donut, donut_rect)
        build_snake()

        # Check the collision between snake and donut + count points
        if snake_rect.colliderect(donut_rect):
            donut_rect.topleft = draw_position()
            points += 1

        # Create the snake body
        for i in range(points):
            chunk_of_snake_body = pygame.Rect(
                snake_positions[-20 * (i + 1)].x + 5, snake_positions[-20 * (i + 1)].y + 5, 30, 30)
            pygame.draw.rect(screen, (0, 124, 0, 255), chunk_of_snake_body)
            # End the game when snake will touch itself
            if i > 1:
                if chunk_of_snake_body.collidepoint(snake_rect.x, snake_rect.y):
                    game_active = False

    else:
        screen.fill('black')

    clock.tick(60)
    pygame.display.update()
