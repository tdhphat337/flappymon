import pygame
from random import randint

pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("FLAPPY BIRD")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

x_bird = 50
y_bird = 100
tube_width = 50
tube_vel = 2
score = 0
gravity = 0.5

tube1_x, tube2_x, tube3_x = 400, 600, 800
tube1_height, tube2_height, tube3_height = randint(100, 400), randint(100, 400), randint(100, 400)
d_2tube = 150
bird_drop_vel = 0

font = pygame.font.SysFont('san', 50)
font2 = pygame.font.SysFont('san', 35)

background_img = pygame.transform.scale(pygame.image.load('bg.png'), (400, 600))
menu_img = pygame.image.load('message.png')
result_img = pygame.image.load('kq.png')
bird_img = pygame.transform.scale(pygame.image.load('mon.png'), (40, 40))
tube_img = pygame.image.load('pipe.png')
base_img = pygame.image.load('base.png')

sound = pygame.mixer.Sound("hit.wav")
swoosh = pygame.mixer.Sound("swoosh.wav")
point = pygame.mixer.Sound("point.wav")

def main():
    global x_bird, y_bird, tube1_x, tube2_x, tube3_x, tube1_height, tube2_height, tube3_height, d_2tube, bird_drop_vel, gravity, tube_vel, score, font, font2
    
    running = True
    tube1_pass = False
    tube2_pass = False
    tube3_pass = False
    dung = False
    sound_played = False
    
    while running:
        clock.tick(60)
        screen.fill(WHITE)
        screen.blit(background_img, (0, 0))

        tube1_img = pygame.transform.scale(tube_img, (tube_width, tube1_height))
        tube1 = screen.blit(tube1_img, (tube1_x, 0))
        tube2_img = pygame.transform.scale(tube_img, (tube_width, tube2_height))
        tube2 = screen.blit(tube2_img, (tube2_x, 0))
        tube3_img = pygame.transform.scale(tube_img, (tube_width, tube3_height))
        tube3 = screen.blit(tube3_img, (tube3_x, 0))

        tube_op_img = pygame.transform.scale(tube_img, (tube_width, 600 - (tube1_height + d_2tube)))
        tube1_op = screen.blit(tube_op_img, (tube1_x, tube1_height + d_2tube))
        tube2_op_img = pygame.transform.scale(tube_img, (tube_width, 600 - (tube2_height + d_2tube)))
        tube2_op = screen.blit(tube2_op_img, (tube2_x, tube2_height + d_2tube))
        tube3_op_img = pygame.transform.scale(tube_img, (tube_width, 600 - (tube3_height + d_2tube)))
        tube3_op = screen.blit(tube3_op_img, (tube3_x, tube3_height + d_2tube))

        base_image = pygame.transform.scale(base_img, (400, 100))
        base = screen.blit(base_image, (0, 500))

        tube1_x -= tube_vel
        tube2_x -= tube_vel
        tube3_x -= tube_vel
        bird = screen.blit(bird_img, (x_bird, y_bird))

        if tube1_x < -tube_width:
            tube1_x = 550
            tube1_height = randint(100, 400)
            tube1_pass = False
            sound_played = False
        if tube2_x < -tube_width:
            tube2_x = 550
            tube2_height = randint(100, 400)
            tube2_pass = False
            sound_played = False
        if tube3_x < -tube_width:
            tube3_x = 550
            tube3_height = randint(100, 400)
            tube3_pass = False
            sound_played = False

        y_bird += bird_drop_vel
        bird_drop_vel += gravity

        score_txt = font.render("Score: " + str(score), True, RED)
        screen.blit(score_txt, (5, 5))

        if tube1_x + tube_width <= x_bird and not tube1_pass:
            pygame.mixer.Sound.play(point)
            score += 1
            tube1_pass = True
        if tube2_x + tube_width <= x_bird and not tube2_pass:
            pygame.mixer.Sound.play(point)
            score += 1
            tube2_pass = True
        if tube3_x + tube_width <= x_bird and not tube3_pass:
            pygame.mixer.Sound.play(point)
            score += 1
            tube3_pass = True

        tubes = [tube1, tube2, tube3, tube1_op, tube2_op, tube3_op]
        num_collisions = 0
        num_collisions2 = 0
        num_collisions3 = 0

        if y_bird < 0 or y_bird + 40 > 500:
            num_collisions3 += 1
        if num_collisions3 > 0:
            if num_collisions3 == 1 and not sound_played:
                pygame.mixer.Sound.play(sound)
                sound_played = True
            game_over()
            dung = True

        if bird.colliderect(base):
            num_collisions2 += 1
        if num_collisions2 > 0:
            if num_collisions2 == 1 and not sound_played:
                pygame.mixer.Sound.play(sound)
                sound_played = True
            game_over()
            dung = True

        for tube in tubes:
            if bird.colliderect(tube):
                num_collisions += 1
        if num_collisions > 0:
            if num_collisions == 1 and not sound_played:
                pygame.mixer.Sound.play(sound)
                sound_played = True
            game_over()
            dung = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(swoosh)
                    bird_drop_vel = 0
                    bird_drop_vel -= 7

        pygame.display.update()

def game_over():
    global font, font2
    
    run = True
    while run:
        result = pygame.transform.scale(result_img, (400, 600))
        result = screen.blit(result, (0, 45))
        game_over_txt = font.render("Game Over!!!", True, RED)
        screen.blit(game_over_txt, (105, 260))
        space_txt = font2.render("Click right mouse to continue! ", True, BLUE)
        screen.blit(space_txt, (30, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                main()

    pygame.quit()

def menu():
    run = True
    while run:
        menu = screen.blit(menu_img, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                main()

    pygame.quit()

menu()
