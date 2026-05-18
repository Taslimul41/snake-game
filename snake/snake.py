import pygame
import random
import os
import sys

# IMPORT PAUSE SYSTEM
from pause import handle_pause_events, draw_pause, handle_mouse_click

# IMPORT BUTTON SYSTEM
from button import draw_buttons, handle_button_click

pygame.init()
pygame.mixer.init()

# SCREEN
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# COLORS
BLACK = (10, 15, 10)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
WHITE = (240, 240, 240)

# PATH FIX FOR EXE
def resource_path(filename):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, filename)

# LOAD IMAGE
def load_image(name):
    path = resource_path(name)

    if os.path.exists(path):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (WIDTH, HEIGHT))

    else:
        print(f"[WARNING] Missing file: {name}")

        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill((30, 30, 30))

        return surface

WELCOME_IMG = load_image("WELCOME_IMG.jpg")
GAMEOVER_IMG = load_image("end.jpg")

# LOAD SOUND
def load_sound(name):
    path = resource_path(name)

    if os.path.exists(path):
        return pygame.mixer.Sound(path)

    else:
        print(f"[WARNING] Missing sound: {name}")
        return None

EAT_SOUND = load_sound("eat.wav")
GAMEOVER_SOUND = load_sound("gameover.wav")

# BACKGROUND MUSIC
bg_music_path = resource_path("bg.mp3")

if os.path.exists(bg_music_path):
    pygame.mixer.music.load(bg_music_path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

# FONT
try:
    font = pygame.font.SysFont("Arial", 18)

except:
    font = pygame.font.SysFont("consolas", 20)

# HIGH SCORE
HS_FILE = resource_path("highscore.txt")

if os.path.exists(HS_FILE):
    with open(HS_FILE, "r") as f:
        high_score = int(f.read())

else:
    high_score = 0

# SNAKE
block = 20

def reset_game():

    snake = [[100, 100]]

    direction = "RIGHT"

    food = [
        random.randrange(0, WIDTH, block),
        random.randrange(0, HEIGHT, block)
    ]

    score = 0

    return snake, direction, food, score

snake, direction, food, score = reset_game()

state = "WELCOME"

# FUNCTIONS
def draw_grid():

    for x in range(0, WIDTH, block):
        pygame.draw.line(screen, (20, 40, 20), (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, block):
        pygame.draw.line(screen, (20, 40, 20), (0, y), (WIDTH, y))

def draw_snake(snake):

    for i, pos in enumerate(snake):

        x, y = pos

# HEAD
        if i == 0:

            pygame.draw.rect(
                screen,
                (0, 255, 120),
                (x, y, block, block),
                border_radius=8
            )

            pygame.draw.circle(screen, (0, 0, 0), (x + 5, y + 6), 3)
            pygame.draw.circle(screen, (0, 0, 0), (x + 15, y + 6), 3)

# BODY
        else:

            pygame.draw.rect(
                screen,
                (0, 180, 0),
                (x, y, block, block),
                border_radius=6
            )

def move_snake(snake, direction):

    head = snake[0].copy()

    if direction == "UP":
        head[1] -= block

    elif direction == "DOWN":
        head[1] += block

    elif direction == "LEFT":
        head[0] -= block

    elif direction == "RIGHT":
        head[0] += block

    snake.insert(0, head)

    return snake

def check_collision(snake):

    head = snake[0]

# WALL COLLISION
    if head[0] < 0 or head[0] >= WIDTH:
        return True

    if head[1] < 0 or head[1] >= HEIGHT:
        return True

# SELF COLLISION
    if head in snake[1:]:
        return True

    return False

def draw_text(txt, x, y, color=WHITE):

    render = font.render(txt, True, color)

    screen.blit(render, (x, y))

# GAME LOOP
running = True

while running:

    screen.fill(BLACK)

# EVENTS
    for event in pygame.event.get():

# QUIT
        if event.type == pygame.QUIT:
            running = False


# KEYBOARD EVENTS

        if event.type == pygame.KEYDOWN:


            if state == "WELCOME":

                if event.key == pygame.K_SPACE:
                    state = "PLAYING"


            elif state == "PLAYING":

                if event.key == pygame.K_SPACE:
                    state = "PAUSE"

                elif event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"

                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"

                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"

                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

# PAUSE
            elif state == "PAUSE":

                state, snake, direction, food, score = handle_pause_events(
                    event,
                    state,
                    snake,
                    direction,
                    food,
                    score,
                    reset_game
                )

# GAME OVER
            elif state == "GAMEOVER":

                if event.key == pygame.K_SPACE:

                    snake, direction, food, score = reset_game()

                    state = "PLAYING"

                    pygame.mixer.music.play(-1)


# MOUSE EVENTS

        if event.type == pygame.MOUSEBUTTONDOWN:

# START GAME
            if state == "WELCOME":
                state = "PLAYING"

# BUTTON CONTROL
            elif state == "PLAYING":

                direction, state = handle_button_click(
                    pygame.mouse.get_pos(),
                    direction,
                    state
                )

# PAUSE MENU
            elif state == "PAUSE":

                state, snake, direction, food, score = handle_mouse_click(
                    pygame.mouse.get_pos(),
                    snake,
                    direction,
                    food,
                    score,
                    reset_game
                )

# WELCOME
    if state == "WELCOME":

        screen.blit(WELCOME_IMG, (0, 0))

# PLAYING
    elif state == "PLAYING":

        draw_grid()

        snake = move_snake(snake, direction)

# FOOD
        pygame.draw.circle(
            screen,
            RED,
            (food[0] + block // 2, food[1] + block // 2),
            block // 2
        )

# EAT FOOD
        if snake[0] == food:

            score += 10

            if EAT_SOUND:
                EAT_SOUND.play()

            food = [
                random.randrange(0, WIDTH, block),
                random.randrange(0, HEIGHT, block)
            ]

        else:
            snake.pop()

# COLLISION
        if check_collision(snake):

            state = "GAMEOVER"

            pygame.mixer.music.stop()

            if GAMEOVER_SOUND:
                GAMEOVER_SOUND.play()

            if score > high_score:

                high_score = score

                with open(HS_FILE, "w") as f:
                    f.write(str(high_score))

        draw_snake(snake)

        draw_text(f"SCORE: {score}", 10, 10)
        draw_text(f"HIGH: {high_score}", 10, 40)

# DRAW BUTTONS
        draw_buttons(screen)

    # PAUSE
    elif state == "PAUSE":

        draw_grid()

        draw_snake(snake)

        draw_pause(screen, draw_text, snake, food, block)

# GAME OVER
    elif state == "GAMEOVER":

        screen.blit(GAMEOVER_IMG, (0, 0))

        draw_text(f"SCORE: {score}", 300, 420)

        draw_text(f"HIGH SCORE: {high_score}", 250, 460)

    pygame.display.update()

    clock.tick(10)

pygame.quit()