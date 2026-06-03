import pygame

pause_menu = [
    "Resume Game",
    "New Game",
    "Quit Game"
]
pause_index = 0

# GET RESPONSIVE MENU POSITIONS

def get_pause_layout(WIDTH, HEIGHT):

    menu_width = int(WIDTH * 0.3)

    menu_height = int(HEIGHT * 0.07)

    spacing = int(HEIGHT * 0.08)

    start_x = WIDTH // 2 - menu_width // 2

    start_y = HEIGHT // 2 - spacing

    return (
        menu_width,
        menu_height,
        spacing,
        start_x,
        start_y
    )

# KEYBOARD CONTROL

def handle_pause_events(
        event,
        state,
        snake,
        direction,
        food,
        score,
        fruit_img,
        reset_game
):

    global pause_index

    if event.type == pygame.KEYDOWN:

        # MOVE UP
        if event.key == pygame.K_UP:

            pause_index = (pause_index - 1) % 3

        # MOVE DOWN
        elif event.key == pygame.K_DOWN:

            pause_index = (pause_index + 1) % 3

        # SELECT
        elif event.key == pygame.K_RETURN:

            # RESUME
            if pause_index == 0:

                return (
                    "PLAYING",
                    snake,
                    direction,
                    food,
                    score,
                    fruit_img
                )

            # NEW GAME
            elif pause_index == 1:

                snake, direction, food, score, fruit_img = reset_game()

                return (
                    "PLAYING",
                    snake,
                    direction,
                    food,
                    score,
                    fruit_img
                )

            # QUIT
            elif pause_index == 2:

                snake, direction, food, score, fruit_img = reset_game()

                return (
                    "WELCOME",
                    snake,
                    direction,
                    food,
                    score,
                    fruit_img
                )

    return (
        state,
        snake,
        direction,
        food,
        score,
        fruit_img
    )

# MOUSE CONTROL

def handle_mouse_click(
        mouse_pos,
        snake,
        direction,
        food,
        score,
        fruit_img,
        reset_game,
        WIDTH,
        HEIGHT
):

    global pause_index

    (
        menu_width,
        menu_height,
        spacing,
        start_x,
        start_y
    ) = get_pause_layout(WIDTH, HEIGHT)

    x, y = mouse_pos

    for i in range(3):

        btn_x = start_x

        btn_y = start_y + i * spacing

        rect = pygame.Rect(
            btn_x,
            btn_y,
            menu_width,
            menu_height
        )

        if rect.collidepoint(x, y):

            pause_index = i

            # RESUME
            if i == 0:

                return (
                    "PLAYING",
                    snake,
                    direction,
                    food,
                    score,
                    fruit_img
                )

            # NEW GAME
            elif i == 1:

                snake, direction, food, score, fruit_img = reset_game()

                return (
                    "PLAYING",
                    snake,
                    direction,
                    food,
                    score,
                    fruit_img
                )

            # QUIT
            elif i == 2:

                snake, direction, food, score, fruit_img = reset_game()

                return (
                    "WELCOME",
                    snake,
                    direction,
                    food,
                    score,
                    fruit_img
                )

    return (
        "PAUSE",
        snake,
        direction,
        food,
        score,
        fruit_img
    )

# DRAW PAUSE MENU

def draw_pause(
        screen,
        draw_text,
        snake,
        food,
        fruit_img,
        WIDTH,
        HEIGHT
):

    mouse_pos = pygame.mouse.get_pos()

    (
        menu_width,
        menu_height,
        spacing,
        start_x,
        start_y
    ) = get_pause_layout(WIDTH, HEIGHT)

    # TITLE
    title_x = WIDTH // 2 - 50

    title_y = HEIGHT // 2 - spacing * 2

    draw_text(
        "PAUSED",
        title_x,
        title_y,
        (255, 255, 255)
    )

    # MENU OPTIONS
    for i, option in enumerate(pause_menu):

        x = start_x

        y = start_y + i * spacing

        rect = pygame.Rect(
            x,
            y,
            menu_width,
            menu_height
        )

        # HOVER
        if rect.collidepoint(mouse_pos):

            color = (255, 255, 0)

        else:

            color = (240, 240, 240)

        # CENTER TEXT
        text_x = WIDTH // 2 - 70

        text_y = y

        draw_text(
            option,
            text_x,
            text_y,
            color
        )

    # DRAW CURRENT FRUIT
    screen.blit(
        fruit_img,
        (
            food[0] - fruit_img.get_width() // 2,
            food[1] - fruit_img.get_height() // 2
        )
    )