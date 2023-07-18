import pygame
from random import randrange
import random
import neat
import neat.config
import os
import math
import sys



pygame.init()


WINDOW = 500
SCREEN = pygame.display.set_mode([WINDOW] * 2)
Tile_Size = 20
Range = (Tile_Size // 2, WINDOW - Tile_Size // 2, Tile_Size)
get_random_postion = lambda: [randrange(*Range), randrange(*Range)]

Font = pygame.font.Font('freesansbold.ttf', 20)

cube = pygame.rect.Rect([0,0, Tile_Size - 2, Tile_Size -2])

def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx ** 2 + dy ** 2)

def normilize(x):
    a1,b1 = 0,1
    min,max = 0,WINDOW
    return(a1+(x+min)*(b1-a1)/max-min)

def remove(index):
    snakes.pop(index)
    ge.pop(index)
    nets.pop(index)

class Snake():
    
    def __init__(self):
        self.dir = random.choice([(0,Tile_Size), (0,-Tile_Size),(Tile_Size,0), (-Tile_Size,0)])
        self.rec = pygame.rect.Rect([0,0, Tile_Size - 2, Tile_Size -2])
        self.rec.center = get_random_postion()
        self.length = 1
        self.segments = [self.rec]
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.dirs = {"up": 1, "down": 1, "left": 1, "right": 1}
        self.points = 0
        self.last_dir = self.dir
        self.last_pos = self.rec.center
        self.moves = 0
        
    def move(self, move):
        self.last_dir = self.dir
        self.last_pos = self.rec.center
        
        if move == "up" and self.dirs["up"]:
            self.dir = (0, -Tile_Size)
            self.dirs = {"up": 1, "down": 0, "left": 1, "right": 1}
        if move == "down" and self.dirs["down"]:
            self.dir = (0, Tile_Size)
            self.dirs = {"up": 0, "down": 1, "left": 1, "right": 1}
        if move == "left" and self.dirs["left"]:
            self.dir = (-Tile_Size, 0)
            self.dirs = {"up": 1, "down": 1, "left": 1, "right": 0}
        if move == "right" and self.dirs["right"]:
            self.dir = (Tile_Size, 0)
            self.dirs = {"up": 1, "down": 1, "left": 0, "right": 1}
            
    # def reset(self):
    #     self.rec.center= [get_random_postion()]
    #     self.length, self.dir = 1, (0,0)
    #     self.segments = [self.rec.copy()]
    #     self.dirs = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 1}
    #     self.points = 0
        
    def update(self):
        time, time_step = 0, 110

        time_now = pygame.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            self.rec.move_ip(self.dir)
            self.segments.append(self.rec.copy())
            self.segments = self.segments[-self.length:]
    
    def dis_to_other_recs(self, list):
        distances = []
        
        for rec in list:
            distances.append(distance(self.rec.center, rec.center))
            
        return(min(distances))
    
        

#def eval_snake_genomes(gemomes, config):s

cube.center = get_random_postion()

def eval_genomes(genomes, config):
    global ge, nets, snakes
    clock = pygame.time.Clock()
    
    snakes = []
    ge = []
    nets = []
    
    foods = []
    
    for i in range(0,5):
        food = cube.copy()
        food.center = get_random_postion()
        foods.append(food)
    
        
    for genome_id, genome in genomes:
        snakes.append(Snake())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        for i, snake in enumerate(snakes):
            output = nets[i].activate((snake.rec.center[0], snake.rec.center[1], snake.last_pos[0], snake.last_pos[1],
                                       snake.dis_to_other_recs(foods), 
                                      normilize(abs(snake.rec.left)), normilize(abs(snake.rec.right-WINDOW)),
                                      normilize(abs(snake.rec.top)), normilize(abs(snake.rec.bottom-WINDOW))))
            
            snake.moves += 1
            if output[0] > 0.5:
                snake.move("up")
            elif output[1] > 0.5:
                snake.move("down")
            elif output[2] > 0.5:
                snake.move("left")
            elif output[3] > 0.5:
                snake.move("right")

        
        SCREEN.fill('black')
        
        for food in foods:
            pygame.draw.rect(SCREEN, 'green', food)
        
        if len(snakes) == 0:
            break
        
        for i, snake in enumerate(snakes):
            for segment in snake.segments:
                pygame.draw.rect(SCREEN, snake.color, segment)
                 
            self_eating = pygame.Rect.collidelist(snake.rec, snake.segments[:-1]) != -1
            
                
            for food in foods: 
                if snake.rec.center == food.center:
                    food.center = get_random_postion()
                    snake.length +=1
                    ge[i].fitness += 1
                    
            # if snake.dir != snake.last_dir:
            #     ge[i].fitness += 1
                
                
            if snake.moves > 50:
                ge[i].fitness +=1
                
            if snake.rec.left < 0 or snake.rec.right > WINDOW or snake.rec.top < 0 or snake.rec.bottom > WINDOW or self_eating:
                ge[i].fitness -= 1
                remove(i)
        
            snake.update()


        clock.tick(15)
        pygame.display.flip()

    
# NEAT Setup
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'configSnakes.txt')
    run(config_path)