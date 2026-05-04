import pygame

pause_menu = ["Resume Game", "New Game", "Quit Game"]
pause_index = 0

def handle_pause_events(event, state, snake, direction, food, score, reset_game):
    global pause_index

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            pause_index = (pause_index - 1) % 3

        elif event.key == pygame.K_DOWN:
            pause_index = (pause_index + 1) % 3

        elif event.key == pygame.K_RETURN:
            if pause_index == 0:
                return "PLAYING", snake, direction, food, score

            elif pause_index == 1:
                snake, direction, food, score = reset_game()
                return "PLAYING", snake, direction, food, score

            elif pause_index == 2:
                return "WELCOME", snake, direction, food, score

    return state, snake, direction, food, score


def handle_mouse_click(mouse_pos, snake, direction, food, score, reset_game):
    global pause_index

    x, y = mouse_pos

    for i in range(3):
        btn_x = 400
        btn_y = 260 + i * 40

        if btn_x <= x <= btn_x + 200 and btn_y <= y <= btn_y + 30:
            pause_index = i

            if i == 0:
                return "PLAYING", snake, direction, food, score

            elif i == 1:
                snake, direction, food, score = reset_game()
                return "PLAYING", snake, direction, food, score

            elif i == 2:
                snake,direction,food,score = reset_game()
                return "WELCOME", snake, direction, food, score

    return "PAUSE", snake, direction, food, score


def draw_pause(screen, draw_text, snake, food, block):
    mouse_pos = pygame.mouse.get_pos()

    draw_text("PAUSED", 420, 200)

    for i, option in enumerate(pause_menu):
        x = 400
        y = 260 + i * 40

        # hover effect
        if x <= mouse_pos[0] <= x+200 and y <= mouse_pos[1] <= y+30:
            color = (255, 255, 0)
        else:
            color = (240, 240, 240)

        draw_text(option, x, y, color)

    # food draw (so screen looks alive)
    pygame.draw.circle(screen, (255, 50, 50),
                       (food[0] + block//2, food[1] + block//2),
                       block//2)