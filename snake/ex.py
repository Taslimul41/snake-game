import pygame
import random
pygame.init()


#colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)

#creating window
screen_width=800
screen_height=500
gameWindow = pygame.display.set_mode((screen_width,screen_height))

#game title
pygame.display.set_caption("EX")
pygame.display.update()

#game specific variable
exit_game = False
game_over = False
snake_x = 45
snake_y = 55
snake_size = 10
fps = 50
velocity_x = 0
velocity_y = 0
food_x = random.randint(20,screen_width//2)
food_y = random.randint(20,screen_height//2)
score = 0


clock = pygame.time.Clock()
font = pygame.font.SysFont(None,55)

def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,(x,y))

#gameloop
while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                velocity_x = 2
                velocity_y = 0
            if event.key == pygame.K_LEFT:
                velocity_x = - 2
                velocity_y = 0
            if event.key == pygame.K_UP:
                velocity_y = - 2
                velocity_x = 0
            if event.key == pygame.K_DOWN:
                velocity_y = 2
                velocity_x = 0

    snake_x = snake_x + velocity_x
    snake_y = snake_y + velocity_y

    if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
        score += 1
        print("Score:", score*10)
        food_x = random.randint(20,screen_width//2)
        food_y = random.randint(20,screen_height//2)

    gameWindow.fill(white)
    text_screen("Score: " + str(score * 10), red, 5, 5)
    pygame.draw.rect(gameWindow,red, [food_x, food_y, snake_size, snake_size])
    pygame.draw.rect(gameWindow,black,[snake_x, snake_y,snake_size,snake_size ])
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()