import pygame
import random
pygame.init()


#colors
blue = (135,206,235)
red = (255,0,0)
purple = (138,43,226)
green = (60,110,60)
dblue = (75,0,130)

#creating window
screen_width=1000
screen_height=600
gameWindow = pygame.display.set_mode((screen_width,screen_height))

#game title
pygame.display.set_caption("Python")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None,30)


def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,(x,y))

def plot_snake(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,color,[x,y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(blue)
        text_screen("Welcome to Python",dblue,390,260)
        text_screen("Press Space To Play", dblue, 385, 290)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)

#gameloop
def gameloop():
    # game specific variable
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 20
    fps = 60
    init_velocity = 3
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    with open("highscore.txt", "r") as f:
        highscore = f.read()

    food_x = random.randint(20, screen_width // 2)
    food_y = random.randint(20, screen_height // 2)
    score = 0

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gameWindow.fill(blue)
            text_screen("Margei madarchod la la ! Phirse khelna hain to Enter main thuk",red,170,260)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()




        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 12 and abs(snake_y - food_y) < 12:
                score += 10

                food_x = random.randint(20,screen_width//2)
                food_y = random.randint(20,screen_height//2)
                snk_length += 5
                if score>int(highscore):
                    highscore = score

            gameWindow.fill(blue)
            text_screen("Score: " + str(score)+"   Best Score: "+str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow,purple, [food_x, food_y, snake_size, snake_size])

            head =[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)


            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True

            plot_snake(gameWindow,green,snk_list,snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
#gameloop()