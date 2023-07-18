import pygame
from random import randrange

pygame.init()


WINDOW = 1000
SCREEN = pygame.display.set_mode([WINDOW] * 2)
Tile_Size = 25
Range = (Tile_Size // 2, WINDOW - Tile_Size // 2, Tile_Size)
get_random_postion = lambda: [randrange(*Range), randrange(*Range)]

Font = pygame.font.Font('freesansbold.ttf', 20)

snake = pygame.rect.Rect([0,0, Tile_Size - 2, Tile_Size -2])
snake.center = get_random_postion()
snake_dir = (0,0)

food = snake.copy()
food.center = get_random_postion()

time, time_step = 0, 110
length = 1
segments = [snake.copy()]
dirs = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 1}
clock = pygame.time.Clock()
points = 0

def normilize(x):
    a1,b1 = 0,1
    min,max = 0,WINDOW
    return(a1+(x+min)*(b1-a1)/max-min)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and dirs[pygame.K_w]:
                snake_dir = (0, -Tile_Size)
                dirs = {pygame.K_w: 1, pygame.K_s: 0, pygame.K_a: 1, pygame.K_d: 1}
            if event.key == pygame.K_s and dirs[pygame.K_s]:
                snake_dir = (0, Tile_Size)
                dirs = {pygame.K_w: 0, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 1}
            if event.key == pygame.K_a and dirs[pygame.K_a]:
                snake_dir = (-Tile_Size, 0)
                dirs = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 0}
            if event.key == pygame.K_d and dirs[pygame.K_d]:
                snake_dir = (Tile_Size, 0)
                dirs = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 0, pygame.K_d: 1}
                
    SCREEN.fill('black')
    [pygame.draw.rect(SCREEN, 'red', segment) for segment in segments]

    
    pygame.draw.rect(SCREEN, 'green', food)
    
    self_eating = pygame.Rect.collidelist(snake, segments[:-1]) != -1

    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        snake.center, food.center = get_random_postion(), get_random_postion()
        length, snake_dir = 1, (0,0)
        segments = [snake.copy()]
        dirs = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 1}
        points = 0

    
    if snake.center == food.center:
        food.center = get_random_postion()
        length +=1
        points += 1

    
    time_now = pygame.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
        
        
    text = Font.render(f'Points: {str(points)}', True, (255, 255, 255))
    SCREEN.blit(text, (15, 15))

    pygame.display.flip()
    clock.tick(30)