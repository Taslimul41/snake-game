import pygame
import random
import os
import sys
import math

# IMPORT PAUSE SYSTEM
from pause import handle_pause_events, draw_pause, handle_mouse_click

# IMPORT BUTTON SYSTEM
from button import draw_buttons, handle_button_click

pygame.init()
pygame.mixer.init()

# SCREEN
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# COLORS
BLACK = (10, 15, 10)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
WHITE = (240, 240, 240)

# GAME SETTINGS
SNAKE_SIZE = 20
SPEED = 5
food_size = 40
block = 20
BODY_GAP = 9
TURN_SPEED = 0.24
HEAD_SIZE = 11
BODY_SIZE = 20
TAIL_SIZE = 3
grow=0


spawn_protection = 180
resize_protection = 0

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

# LOAD FRUITS
def load_fruits():
    fruit_names = ["apple.png", "orange.png", "grape.png",
                   "watermelon.png", "lichy.png", "cherry.png"]
    images = []
    for name in fruit_names:
        path = resource_path(name)
        if os.path.exists(path):
            img = pygame.transform.scale(
                pygame.image.load(path),
                (food_size, food_size)
            )
            images.append(img)
        else:
            print(f"[WARNING] Missing fruit: {name}")
            surf = pygame.Surface((food_size, food_size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 80, 80), (food_size // 2, food_size // 2), food_size // 2)
            images.append(surf)
    return images

fruit_images = load_fruits()
BG_IMG = load_image("bg.jpg")

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
    font = pygame.font.SysFont("impact", 20,)
except:
    font = pygame.font.SysFont("arial", 20)

# HIGH SCORE
HS_FILE = resource_path("highscore.txt")
if os.path.exists(HS_FILE):
    with open(HS_FILE, "r") as f:
        try:
            high_score = int(f.read().strip())
        except:
            high_score = 0
else:
    high_score = 0


def reset_game():
    global spawn_protection
    spawn_protection = 180  # FIX: 3 second safe time

    snake = []
    start_x = 300
    start_y = 300

    # SNAKE SIZE
    for i in range(15):
        snake.append([start_x - i * (BODY_GAP * 5), start_y])

    direction = "RIGHT"

    food = spawn_food_safe(snake)
    score = 0
    fruit_img = random.choice(fruit_images)

    return snake, direction, food, score, fruit_img


def spawn_food_safe(snake):
    max_tries = 100
    for _ in range(max_tries):
        fx = random.randrange(food_size // 2, WIDTH - food_size // 2, block)
        fy = random.randrange(food_size // 2, HEIGHT - food_size // 2, block)

        too_close = False
        for seg in snake:
            dx = seg[0] - fx
            dy = seg[1] - fy
            if math.sqrt(dx * dx + dy * dy) < 60:
                too_close = True
                break

        if not too_close:
            return [fx, fy]

    # fallback
    return [random.randrange(food_size // 2, WIDTH - food_size // 2, block),
            random.randrange(food_size // 2, HEIGHT - food_size // 2, block)]


snake, direction, food, score, fruit_img = reset_game()
angle = 0
state = "WELCOME"

# FIREFLIES
fireflies = []
for i in range(20):
    fireflies.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "size": random.choice([1, 1, 2, 1]),
        "alpha": random.randint(50, 255),
        "fade_speed": random.uniform(2, 5),
        "life": random.randint(20, 80),
        "dx": random.uniform(-0.3, 0.3),
        "dy": random.uniform(-0.3, 0.3)
    })



# DRAW SNAKE
def draw_snake(snake):
    n = len(snake)
    if n < 2:
        return

    #BODY
    for i in range(n - 1, 0, -1):
        x1, y1 = snake[i]
        x2, y2 = snake[i - 1]

        progress = i / n

        thickness = 14 - progress * 8
        if thickness < 4:
            thickness = 4

        # Color
        g = int(200 - progress * 60)
        r = int(10 + progress * 30)
        body_color = (r, g, 30)

        # Draw rounded segment
        pygame.draw.line(screen, body_color, (int(x1), int(y1)), (int(x2), int(y2)), int(thickness * 2))
        pygame.draw.circle(screen, body_color, (int(x1), int(y1)), int(thickness))
        pygame.draw.circle(screen, body_color, (int(x2), int(y2)), int(thickness))

        dx = x2 - x1
        dy = y2 - y1
        seg_len = math.sqrt(dx * dx + dy * dy)

        if seg_len < 1:
            continue

        nx = dx / seg_len
        ny = dy / seg_len

        px = -ny
        py = nx

        scale_spacing = 9
        num_scales = max(1, int(seg_len / scale_spacing))

        sd = int(20 + progress * 30)
        scale_dark  = (max(0, r - sd), max(0, g - 50), 10)    # darker shade
        scale_mid   = (max(0, r + 10), min(255, g + 30), 40)  # lighter highlight

        for s in range(num_scales):
            t = (s + 0.5) / num_scales
            cx = x1 + dx * t
            cy = y1 + dy * t
            sr = thickness * 0.72   # scale radius ~ 72% of body thickness

            row_offset = sr * 0.5 if (s % 2 == 0) else -sr * 0.5
            scx = cx + px * row_offset
            scy = cy + py * row_offset

            pygame.draw.circle(screen, scale_dark, (int(scx), int(scy)), max(1, int(sr)))
            hi_x = scx - sr * 0.3
            hi_y = scy - sr * 0.3
            pygame.draw.circle(screen, scale_mid, (int(hi_x), int(hi_y)), max(1, int(sr * 0.35)))

    # HEAD
    head_x, head_y = snake[0]
    forward_x = math.cos(angle)
    forward_y = math.sin(angle)
    side_x = math.cos(angle + math.pi / 2)
    side_y = math.sin(angle + math.pi / 2)

    pygame.draw.circle(screen, (20, 160, 40), (int(head_x), int(head_y)), 15)

    front_x = head_x + forward_x * 9
    front_y = head_y + forward_y * 9
    pygame.draw.circle(screen, (15, 180, 50), (int(front_x), int(front_y)), 10)

    cheek1 = (int(head_x - forward_x * 2 + side_x * 8),
               int(head_y - forward_y * 2 + side_y * 8))
    cheek2 = (int(head_x - forward_x * 2 - side_x * 8),
               int(head_y - forward_y * 2 - side_y * 8))
    pygame.draw.circle(screen, (18, 155, 45), cheek1, 7)
    pygame.draw.circle(screen, (18, 155, 45), cheek2, 7)

    for hsi in range(6):
        a = math.pi * hsi / 3
        hsx = head_x + math.cos(a) * 7
        hsy = head_y + math.sin(a) * 7
        pygame.draw.circle(screen, (10, 120, 30), (int(hsx), int(hsy)), 3)
        pygame.draw.circle(screen, (30, 200, 70), (int(hsx - 1), int(hsy - 1)), 1)

    hi_hx = int(head_x - forward_x * 4 + side_x * 2)
    hi_hy = int(head_y - forward_y * 4 + side_y * 2)
    pygame.draw.circle(screen, (120, 255, 140), (hi_hx, hi_hy), 5)
    pygame.draw.circle(screen, (200, 255, 200), (hi_hx, hi_hy), 2)

    # Eyes
    eye_offset = 6
    left_eye  = (head_x + forward_x * 8 + side_x * eye_offset,
                 head_y + forward_y * 8 + side_y * eye_offset)
    right_eye = (head_x + forward_x * 8 - side_x * eye_offset,
                 head_y + forward_y * 8 - side_y * eye_offset)

    for ex, ey in [left_eye, right_eye]:
        pygame.draw.circle(screen, (220, 240, 220), (int(ex), int(ey)), 3)   # white
        pygame.draw.circle(screen, (5, 10, 5),      (int(ex), int(ey)), 2)   # pupil
        pygame.draw.circle(screen, (255, 255, 255), (int(ex + 1), int(ey - 1)), 1)  # gleam

    # Tongue
    tick = pygame.time.get_ticks() // 60
    if tick % 4 < 2:
        tx = head_x + forward_x * 20
        ty = head_y + forward_y * 20
        pygame.draw.line(screen, (220, 30, 50),
                         (int(head_x + forward_x * 14), int(head_y + forward_y * 14)),
                         (int(tx), int(ty)), 1)
        # forked tips
        pygame.draw.line(screen, (220, 30, 50),
                         (int(tx), int(ty)),
                         (int(tx + forward_x * 4 + side_x * 3),
                          int(ty + forward_y * 4 + side_y * 3)), 1)
        pygame.draw.line(screen, (220, 30, 50),
                         (int(tx), int(ty)),
                         (int(tx + forward_x * 4 - side_x * 3),
                          int(ty + forward_y * 4 - side_y * 3)), 1)


# MOVE SNAKE

def move_snake(snake, direction):
    global angle, spawn_protection

    if direction == "RIGHT":
        target_angle = 0
    elif direction == "LEFT":
        target_angle = math.pi
    elif direction == "UP":
        target_angle = -math.pi / 2
    elif direction == "DOWN":
        target_angle = math.pi / 2

    turn_step = TURN_SPEED
    diff = target_angle - angle

    while diff > math.pi:
        diff -= 2 * math.pi
    while diff < -math.pi:
        diff += 2 * math.pi

    if abs(diff) < turn_step:
        angle = target_angle
    elif diff > 0:
        angle += turn_step
    else:
        angle -= turn_step

    if spawn_protection > 0:
        spawn_protection -= 1

    head_x, head_y = snake[0]
    head_x += math.cos(angle) * SPEED
    head_y += math.sin(angle) * SPEED
    snake.insert(0, [head_x, head_y])

    for i in range(1, len(snake)):
        prev_x, prev_y = snake[i - 1]
        curr_x, curr_y = snake[i]
        dx = prev_x - curr_x
        dy = prev_y - curr_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > BODY_GAP:
            move_amount = (distance - BODY_GAP) * 0.72
            snake[i][0] += (dx / distance) * move_amount
            snake[i][1] += (dy / distance) * move_amount

    return snake


def check_collision(snake):

    global resize_protection

    if resize_protection > 0:
        return False

    head = snake[0]

    if head[0] < 2 or head[0] >= WIDTH - 2:
        return True
    if head[1] < 2 or head[1] >= HEIGHT - 2:
        return True

    global spawn_protection


    if spawn_protection <= 0:
        for segment in snake[10:]:
            dx = head[0] - segment[0]
            dy = head[1] - segment[1]
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 7:   # FIX: 10 → 7
                return True

    return False


# VIGNETTE
def draw_vignette():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    cx, cy = WIDTH // 2, HEIGHT // 2
    max_radius = math.sqrt(cx ** 2 + cy ** 2)

    for i in range(0, int(max_radius), 10):
        alpha = int((i / max_radius) * 180)
        pygame.draw.circle(overlay, (0, 0, 0, alpha), (cx, cy), i)

    screen.blit(overlay, (0, 0))


def draw_text(txt, x, y, color=WHITE):
    render = font.render(txt, True, color)
    screen.blit(render, (x, y))


def draw_glowing_food(food, fruit_img):
    food_x, food_y = food

    glow = pygame.transform.scale(
        fruit_img, (food_size + 8, food_size + 8)
    ).convert_alpha()

    glow_mask = glow.copy()
    glow_mask.fill((255, 210, 80, 0), special_flags=pygame.BLEND_RGBA_ADD)

    screen.blit(glow_mask, (food_x - glow.get_width() // 2, food_y - glow.get_height() // 2))
    screen.blit(fruit_img, (food_x - food_size // 2, food_y - food_size // 2))


def draw_fireflies():

    time = pygame.time.get_ticks() * 0.001

    for f in fireflies:

        # MOVEMENT
        f["x"] += f["dx"]
        f["y"] += f["dy"]

        # slight floating
        f["x"] += math.sin(time + f["y"] * 0.01) * 0.15
        f["y"] += math.cos(time + f["x"] * 0.01) * 0.15

        # LIFE RESET
        f["life"] -= 1

        if f["life"] <= 0:
            f["x"] = random.randint(0, WIDTH)
            f["y"] = random.randint(0, HEIGHT)
            f["life"] = random.randint(60, 140)

        # SIMPLE PULSE
        pulse = 0.6 + 0.4 * math.sin(time * 2 + f["life"])

        size = f["size"]

        # SOFT LIGHT GLOW
        glow = pygame.Surface((10, 10), pygame.SRCALPHA)

        pygame.draw.circle(
            glow,
            (255, 230, 140, int(60 * pulse)),
            (9, 9),
            size + 2
        )

        screen.blit(
            glow,
            (f["x"] - 9, f["y"] - 9),
            special_flags=pygame.BLEND_RGBA_ADD
        )

        # CORE DOT

        pygame.draw.circle(
            screen,
            (255, 240, 180),
            (int(f["x"]), int(f["y"])),
            size
        )


# GAME LOOP

running = True

while running:
    if resize_protection > 0:
        resize_protection -= 1
    screen.blit(BG_IMG, (0, 0))
    #draw_vignette()
    draw_fireflies()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:

            old_width = WIDTH
            old_height = HEIGHT

            WIDTH, HEIGHT = event.w, event.h

            scale_x = WIDTH / old_width
            scale_y = HEIGHT / old_height

            # Snake scale
            for seg in snake:
                seg[0] *= scale_x
                seg[1] *= scale_y

            # Food scale
            food[0] *= scale_x
            food[1] *= scale_y

            screen = pygame.display.set_mode(
                (WIDTH, HEIGHT),
                pygame.RESIZABLE
            )

            BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))
            WELCOME_IMG = pygame.transform.scale(WELCOME_IMG, (WIDTH, HEIGHT))
            GAMEOVER_IMG = pygame.transform.scale(GAMEOVER_IMG, (WIDTH, HEIGHT))

            resize_protection = 60

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


                elif event.key == pygame.K_w and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_s and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_a and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_d and direction != "LEFT":
                    direction = "RIGHT"


            elif state == "PAUSE":

                # SPACE-RESUME

                if event.key == pygame.K_SPACE:

                    state = "PLAYING"


                else:
                    state, snake, direction, food, score, fruit_img = handle_pause_events(
                        event,
                        state,
                        snake,
                        direction,
                        food,
                        score,
                        fruit_img,
                        reset_game
                    )

            elif state == "GAMEOVER":
                if event.key == pygame.K_SPACE:
                    snake, direction, food, score, fruit_img = reset_game()
                    state = "PLAYING"
                    pygame.mixer.music.play(-1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "WELCOME":
                state = "PLAYING"

            elif state == "PLAYING":
                direction, state = handle_button_click(
                    pygame.mouse.get_pos(), direction, state,WIDTH,HEIGHT
                )

            elif state == "PAUSE":

                state, snake, direction, food, score, fruit_img = handle_mouse_click(
                    pygame.mouse.get_pos(),
                    snake,
                    direction,
                    food,
                    score,
                    fruit_img,
                    reset_game,
                    WIDTH,
                    HEIGHT

                )

    # WELCOME
    if state == "WELCOME":
        screen.blit(WELCOME_IMG, (0, 0))

    # PLAYING
    elif state == "PLAYING":
        snake = move_snake(snake, direction)

        draw_glowing_food(food, fruit_img)

        # EAT FOOD
        dx = snake[0][0] - food[0]
        dy = snake[0][1] - food[1]
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 25:
            score += 10
            grow += 2

            if EAT_SOUND:
                EAT_SOUND.play()


            food = spawn_food_safe(snake)
            fruit_img = random.choice(fruit_images)



        if grow > 0:

            grow -= 1

        else:

            snake.pop()

        # COLLISION CHECK
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


        if spawn_protection > 0:
            pass
            #draw_text(f"SAFE: {spawn_protection // 60 + 1}s", WIDTH // 2 - 30, 10, (100, 255, 150))

        draw_text(f"SCORE: {score}", 10, 10, (0, 255, 255))
        draw_text(f"HIGH: {high_score}", 10, 40, (255, 0, 255))
        draw_buttons(screen, WIDTH, HEIGHT)

    # PAUSE
    elif state == "PAUSE":
        draw_snake(snake)
        draw_pause(screen, draw_text, snake, food, fruit_img,WIDTH,HEIGHT)

    # GAME OVER
    elif state == "GAMEOVER":
        screen.blit(GAMEOVER_IMG, (0, 0))

        draw_text(f"SCORE: {score}", 300, 390, (0, 255, 255))
        draw_text(f"HIGH: {high_score}", 300, 420, (255, 0, 255))

    pygame.display.update()
    clock.tick(60)

pygame.quit()