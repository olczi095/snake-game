import pygame
from random import randint, choice
from sys import exit
from time import sleep


# Draw a random donut from the list of donut images
def draw_donut():
    number = randint(1, 6)
    random_donut = 'donut' + str(number) + '.png'
    return random_donut


# Draw a random position for a random donut
def draw_position():
    scope_x = [num for num in range(game_screen_x[0], game_screen_x[1] - 39) if num % 40 == 0]
    scope_y = [num for num in range(game_screen_y[0], game_screen_y[1] - 39) if num % 40 == 0]
    x, y = choice(scope_x), choice(scope_y)
    return x, y


# Draw a grid for game board
def draw_grid():
    grid_color = (222, 255, 235)
    block_size = 40
    for x in range(game_screen_x[0], game_screen_x[1], block_size):
        for y in range(game_screen_y[0], game_screen_y[1], block_size):
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


# Draw the screen to start the game
def start_screen(base_screen):
    base_screen.blit(background, (0, 0))
    text = first_font.render('SNAKE', False, (255, 215, 0))
    text_rect = text.get_rect(center=(width / 2, height / 2 - 80))
    base_screen.blit(text, text_rect)
    second_font.set_bold(True)
    text2 = second_font.render('Press SPACE to start', False, '#7cda9e')
    text2_rect = text2.get_rect(center=(width / 2, height / 2 + 30))
    base_screen.blit(text2, text2_rect)


# Draw the screen to end the game and ask if user wants to play again
def end_screen(base_screen, score):
    base_screen.blit(background, (0, 0))
    first_font.size('80')
    text = third_font.render(f'Your score: {score}', False, (255, 215, 0))
    text_rect = text.get_rect(center=(width / 2, height / 2 - 50))
    base_screen.blit(text, text_rect)
    text2 = second_font.render('Press SPACE to play again', False, '#7cda9e')
    text3 = second_font.render('Press ESC to quit', False, '#7cda9e')
    text2_rect = text2.get_rect(center=(width / 2, height / 2 + 30))
    text3_rect = text3.get_rect(center=(width / 2, height / 2 + 60))
    base_screen.blit(text2, text2_rect)
    base_screen.blit(text3, text3_rect)


# Draw the score above the game screen
def display_score(score):
    text = second_font.render(f'{score}', False, (255, 215, 0))
    text_rect = text.get_rect(center=(game_screen_x[0] + 60, game_screen_y[0] / 2))
    donut_score_rect = donut.get_rect(midleft=(game_screen_x[0], game_screen_y[0] / 2))
    screen.blit(text, text_rect)
    screen.blit(donut, donut_score_rect)


# Draw game time above the game screen
def display_time(time):
    text = second_font.render(f'{time}', False, (0, 180, 50, 190))
    text_rect = text.get_rect(midleft=(width / 2, game_screen_y[0] / 2))
    clock_image = pygame.image.load('screen/clock-image.png').convert_alpha()
    clock_image = pygame.transform.smoothscale(clock_image, (40, 40))
    clock_rect = clock_image.get_rect(midright=(width / 2 - 10, game_screen_y[0] / 2))
    screen.blit(text, text_rect)
    screen.blit(clock_image, clock_rect)


# Draw sound image
def display_sound():
    if audio_status:
        screen.blit(sound_image, sound_rect)
        pygame.mixer.music.unpause()
    else:
        screen.blit(sound_image, sound_rect)
        pygame.draw.line(screen, 'red', sound_rect.topleft, sound_rect.bottomright, 2)
        pygame.mixer.music.pause()


# Stop the board and play "negative-beep"
def the_end():
    pygame.mixer.music.stop()
    negative_beep.play()
    sleep(3)
    pygame.mixer.music.play()
    pygame.mixer.music.pause()


pygame.init()
pygame.mixer.init()
game_size = game_width, game_height = 760, 440
screen_size = width, height = 840, 560
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('SNAKE')
clock = pygame.time.Clock()
state = 'start_menu'  # To choose -> start_menu, game_active, end_game
snake_positions = []
points = 0
end_score = 0
start_time = 0
audio_status = False  # Only check status while playing
game_screen_x = (40, game_width + 40)  # For displaying the game board (when snake can move)
game_screen_y = (80, game_height + 80)  # For displaying the game board (when snake can move)

# Load audio
pygame.mixer.music.load('sounds/magic-sound.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)
eating_sound = pygame.mixer.Sound('sounds/eating-sound.mp3')
negative_beep = pygame.mixer.Sound('sounds/negative-beep.mp3')
negative_beep.set_volume(0.5)

# Load sound image
sound_image = pygame.image.load('screen/sound.svg').convert_alpha()
sound_image = pygame.transform.smoothscale(sound_image, (40, 40))
sound_rect = sound_image.get_rect(midright=(game_screen_x[1], game_screen_y[0] / 2))

# Load the fonts
first_font = pygame.font.Font('fonts/SparkyStonesRegular.ttf', 150)
second_font = pygame.font.Font('fonts/OpenSans-Light.ttf', 30)
third_font = pygame.font.Font('fonts/SparkyStonesRegular.ttf', 80)

# Load the background image
background = pygame.image.load('screen/background.jpg').convert()
pygame.transform.scale(background, screen_size)

# Donut with rect
donut = pygame.image.load(f'donuts/{draw_donut()}').convert_alpha()
donut_rect = donut.get_rect(topleft=(draw_position()))

# Snake with rect
snake_head = pygame.image.load('snake/snake-head.png').convert_alpha()
snake_rect = snake_head.get_rect(center=((game_screen_x[1] + game_screen_x[0]) / 2,
                                         (game_screen_y[1] + game_screen_y[0]) / 2))
move = (0, 0)

# Labels for buttons which are selected by player
pressed_keys = {'up': False, 'down': False, 'right': False, 'left': False}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state = 'game_active'
                end_score = 0  # Reset the score before the new game
                start_time = pygame.time.get_ticks()

                # Change background music
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('sounds/background-music.mp3')
                pygame.mixer.music.play(-1)

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if sound_rect.collidepoint(pygame.mouse.get_pos()):
                if audio_status is True:
                    audio_status = False
                else:
                    audio_status = True

    if state == 'start_menu':
        start_screen(screen)

    elif state == 'game_active':
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
        if snake_rect.left < game_screen_x[0] or snake_rect.right > game_screen_x[1] \
                or snake_rect.top < game_screen_y[0] or snake_rect.bottom > game_screen_y[1]:
            state = 'end_game'
            the_end()

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

        # Display some element during the game
        display_score(points)
        game_time = round((pygame.time.get_ticks() - start_time) / 1000, 2)
        display_time(game_time)
        display_sound()

        # Check the collision between snake and donut + count points
        if snake_rect.colliderect(donut_rect):
            donut_rect.topleft = draw_position()
            eating_sound.play()
            points += 1
            end_score += 1

        # Create the snake body
        for i in range(points):
            chunk_of_snake_body = pygame.Rect(
                snake_positions[-20 * (i + 1)].x + 5, snake_positions[-20 * (i + 1)].y + 5, 30, 30)
            pygame.draw.rect(screen, (0, 124, 0, 255), chunk_of_snake_body)
            # End the game when snake will touch itself
            if i > 1:
                if chunk_of_snake_body.collidepoint(snake_rect.x, snake_rect.y):
                    state = 'end_game'
                    the_end()

    elif state == 'end_game':
        end_screen(screen, end_score)
        snake_rect = snake_head.get_rect(center=(width / 2, height / 2))
        move = (0, 0)
        points = 0
        pygame.mixer.music.unpause()

    clock.tick(60)
    pygame.display.update()
