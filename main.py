import math
import neat
import neat.config
import pygame
import random
import os
import sys

pygame.init()

# Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

Running = [pygame.image.load(os.path.join('Assets/Dino', 'DinoRun1.png')),
           pygame.image.load(os.path.join('Assets/Dino', 'DinoRun2.png'))]

Jumping = pygame.image.load(os.path.join('Assets/Dino', 'DinoJump.png'))

Small_Cactus = [pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus1.png')),
                pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus2.png')),
                pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus3.png'))]
Large_Cactus = [pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus1.png')),
                pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus2.png')),
                pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus3.png'))]

BG = pygame.image.load(os.path.join('Assets/Other', 'Track.png'))

Font = pygame.font.Font('freesansbold.ttf', 20)


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Jump_Vel = 8.5

    def __init__(self, img=Running[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.Jump_Vel
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0

    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        self.image = Jumping
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.Jump_Vel:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.Jump_Vel

    def run(self):
        self.image = Running[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def draw(self, Screen):
        Screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(Screen, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        for obstacle in obstacles:
            pygame.draw.line(Screen, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2)


class Obstacle:
    def __init__(self, image, number_of_cacti):
        self.image = image
        self.type = number_of_cacti
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 300


def remove(index):
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)


def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx ** 2 + dy ** 2)




def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, obstacles, dinosaurs, ge, nets, y_pos_bg, points, obstacle, high_score
    clock = pygame.time.Clock()
    points = 0

    high_score = 0
    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    obstacles = []
    dinosaurs = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def score():
        global points, game_speed, high_score
        points += 1
        if points % 100 == 0:
            game_speed += 1
        if points > high_score:
            high_score = points
        text = Font.render(f'Points: {str(points)}', True, (0, 0, 0))
        Screen.blit(text, (950, 50))

    def statistics():
        global dinosaurs, game_speed, ge, high_score

        text_1 = Font.render(f'Dinosaurs Alive: {str(len(dinosaurs))}', True, (0, 0, 0))
        text_2 = Font.render(f'Generation: {pop.generation + 1}', True, (0, 0, 0))
        text_3 = Font.render(f'Game Speed: {str(game_speed)}', True, (0, 0, 0))
        text_4 = Font.render(f'High Score: {str(high_score)}', True, (0, 0, 0))

        Screen.blit(text_1, (50, 450))
        Screen.blit(text_2, (50, 480))
        Screen.blit(text_3, (50, 510))
        Screen.blit(text_4, (50, 540))

    def background():
        global x_pos_bg, y_pos_bg, high_score
        image_width = BG.get_width()
        Screen.blit(BG, (x_pos_bg, y_pos_bg))
        Screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        Screen.fill((255, 255, 255))

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(Screen)

        if len(dinosaurs) == 0:
            save = high_score
            break

        if len(obstacles) == 0:
            rand_in = random.randint(0, 1)
            if rand_in == 0:
                obstacles.append(SmallCactus(Small_Cactus, random.randint(0, 2)))
            elif rand_in == 1:
                obstacles.append(LargeCactus(Large_Cactus, random.randint(0, 2)))

        for obstacle in obstacles:
            obstacle.draw(Screen)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 1
                    remove(i)

        for i, dinosaur in enumerate(dinosaurs):
            output = nets[i].activate((dinosaur.rect.y,
                                       distance((dinosaur.rect.x, dinosaur.rect.y),
                                                obstacle.rect.midtop)))
            if output[0] > 0.5 and dinosaur.rect.y == dinosaur.Y_POS:
                dinosaur.dino_jump = True
                dinosaur.dino_run = False

        statistics()
        score()
        background()
        clock.tick(30)

        pygame.display.update()


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
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
